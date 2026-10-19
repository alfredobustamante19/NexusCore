<!-- language: Modern Standard Arabic (ar) -->

# NexusCore
[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> اللغة: **العربية**

هذا المستودع على GitHub هو توثيق المنتج والعرض المجاني. NexusCore تجاري. يُسلَّم المصدر المرخّص بعد الدفع في [المتجر](https://nexuscore-store.whop.site).

**توقّف عن استئجار حزمتك. أدوات مطورين مستضافة ذاتيًا وتملكها أنت.**

Cron وwebhooks وخطوط المعالجة والسجلات ومزامنة البيئة وإعادة محاولات API على VPS تدفع ثمنه أصلًا. ترخيص واحد مدى الحياة. المصدر الكامل بعد الشراء. SQLite على القرص. القياس عن بُعد متوقف.

[![استضافة ذاتية](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![قياس عن بُعد](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![ترخيص](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[المتجر](https://nexuscore-store.whop.site) · [الأدلة](https://nexuscore-store.whop.site/guides) · [البنية](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [وكيل API](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[بدء سريع](#quick-start) · [كيف يعمل](#how-it-works) · [الحزمة](#the-suite) · [SaaS مقابل الاستضافة الذاتية](#saas-vs-self-hosted) · [ما تشغّله بعد الدفع](#what-you-run-after-checkout) · [أسئلة شائعة](#faq) · [الأدلة](#guides)

`DEVLAUNCH` → خصم 20% على كل ترخيص مدى الحياة

---

## لماذا وُجد هذا

EasyCron وHookdeck وZapier وDoppler وDatadog وبوابات API تحتسب العمل نفسه: إطلاق HTTP، وتوجيه حمولة، وإبقاء `.env` متزامنًا، وإعادة المحاولة نحو المصدر.

NexusCore هو ذلك العمل كعمليات على مضيفك **أنت**.

- ادفع مرة واحدة. احتفظ بالمصدر.
- FastAPI + SQLite + Docker من أجل cron وwebhooks وخط المعالجة والإدارة.
- عمليات Node.js من أجل LogStream وEnvSync وAPI Proxy.
- لا ترسل الخدمات بيانات استخدام. تبقى العيّنة الخفيفة صامتة ما لم يُضبط `NEXUS_TELEMETRY`.
- بلا Kubernetes. بلا صندوق وارد لبائع بين القفزات.

**احصل على ترخيص → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## بدء سريع <a id="quick-start"></a>

العرض المجاني في `NexusCore Developer Demo.zip` (`./start-demo.sh`، وعلى Windows `.\Start Demo.ps1`، ووحدة التحكم على http://127.0.0.1:7400). يستمع `nexuscore_lite.py` على http://127.0.0.1:8000 بعد `pip install -r requirements.txt`. يُسلَّم المصدر المرخّص بعد الدفع. المقتطفات أدناه هي ما تشغّله حينئذ.

### مثال Compose (بعد الدفع)

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

### إنشاء مهمة عبر REST

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

### عمليات Node.js (Compose غير مطلوب)

```bash
npm start          # EnvSync, http://127.0.0.1:8787. مزامنة مشفّرة لملفات .env بين VPS والحاسوب المحمول والخدمات
npm start          # API Proxy, http://127.0.0.1:8080. إعادات المحاولة وحدود المعدّل وcircuit breaker والبدائل
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. استقبال HTTP + UDP وSQLite ولوحة مباشرة
```

يضبط EnvSync كلمة مرور للمسؤول عند أول تشغيل (`NEXUSENV_ADMIN_PASSWORD`). يتوقع LogStream المتغير `NEXUS_TOKEN` في `.env`. اربط بـ localhost، واحفظ نسخة احتياطية من مجلد البيانات مع بقية الجهاز.

---

## كيف يعمل <a id="how-it-works"></a>

1. الدخول: Stripe أو GitHub أو النماذج أو نبضة cron. HTTP عادي إلى نقطة نهاية تستضيفها أنت.
2. VPS الخاص بك: FastAPI + SQLite على Docker، أو عملية Node.js. المهام والأسرار والحمولات تبقى على القرص الذي تركّبه.
3. وجهات تملكها: واجهة API لديك، أو Discord، أو ملف. لا صندوق وارد لبائع بين القفزات.

توجيه webhooks يعمل على SQLite WAL، بأقل من 50 ميغابايت من الذاكرة، مع إعادات المحاولة وإعادة تشغيل dead-letter. يُبقي EnvSync مخزن مفتاح-قيمة مشفّرًا لقيم `.env`. يجلس API Proxy على المسار كي لا ينسخ تطبيقك حلقات إعادة المحاولة.

تخطيط cron والانتقال من EasyCron: [بنية مستضافة ذاتيًا](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## الحزمة <a id="the-suite"></a>

| الأداة | ما تستبدله | الشكل | الترخيص |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron وcron-job.org | FastAPI + SQLite + Docker | $94.99 مدى الحياة |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck وSvix وتوجيه Zapier | FastAPI + SQLite WAL + Docker | $94.99 مدى الحياة |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | SaaS لسير العمل والعاملين في السحابة | FastAPI + SQLModel + SQLite | $149.00 مدى الحياة |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | لوحة تشغيل مستضافة | لوحة Docker إلى جانب Pipeline | $94.99 مدى الحياة |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | SaaS للمراقبة | عملية Node.js، HTTP + UDP | $79.99 مدى الحياة |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / مستأجر أسرار إضافي | وكيل zero-trust وKV مشفّر وREST | $99 مدى الحياة |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | SaaS بوابة لإعادات المحاولة | عملية Node.js: تراجع وحدود وقاطع | $99 مدى الحياة |

### الحزم المجمّعة

| الحزمة | تشمل | السعر |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (توفّر $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | الأدوات السبع كلها | $399.99 (توفّر $312) |

رمز الإطلاق `DEVLAUNCH` يخصم 20% من كل ترخيص، بما في ذلك الحزم المجمّعة.

---

## SaaS مقابل الاستضافة الذاتية <a id="saas-vs-self-hosted"></a>

| | SaaS شهري | NexusCore |
|-|--------------|-----------|
| الفوترة | فواتير متكررة من EasyCron وZapier ومحركات سير العمل | صفر فواتير شهرية. ترخيص واحد مدى الحياة |
| البيانات | الحمولات والجداول والسجلات على سحابة غيرك | ملكية كاملة للبيانات على مضيفك |
| الإعداد | إنشاء حساب وحدود الخطة والارتباط بالبائع | إعداد Docker خلال 60 ثانية على عقدة واحدة |
| الشيفرة | SaaS مغلق لا يمكنك فحصه ولا تفريعه | مصدر كامل مع الترخيص |
| القياس عن بُعد | عدّادات الاستخدام | بلا عدّاد استخدام |
| العنقود | مستواهم متعدد المستأجرين | عقدة واحدة. بلا Kubernetes |

Cron مستضاف بسعر $20–$50 شهريًا يساوي $240–$600 في السنة الأولى. NexusCron سعره $94.99 مرة واحدة. إن كان VPS داخل الميزانية أصلًا، فالتكلفة الجديدة الوحيدة هي الترخيص.

---

## ما تشغّله بعد الدفع <a id="what-you-run-after-checkout"></a>

### NexusCron. طلبات HTTP على مؤقّت تملكه

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[إعداد cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [بديل EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [الانتقال من EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. استقبل، وحوّل، وأعد التوجيه

Stripe والنماذج وGitHub → واجهة API لديك. SQLite WAL، وإعادات المحاولة، وإعادة تشغيل dead-letter.

[إعداد webhook](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [التوجيه عبر SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. توقّف عن نسخ `.env` يدويًا

```bash
npm start
# http://127.0.0.1:8787
```

1. نزّل الوكيل من ملفات العضوية.
2. هيّئ المخزن المشفّر وأضف أول مضيف هدف.
3. أكّد المزامنة في اللوحة. اربط واجهة REST إن احتاجها CI.

[دليل EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. إعادات المحاولة في المسار، لا في كل خدمة

```bash
npm start
# http://127.0.0.1:8080
```

وجّه خدماتك إلى الوكيل بدل المصدر. اضبط إعادة المحاولة وحدّ المعدّل والبديل. أكّد المقاييس على اللوحة المحلية.

[دليل API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## أسئلة شائعة <a id="faq"></a>

### هل هذا مفتوح المصدر؟

لا. NexusCore تجاري. ترخيص مدى الحياة يشمل المصدر الكامل بعد الدفع على Whop. هذا GitHub فيه التوثيق والعرض المجاني، وليس شجرة المصدر المرخّص، وهو ليس FOSS.

### هل أحتاج إلى VPS جديد؟

لا. شغّل Compose على حاسوب محمول أو على جهاز تديره أصلًا. اربط الواجهة بـ 127.0.0.1.

### هل أحتاج إلى Kubernetes؟

لا.

### هل يتصل شيء بالخارج؟

لا ترسل الخدمات بيانات استخدام. تبقى العيّنة الخفيفة صامتة ما لم يُضبط `NEXUS_TELEMETRY`.

### أين تقبع الأسرار والسجلات؟

على المجلد الذي تركّبه. احفظ نسخته الاحتياطية مع بقية المضيف.

### هل EnvSync بديل عن Vault أو Doppler؟

إن كان غير المهندسين يعيشون أصلًا في خزنة مشتركة، فأبقها. إن كانت الحزمة مستضافة ذاتيًا أصلًا وتريد إعدادًا مشفّرًا على المضيفين أنفسهم، فشغّل EnvSync.

### هل API Proxy بوابة API كاملة؟

لا. هو إعادات محاولة وحدود معدّل وcircuit breaker وبديل على مضيف تملكه. استخدم شبكة خدمات إن احتجت هوية على مستوى المؤسسة.

### هل يمكنني شراء أداة واحدة؟

نعم. ابدأ بـ [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) أو [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron). حزمة [Ops Microservices](https://nexuscore-store.whop.site) هي LogStream + EnvSync + API Proxy بسعر $199.99.

---

## الأدلة <a id="guides"></a>

صفحات لمن يبحث أصلًا عن طريق للخروج من cron وwebhooks المستضافة.

- [بديل cron مستضاف ذاتيًا](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [بديل EasyCron وcron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [الانتقال من EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [استبدال خدمات webhook السحابية](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [توجيه webhooks عبر SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [خط معالجة مستضاف ذاتيًا](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [إدارة مستضافة ذاتيًا](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## احصل عليه

[اشترِ تراخيص مدى الحياة → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

استخدم الرمز `DEVLAUNCH` للحصول على خصم 20%.

[اشترِ API Proxy](https://nexuscore-store.whop.site) · [اشترِ Ops Microservices ‏($199.99)](https://nexuscore-store.whop.site) · [اشترِ Complete Stack ‏($399.99)](https://nexuscore-store.whop.site)

NexusCore برمجيات تجارية مستضافة ذاتيًا. التراخيص مدى الحياة، وتُدفع مرة واحدة، وتشمل المصدر. شغّله على عتاد تتحكم به.
