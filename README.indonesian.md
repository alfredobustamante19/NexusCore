<!-- language: Indonesian (id) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> Bahasa: **Bahasa Indonesia**

GitHub ini adalah dokumentasi produk dan demo gratis. NexusCore bersifat komersial. Kode berlisensi dikirim setelah checkout di [toko](https://nexuscore-store.whop.site).

**Berhenti menyewa stack Anda. Alat pengembang yang dihosting sendiri dan menjadi milik Anda.**

Cron, webhook, pipeline, log, sinkronisasi env, dan percobaan ulang API di VPS yang sudah Anda bayar. Satu lisensi seumur hidup. Kode sumber lengkap setelah pembelian. SQLite di disk. Telemetri mati.

[![self-hosted](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![telemetri](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![lisensi](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[Toko](https://nexuscore-store.whop.site) · [Panduan](https://nexuscore-store.whop.site/guides) · [Arsitektur](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [Proxy API](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[Mulai cepat](#quick-start) · [Cara kerja](#how-it-works) · [Rangkaian alat](#the-suite) · [SaaS vs self-hosted](#saas-vs-self-hosted) · [Yang Anda jalankan setelah checkout](#what-you-run-after-checkout) · [FAQ](#faq) · [Panduan](#guides)

`DEVLAUNCH` → diskon 20% untuk setiap lisensi seumur hidup

---

## Mengapa ini ada

EasyCron, Hookdeck, Zapier, Doppler, Datadog, dan gateway API menagih pekerjaan yang sama: menembakkan HTTP, merutekan payload, menjaga `.env` tetap sinkron, mencoba ulang permintaan ke upstream.

NexusCore adalah pekerjaan itu sebagai proses di host **Anda**.

- Bayar sekali. Simpan kode sumbernya.
- FastAPI + SQLite + Docker untuk cron, webhook, pipeline, dan admin.
- Proses Node.js untuk LogStream, EnvSync, dan API Proxy.
- Layanan tidak mengirim data penggunaan. Sampel lite tetap diam kecuali `NEXUS_TELEMETRY` diatur.
- Tanpa Kubernetes. Tanpa kotak masuk vendor di antara lompatan.

**Dapatkan lisensi → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Mulai cepat <a id="quick-start"></a>

Demo gratis ada di `NexusCore Developer Demo.zip` (`./start-demo.sh`, di Windows `.\Start Demo.ps1`, konsol di http://127.0.0.1:7400). `nexuscore_lite.py` mendengarkan di http://127.0.0.1:8000 setelah `pip install -r requirements.txt`. Kode berlisensi dikirim setelah checkout. Cuplikan di bawah ini adalah yang Anda jalankan saat itu.

### Contoh Compose (setelah checkout)

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

### Membuat job lewat REST

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

### Proses Node.js (Compose tidak wajib)

```bash
npm start          # EnvSync, http://127.0.0.1:8787. sinkronisasi .env terenkripsi lintas VPS, laptop, dan layanan
npm start          # API Proxy, http://127.0.0.1:8080. percobaan ulang, batas laju, circuit breaker, fallback
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. ingest HTTP + UDP, SQLite, dasbor langsung
```

EnvSync meminta kata sandi admin saat pertama kali jalan (`NEXUSENV_ADMIN_PASSWORD`). LogStream mengharapkan `NEXUS_TOKEN` di `.env`. Ikat ke localhost, dan cadangkan direktori data bersama sisa mesin.

---

## Cara kerja <a id="how-it-works"></a>

1. Masuk: Stripe, GitHub, formulir, atau tick cron. HTTP biasa ke endpoint yang Anda host.
2. VPS Anda: FastAPI + SQLite di Docker, atau satu proses Node.js. Job, rahasia, dan payload tetap di disk yang Anda mount.
3. Tujuan yang Anda miliki: API Anda, Discord, sebuah berkas. Tidak ada kotak masuk vendor di antara lompatan.

Perutean webhook berjalan di SQLite WAL, di bawah 50 MB RAM, dengan percobaan ulang dan pemutaran ulang dead-letter. EnvSync menyimpan penyimpanan kunci-nilai terenkripsi untuk nilai `.env`. API Proxy berada di jalur agar aplikasi Anda tidak menyalin loop percobaan ulang.

Tata letak cron dan perpindahan dari EasyCron: [arsitektur self-hosted](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## Rangkaian alat <a id="the-suite"></a>

| Alat | Yang digantikan | Bentuk | Lisensi |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 seumur hidup |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck, Svix, perutean Zapier | FastAPI + SQLite WAL + Docker | $94.99 seumur hidup |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | SaaS alur kerja / worker cloud | FastAPI + SQLModel + SQLite | $149.00 seumur hidup |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | Dasbor operasi yang dihosting | Dasbor Docker di samping Pipeline | $94.99 seumur hidup |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | SaaS observabilitas | Proses Node.js, HTTP + UDP | $79.99 seumur hidup |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / tenant rahasia tambahan | Agen zero-trust, KV terenkripsi, REST | $99 seumur hidup |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | SaaS gateway untuk percobaan ulang | Proses Node.js: backoff, batas, breaker | $99 seumur hidup |

### Bundel

| Bundel | Isi | Harga |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (hemat $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | Ketujuh alat | $399.99 (hemat $312) |

Kode peluncuran `DEVLAUNCH` memberi diskon 20% untuk setiap lisensi, termasuk bundel.

---

## SaaS vs self-hosted <a id="saas-vs-self-hosted"></a>

| | SaaS bulanan | NexusCore |
|-|--------------|-----------|
| Tagihan | Faktur berulang EasyCron, Zapier, dan mesin alur kerja | Nol tagihan bulanan. Satu lisensi seumur hidup |
| Data | Payload, jadwal, dan log berada di cloud orang lain | Kepemilikan data penuh di host Anda sendiri |
| Penyiapan | Pendaftaran akun, batas paket, dan ketergantungan vendor | Penyiapan Docker 60 detik di satu node |
| Kode | SaaS tertutup yang tidak bisa Anda periksa atau fork | Kode sumber lengkap bersama lisensi |
| Telemetri | Meter penggunaan | Tidak ada meter penggunaan |
| Kluster | Bidang multi-tenant mereka | Satu node. Tanpa Kubernetes |

Cron yang dihosting seharga $20–$50 per bulan menjadi $240–$600 di tahun pertama. NexusCron $94.99 sekali. Jika VPS sudah ada dalam anggaran, satu-satunya biaya baru adalah lisensi.

---

## Yang Anda jalankan setelah checkout <a id="what-you-run-after-checkout"></a>

### NexusCron. HTTP pada pengatur waktu yang Anda miliki

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[Penyiapan cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Alternatif EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Pindah dari EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Terima, ubah, teruskan

Stripe, formulir, GitHub → API Anda. SQLite WAL, percobaan ulang, pemutaran ulang dead-letter.

[Penyiapan webhook](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Perutean SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Berhenti menyalin `.env` dengan tangan

```bash
npm start
# http://127.0.0.1:8787
```

1. Unduh agen dari berkas anggota.
2. Inisialisasi penyimpanan terenkripsi dan tambahkan host tujuan pertama.
3. Konfirmasi sinkronisasi di dasbor. Sambungkan API REST jika CI membutuhkannya.

[Panduan EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Percobaan ulang ada di jalur, bukan di setiap layanan

```bash
npm start
# http://127.0.0.1:8080
```

Arahkan layanan Anda ke proxy, bukan ke upstream. Atur percobaan ulang, batas laju, dan fallback. Konfirmasi metrik di dasbor lokal.

[Panduan API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## FAQ <a id="faq"></a>

### Apakah ini sumber terbuka?

Tidak. NexusCore bersifat komersial. Lisensi seumur hidup mencakup kode sumber lengkap setelah checkout di Whop. GitHub ini berisi dokumentasi dan demo gratis, bukan pohon kode berlisensi, dan ini bukan FOSS.

### Apakah saya perlu VPS baru?

Tidak. Jalankan Compose di laptop atau mesin yang sudah Anda operasikan. Ikat antarmuka ke 127.0.0.1.

### Apakah saya perlu Kubernetes?

Tidak.

### Apakah ada yang menghubungi luar?

Layanan tidak mengirim data penggunaan. Sampel lite tetap diam kecuali `NEXUS_TELEMETRY` diatur.

### Di mana rahasia dan log berada?

Di volume yang Anda mount. Cadangkan bersama sisa host.

### Apakah EnvSync pengganti Vault/Doppler?

Jika orang non-engineer sudah bekerja di brankas bersama, pertahankan itu. Jika stack sudah dihosting sendiri dan Anda ingin konfigurasi terenkripsi di host yang sama, jalankan EnvSync.

### Apakah API Proxy gateway API yang lengkap?

Tidak. Ini adalah percobaan ulang, batas laju, circuit breaker, dan fallback di host yang Anda miliki. Gunakan mesh jika Anda membutuhkan identitas seluruh organisasi.

### Bisakah saya membeli satu alat saja?

Ya. Mulai dari [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) atau [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron). Bundel [Ops Microservices](https://nexuscore-store.whop.site) adalah LogStream + EnvSync + API Proxy seharga $199.99.

---

## Panduan <a id="guides"></a>

Halaman berniat tinggi untuk orang yang sudah mencari jalan keluar dari cron dan webhook yang dihosting.

- [Alternatif cron self-hosted](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [Alternatif EasyCron dan cron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [Pindah dari EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [Mengganti layanan webhook cloud](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [Perutean webhook SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [Pipeline self-hosted](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [Admin self-hosted](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Dapatkan

[Beli lisensi seumur hidup → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

Gunakan kode `DEVLAUNCH` untuk diskon 20%.

[Beli API Proxy](https://nexuscore-store.whop.site) · [Beli Ops Microservices ($199.99)](https://nexuscore-store.whop.site) · [Beli Complete Stack ($399.99)](https://nexuscore-store.whop.site)

NexusCore adalah perangkat lunak komersial yang dihosting sendiri. Lisensi bersifat seumur hidup, sekali bayar, dan mencakup kode sumber. Jalankan di perangkat keras yang Anda kendalikan.
