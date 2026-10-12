<!-- language: Bengali (bn) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> ভাষা: **বাংলা**

এই GitHub পণ্যের ডকুমেন্টেশন। NexusCore বাণিজ্যিক। সোর্স, ইমেজ ও বাইনারি চেকআউটের পর [স্টোরে](https://nexuscore-store.whop.site) পাওয়া যায়। এই ট্রিতে শুধু README আছে।

**স্ট্যাক ভাড়া নেওয়া বন্ধ করুন। স্ব-হোস্টেড ডেভেলপার টুল যা আপনার নিজের।**

Cron, webhook, পাইপলাইন, লগ, env সিঙ্ক এবং API পুনরায় চেষ্টা সেই VPS-এ যা আপনি আগেই দিচ্ছেন। একটি আজীবন লাইসেন্স। কেনার পর সম্পূর্ণ সোর্স। ডিস্কে SQLite। টেলিমেট্রি বন্ধ।

[![স্ব-হোস্টেড](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![টেলিমেট্রি](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![লাইসেন্স](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[স্টোর](https://nexuscore-store.whop.site) · [গাইড](https://nexuscore-store.whop.site/guides) · [আর্কিটেকচার](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [API প্রক্সি](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[দ্রুত শুরু](#quick-start) · [কীভাবে কাজ করে](#how-it-works) · [স্যুট](#the-suite) · [SaaS বনাম স্ব-হোস্টেড](#saas-vs-self-hosted) · [চেকআউটের পর আপনি কী চালান](#what-you-run-after-checkout) · [সাধারণ প্রশ্ন](#faq) · [গাইড](#guides)

`DEVLAUNCH` → প্রতিটি আজীবন লাইসেন্সে ২০% ছাড়

---

## এটা কেন আছে

EasyCron, Hookdeck, Zapier, Doppler, Datadog এবং API গেটওয়ে একই কাজের হিসাব রাখে: HTTP ছোড়া, একটি পেলোড রুট করা, `.env` সিঙ্কে রাখা, আপস্ট্রিমে আবার চেষ্টা করা।

NexusCore সেই কাজ **আপনার** হোস্টে প্রসেস হিসেবে।

- একবার দিন। সোর্স রেখে দিন।
- cron, webhook, পাইপলাইন ও অ্যাডমিনের জন্য FastAPI + SQLite + Docker।
- LogStream, EnvSync ও API Proxy-এর জন্য একক-বাইনারি মাইক্রোসার্ভিস।
- `NEXUS_TELEMETRY=off` ডিফল্ট। কিছুই বাইরে যোগাযোগ করে না।
- Kubernetes নেই। হপের মাঝে কোনো ভেন্ডরের ইনবক্স নেই।

**একটি লাইসেন্স নিন → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## দ্রুত শুরু <a id="quick-start"></a>

এই রিপো ক্লোন করে চলমান স্ট্যাক আশা করবেন না। চেকআউটের পর লাইসেন্স সোর্স, Docker ইমেজ ও বাইনারি হিসেবে আপনার সদস্য ফাইলে আসে। নিচের অংশগুলো তখন আপনি চালান।

### Compose-এর উদাহরণ (চেকআউটের পর)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — একটি নোড, প্রায় ৬০ সেকেন্ড
# ইমেজ সদস্য ফাইলে আসে। এগুলো এই GitHub থেকে পাবলিক pull নয়।
services:
  nexuscron:
    image: nexuscron:latest
    restart: unless-stopped
    ports:
      - "127.0.0.1:8787:8787"
    environment:
      TZ: Europe/Madrid
      NEXUSCRON_DATA: /data
      NEXUS_TELEMETRY: "off"
    volumes:
      - ./data/cron:/data

  webhook-router:
    image: webhook-router:latest
    restart: unless-stopped
    ports:
      - "127.0.0.1:8090:8090"
    environment:
      NEXUS_TELEMETRY: "off"
    volumes:
      - ./data/webhooks:/var/lib/webhook-router
```

### REST-এ একটি জব তৈরি

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{
    "name": "invoice-reminders",
    "cron": "0 8 * * 1-5",
    "method": "POST",
    "url": "https://billing.internal/jobs/remind",
    "timeout_ms": 15000
  }'
```

### একক-বাইনারি মাইক্রোসার্ভিস (Compose লাগে না)

```bash
./envsync-agent    # VPS, ল্যাপটপ ও সার্ভিসের মধ্যে এনক্রিপ্টেড .env সিঙ্ক
./api-proxy        # পুনরায় চেষ্টা, রেট লিমিট, circuit breaker, ফলব্যাক
./logstream        # HTTP + UDP ইনজেস্ট, SQLite, লাইভ ড্যাশবোর্ড
```

চেকআউটের পর কোনো অ্যাকাউন্ট বানাতে হয় না। localhost-এ বাঁধুন, আর `./data` বাকি মেশিনের সঙ্গে ব্যাকআপ রাখুন।

---

## কীভাবে কাজ করে <a id="how-it-works"></a>

1. প্রবেশ: Stripe, GitHub, ফর্ম, অথবা একটি cron টিক। সাধারণ HTTP আপনার হোস্ট করা এন্ডপয়েন্টে।
2. আপনার VPS: Docker-এ FastAPI + SQLite, অথবা একটি বাইনারি। জব, সিক্রেট ও পেলোড আপনার মাউন্ট করা ডিস্কে থাকে।
3. আপনার নিজের গন্তব্য: আপনার API, Discord, একটি ফাইল। হপের মাঝে কোনো ভেন্ডরের ইনবক্স নেই।

Webhook রাউটিং SQLite WAL-এ চলে, ৫০ এমবি RAM-এর নিচে, পুনরায় চেষ্টা ও dead-letter রিপ্লে সহ। EnvSync `.env` মানের জন্য একটি এনক্রিপ্টেড কী-ভ্যালু স্টোর রাখে। API Proxy পথে বসে, যাতে আপনার অ্যাপ রিট্রাই লুপ কপি না করে।

Cron-এর বিন্যাস ও EasyCron থেকে সরে আসা: [স্ব-হোস্টেড আর্কিটেকচার](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## স্যুট <a id="the-suite"></a>

| টুল | এটি কী প্রতিস্থাপন করে | রূপ | লাইসেন্স |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 আজীবন |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, Zapier রাউটিং | FastAPI + SQLite WAL + Docker | $94.99 আজীবন |
| [NexusPipeline](https://nexuscore-store.whop.site) | ক্লাউড ওয়ার্কফ্লো / ওয়ার্কার SaaS | FastAPI + SQLModel + SQLite | $149.00 আজীবন |
| [NexusAdmin](https://nexuscore-store.whop.site) | হোস্টেড অপস ড্যাশবোর্ড | Pipeline-এর পাশে Docker ড্যাশবোর্ড | $94.99 আজীবন |
| [LogStream](https://nexuscore-store.whop.site) | অবজারভেবিলিটি SaaS | একক-বাইনারি Node.js, HTTP + UDP | $79.99 আজীবন |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / অতিরিক্ত সিক্রেট টেন্যান্ট | জিরো-ট্রাস্ট এজেন্ট, এনক্রিপ্টেড KV, REST | $99 আজীবন |
| [API Proxy Service](https://nexuscore-store.whop.site) | পুনরায় চেষ্টার জন্য গেটওয়ে SaaS | একক বাইনারি: ব্যাকঅফ, সীমা, ব্রেকার | $99 আজীবন |

### বান্ডল

| বান্ডল | যাতে আছে | দাম |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 ($78 সাশ্রয়) |
| [Complete Stack](https://nexuscore-store.whop.site) | সাতটি টুলই | $399.99 ($312 সাশ্রয়) |

লঞ্চ কোড `DEVLAUNCH` প্রতিটি লাইসেন্সে ২০% ছাড়, বান্ডলসহ।

---

## SaaS বনাম স্ব-হোস্টেড <a id="saas-vs-self-hosted"></a>

| | মাসিক SaaS | NexusCore |
|-|--------------|-----------|
| বিল | EasyCron, Zapier ও ওয়ার্কফ্লো ইঞ্জিনের পুনরাবৃত্ত বিল | শূন্য মাসিক বিল। একটি আজীবন লাইসেন্স |
| ডেটা | পেলোড, সময়সূচি ও লগ অন্যের ক্লাউডে | আপনার নিজের হোস্টে ডেটার পূর্ণ মালিকানা |
| সেটআপ | অ্যাকাউন্ট, প্ল্যানের সীমা ও ভেন্ডর লক-ইন | একটি নোডে ৬০ সেকেন্ডের Docker সেটআপ |
| কোড | বন্ধ SaaS, যা আপনি দেখতে বা ফর্ক করতে পারেন না | লাইসেন্সের সঙ্গে সম্পূর্ণ সোর্স কোড |
| টেলিমেট্রি | ব্যবহারের মিটার | `NEXUS_TELEMETRY=off` |
| ক্লাস্টার | তাদের মাল্টি-টেন্যান্ট প্লেন | একটি নোড। Kubernetes নেই |

মাসে $20–$50-এর হোস্টেড cron প্রথম বছরে $240–$600। NexusCron একবার $94.99। VPS আগেই বাজেটে থাকলে নতুন খরচ শুধু লাইসেন্স।

---

## চেকআউটের পর আপনি কী চালান <a id="what-you-run-after-checkout"></a>

### NexusCron। আপনার নিজের টাইমারে HTTP

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Cron সেটআপ](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [EasyCron-এর বিকল্প](https://nexuscore-store.whop.site/guides/easycron-alternative) · [EasyCron থেকে সরে আসুন](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router। গ্রহণ, রূপান্তর, ফরওয়ার্ড

Stripe, ফর্ম, GitHub → আপনার API। WAL SQLite, পুনরায় চেষ্টা, dead-letter রিপ্লে।

[Webhook সেটআপ](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [SQLite রাউটিং](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync। হাতে `.env` কপি করা বন্ধ করুন

```bash
./envsync-agent
```

1. সদস্য ফাইল থেকে এজেন্ট ডাউনলোড করুন।
2. এনক্রিপ্টেড স্টোর চালু করুন এবং প্রথম লক্ষ্য হোস্ট যোগ করুন।
3. ড্যাশবোর্ডে সিঙ্ক নিশ্চিত করুন। CI লাগলে REST API যুক্ত করুন।

[EnvSync গাইড](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy। পুনরায় চেষ্টা পথে থাকুক, প্রতিটি সার্ভিসে নয়

```bash
./api-proxy
```

সার্ভিসগুলোকে আপস্ট্রিমের বদলে প্রক্সিতে নির্দেশ করুন। পুনরায় চেষ্টা, রেট লিমিট ও ফলব্যাক সেট করুন। স্থানীয় ড্যাশবোর্ডে মেট্রিক নিশ্চিত করুন।

[API Proxy গাইড](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## সাধারণ প্রশ্ন <a id="faq"></a>

### এটা কি ওপেন সোর্স?

না। NexusCore বাণিজ্যিক। আজীবন লাইসেন্সে Whop-এ চেকআউটের পর সম্পূর্ণ সোর্স থাকে। এই GitHub শুধু ডকুমেন্টেশন, সোর্স ট্রি নয়, এবং এটা FOSS নয়।

### আমার কি নতুন VPS লাগবে?

না। ল্যাপটপে বা যে মেশিন আপনি আগেই চালান, সেখানে Compose তুলুন। UI-কে 127.0.0.1-এ বাঁধুন।

### আমার কি Kubernetes লাগবে?

না।

### কিছু কি বাইরে যোগাযোগ করে?

`NEXUS_TELEMETRY=off` ডিফল্ট। কোনো ব্যবহার মিটার নেই, কোনো অ্যানালিটিক্স বিকন নেই, কোনো ভেন্ডর API নেই।

### সিক্রেট ও লগ কোথায় থাকে?

আপনি যে ভলিউম মাউন্ট করেন, সেখানে। বাকি হোস্টের সঙ্গে তার ব্যাকআপ রাখুন।

### EnvSync কি Vault বা Doppler-এর বিকল্প?

অ-ইঞ্জিনিয়াররা আগে থেকে একটি শেয়ারড ভল্টে থাকলে সেটা রাখুন। স্ট্যাক আগেই স্ব-হোস্টেড হলে এবং একই হোস্টে এনক্রিপ্টেড কনফিগ চাইলে EnvSync চালান।

### API Proxy কি পূর্ণ API গেটওয়ে?

না। এটা আপনার নিজের হোস্টে পুনরায় চেষ্টা, রেট লিমিট, circuit breaker ও ফলব্যাক। পুরো প্রতিষ্ঠানের পরিচয় লাগলে মেশ ব্যবহার করুন।

### আমি কি একটি টুল কিনতে পারি?

হ্যাঁ। [API Proxy](https://nexuscore-store.whop.site) বা [NexusCron](https://nexuscore-store.whop.site) দিয়ে শুরু করুন। [Ops Microservices](https://nexuscore-store.whop.site) বান্ডল হলো LogStream + EnvSync + API Proxy, দাম $199.99।

---

## গাইড <a id="guides"></a>

যারা হোস্টেড cron ও webhook ছাড়ার পথ আগেই খুঁজছেন, তাদের জন্য পাতা।

- [স্ব-হোস্টেড cron বিকল্প](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [EasyCron ও cron-job.org-এর বিকল্প](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [EasyCron থেকে সরে আসুন](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [ক্লাউড webhook সার্ভিস প্রতিস্থাপন](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [SQLite WAL webhook রাউটিং](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [স্ব-হোস্টেড পাইপলাইন](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [স্ব-হোস্টেড অ্যাডমিন](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## নিন

[আজীবন লাইসেন্স কিনুন → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

২০% ছাড়ের জন্য কোড `DEVLAUNCH` ব্যবহার করুন।

[API Proxy কিনুন](https://nexuscore-store.whop.site) · [Ops Microservices কিনুন ($199.99)](https://nexuscore-store.whop.site) · [Complete Stack কিনুন ($399.99)](https://nexuscore-store.whop.site)

NexusCore বাণিজ্যিক স্ব-হোস্টেড সফটওয়্যার। লাইসেন্স আজীবন, এককালীন, এবং সোর্সসহ। আপনি যে হার্ডওয়্যার নিয়ন্ত্রণ করেন, সেখানে চালান।
