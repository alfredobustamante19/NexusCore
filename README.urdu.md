<!-- language: Urdu (ur) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> زبان: **اردو**

یہ GitHub پروڈکٹ کی دستاویزات اور مفت ڈیمو ہے۔ NexusCore تجارتی ہے۔ لائسنس شدہ سورس چیک آؤٹ کے بعد [اسٹور](https://nexuscore-store.whop.site) پر ملتا ہے۔

**اپنا اسٹیک کرایے پر لینا بند کریں۔ خود میزبانی والے ڈویلپر ٹولز جو آپ کے اپنے ہوں۔**

Cron، webhook، پائپ لائن، لاگ، env سنک اور API کی دوبارہ کوششیں اس VPS پر جس کی قیمت آپ پہلے ہی ادا کرتے ہیں۔ ایک تاحیات لائسنس۔ خریداری کے بعد مکمل سورس۔ ڈسک پر SQLite۔ ٹیلی میٹری بند۔

[![خود میزبانی](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![ٹیلی میٹری](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![لائسنس](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[اسٹور](https://nexuscore-store.whop.site) · [رہنما](https://nexuscore-store.whop.site/guides) · [معماری](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [API پراکسی](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[فوری آغاز](#quick-start) · [یہ کیسے کام کرتا ہے](#how-it-works) · [سوٹ](#the-suite) · [SaaS بمقابلہ خود میزبانی](#saas-vs-self-hosted) · [چیک آؤٹ کے بعد آپ کیا چلاتے ہیں](#what-you-run-after-checkout) · [عمومی سوالات](#faq) · [رہنما](#guides)

`DEVLAUNCH` → ہر تاحیات لائسنس پر 20٪ رعایت

---

## یہ کیوں موجود ہے

EasyCron، Hookdeck، Zapier، Doppler، Datadog اور API گیٹ وے ایک ہی کام کا حساب رکھتے ہیں: HTTP بھیجنا، پے لوڈ روٹ کرنا، `.env` کو سنک رکھنا، اپ اسٹریم پر دوبارہ کوشش کرنا۔

NexusCore وہی کام **آپ کے** ہوسٹ پر عمل کے طور پر ہے۔

- ایک بار ادا کریں۔ سورس اپنے پاس رکھیں۔
- cron، webhook، پائپ لائن اور ایڈمن کے لیے FastAPI + SQLite + Docker۔
- LogStream، EnvSync اور API Proxy کے لیے Node.js عمل۔
- سروسز استعمال کا ڈیٹا نہیں بھیجتیں۔ لائٹ نمونہ اس وقت تک خاموش رہتا ہے جب تک `NEXUS_TELEMETRY` سیٹ نہ ہو۔
- Kubernetes نہیں۔ ہاپس کے درمیان کسی وینڈر کا ان باکس نہیں۔

**لائسنس لیں → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## فوری آغاز <a id="quick-start"></a>

مفت ڈیمو `NexusCore Developer Demo.zip` میں ہے۔ `NexusCore Developer Demo` فولڈر کھولیں (`./start-demo.sh`، Windows پر `.\Start Demo.ps1`، کنسول http://127.0.0.1:7400)۔ Python 3.12 یا نیا اور Node.js 24 یا نیا چاہیے۔ `pip install -r requirements.txt` کے بعد `nexuscore_lite.py` http://127.0.0.1:8000 پر سنتا ہے۔ لائسنس شدہ سورس چیک آؤٹ کے بعد ملتا ہے۔ نیچے دیے ٹکڑے وہی ہیں جو آپ تب چلاتے ہیں۔

### Compose کی مثال (چیک آؤٹ کے بعد)

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

### REST پر ایک جاب بنائیں

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

### Node.js عمل (Compose ضروری نہیں)

```bash
npm start          # EnvSync, http://127.0.0.1:8787. VPS، لیپ ٹاپ اور سروسز کے درمیان خفیہ .env سنک
npm start          # API Proxy, http://127.0.0.1:8080. دوبارہ کوشش، شرح کی حد، circuit breaker، فال بیک
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. HTTP + UDP انٹیک، SQLite، براہ راست ڈیش بورڈ
```

EnvSync پہلی بار چلتے وقت ایڈمن پاس ورڈ مانگتا ہے (`NEXUSENV_ADMIN_PASSWORD`)۔ LogStream `.env` میں `NEXUS_TOKEN` چاہتا ہے۔ localhost سے جوڑیں، اور ڈیٹا ڈائریکٹری کا بیک اپ باقی مشین کے ساتھ رکھیں۔

---

## یہ کیسے کام کرتا ہے <a id="how-it-works"></a>

1. داخلہ: Stripe، GitHub، فارم، یا ایک cron ٹک۔ سادہ HTTP اس اینڈ پوائنٹ پر جس کی میزبانی آپ کرتے ہیں۔
2. آپ کا VPS: Docker پر FastAPI + SQLite، یا ایک Node.js عمل۔ جابز، سیکرٹس اور پے لوڈ اس ڈسک پر رہتے ہیں جسے آپ ماؤنٹ کرتے ہیں۔
3. آپ کی اپنی منزل: آپ کا API، Discord، ایک فائل۔ ہاپس کے درمیان کسی وینڈر کا ان باکس نہیں۔

Webhook روٹنگ SQLite WAL پر چلتی ہے، دوبارہ کوشش اور ری پلے کے ساتھ۔ EnvSync `.env` کی قدروں کے لیے خفیہ کلید-قدر اسٹور رکھتا ہے۔ API Proxy راستے میں بیٹھتا ہے تاکہ آپ کی ایپ ری ٹرائی لوپ نقل نہ کرے۔

Cron کی ترتیب اور EasyCron سے منتقلی: [خود میزبانی والی معماری](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## سوٹ <a id="the-suite"></a>

| ٹول | یہ کس کی جگہ لیتا ہے | شکل | لائسنس |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron، cron-job.org | FastAPI + SQLite + Docker | $94.99 تاحیات |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck، Svix، Zapier روٹنگ | FastAPI + SQLite WAL + Docker | $94.99 تاحیات |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | کلاؤڈ ورک فلو / ورکر SaaS | FastAPI + SQLModel + SQLite | $149.00 تاحیات |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | میزبانی شدہ آپریشنز ڈیش بورڈ | Pipeline کے ساتھ Docker ڈیش بورڈ | $94.99 تاحیات |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | مشاہدے کا SaaS | Node.js عمل، HTTP + UDP | $79.99 تاحیات |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / اضافی سیکرٹ ٹیننٹ | زیرو ٹرسٹ ایجنٹ، خفیہ KV، REST | $99 تاحیات |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | دوبارہ کوشش کے لیے گیٹ وے SaaS | Node.js عمل: بیک آف، حد، بریکر | $99 تاحیات |

### بنڈل

| بنڈل | اس میں کیا ہے | قیمت |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 ($78 کی بچت) |
| [Complete Stack](https://nexuscore-store.whop.site) | تمام سات ٹولز | $399.99 ($312 کی بچت) |

لانچ کوڈ `DEVLAUNCH` ہر لائسنس پر 20٪ رعایت ہے، بنڈل سمیت۔

---

## SaaS بمقابلہ خود میزبانی <a id="saas-vs-self-hosted"></a>

| | ماہانہ SaaS | NexusCore |
|-|--------------|-----------|
| بل | EasyCron، Zapier اور ورک فلو انجن کے بار بار آنے والے بل | صفر ماہانہ بل۔ ایک تاحیات لائسنس |
| ڈیٹا | پے لوڈ، شیڈول اور لاگ کسی اور کے کلاؤڈ پر | آپ کے اپنے ہوسٹ پر ڈیٹا کی مکمل ملکیت |
| سیٹ اپ | اکاؤنٹ، پلان کی حدیں اور وینڈر پر انحصار | ایک نوڈ پر 60 سیکنڈ کا Docker سیٹ اپ |
| کوڈ | بند SaaS، جسے آپ نہ دیکھ سکتے ہیں نہ فورک کر سکتے ہیں | لائسنس کے ساتھ مکمل سورس کوڈ |
| ٹیلی میٹری | استعمال کے میٹر | کوئی استعمال میٹر نہیں |
| کلسٹر | ان کا ملٹی ٹیننٹ پلین | ایک نوڈ۔ Kubernetes نہیں |

$20–$50 فی ماہ کا میزبانی شدہ cron پہلے سال میں $240–$600 ہوتا ہے۔ NexusCron ایک بار $94.99 ہے۔ اگر VPS پہلے سے بجٹ میں ہے تو نیا خرچ صرف لائسنس ہے۔

---

## چیک آؤٹ کے بعد آپ کیا چلاتے ہیں <a id="what-you-run-after-checkout"></a>

### NexusCron۔ آپ کے اپنے ٹائمر پر HTTP

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[Cron سیٹ اپ](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [EasyCron کا متبادل](https://nexuscore-store.whop.site/guides/easycron-alternative) · [EasyCron سے نکلے](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router۔ وصول کریں، بدلیں، آگے بھیجیں

Stripe، فارم، GitHub → آپ کا API۔ WAL SQLite، دوبارہ کوشش اور ری پلے۔

[Webhook سیٹ اپ](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [SQLite روٹنگ](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync۔ `.env` ہاتھ سے نقل کرنا بند کریں

```bash
npm start
# http://127.0.0.1:8787
```

1. ممبر فائلوں سے ایجنٹ ڈاؤن لوڈ کریں۔
2. خفیہ اسٹور شروع کریں اور پہلا ہدف ہوسٹ شامل کریں۔
3. ڈیش بورڈ میں سنک کی تصدیق کریں۔ اگر CI کو چاہیے تو REST API جوڑیں۔

[EnvSync رہنما](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy۔ دوبارہ کوشش راستے میں ہو، ہر سروس میں نہیں

```bash
npm start
# http://127.0.0.1:8080
```

اپنی سروسز کو اپ اسٹریم کی بجائے پراکسی کی طرف کریں۔ دوبارہ کوشش، شرح کی حد اور فال بیک مقرر کریں۔ مقامی ڈیش بورڈ پر میٹرکس کی تصدیق کریں۔

[API Proxy رہنما](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## عمومی سوالات <a id="faq"></a>

### کیا یہ اوپن سورس ہے؟

نہیں۔ NexusCore تجارتی ہے۔ تاحیات لائسنس میں Whop پر چیک آؤٹ کے بعد مکمل سورس شامل ہے۔ اس GitHub میں دستاویزات اور مفت ڈیمو ہے، لائسنس شدہ سورس ٹری نہیں، اور یہ FOSS نہیں۔

### کیا مجھے نیا VPS چاہیے؟

نہیں۔ Compose کو لیپ ٹاپ پر یا اس مشین پر چلائیں جسے آپ پہلے سے چلا رہے ہیں۔ UI کو 127.0.0.1 سے جوڑیں۔

### کیا مجھے Kubernetes چاہیے؟

نہیں۔

### کیا کچھ باہر رابطہ کرتا ہے؟

سروسز استعمال کا ڈیٹا نہیں بھیجتیں۔ لائٹ نمونہ اس وقت تک خاموش رہتا ہے جب تک `NEXUS_TELEMETRY` سیٹ نہ ہو۔

### سیکرٹس اور لاگ کہاں رہتے ہیں؟

اس والیوم پر جسے آپ ماؤنٹ کرتے ہیں۔ اس کا بیک اپ باقی ہوسٹ کے ساتھ رکھیں۔

### کیا EnvSync، Vault یا Doppler کی جگہ ہے؟

اگر غیر انجینئر پہلے سے مشترکہ والٹ میں رہتے ہیں تو اسے رکھیں۔ اگر اسٹیک پہلے سے خود میزبانی والا ہے اور آپ انہی ہوسٹ پر خفیہ کنفیگ چاہتے ہیں تو EnvSync چلائیں۔

### کیا API Proxy مکمل API گیٹ وے ہے؟

نہیں۔ یہ آپ کے اپنے ہوسٹ پر دوبارہ کوشش، شرح کی حد، circuit breaker اور فال بیک ہے۔ پورے ادارے کی شناخت چاہیے تو میش استعمال کریں۔

### کیا میں ایک ہی ٹول خرید سکتا ہوں؟

ہاں۔ [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) یا [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) سے شروع کریں۔ [Ops Microservices](https://nexuscore-store.whop.site) بنڈل LogStream + EnvSync + API Proxy ہے، $199.99 میں۔

---

## رہنما <a id="guides"></a>

وہ صفحات ان لوگوں کے لیے ہیں جو میزبانی شدہ cron اور webhook سے نکلنے کا راستہ پہلے سے تلاش کر رہے ہیں۔

- [خود میزبانی والا cron متبادل](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [EasyCron اور cron-job.org کا متبادل](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [EasyCron سے نکلے](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [کلاؤڈ webhook سروسز بدلیں](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [SQLite WAL webhook روٹنگ](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [خود میزبانی والی پائپ لائن](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [خود میزبانی والا ایڈمن](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## حاصل کریں

[تاحیات لائسنس خریدیں → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

20٪ رعایت کے لیے کوڈ `DEVLAUNCH` استعمال کریں۔

[API Proxy خریدیں](https://nexuscore-store.whop.site) · [Ops Microservices خریدیں ($199.99)](https://nexuscore-store.whop.site) · [Complete Stack خریدیں ($399.99)](https://nexuscore-store.whop.site)

NexusCore تجارتی خود میزبانی والا سافٹ ویئر ہے۔ لائسنس تاحیات ہیں، یکمشت ادائیگی والے ہیں، اور سورس شامل ہے۔ اسے اس ہارڈ ویئر پر چلائیں جسے آپ کنٹرول کرتے ہیں۔
