<!-- language: Spanish (es) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> Idioma: **Español**

Este GitHub es la documentación del producto. NexusCore es comercial. El código fuente, las imágenes y los binarios se entregan después del pago en la [tienda](https://nexuscore-store.whop.site). Este árbol contiene solo el README.

**Deja de alquilar tu stack. Herramientas de desarrollo autohospedadas que son tuyas.**

Cron, webhooks, pipelines, logs, sincronización de variables de entorno y reintentos de API en un VPS que ya pagas. Una licencia de por vida. Código fuente completo tras la compra. SQLite en disco. Telemetría desactivada.

[![autohospedado](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![telemetría](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![licencia](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[Tienda](https://nexuscore-store.whop.site) · [Guías](https://nexuscore-store.whop.site/guides) · [Arquitectura](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [Proxy de API](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[Inicio rápido](#quick-start) · [Cómo funciona](#how-it-works) · [La suite](#the-suite) · [SaaS frente a autohospedado](#saas-vs-self-hosted) · [Qué ejecutas después del pago](#what-you-run-after-checkout) · [Preguntas frecuentes](#faq) · [Guías](#guides)

`DEVLAUNCH` → 20 % de descuento en cada licencia de por vida

---

## Por qué existe

EasyCron, Hookdeck, Zapier, Doppler, Datadog y las pasarelas de API miden el mismo trabajo: lanzar HTTP, enrutar un payload, mantener un `.env` sincronizado y reintentar una petición al origen.

NexusCore es ese trabajo como procesos en **tu** host.

- Paga una vez. Quédate con el código fuente.
- FastAPI + SQLite + Docker para cron, webhooks, pipeline y admin.
- Microservicios de un solo binario para LogStream, EnvSync y API Proxy.
- `NEXUS_TELEMETRY=off` es el valor predeterminado. Nada contacta con el exterior.
- Sin Kubernetes. Sin una bandeja de un proveedor entre cada salto.

**Consigue una licencia → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Inicio rápido <a id="quick-start"></a>

No clones este repositorio esperando un stack en marcha. Tras el pago, las licencias llegan como código fuente, imágenes de Docker y binarios en tus archivos de miembro. Los fragmentos de abajo son lo que ejecutas entonces.

### Ejemplo de Compose (después del pago)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — un solo nodo, ~60 s
# Las imágenes se entregan en los archivos de miembro. No son un pull público de este GitHub.
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

### Crear un trabajo por REST

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

### Microservicios de un solo binario (no hace falta Compose)

```bash
./envsync-agent    # sincronización cifrada de .env entre VPS, portátil y servicios
./api-proxy        # reintentos, límites de tasa, circuit breaker y alternativas
./logstream        # ingesta HTTP + UDP, SQLite y panel en vivo
```

No hay que crear ninguna cuenta después del pago. Enlaza a localhost y haz copia de seguridad de `./data` junto con el resto del equipo.

---

## Cómo funciona <a id="how-it-works"></a>

1. Entrada: Stripe, GitHub, formularios o un tick de cron. HTTP simple hacia un endpoint que tú alojas.
2. Tu VPS: FastAPI + SQLite en Docker, o un solo binario. Los trabajos, los secretos y los payloads permanecen en el disco que montas.
3. Destinos que son tuyos: tu API, Discord, un archivo. Ninguna bandeja de un proveedor entre los saltos.

El enrutamiento de webhooks corre en SQLite WAL, con menos de 50 MB de RAM, con reintentos y reproducción de dead-letter. EnvSync mantiene un almacén clave-valor cifrado para los valores de `.env`. API Proxy se sitúa en el camino para que tu aplicación no copie bucles de reintento.

Diseño de cron y migración desde EasyCron: [arquitectura autohospedada](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## La suite <a id="the-suite"></a>

| Herramienta | Qué sustituye | Forma | Licencia |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 de por vida |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, enrutamiento de Zapier | FastAPI + SQLite WAL + Docker | $94.99 de por vida |
| [NexusPipeline](https://nexuscore-store.whop.site) | SaaS de flujos de trabajo / workers en la nube | FastAPI + SQLModel + SQLite | $149.00 de por vida |
| [NexusAdmin](https://nexuscore-store.whop.site) | Panel de operaciones alojado | Panel Docker junto a Pipeline | $94.99 de por vida |
| [LogStream](https://nexuscore-store.whop.site) | SaaS de observabilidad | Node.js de un solo binario, HTTP + UDP | $79.99 de por vida |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / inquilino extra de secretos | Agente zero-trust, KV cifrado, REST | $99 de por vida |
| [API Proxy Service](https://nexuscore-store.whop.site) | SaaS de pasarela para reintentos | Un solo binario: backoff, límites, breaker | $99 de por vida |

### Paquetes

| Paquete | Incluye | Precio |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (ahorras $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | Las siete herramientas | $399.99 (ahorras $312) |

El código de lanzamiento `DEVLAUNCH` aplica un 20 % de descuento en cada licencia, incluidos los paquetes.

---

## SaaS frente a autohospedado <a id="saas-vs-self-hosted"></a>

| | SaaS mensual | NexusCore |
|-|--------------|-----------|
| Facturación | Facturas recurrentes de EasyCron, Zapier y motores de flujo | Cero facturas mensuales. Una licencia de por vida |
| Datos | Payloads, programaciones y logs en la nube de otro | Propiedad total de los datos en tu propio host |
| Puesta en marcha | Alta de cuenta, límites del plan y dependencia del proveedor | Puesta en marcha con Docker en 60 segundos en un solo nodo |
| Código | SaaS cerrado que no puedes inspeccionar ni bifurcar | Código fuente completo con la licencia |
| Telemetría | Medidores de uso | `NEXUS_TELEMETRY=off` |
| Clúster | Su plano multiinquilino | Un solo nodo. Sin Kubernetes |

Un cron alojado a $20–$50 al mes son $240–$600 el primer año. NexusCron cuesta $94.99 una sola vez. Si el VPS ya está en el presupuesto, el único coste nuevo es la licencia.

---

## Qué ejecutas después del pago <a id="what-you-run-after-checkout"></a>

### NexusCron. HTTP con un temporizador que es tuyo

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Configuración de cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Alternativa a EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Migrar desde EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Recibir, transformar, reenviar

Stripe, formularios, GitHub → tu API. SQLite WAL, reintentos, reproducción de dead-letter.

[Configuración de webhooks](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Enrutamiento con SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Deja de copiar `.env` a mano

```bash
./envsync-agent
```

1. Descarga el agente desde los archivos de miembro.
2. Inicializa el almacén cifrado y añade el primer host de destino.
3. Confirma la sincronización en el panel. Conecta la API REST si la CI lo necesita.

[Guía de EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Los reintentos van en el camino, no en cada servicio

```bash
./api-proxy
```

Apunta tus servicios al proxy en lugar del origen. Configura el reintento, el límite de tasa y la alternativa. Confirma las métricas en el panel local.

[Guía de API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Preguntas frecuentes <a id="faq"></a>

### ¿Es esto código abierto?

No. NexusCore es comercial. Una licencia de por vida incluye el código fuente completo tras el pago en Whop. Este GitHub es solo documentación, no el árbol de código, y no es FOSS.

### ¿Necesito un VPS nuevo?

No. Levanta Compose en un portátil o en un equipo que ya ejecutes. Enlaza la interfaz a 127.0.0.1.

### ¿Necesito Kubernetes?

No.

### ¿Algo contacta con el exterior?

`NEXUS_TELEMETRY=off` es el valor predeterminado. Sin medidores de uso, sin baliza de analítica, sin API del proveedor.

### ¿Dónde quedan los secretos y los logs?

En el volumen que montas. Haz copia de seguridad junto con el resto del host.

### ¿EnvSync sustituye a Vault o a Doppler?

Si quienes no son ingenieros ya trabajan en una bóveda compartida, consérvala. Si el stack ya es autohospedado y quieres configuración cifrada en los mismos hosts, ejecuta EnvSync.

### ¿API Proxy es una pasarela de API completa?

No. Son reintentos, límites de tasa, circuit breaker y alternativa en un host que es tuyo. Usa una malla si necesitas identidad para toda la organización.

### ¿Puedo comprar una sola herramienta?

Sí. Empieza con [API Proxy](https://nexuscore-store.whop.site) o [NexusCron](https://nexuscore-store.whop.site). El paquete [Ops Microservices](https://nexuscore-store.whop.site) es LogStream + EnvSync + API Proxy por $199.99.

---

## Guías <a id="guides"></a>

Páginas de alta intención para quien ya busca una salida del cron y los webhooks alojados.

- [Alternativa de cron autohospedada](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [Alternativa a EasyCron y cron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [Migrar desde EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [Sustituir servicios de webhook en la nube](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [Enrutamiento de webhooks con SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [Pipeline autohospedado](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [Admin autohospedado](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Consíguelo

[Compra licencias de por vida → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

Usa el código `DEVLAUNCH` para un 20 % de descuento.

[Comprar API Proxy](https://nexuscore-store.whop.site) · [Comprar Ops Microservices ($199.99)](https://nexuscore-store.whop.site) · [Comprar Complete Stack ($399.99)](https://nexuscore-store.whop.site)

NexusCore es software comercial autohospedado. Las licencias son de por vida, de pago único, e incluyen el código fuente. Ejecútalo en hardware que controlas.
