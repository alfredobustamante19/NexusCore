<!-- language: Russian (ru) -->

# NexusCore

> Язык: **Русский**

Этот GitHub — документация продукта. NexusCore коммерческий. Исходный код, образы и бинарные файлы выдаются после оплаты в [магазине](https://nexuscore-store.whop.site). В этом дереве только README.

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
- Микросервисы из одного бинарного файла для LogStream, EnvSync и API Proxy.
- `NEXUS_TELEMETRY=off` — значение по умолчанию. Ничего не связывается снаружи.
- Без Kubernetes. Без ящика поставщика между переходами.

**Получить лицензию → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Быстрый старт <a id="quick-start"></a>

Не клонируйте этот репозиторий в расчёте на уже работающий стек. После оплаты лицензии приходят как исходный код, образы Docker и бинарные файлы в ваших файлах участника. Фрагменты ниже — это то, что вы запускаете тогда.

### Пример Compose (после оплаты)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — один узел, ~60 с
# Образы приходят в файлах участника. Это не публичный pull с этого GitHub.
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

### Создать задачу по REST

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

### Микросервисы из одного бинарного файла (Compose не нужен)

```bash
./envsync-agent    # шифрованная синхронизация .env между VPS, ноутбуком и сервисами
./api-proxy        # повторы, лимиты частоты, circuit breaker, запасные варианты
./logstream        # приём HTTP + UDP, SQLite, живая панель
```

После оплаты учётную запись создавать не нужно. Привяжите к localhost и сохраняйте резервную копию `./data` вместе с остальной машиной.

---

## Как это работает <a id="how-it-works"></a>

1. Вход: Stripe, GitHub, формы или тик cron. Обычный HTTP на endpoint, который размещаете вы.
2. Ваш VPS: FastAPI + SQLite в Docker или один бинарный файл. Задачи, секреты и полезные нагрузки остаются на диске, который вы монтируете.
3. Назначения, которые принадлежат вам: ваш API, Discord, файл. Между переходами нет ящика поставщика.

Маршрутизация вебхуков работает на SQLite WAL, менее чем на 50 МБ ОЗУ, с повторами и повторным воспроизведением dead-letter. EnvSync хранит зашифрованное хранилище ключ-значение для значений `.env`. API Proxy стоит на пути, чтобы приложение не копировало циклы повторов.

Схема cron и переход с EasyCron: [архитектура на своём хостинге](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## Набор <a id="the-suite"></a>

| Инструмент | Что заменяет | Форма | Лицензия |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 пожизненно |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, маршрутизация Zapier | FastAPI + SQLite WAL + Docker | $94.99 пожизненно |
| [NexusPipeline](https://nexuscore-store.whop.site) | Облачный SaaS рабочих процессов и воркеров | FastAPI + SQLModel + SQLite | $149.00 пожизненно |
| [NexusAdmin](https://nexuscore-store.whop.site) | Размещаемая панель эксплуатации | Панель Docker рядом с Pipeline | $94.99 пожизненно |
| [LogStream](https://nexuscore-store.whop.site) | SaaS наблюдаемости | Node.js одним бинарным файлом, HTTP + UDP | $79.99 пожизненно |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / дополнительный арендатор секретов | Агент zero-trust, шифрованный KV, REST | $99 пожизненно |
| [API Proxy Service](https://nexuscore-store.whop.site) | SaaS-шлюз для повторов | Один бинарный файл: backoff, лимиты, breaker | $99 пожизненно |

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
| Телеметрия | Счётчики использования | `NEXUS_TELEMETRY=off` |
| Кластер | Их мультитенантная плоскость | Один узел. Без Kubernetes |

Размещаемый cron за $20–$50 в месяц — это $240–$600 за первый год. NexusCron стоит $94.99 один раз. Если VPS уже заложен в бюджет, единственная новая трата — лицензия.

---

## Что вы запускаете после оплаты <a id="what-you-run-after-checkout"></a>

### NexusCron. HTTP по таймеру, который принадлежит вам

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Настройка cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Альтернатива EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Уход с EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Принять, преобразовать, переслать

Stripe, формы, GitHub → ваш API. SQLite WAL, повторы, повторное воспроизведение dead-letter.

[Настройка вебхуков](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Маршрутизация на SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Хватит копировать `.env` вручную

```bash
./envsync-agent
```

1. Скачайте агент из файлов участника.
2. Инициализируйте зашифрованное хранилище и добавьте первый целевой хост.
3. Подтвердите синхронизацию на панели. Подключите REST API, если это нужно CI.

[Руководство по EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Повторы живут на пути, а не в каждом сервисе

```bash
./api-proxy
```

Направьте сервисы на прокси, а не на upstream. Задайте повтор, лимит частоты и запасной вариант. Проверьте метрики на локальной панели.

[Руководство по API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Вопросы <a id="faq"></a>

### Это открытый исходный код?

Нет. NexusCore коммерческий. Пожизненная лицензия включает полный исходный код после оплаты на Whop. Этот GitHub — только документация, не дерево исходников, и это не FOSS.

### Нужен новый VPS?

Нет. Поднимите Compose на ноутбуке или на машине, которую вы уже ведёте. Привяжите интерфейс к 127.0.0.1.

### Нужен Kubernetes?

Нет.

### Что-нибудь связывается снаружи?

`NEXUS_TELEMETRY=off` — значение по умолчанию. Нет счётчиков использования, нет маяка аналитики, нет API поставщика.

### Где лежат секреты и журналы?

На томе, который вы монтируете. Делайте его резервную копию вместе с остальным хостом.

### EnvSync заменяет Vault или Doppler?

Если люди вне инженерии уже живут в общем хранилище секретов, оставьте его. Если стек уже на своём хостинге и вам нужна шифрованная конфигурация на тех же хостах, запускайте EnvSync.

### API Proxy — это полноценный API-шлюз?

Нет. Это повторы, лимиты частоты, circuit breaker и запасной вариант на хосте, который принадлежит вам. Используйте mesh, если нужна идентификация на всю организацию.

### Можно купить один инструмент?

Да. Начните с [API Proxy](https://nexuscore-store.whop.site) или [NexusCron](https://nexuscore-store.whop.site). Набор [Ops Microservices](https://nexuscore-store.whop.site) — это LogStream + EnvSync + API Proxy за $199.99.

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
