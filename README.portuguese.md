<!-- language: Portuguese (pt) — Brazilian Portuguese, the larger share of Portuguese speakers -->

# NexusCore

> Idioma: **Português**

Este GitHub é a documentação do produto. O NexusCore é comercial. O código-fonte, as imagens e os binários são entregues após o pagamento na [loja](https://nexuscore-store.whop.site). Esta árvore contém apenas o README.

**Pare de alugar a sua stack. Ferramentas de desenvolvedor auto-hospedadas que são suas.**

Cron, webhooks, pipelines, logs, sincronização de ambiente e novas tentativas de API em um VPS que você já paga. Uma licença vitalícia. Código-fonte completo após a compra. SQLite em disco. Telemetria desligada.

[![auto-hospedado](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![telemetria](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![licença](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[Loja](https://nexuscore-store.whop.site) · [Guias](https://nexuscore-store.whop.site/guides) · [Arquitetura](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [Proxy de API](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[Início rápido](#quick-start) · [Como funciona](#how-it-works) · [A suíte](#the-suite) · [SaaS e auto-hospedado](#saas-vs-self-hosted) · [O que você executa após o pagamento](#what-you-run-after-checkout) · [Perguntas frequentes](#faq) · [Guias](#guides)

`DEVLAUNCH` → 20% de desconto em cada licença vitalícia

---

## Por que isto existe

EasyCron, Hookdeck, Zapier, Doppler, Datadog e gateways de API medem o mesmo trabalho: disparar HTTP, rotear um payload, manter um `.env` sincronizado, tentar de novo uma chamada upstream.

O NexusCore é esse trabalho como processos no **seu** host.

- Pague uma vez. Fique com o código-fonte.
- FastAPI + SQLite + Docker para cron, webhooks, pipeline e admin.
- Microsserviços de binário único para LogStream, EnvSync e API Proxy.
- `NEXUS_TELEMETRY=off` é o padrão. Nada entra em contato com o exterior.
- Sem Kubernetes. Sem uma caixa de entrada de fornecedor entre os saltos.

**Obter uma licença → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Início rápido <a id="quick-start"></a>

Não clone este repositório esperando uma stack em execução. Após o pagamento, as licenças chegam como código-fonte, imagens Docker e binários nos seus arquivos de membro. Os trechos abaixo são o que você executa nesse momento.

### Exemplo de Compose (após o pagamento)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — nó único, ~60 s
# As imagens vêm nos arquivos de membro. Não são um pull público deste GitHub.
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

### Criar um job por REST

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

### Microsserviços de binário único (Compose não é necessário)

```bash
./envsync-agent    # sincronização criptografada de .env entre VPS, notebook e serviços
./api-proxy        # novas tentativas, limites de taxa, circuit breaker e fallbacks
./logstream        # ingestão HTTP + UDP, SQLite, painel ao vivo
```

Não há conta para criar após o pagamento. Associe a localhost e faça backup de `./data` junto com o resto da máquina.

---

## Como funciona <a id="how-it-works"></a>

1. Entrada: Stripe, GitHub, formulários ou um tick de cron. HTTP simples para um endpoint que você hospeda.
2. O seu VPS: FastAPI + SQLite no Docker, ou um binário único. Jobs, segredos e payloads ficam no disco que você monta.
3. Destinos que são seus: a sua API, o Discord, um arquivo. Nenhuma caixa de entrada de fornecedor entre os saltos.

O roteamento de webhooks corre em SQLite WAL, com menos de 50 MB de RAM, com novas tentativas e reexecução de dead-letter. O EnvSync mantém um armazenamento chave-valor criptografado para os valores de `.env`. O API Proxy fica no caminho para que a sua aplicação não copie laços de nova tentativa.

Disposição do cron e saída do EasyCron: [arquitetura auto-hospedada](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## A suíte <a id="the-suite"></a>

| Ferramenta | O que substitui | Forma | Licença |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 vitalício |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, roteamento do Zapier | FastAPI + SQLite WAL + Docker | $94.99 vitalício |
| [NexusPipeline](https://nexuscore-store.whop.site) | SaaS de workflow / workers na nuvem | FastAPI + SQLModel + SQLite | $149.00 vitalício |
| [NexusAdmin](https://nexuscore-store.whop.site) | Painel de operações hospedado | Painel Docker ao lado do Pipeline | $94.99 vitalício |
| [LogStream](https://nexuscore-store.whop.site) | SaaS de observabilidade | Node.js de binário único, HTTP + UDP | $79.99 vitalício |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / inquilino extra de segredos | Agente zero-trust, KV criptografado, REST | $99 vitalício |
| [API Proxy Service](https://nexuscore-store.whop.site) | SaaS de gateway para novas tentativas | Binário único: backoff, limites, breaker | $99 vitalício |

### Pacotes

| Pacote | Inclui | Preço |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (economiza $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | As sete ferramentas | $399.99 (economiza $312) |

O código de lançamento `DEVLAUNCH` dá 20% de desconto em cada licença, incluindo os pacotes.

---

## SaaS e auto-hospedado <a id="saas-vs-self-hosted"></a>

| | SaaS mensal | NexusCore |
|-|--------------|-----------|
| Cobrança | Faturas recorrentes de EasyCron, Zapier e motores de workflow | Zero faturas mensais. Uma licença vitalícia |
| Dados | Payloads, agendamentos e logs na nuvem de outra pessoa | Propriedade total dos dados no seu próprio host |
| Preparação | Criação de conta, limites de plano e dependência do fornecedor | Preparação com Docker em 60 segundos em um único nó |
| Código | SaaS fechado que você não pode inspecionar nem fazer fork | Código-fonte completo com a licença |
| Telemetria | Medidores de uso | `NEXUS_TELEMETRY=off` |
| Cluster | O plano multi-inquilino deles | Nó único. Sem Kubernetes |

Cron hospedado a $20–$50 por mês são $240–$600 no primeiro ano. O NexusCron custa $94.99 uma vez. Se o VPS já está no orçamento, o único custo novo é a licença.

---

## O que você executa após o pagamento <a id="what-you-run-after-checkout"></a>

### NexusCron. HTTP em um temporizador que é seu

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Configuração de cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Alternativa ao EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Sair do EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Receber, transformar, encaminhar

Stripe, formulários, GitHub → a sua API. SQLite WAL, novas tentativas, reexecução de dead-letter.

[Configuração de webhooks](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Roteamento com SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Pare de copiar `.env` à mão

```bash
./envsync-agent
```

1. Baixe o agente a partir dos arquivos de membro.
2. Inicialize o armazenamento criptografado e adicione o primeiro host de destino.
3. Confirme a sincronização no painel. Ligue a API REST se a CI precisar.

[Guia do EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. As novas tentativas ficam no caminho, não em cada serviço

```bash
./api-proxy
```

Aponte os seus serviços para o proxy em vez do upstream. Defina nova tentativa, limite de taxa e fallback. Confirme as métricas no painel local.

[Guia do API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Perguntas frequentes <a id="faq"></a>

### Isto é código aberto?

Não. O NexusCore é comercial. Uma licença vitalícia inclui o código-fonte completo após o pagamento na Whop. Este GitHub é só documentação, não a árvore de código, e não é FOSS.

### Preciso de um VPS novo?

Não. Suba o Compose em um notebook ou em uma máquina que você já executa. Associe a interface a 127.0.0.1.

### Preciso de Kubernetes?

Não.

### Alguma coisa entra em contato com o exterior?

`NEXUS_TELEMETRY=off` é o padrão. Sem medidores de uso, sem beacon de analítica, sem API do fornecedor.

### Onde ficam os segredos e os logs?

No volume que você monta. Faça backup dele junto com o resto do host.

### O EnvSync substitui o Vault ou o Doppler?

Se quem não é engenheiro já vive em um cofre compartilhado, mantenha-o. Se a stack já é auto-hospedada e você quer configuração criptografada nos mesmos hosts, execute o EnvSync.

### O API Proxy é um gateway de API completo?

Não. São novas tentativas, limites de taxa, circuit breaker e fallback em um host que é seu. Use uma mesh se precisar de identidade para toda a organização.

### Posso comprar uma só ferramenta?

Sim. Comece pelo [API Proxy](https://nexuscore-store.whop.site) ou pelo [NexusCron](https://nexuscore-store.whop.site). O pacote [Ops Microservices](https://nexuscore-store.whop.site) é LogStream + EnvSync + API Proxy por $199.99.

---

## Guias <a id="guides"></a>

Páginas de alta intenção para quem já procura uma saída do cron e dos webhooks hospedados.

- [Alternativa de cron auto-hospedada](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [Alternativa ao EasyCron e ao cron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [Sair do EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [Substituir serviços de webhook na nuvem](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [Roteamento de webhooks com SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [Pipeline auto-hospedado](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [Admin auto-hospedado](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## Obtenha

[Comprar licenças vitalícias → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

Use o código `DEVLAUNCH` para 20% de desconto.

[Comprar API Proxy](https://nexuscore-store.whop.site) · [Comprar Ops Microservices ($199.99)](https://nexuscore-store.whop.site) · [Comprar Complete Stack ($399.99)](https://nexuscore-store.whop.site)

O NexusCore é software comercial auto-hospedado. As licenças são vitalícias, de pagamento único, e incluem o código-fonte. Execute-o em hardware que você controla.
