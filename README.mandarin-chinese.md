<!-- language: Mandarin Chinese, Simplified (zh-Hans) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> 语言：**简体中文（普通话）**

本 GitHub 是产品文档和免费演示。NexusCore 是商业软件。授权源代码在 [商店](https://nexuscore-store.whop.site) 结账后交付。

**别再租用你的技术栈。自托管、归你所有的开发者工具。**

在你已经付费的 VPS 上运行 cron、webhook、流水线、日志、环境变量同步和 API 重试。一次买断的终身许可。购买后提供完整源代码。SQLite 落在磁盘上。遥测关闭。

[![自托管](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![遥测](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![许可](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[商店](https://nexuscore-store.whop.site) · [指南](https://nexuscore-store.whop.site/guides) · [架构](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [API 代理](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[快速开始](#quick-start) · [工作原理](#how-it-works) · [套件](#the-suite) · [SaaS 与自托管](#saas-vs-self-hosted) · [结账后你运行什么](#what-you-run-after-checkout) · [常见问题](#faq) · [指南](#guides)

`DEVLAUNCH` → 每份终身许可优惠 20%

---

## 为什么有这个产品

EasyCron、Hookdeck、Zapier、Doppler、Datadog 和 API 网关计量的是同一件事：发出 HTTP、路由一份载荷、让 `.env` 保持同步、对上游重试。

NexusCore 把这件事做成跑在**你的**主机上的进程。

- 付一次钱。源代码留在你手里。
- 用 FastAPI + SQLite + Docker 跑 cron、webhook、流水线和后台。
- LogStream、EnvSync 和 API Proxy 是 Node.js 进程。
- 这些服务不发送用量数据。除非设置了 `NEXUS_TELEMETRY`，轻量示例保持静默。
- 不需要 Kubernetes。跳转之间没有供应商的收件箱。

**获取许可 → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## 快速开始 <a id="quick-start"></a>

免费演示在 `NexusCore Developer Demo.zip`（`./start-demo.sh`，Windows 上是 `.\Start Demo.ps1`，控制台为 http://127.0.0.1:7400）。`pip install -r requirements.txt` 之后，`nexuscore_lite.py` 监听 http://127.0.0.1:8000。授权源代码在结账后交付。下面的片段就是那时要运行的内容。

### Compose 示例（结账后）

```bash
docker compose up --build -d
```

```yaml
# NexusCron/docker-compose.yml — built from the licensed source, not pulled from this GitHub.
# Webhook Router ships its own compose file and also binds host port 8000, so run it from its own folder.
services:
  scheduler:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DATABASE_PATH: /data/scheduler.db
      SCHEDULER_TIMEZONE: UTC
    volumes:
      - pulse-data:/data

volumes:
  pulse-data:
```

```yaml
# Webhook Router/docker-compose.yml
services:
  bridge:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      ADMIN_API_TOKEN: ${ADMIN_API_TOKEN:?Set ADMIN_API_TOKEN}
      DATABASE_URL: sqlite:////app/data/bridge.db
    volumes:
      - bridge-data:/app/data

volumes:
  bridge-data:
```

### 通过 REST 创建任务

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{
    "name": "invoice-reminders",
    "cron_expression": "0 8 * * 1-5",
    "http_method": "POST",
    "target_url": "https://billing.internal/jobs/remind"
  }'
```

### Node.js 进程（不需要 Compose）

```bash
npm start          # EnvSync, http://127.0.0.1:8787. 在 VPS、笔记本和服务之间加密同步 .env
npm start          # API Proxy, http://127.0.0.1:8080. 重试、速率限制、熔断和回退
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. HTTP + UDP 接入、SQLite、实时仪表盘
```

EnvSync 在首次启动时设置管理员密码（`NEXUSENV_ADMIN_PASSWORD`）。LogStream 需要 `.env` 里的 `NEXUS_TOKEN`。绑定到 localhost，并把数据目录和这台机器上的其他数据一起备份。

---

## 工作原理 <a id="how-it-works"></a>

1. 入口：Stripe、GitHub、表单，或一次 cron 触发。普通 HTTP 进入你自己托管的端点。
2. 你的 VPS：Docker 上的 FastAPI + SQLite，或一个 Node.js 进程。任务、密钥和载荷留在你挂载的磁盘上。
3. 你拥有的目的地：你的 API、Discord、一个文件。跳转之间没有供应商的收件箱。

Webhook 路由运行在 SQLite WAL 上，内存低于 50MB，带重试和死信重放。EnvSync 为 `.env` 的值维护一个加密的键值存储。API Proxy 位于调用路径上，这样你的应用就不必复制重试循环。

Cron 布局与从 EasyCron 迁移：[自托管架构](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## 套件 <a id="the-suite"></a>

| 工具 | 它替代什么 | 形态 | 许可 |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron、cron-job.org | FastAPI + SQLite + Docker | $94.99 终身 |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck、Svix、Zapier 路由 | FastAPI + SQLite WAL + Docker | $94.99 终身 |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | 云端工作流 / worker SaaS | FastAPI + SQLModel + SQLite | $149.00 终身 |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | 托管运维仪表盘 | 与 Pipeline 并排的 Docker 仪表盘 | $94.99 终身 |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | 可观测性 SaaS | Node.js 进程，HTTP + UDP | $79.99 终身 |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / 额外的密钥租户 | 零信任代理、加密 KV、REST | $99 终身 |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | 用于重试的网关 SaaS | Node.js 进程：退避、限制、熔断 | $99 终身 |

### 套装

| 套装 | 包含 | 价格 |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99（省 $78） |
| [Complete Stack](https://nexuscore-store.whop.site) | 全部七个工具 | $399.99（省 $312） |

发布码 `DEVLAUNCH` 对每份许可（含套装）优惠 20%。

---

## SaaS 与自托管 <a id="saas-vs-self-hosted"></a>

| | 按月 SaaS | NexusCore |
|-|--------------|-----------|
| 账单 | EasyCron、Zapier 和工作流引擎的持续账单 | 没有月费。一份终身许可 |
| 数据 | 载荷、计划和日志放在别人的云上 | 数据完全归你，在你自己的主机上 |
| 搭建 | 注册账户、套餐限制、供应商锁定 | 单节点上约 60 秒的 Docker 搭建 |
| 代码 | 无法检查或分叉的封闭 SaaS | 许可附带完整源代码 |
| 遥测 | 用量计量 | 没有用量计量 |
| 集群 | 他们的多租户控制面 | 单节点。没有 Kubernetes |

托管 cron 每月 $20–$50，第一年就是 $240–$600。NexusCron 一次 $94.99。如果 VPS 已在预算里，唯一的新成本就是许可。

---

## 结账后你运行什么 <a id="what-you-run-after-checkout"></a>

### NexusCron。你自己的定时 HTTP

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[Cron 搭建](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [EasyCron 替代方案](https://nexuscore-store.whop.site/guides/easycron-alternative) · [从 EasyCron 迁出](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router。接收、转换、转发

Stripe、表单、GitHub → 你的 API。WAL SQLite、重试、死信重放。

[Webhook 搭建](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [SQLite 路由](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync。不用再手工复制 `.env`

```bash
npm start
# http://127.0.0.1:8787
```

1. 从会员文件下载代理。
2. 初始化加密存储，并添加第一台目标主机。
3. 在仪表盘确认同步。如果 CI 需要，接上 REST API。

[EnvSync 指南](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy。重试属于调用路径，而不是每个服务

```bash
npm start
# http://127.0.0.1:8080
```

把服务指向代理，而不是上游。设置重试、速率限制和回退。在本地仪表盘确认指标。

[API Proxy 指南](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## 常见问题 <a id="faq"></a>

### 这是开源的吗？

不是。NexusCore 是商业软件。终身许可在 Whop 结账后包含完整源代码。这个 GitHub 有文档和免费演示，不是授权源代码树，也不是 FOSS。

### 我需要一台新的 VPS 吗？

不需要。在笔记本或你已经在跑的机器上启动 Compose。把界面绑定到 127.0.0.1。

### 我需要 Kubernetes 吗？

不需要。

### 有东西会向外回连吗？

这些服务不发送用量数据。除非设置了 `NEXUS_TELEMETRY`，轻量示例保持静默。

### 密钥和日志放在哪里？

在你挂载的卷上。和主机上的其他数据一起备份。

### EnvSync 能替代 Vault 或 Doppler 吗？

如果非工程师已经在用共享保险库，就继续用。如果技术栈已经自托管，而你想在同一批主机上放加密配置，就运行 EnvSync。

### API Proxy 是完整的 API 网关吗？

不是。它是你自己主机上的重试、速率限制、熔断和回退。如果需要全组织的身份，请使用服务网格。

### 我可以只买一个工具吗？

可以。从 [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) 或 [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) 开始。[Ops Microservices](https://nexuscore-store.whop.site) 套装是 LogStream + EnvSync + API Proxy，价格 $199.99。

---

## 指南 <a id="guides"></a>

给已经在找办法离开托管 cron 和 webhook 的人准备的页面。

- [自托管 cron 替代方案](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [EasyCron 与 cron-job.org 替代方案](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [从 EasyCron 迁出](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [替换云端 webhook 服务](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [SQLite WAL webhook 路由](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [自托管流水线](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [自托管管理端](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## 获取

[购买终身许可 → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

使用优惠码 `DEVLAUNCH`，优惠 20%。

[购买 API Proxy](https://nexuscore-store.whop.site) · [购买 Ops Microservices（$199.99）](https://nexuscore-store.whop.site) · [购买 Complete Stack（$399.99）](https://nexuscore-store.whop.site)

NexusCore 是商业自托管软件。许可为终身、一次性付费，并包含源代码。在你控制的硬件上运行。
