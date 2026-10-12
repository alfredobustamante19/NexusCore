<!-- language: Hindi (hi) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> भाषा: **हिन्दी**

यह GitHub उत्पाद का दस्तावेज़ है। NexusCore व्यावसायिक है। स्रोत, इमेज और बाइनरी चेकआउट के बाद [स्टोर](https://nexuscore-store.whop.site) पर मिलते हैं। इस ट्री में केवल README है।

**अपना स्टैक किराए पर लेना बंद करें। स्वयं होस्ट किए गए डेवलपर उपकरण, जो आपके अपने हों।**

Cron, webhook, पाइपलाइन, लॉग, env सिंक और API की पुनः कोशिशें उस VPS पर जिसे आप पहले ही चुकाते हैं। एक आजीवन लाइसेंस। खरीद के बाद पूरा स्रोत। डिस्क पर SQLite। टेलीमेट्री बंद।

[![स्वयं होस्ट](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![टेलीमेट्री](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![लाइसेंस](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[स्टोर](https://nexuscore-store.whop.site) · [गाइड](https://nexuscore-store.whop.site/guides) · [आर्किटेक्चर](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [API प्रॉक्सी](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[त्वरित शुरुआत](#quick-start) · [यह कैसे काम करता है](#how-it-works) · [सूट](#the-suite) · [SaaS बनाम स्वयं होस्ट](#saas-vs-self-hosted) · [चेकआउट के बाद आप क्या चलाते हैं](#what-you-run-after-checkout) · [सामान्य प्रश्न](#faq) · [गाइड](#guides)

`DEVLAUNCH` → हर आजीवन लाइसेंस पर 20% की छूट

---

## यह क्यों मौजूद है

EasyCron, Hookdeck, Zapier, Doppler, Datadog और API गेटवे एक ही काम का हिसाब रखते हैं: HTTP भेजना, पेलोड रूट करना, `.env` को सिंक रखना, अपस्ट्रीम पर पुनः कोशिश करना।

NexusCore वही काम **आपके** होस्ट पर प्रक्रियाओं के रूप में है।

- एक बार भुगतान करें। स्रोत अपने पास रखें।
- cron, webhook, पाइपलाइन और एडमिन के लिए FastAPI + SQLite + Docker।
- LogStream, EnvSync और API Proxy के लिए एकल-बाइनरी माइक्रोसर्विस।
- `NEXUS_TELEMETRY=off` डिफ़ॉल्ट है। कुछ भी बाहर संपर्क नहीं करता।
- Kubernetes नहीं। hops के बीच किसी विक्रेता का इनबॉक्स नहीं।

**लाइसेंस लें → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## त्वरित शुरुआत <a id="quick-start"></a>

इस रिपो को क्लोन करके चलता हुआ स्टैक मिलने की उम्मीद न करें। चेकआउट के बाद लाइसेंस स्रोत, Docker इमेज और बाइनरी के रूप में आपकी सदस्य फ़ाइलों में आते हैं। नीचे दिए अंश वही हैं जो आप तब चलाते हैं।

### Compose का उदाहरण (चेकआउट के बाद)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — एक नोड, ~60 सेकंड
# इमेज सदस्य फ़ाइलों में आती हैं। वे इस GitHub से सार्वजनिक pull नहीं हैं।
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

### REST पर एक जॉब बनाएँ

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

### एकल-बाइनरी माइक्रोसर्विस (Compose ज़रूरी नहीं)

```bash
./envsync-agent    # VPS, लैपटॉप और सेवाओं के बीच एन्क्रिप्टेड .env सिंक
./api-proxy        # पुनः कोशिश, दर सीमा, circuit breaker, फ़ॉलबैक
./logstream        # HTTP + UDP इनजेस्ट, SQLite, लाइव डैशबोर्ड
```

चेकआउट के बाद कोई खाता बनाना नहीं है। localhost से बाँधें, और `./data` का बैकअप बाकी मशीन के साथ लें।

---

## यह कैसे काम करता है <a id="how-it-works"></a>

1. प्रवेश: Stripe, GitHub, फ़ॉर्म, या एक cron tick। सादा HTTP उस एंडपॉइंट पर जिसे आप होस्ट करते हैं।
2. आपका VPS: Docker पर FastAPI + SQLite, या एक बाइनरी। जॉब, सीक्रेट और पेलोड उस डिस्क पर रहते हैं जिसे आप माउंट करते हैं।
3. आपके अपने गंतव्य: आपका API, Discord, एक फ़ाइल। hops के बीच किसी विक्रेता का इनबॉक्स नहीं।

Webhook रूटिंग SQLite WAL पर चलती है, 50MB RAM से कम में, पुनः कोशिश और dead-letter रीप्ले के साथ। EnvSync `.env` के मानों के लिए एन्क्रिप्टेड की-वैल्यू स्टोर रखता है। API Proxy रास्ते में बैठता है, ताकि आपका ऐप रिट्राय लूप की नकल न करे।

Cron का लेआउट और EasyCron से स्थानांतरण: [स्वयं होस्ट की गई आर्किटेक्चर](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## सूट <a id="the-suite"></a>

| उपकरण | यह किसकी जगह लेता है | रूप | लाइसेंस |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 आजीवन |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, Zapier रूटिंग | FastAPI + SQLite WAL + Docker | $94.99 आजीवन |
| [NexusPipeline](https://nexuscore-store.whop.site) | क्लाउड वर्कफ़्लो / वर्कर SaaS | FastAPI + SQLModel + SQLite | $149.00 आजीवन |
| [NexusAdmin](https://nexuscore-store.whop.site) | होस्टेड ऑप्स डैशबोर्ड | Pipeline के साथ Docker डैशबोर्ड | $94.99 आजीवन |
| [LogStream](https://nexuscore-store.whop.site) | ऑब्ज़र्वेबिलिटी SaaS | एकल-बाइनरी Node.js, HTTP + UDP | $79.99 आजीवन |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / अतिरिक्त सीक्रेट टेनेंट | ज़ीरो-ट्रस्ट एजेंट, एन्क्रिप्टेड KV, REST | $99 आजीवन |
| [API Proxy Service](https://nexuscore-store.whop.site) | पुनः कोशिश के लिए गेटवे SaaS | एकल बाइनरी: बैकऑफ़, सीमा, ब्रेकर | $99 आजीवन |

### बंडल

| बंडल | इसमें क्या है | कीमत |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 ($78 की बचत) |
| [Complete Stack](https://nexuscore-store.whop.site) | सभी सात उपकरण | $399.99 ($312 की बचत) |

लॉन्च कोड `DEVLAUNCH` हर लाइसेंस पर 20% की छूट है, बंडल सहित।

---

## SaaS बनाम स्वयं होस्ट <a id="saas-vs-self-hosted"></a>

| | मासिक SaaS | NexusCore |
|-|--------------|-----------|
| बिलिंग | EasyCron, Zapier और वर्कफ़्लो इंजन के बार-बार आने वाले बिल | शून्य मासिक बिल। एक आजीवन लाइसेंस |
| डेटा | पेलोड, शेड्यूल और लॉग किसी और के क्लाउड पर | आपके अपने होस्ट पर डेटा का पूरा स्वामित्व |
| सेटअप | खाता, प्लान की सीमाएँ और विक्रेता पर निर्भरता | एक नोड पर 60 सेकंड का Docker सेटअप |
| कोड | बंद SaaS, जिसे आप न देख सकते हैं न फ़ॉर्क कर सकते हैं | लाइसेंस के साथ पूरा स्रोत कोड |
| टेलीमेट्री | उपयोग के मीटर | `NEXUS_TELEMETRY=off` |
| क्लस्टर | उनका मल्टी-टेनेंट प्लेन | एक नोड। Kubernetes नहीं |

$20–$50 प्रति माह का होस्टेड cron पहले वर्ष में $240–$600 होता है। NexusCron एक बार $94.99 है। अगर VPS पहले से बजट में है, तो नया खर्च केवल लाइसेंस है।

---

## चेकआउट के बाद आप क्या चलाते हैं <a id="what-you-run-after-checkout"></a>

### NexusCron। आपके अपने टाइमर पर HTTP

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Cron सेटअप](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [EasyCron का विकल्प](https://nexuscore-store.whop.site/guides/easycron-alternative) · [EasyCron से हटें](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router। प्राप्त करें, बदलें, आगे भेजें

Stripe, फ़ॉर्म, GitHub → आपका API। WAL SQLite, पुनः कोशिश, dead-letter रीप्ले।

[Webhook सेटअप](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [SQLite रूटिंग](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync। `.env` हाथ से कॉपी करना बंद करें

```bash
./envsync-agent
```

1. सदस्य फ़ाइलों से एजेंट डाउनलोड करें।
2. एन्क्रिप्टेड स्टोर शुरू करें और पहला लक्ष्य होस्ट जोड़ें।
3. डैशबोर्ड में सिंक की पुष्टि करें। अगर CI को चाहिए, तो REST API जोड़ें।

[EnvSync गाइड](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy। पुनः कोशिश रास्ते में हो, हर सेवा में नहीं

```bash
./api-proxy
```

अपनी सेवाओं को अपस्ट्रीम की बजाय प्रॉक्सी पर इंगित करें। पुनः कोशिश, दर सीमा और फ़ॉलबैक सेट करें। स्थानीय डैशबोर्ड पर मेट्रिक की पुष्टि करें।

[API Proxy गाइड](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## सामान्य प्रश्न <a id="faq"></a>

### क्या यह ओपन सोर्स है?

नहीं। NexusCore व्यावसायिक है। आजीवन लाइसेंस में Whop पर चेकआउट के बाद पूरा स्रोत शामिल है। यह GitHub केवल दस्तावेज़ है, स्रोत ट्री नहीं, और यह FOSS नहीं है।

### क्या मुझे नया VPS चाहिए?

नहीं। Compose को लैपटॉप पर या उस मशीन पर चलाएँ जिसे आप पहले से चलाते हैं। UI को 127.0.0.1 से बाँधें।

### क्या मुझे Kubernetes चाहिए?

नहीं।

### क्या कुछ बाहर संपर्क करता है?

`NEXUS_TELEMETRY=off` डिफ़ॉल्ट है। कोई उपयोग मीटर नहीं, कोई एनालिटिक्स बीकन नहीं, कोई विक्रेता API नहीं।

### सीक्रेट और लॉग कहाँ रहते हैं?

उस वॉल्यूम पर जिसे आप माउंट करते हैं। उसका बैकअप बाकी होस्ट के साथ लें।

### क्या EnvSync, Vault या Doppler की जगह है?

अगर गैर-इंजीनियर पहले से साझा वॉल्ट में रहते हैं, तो उसे रखें। अगर स्टैक पहले से स्वयं होस्ट है और आप उन्हीं होस्ट पर एन्क्रिप्टेड कॉन्फ़िग चाहते हैं, तो EnvSync चलाएँ।

### क्या API Proxy पूरा API गेटवे है?

नहीं। यह आपके अपने होस्ट पर पुनः कोशिश, दर सीमा, circuit breaker और फ़ॉलबैक है। पूरे संगठन की पहचान चाहिए तो मेश इस्तेमाल करें।

### क्या मैं एक ही उपकरण खरीद सकता हूँ?

हाँ। [API Proxy](https://nexuscore-store.whop.site) या [NexusCron](https://nexuscore-store.whop.site) से शुरू करें। [Ops Microservices](https://nexuscore-store.whop.site) बंडल LogStream + EnvSync + API Proxy है, $199.99 में।

---

## गाइड <a id="guides"></a>

वे पृष्ठ उन लोगों के लिए हैं जो होस्टेड cron और webhook से निकलने का रास्ता पहले से खोज रहे हैं।

- [स्वयं होस्ट किया cron विकल्प](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [EasyCron और cron-job.org का विकल्प](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [EasyCron से हटें](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [क्लाउड webhook सेवाएँ बदलें](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [SQLite WAL webhook रूटिंग](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [स्वयं होस्ट की गई पाइपलाइन](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [स्वयं होस्ट किया एडमिन](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## इसे प्राप्त करें

[आजीवन लाइसेंस खरीदें → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

20% छूट के लिए कोड `DEVLAUNCH` इस्तेमाल करें।

[API Proxy खरीदें](https://nexuscore-store.whop.site) · [Ops Microservices खरीदें ($199.99)](https://nexuscore-store.whop.site) · [Complete Stack खरीदें ($399.99)](https://nexuscore-store.whop.site)

NexusCore व्यावसायिक स्वयं-होस्टेड सॉफ़्टवेयर है। लाइसेंस आजीवन हैं, एक बार के भुगतान वाले हैं, और स्रोत शामिल है। इसे उस हार्डवेयर पर चलाएँ जिसे आप नियंत्रित करते हैं।
