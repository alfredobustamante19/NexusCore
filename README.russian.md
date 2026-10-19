<!-- language: Russian (ru) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> Язык: **Русский**

Этот GitHub — документация продукта и бесплатное демо. NexusCore коммерческий. Лицензированный исходный код выдаётся после оплаты в [магазине](https://nexuscore-store.whop.site).

**Хватит арендовать свой стек. Самостоятельно размещаемые инструменты разработчика, которые принадлежат вам.**

Cron, вебхуки, конвейеры, журналы, синхронизация окружения и повторные запросы к API на VPS, который вы уже оплачиваете. Одна пожизненная лицензия. Полный исходный код после покупки. SQLite на диске. Телеметрия выключена.

[![свой хостинг](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![телеметрия](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![лицензия](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[Магазин](https://nexuscore-store.whop.site) · [Руководства](https://nexuscore-store.whop.site/guides) · [Архитектура](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [API-прокси](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[Быстрый старт](#quick-start) · [Как это работает](#how-it-works) · [Набор](#the-suite) · [SaaS и свой хостинг](#saas-vs-self-hosted) · [Что вы запускаете после оплаты](#what-you-run-after-checkout) · [Вопросы](#faq) · [Руководства](#guides)

`DEVLAUNCH` → скидка 20% на каждую пожизненную лицензию

---

## Зачем это существует

EasyCron, Hookdeck, Zapier, Doppler, Datadog и API-шлюзы тарифицируют одну и ту же работу: отправить HTTP, маршрутизировать полезную нагрузку, держать `.env` в синхронизации, повторить запрос к upstream.

NexusCore — это та же работа в виде процессов на **вашем** хосте.

- Платите один раз. Оставляете исходный код себе.
- FastAPI + SQLite + Docker для cron, вебхуков, конвейера и админки.
- Процессы Node.js для LogStream, EnvSync и API Proxy.
- Сервисы не отправляют данные об использовании. Лёгкий образец молчит, пока не задан `NEXUS_TELEMETRY`.
- Без Kubernetes. Без ящика поставщика между переходами.

**Получить лицензию → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Быстрый старт <a id="quick-start"></a>

Бесплатное демо лежит в `NexusCore Developer Demo.zip` (`./start-demo.sh`, в Windows `.\Start Demo.ps1`, консоль на http://127.0.0.1:7400). `nexuscore_lite.py` слушает http://127.0.0.1:8000 после `pip install -r requirements.txt`. Лицензированный исходный код выдаётся после оплаты. Фрагменты ниже — это то, что вы запускаете тогда.

### Пример Compose (после оплаты)

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

### Создать задачу по REST

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

### Процессы Node.js (Compose не нужен)

```bash
npm start          # EnvSync, http://127.0.0.1:8787. шифрованная синхронизация .env между VPS, ноутбуком и сервисами
npm start          # API Proxy, http://127.0.0.1:8080. повторы, лимиты частоты, circuit breaker, запасные варианты
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. приём HTTP + UDP, SQLite, живая панель
```

EnvSync задаёт пароль администратора при первом запуске (`NEXUSENV_ADMIN_PASSWORD`). LogStream ждёт `NEXUS_TOKEN` в `.env`. Привяжите к localhost и сохраняйте резервную копию каталога данных вместе с остальной машиной.

---

## Как это работает <a id="how-it-works"></a>

1. Вход: Stripe, GitHub, формы или тик cron. Обычный HTTP на endpoint, который размещаете вы.
2. Ваш VPS: FastAPI + SQLite в Docker или процесс Node.js. Задачи, секреты и полезные нагрузки остаются на диске, который вы монтируете.
3. Назначения, которые принадлежат вам: ваш API, Discord, файл. Между переходами нет ящика поставщика.

Маршрутизация вебхуков работает на SQLite WAL, менее чем на 50 МБ ОЗУ, с повторами и повторным воспроизведением dead-letter. EnvSync хранит зашифрованное хранилище ключ-значение для значений `.env`. API Proxy стоит на пути, чтобы приложение не копировало циклы повторов.

Схема cron и переход с EasyCron: [архитектура на своём хостинге](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## Набор <a id="the-suite"></a>

| Инструмент | Что заменяет | Форма | Лицензия |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 пожизненно |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck, Svix, маршрутизация Zapier | FastAPI + SQLite WAL + Docker | $94.99 пожизненно |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | Облачный SaaS рабочих процессов и воркеров | FastAPI + SQLModel + SQLite | $149.00 пожизненно |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | Размещаемая панель эксплуатации | Панель Docker рядом с Pipeline | $94.99 пожизненно |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | SaaS наблюдаемости | Процесс Node.js, HTTP + UDP | $79.99 пожизненно |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / дополнительный арендатор секретов | Агент zero-trust, шифрованный KV, REST | $99 пожизненно |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | SaaS-шлюз для повторов | Процесс Node.js: backoff, лимиты, breaker | $99 пожизненно |

### Наборы

| Набор | Состав | Цена |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (экономия $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | Все семь инструментов | $399.99 (экономия $312) |

Код запуска `DEVLAUNCH` даёт скидку 20% на каждую лицензию, включая наборы.

---

## SaaS и свой хостинг <a id="saas-vs-self-hosted"></a>

| | Ежемесячный SaaS | NexusCore |
|-|--------------|-----------|
| Оплата | Повторяющиеся счета EasyCron, Zapier и движков рабочих процессов | Ноль ежемесячных счетов. Одна пожизненная лицензия |
| Данные | Нагрузки, расписания и журналы лежат в чужом облаке | Полное владение данными на вашем хосте |
| Запуск | Регистрация, лимиты тарифа и привязка к поставщику | Запуск в Docker за 60 секунд на одном узле |
| Код | Закрытый SaaS, который нельзя изучить или форкнуть | Полный исходный код вместе с лицензией |
| Телеметрия | Счётчики использования | Без счётчика использования |
| Кластер | Их мультитенантная плоскость | Один узел. Без Kubernetes |

Размещаемый cron за $20–$50 в месяц — это $240–$600 за первый год. NexusCron стоит $94.99 один раз. Если VPS уже заложен в бюджет, единственная новая трата — лицензия.

---

## Что вы запускаете после оплаты <a id="what-you-run-after-checkout"></a>

### NexusCron. HTTP по таймеру, который принадлежит вам

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[Настройка cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Альтернатива EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Уход с EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Принять, преобразовать, переслать

Stripe, формы, GitHub → ваш API. SQLite WAL, повторы, повторное воспроизведение dead-letter.

[Настройка вебхуков](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Маршрутизация на SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Хватит копировать `.env` вручную

```bash
npm start
# http://127.0.0.1:8787
```

1. Скачайте агент из файлов участника.
2. Инициализируйте зашифрованное хранилище и добавьте первый целевой хост.
3. Подтвердите синхронизацию на панели. Подключите REST API, если это нужно CI.

[Руководство по EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Повторы живут на пути, а не в каждом сервисе

```bash
npm start
# http://127.0.0.1:8080
```

Направьте сервисы на прокси, а не на upstream. Задайте повтор, лимит частоты и запасной вариант. Проверьте метрики на локальной панели.

[Руководство по API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Вопросы <a id="faq"></a>

### Это открытый исходный код?

Нет. NexusCore коммерческий. Пожизненная лицензия включает полный исходный код после оплаты на Whop. В этом GitHub документация и бесплатное демо, а не дерево лицензированных исходников, и это не FOSS.

### Нужен новый VPS?

Нет. Поднимите Compose на ноутбуке или на машине, которую вы уже ведёте. Привяжите интерфейс к 127.0.0.1.

### Нужен Kubernetes?

Нет.

### Что-нибудь связывается снаружи?

Сервисы не отправляют данные об использовании. Лёгкий образец молчит, пока не задан `NEXUS_TELEMETRY`.

### Где лежат секреты и журналы?

На томе, который вы монтируете. Делайте его резервную копию вместе с остальным хостом.

### EnvSync заменяет Vault или Doppler?

Если люди вне инженерии уже живут в общем хранилище секретов, оставьте его. Если стек уже на своём хостинге и вам нужна шифрованная конфигурация на тех же хостах, запускайте EnvSync.

### API Proxy — это полноценный API-шлюз?

Нет. Это повторы, лимиты частоты, circuit breaker и запасной вариант на хосте, который принадлежит вам. Используйте mesh, если нужна идентификация на всю организацию.

### Можно купить один инструмент?

Да. Начните с [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) или [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron). Набор [Ops Microservices](https://nexuscore-store.whop.site) — это LogStream + EnvSync + API Proxy за $199.99.

---

## Руководства <a id="guides"></a>

Страницы для тех, кто уже ищет способ уйти с размещаемого cron и вебхуков.

- [Свой cron вместо чужого](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [Альтернатива EasyCron и cron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [Уход с EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [Замена облачных сервисов вебхуков](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [Маршрутизация вебхуков на SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [Свой конвейер](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [Своя админка](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Получить

[Купить пожизненные лицензии → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

Используйте код `DEVLAUNCH`, чтобы получить скидку 20%.

[Купить API Proxy](https://nexuscore-store.whop.site) · [Купить Ops Microservices ($199.99)](https://nexuscore-store.whop.site) · [Купить Complete Stack ($399.99)](https://nexuscore-store.whop.site)

NexusCore — коммерческое ПО для своего хостинга. Лицензии пожизненные, разовая оплата, исходный код входит в комплект. Запускайте на оборудовании, которым управляете вы.
