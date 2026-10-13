#!/usr/bin/env python3
"""NexusCore Lite — local webhook routing and SQLite WAL persistence.

A single-process preview with no external services. Payloads posted to
/webhook are committed to a local SQLite file in WAL mode. A micro-cron
pings /health every 10 seconds and stores each run in memory and SQLite.

    pip install -r requirements.txt
    python nexuscore_lite.py

Telemetry stays off unless NEXUS_TELEMETRY is set to a value other than
off/false/0/no. This process never sends events off the machine.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import os
import sqlite3
import sys
import time
from collections import deque
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from http.client import HTTPConnection
from pathlib import Path
from typing import Any

try:
    import uvicorn
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
except ImportError:
    sys.stderr.write(
        "NexusCore Lite needs fastapi and uvicorn.\n"
        "Install them with: pip install -r requirements.txt\n"
    )
    raise SystemExit(1)


NOTICE = (
    "Looking for full microservices (EnvSync, API Proxy, LogStream, Docker Suite)? "
    "Visit https://nexuscore-store.whop.site"
)
MAX_BODY_BYTES = 256 * 1024
JOB_NAME = "sample-ping"
JOB_INTERVAL_SECONDS = 10
HISTORY_LIMIT = 20

_OFF_VALUES = {"", "0", "off", "false", "no"}


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    db_path: Path
    telemetry: str

    @property
    def public_base(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    @property
    def ping_host(self) -> str:
        if self.host in {"0.0.0.0", "::", ""}:
            return "127.0.0.1"
        return self.host


def load_settings() -> Settings:
    raw_port = os.environ.get("NEXUS_PORT", "8000")
    try:
        port = int(raw_port)
    except ValueError:
        sys.stderr.write(f"NEXUS_PORT must be an integer, got {raw_port!r}\n")
        raise SystemExit(1)
    if not 1 <= port <= 65535:
        sys.stderr.write(f"NEXUS_PORT must be between 1 and 65535, got {port}\n")
        raise SystemExit(1)

    telemetry = os.environ.get("NEXUS_TELEMETRY", "off").strip().lower()
    if telemetry in _OFF_VALUES:
        telemetry = "off"
    else:
        telemetry = "on"

    db_raw = os.environ.get("NEXUS_DB", "data/nexuscore_lite.db")
    return Settings(
        host=os.environ.get("NEXUS_HOST", "127.0.0.1"),
        port=port,
        db_path=Path(db_raw),
        telemetry=telemetry,
    )


def log(message: str) -> None:
    print(f"[NexusCore Lite] {message}", flush=True)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def print_banner(cfg: Settings) -> None:
    base = cfg.public_base
    curl = (
        f'curl -X POST {base}/webhook '
        '-H "Content-Type: application/json" '
        '-d "{\\"event\\":\\"preview\\",\\"source\\":\\"curl\\"}"'
    )
    rule = "=" * 78
    print(rule)
    print("  NexusCore Lite")
    print("  Local webhook routing and SQLite WAL persistence")
    print(rule)
    print(f"  Local endpoints: {base}")
    print(f"    POST {base}/webhook")
    print(f"    GET  {base}/jobs")
    print(f"    GET  {base}/health")
    print()
    print("  Send a test payload:")
    print(f"    {curl}")
    print()
    print(f"  NEXUS_TELEMETRY={cfg.telemetry}")
    print()
    print(f"  {NOTICE}")
    print(rule, flush=True)


def _json_media(content_type: str) -> bool:
    media = content_type.split(";", 1)[0].strip().lower()
    return media == "application/json" or media.endswith("+json")


class Store:
    """Single SQLite connection. Writes run off the event loop, one at a time."""

    def __init__(self, cfg: Settings) -> None:
        self.path = cfg.db_path
        self.journal_mode = ""
        self._conn: sqlite3.Connection | None = None
        self._lock = asyncio.Lock()

    async def open(self) -> None:
        async with self._lock:
            self.journal_mode = await asyncio.to_thread(self._open_sync)

    def _open_sync(self) -> str:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Autocommit so PRAGMA journal_mode is not wrapped in a transaction.
        conn = sqlite3.connect(self.path, check_same_thread=False, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        mode_row = conn.execute("PRAGMA journal_mode;").fetchone()
        mode = str(mode_row[0]).lower() if mode_row else ""
        if mode != "wal":
            conn.close()
            raise RuntimeError(f"SQLite journal_mode is {mode or 'unknown'}, expected wal")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=2000;")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS webhooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                received_at TEXT NOT NULL,
                content_type TEXT NOT NULL,
                body TEXT NOT NULL,
                is_json INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS job_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                fired_at TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                detail TEXT NOT NULL,
                duration_ms INTEGER NOT NULL
            )
            """
        )
        self._conn = conn
        return mode

    async def close(self) -> None:
        async with self._lock:
            await asyncio.to_thread(self._close_sync)

    def _close_sync(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    async def insert_webhook(self, content_type: str, body: str, is_json: bool) -> int:
        async with self._lock:
            return await asyncio.to_thread(
                self._insert_webhook_sync, content_type, body, is_json
            )

    def _insert_webhook_sync(self, content_type: str, body: str, is_json: bool) -> int:
        assert self._conn is not None
        cursor = self._conn.execute(
            """
            INSERT INTO webhooks (received_at, content_type, body, is_json)
            VALUES (?, ?, ?, ?)
            """,
            (utc_now(), content_type, body, 1 if is_json else 0),
        )
        return int(cursor.lastrowid)

    async def recent_webhooks(self, limit: int = HISTORY_LIMIT) -> list[dict[str, Any]]:
        async with self._lock:
            return await asyncio.to_thread(self._recent_sync, "webhooks", limit)

    async def insert_job(
        self,
        name: str,
        status_code: int,
        detail: str,
        duration_ms: int,
    ) -> int:
        async with self._lock:
            return await asyncio.to_thread(
                self._insert_job_sync, name, status_code, detail, duration_ms
            )

    def _insert_job_sync(
        self,
        name: str,
        status_code: int,
        detail: str,
        duration_ms: int,
    ) -> int:
        assert self._conn is not None
        cursor = self._conn.execute(
            """
            INSERT INTO job_runs (name, fired_at, status_code, detail, duration_ms)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, utc_now(), status_code, detail, duration_ms),
        )
        return int(cursor.lastrowid)

    async def recent_jobs(self, limit: int = HISTORY_LIMIT) -> list[dict[str, Any]]:
        async with self._lock:
            return await asyncio.to_thread(self._recent_sync, "job_runs", limit)

    async def count_jobs(self) -> int:
        async with self._lock:
            return await asyncio.to_thread(self._count_sync, "job_runs")

    def _recent_sync(self, table: str, limit: int) -> list[dict[str, Any]]:
        assert self._conn is not None
        if table not in {"webhooks", "job_runs"}:
            raise ValueError(table)
        rows = self._conn.execute(
            f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def _count_sync(self, table: str) -> int:
        assert self._conn is not None
        if table not in {"webhooks", "job_runs"}:
            raise ValueError(table)
        row = self._conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()
        return int(row["n"]) if row else 0


def ping_health(host: str, port: int) -> tuple[int, str]:
    connection = HTTPConnection(host, port, timeout=2)
    try:
        connection.request("GET", "/health")
        response = connection.getresponse()
        detail = response.read(512).decode("utf-8", "replace")
        return response.status, detail
    finally:
        connection.close()


class JobRunner:
    """In-memory schedule with each fire appended to SQLite."""

    def __init__(self, cfg: Settings, store: Store) -> None:
        self.cfg = cfg
        self.store = store
        self.recent: deque[dict[str, Any]] = deque(maxlen=HISTORY_LIMIT)
        self.fires = 0
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        # recent_jobs() is newest-first, which matches appendleft() on each fire.
        history = await self.store.recent_jobs()
        for row in history:
            self.recent.append(row)
        self.fires = await self.store.count_jobs()
        self._task = asyncio.create_task(self._loop(), name="nexuscore-lite-sample-ping")

    async def stop(self) -> None:
        if self._task is None:
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None

    async def _loop(self) -> None:
        while True:
            try:
                await self.fire()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                log(f"Job fired -> sample ping [error] {exc}")
            await asyncio.sleep(JOB_INTERVAL_SECONDS)

    async def fire(self) -> dict[str, Any]:
        started = time.perf_counter()
        status_code, detail = await self._ping_until_ready()
        duration_ms = int((time.perf_counter() - started) * 1000)
        row_id = await self.store.insert_job(JOB_NAME, status_code, detail[:200], duration_ms)
        record = {
            "id": row_id,
            "name": JOB_NAME,
            "fired_at": utc_now(),
            "status_code": status_code,
            "detail": detail[:200],
            "duration_ms": duration_ms,
        }
        self.recent.appendleft(record)
        self.fires += 1
        label = "200 OK" if status_code == 200 else ("error" if status_code <= 0 else str(status_code))
        log(f"Job fired -> sample ping [{label}]")
        if self.cfg.telemetry == "on":
            log("Telemetry local only -> sample-ping (nothing leaves this machine)")
        return record

    async def _ping_until_ready(self) -> tuple[int, str]:
        last_error = "health endpoint not reachable"
        for _ in range(25):
            try:
                return await asyncio.to_thread(
                    ping_health, self.cfg.ping_host, self.cfg.port
                )
            except OSError as exc:
                last_error = str(exc)
                await asyncio.sleep(0.1)
        return 0, last_error

    def snapshot(self, history: list[dict[str, Any]]) -> dict[str, Any]:
        last = self.recent[0] if self.recent else None
        return {
            "name": JOB_NAME,
            "interval_seconds": JOB_INTERVAL_SECONDS,
            "backing": "memory+sqlite-wal",
            "fires": self.fires,
            "last": last,
            "memory": list(self.recent),
            "history": history,
        }


def create_app(cfg: Settings) -> FastAPI:
    store = Store(cfg)
    runner = JobRunner(cfg, store)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await store.open()
        app.state.settings = cfg
        app.state.store = store
        app.state.runner = runner
        log(f"SQLite WAL ready -> {store.path} (journal_mode={store.journal_mode})")
        await runner.start()
        try:
            yield
        finally:
            await runner.stop()
            await store.close()
            log("Stopped")

    app_kwargs: dict[str, Any] = {"title": "NexusCore Lite", "lifespan": lifespan}
    # Newer FastAPI builds can instrument requests. Keep that off unless this
    # process was explicitly opted in, and never attach an OTLP exporter.
    if "telemetry" in inspect.signature(FastAPI).parameters:
        enabled = cfg.telemetry == "on"
        app_kwargs["telemetry"] = {
            "tracing": enabled,
            "metrics": enabled,
            "logs": enabled,
            "operation_spans": enabled,
            "auto_configure": False,
        }
    app = FastAPI(**app_kwargs)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {
            "status": "ok",
            "journal_mode": store.journal_mode,
            "telemetry": cfg.telemetry,
        }

    @app.get("/")
    async def root() -> dict[str, str]:
        base = cfg.public_base
        return {
            "name": "NexusCore Lite",
            "endpoints": base,
            "webhook": f"{base}/webhook",
            "jobs": f"{base}/jobs",
            "telemetry": cfg.telemetry,
        }

    @app.post("/webhook")
    async def receive_webhook(request: Request) -> JSONResponse:
        body = await request.body()
        if len(body) > MAX_BODY_BYTES:
            log("Webhook rejected -> payload too large [413]")
            return JSONResponse(
                {"ok": False, "error": "payload too large"},
                status_code=413,
            )

        content_type = request.headers.get("content-type", "")
        text = body.decode("utf-8", "replace")
        wants_json = _json_media(content_type)
        is_json = False
        if text and (wants_json or not content_type):
            try:
                json.loads(text)
                is_json = True
            except json.JSONDecodeError:
                if wants_json:
                    log("Webhook rejected -> invalid JSON [400]")
                    return JSONResponse(
                        {"ok": False, "error": "invalid JSON"},
                        status_code=400,
                    )

        row_id = await store.insert_webhook(content_type or "application/octet-stream", text, is_json)
        log("Webhook routed -> SQLite WAL [200 OK]")
        if cfg.telemetry == "on":
            log("Telemetry local only -> webhook (nothing leaves this machine)")
        return JSONResponse(
            {"ok": True, "id": row_id, "journal_mode": store.journal_mode},
            status_code=200,
        )

    @app.get("/webhook")
    async def list_webhooks() -> dict[str, Any]:
        rows = await store.recent_webhooks()
        return {"journal_mode": store.journal_mode, "webhooks": rows}

    @app.get("/jobs")
    async def list_jobs() -> dict[str, Any]:
        history = await store.recent_jobs()
        return {
            "telemetry": cfg.telemetry,
            "runner": runner.snapshot(history),
        }

    return app


def main() -> None:
    cfg = load_settings()
    print_banner(cfg)
    app = create_app(cfg)
    uvicorn.run(app, host=cfg.host, port=cfg.port, log_level="warning", access_log=False)


if __name__ == "__main__":
    main()
