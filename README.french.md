<!-- language: French (fr) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> Langue : **Français**

Ce dépôt GitHub est la documentation du produit. NexusCore est commercial. Le code source, les images et les binaires sont livrés après paiement sur la [boutique](https://nexuscore-store.whop.site). Cette arborescence ne contient que le README.

**Arrêtez de louer votre stack. Des outils de développement auto-hébergés qui vous appartiennent.**

Cron, webhooks, pipelines, journaux, synchronisation d'environnement et nouvelles tentatives d'API sur un VPS que vous payez déjà. Une licence à vie. Le code source complet après l'achat. SQLite sur disque. Télémétrie désactivée.

[![auto-hébergé](https://img.shields.io/badge/self--hosted-your_VPS-3dd6c6?style=flat-square)](https://nexuscore-store.whop.site)
[![sqlite](https://img.shields.io/badge/storage-SQLite_WAL-0c1118?style=flat-square)](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
[![docker](https://img.shields.io/badge/deploy-Docker_60s-2496ED?style=flat-square&logo=docker&logoColor=white)](https://nexuscore-store.whop.site)
[![télémétrie](https://img.shields.io/badge/telemetry-off-informational?style=flat-square)](https://nexuscore-store.whop.site)
[![licence](https://img.shields.io/badge/license-commercial-0c1118?style=flat-square)](https://nexuscore-store.whop.site)

[Boutique](https://nexuscore-store.whop.site) · [Guides](https://nexuscore-store.whop.site/guides) · [Architecture](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide) · [Proxy d'API](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) · [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

[Démarrage rapide](#quick-start) · [Fonctionnement](#how-it-works) · [La suite](#the-suite) · [SaaS et auto-hébergement](#saas-vs-self-hosted) · [Ce que vous lancez après le paiement](#what-you-run-after-checkout) · [FAQ](#faq) · [Guides](#guides)

`DEVLAUNCH` → 20 % de réduction sur chaque licence à vie

---

## Pourquoi ce produit existe

EasyCron, Hookdeck, Zapier, Doppler, Datadog et les passerelles d'API facturent le même travail : émettre du HTTP, router une charge utile, garder un `.env` synchronisé, relancer un appel vers l'amont.

NexusCore, c'est ce travail sous forme de processus sur **votre** hôte.

- Payez une fois. Gardez le code source.
- FastAPI + SQLite + Docker pour le cron, les webhooks, le pipeline et l'admin.
- Microservices en binaire unique pour LogStream, EnvSync et API Proxy.
- `NEXUS_TELEMETRY=off` est la valeur par défaut. Rien ne contacte l'extérieur.
- Pas de Kubernetes. Pas de boîte de réception d'un éditeur entre les sauts.

**Obtenir une licence → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Démarrage rapide <a id="quick-start"></a>

Ne clonez pas ce dépôt en espérant une stack déjà en marche. Après le paiement, les licences arrivent sous forme de code source, d'images Docker et de binaires dans vos fichiers membre. Les extraits ci-dessous sont ce que vous lancez à ce moment-là.

### Exemple Compose (après le paiement)

```bash
docker compose up -d
```

```yaml
# docker-compose.yml  — nœud unique, ~60 s
# Les images sont livrées dans les fichiers membre. Ce n'est pas un pull public depuis ce GitHub.
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

### Créer une tâche en REST

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

### Microservices en binaire unique (Compose n'est pas requis)

```bash
./envsync-agent    # synchro chiffrée des .env entre VPS, portable et services
./api-proxy        # nouvelles tentatives, limites de débit, circuit breaker, replis
./logstream        # ingestion HTTP + UDP, SQLite, tableau de bord en direct
```

Aucun compte à créer après le paiement. Liez l'écoute à localhost et sauvegardez `./data` avec le reste de la machine.

---

## Fonctionnement <a id="how-it-works"></a>

1. Entrée : Stripe, GitHub, des formulaires, ou un top de cron. Du HTTP simple vers un endpoint que vous hébergez.
2. Votre VPS : FastAPI + SQLite sur Docker, ou un binaire unique. Tâches, secrets et charges utiles restent sur le disque que vous montez.
3. Des destinations qui vous appartiennent : votre API, Discord, un fichier. Aucune boîte de réception d'éditeur entre les sauts.

Le routage des webhooks tourne en SQLite WAL, sous 50 Mo de RAM, avec nouvelles tentatives et rejeu des dead-letters. EnvSync conserve un magasin clé-valeur chiffré pour les valeurs de `.env`. API Proxy se place sur le chemin pour que votre application ne recopie pas des boucles de nouvelle tentative.

Agencement du cron et bascule depuis EasyCron : [architecture auto-hébergée](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## La suite <a id="the-suite"></a>

| Outil | Ce qu'il remplace | Forme | Licence |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 à vie |
| [Webhook Router](https://nexuscore-store.whop.site) | Hookdeck, Svix, routage Zapier | FastAPI + SQLite WAL + Docker | $94.99 à vie |
| [NexusPipeline](https://nexuscore-store.whop.site) | SaaS de workflows / workers dans le cloud | FastAPI + SQLModel + SQLite | $149.00 à vie |
| [NexusAdmin](https://nexuscore-store.whop.site) | Tableau de bord d'exploitation hébergé | Tableau de bord Docker à côté de Pipeline | $94.99 à vie |
| [LogStream](https://nexuscore-store.whop.site) | SaaS d'observabilité | Node.js en binaire unique, HTTP + UDP | $79.99 à vie |
| [EnvSync Agent](https://nexuscore-store.whop.site) | Doppler / locataire de secrets supplémentaire | Agent zero-trust, KV chiffré, REST | $99 à vie |
| [API Proxy Service](https://nexuscore-store.whop.site) | SaaS de passerelle pour les nouvelles tentatives | Binaire unique : backoff, limites, breaker | $99 à vie |

### Offres groupées

| Offre | Comprend | Prix |
|--------|----------|-------|
| [Ops Microservices](https://nexuscore-store.whop.site) | LogStream + EnvSync + API Proxy | $199.99 (vous économisez $78) |
| [Complete Stack](https://nexuscore-store.whop.site) | Les sept outils | $399.99 (vous économisez $312) |

Le code de lancement `DEVLAUNCH` accorde 20 % de réduction sur chaque licence, offres groupées comprises.

---

## SaaS et auto-hébergement <a id="saas-vs-self-hosted"></a>

| | SaaS mensuel | NexusCore |
|-|--------------|-----------|
| Facturation | Factures récurrentes EasyCron, Zapier et moteurs de workflow | Zéro facture mensuelle. Une licence à vie |
| Données | Charges utiles, planifications et journaux sur le cloud de quelqu'un d'autre | Pleine propriété des données sur votre propre hôte |
| Mise en place | Création de compte, limites de forfait et dépendance à l'éditeur | Mise en place Docker en 60 secondes sur un seul nœud |
| Code | SaaS fermé que vous ne pouvez ni inspecter ni forker | Code source complet avec la licence |
| Télémétrie | Compteurs d'usage | `NEXUS_TELEMETRY=off` |
| Cluster | Leur plan multi-locataire | Un seul nœud. Pas de Kubernetes |

Un cron hébergé à $20–$50 par mois représente $240–$600 la première année. NexusCron coûte $94.99 une seule fois. Si le VPS est déjà dans le budget, le seul coût nouveau est la licence.

---

## Ce que vous lancez après le paiement <a id="what-you-run-after-checkout"></a>

### NexusCron. Du HTTP sur une minuterie qui vous appartient

```bash
curl -sS -X POST http://127.0.0.1:8787/api/jobs \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron":"*/5 * * * *","method":"GET","url":"https://app.internal/health"}'
```

[Configuration du cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Alternative à EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Quitter EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Recevoir, transformer, transmettre

Stripe, formulaires, GitHub → votre API. SQLite WAL, nouvelles tentatives, rejeu des dead-letters.

[Configuration des webhooks](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Routage SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Arrêtez de copier les `.env` à la main

```bash
./envsync-agent
```

1. Téléchargez l'agent depuis les fichiers membre.
2. Initialisez le magasin chiffré et ajoutez le premier hôte cible.
3. Confirmez la synchronisation dans le tableau de bord. Branchez l'API REST si la CI en a besoin.

[Guide EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Les nouvelles tentatives sont sur le chemin, pas dans chaque service

```bash
./api-proxy
```

Pointez vos services vers le proxy plutôt que vers l'amont. Réglez la nouvelle tentative, la limite de débit et le repli. Confirmez les métriques sur le tableau de bord local.

[Guide API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## FAQ <a id="faq"></a>

### Est-ce open source ?

Non. NexusCore est commercial. Une licence à vie inclut le code source complet après paiement sur Whop. Ce GitHub est uniquement de la documentation, pas l'arbre des sources, et ce n'est pas du FOSS.

### Faut-il un nouveau VPS ?

Non. Lancez Compose sur un portable ou sur une machine que vous faites déjà tourner. Liez l'interface à 127.0.0.1.

### Faut-il Kubernetes ?

Non.

### Quelque chose contacte-t-il l'extérieur ?

`NEXUS_TELEMETRY=off` est la valeur par défaut. Pas de compteurs d'usage, pas de balise d'analytique, pas d'API éditeur.

### Où se trouvent les secrets et les journaux ?

Sur le volume que vous montez. Sauvegardez-le avec le reste de l'hôte.

### EnvSync remplace-t-il Vault ou Doppler ?

Si les non-ingénieurs vivent déjà dans un coffre partagé, gardez-le. Si la stack est déjà auto-hébergée et que vous voulez une configuration chiffrée sur les mêmes hôtes, lancez EnvSync.

### API Proxy est-il une passerelle d'API complète ?

Non. Ce sont des nouvelles tentatives, des limites de débit, un circuit breaker et un repli sur un hôte qui vous appartient. Utilisez un mesh si vous avez besoin d'une identité à l'échelle de l'organisation.

### Puis-je n'acheter qu'un outil ?

Oui. Commencez par [API Proxy](https://nexuscore-store.whop.site) ou [NexusCron](https://nexuscore-store.whop.site). L'offre [Ops Microservices](https://nexuscore-store.whop.site) réunit LogStream + EnvSync + API Proxy pour $199.99.

---

## Guides <a id="guides"></a>

Pages à forte intention pour les personnes qui cherchent déjà à quitter le cron et les webhooks hébergés.

- [Alternative de cron auto-hébergée](https://nexuscore-store.whop.site/guides/self-hosted-cron)
- [Alternative à EasyCron et cron-job.org](https://nexuscore-store.whop.site/guides/easycron-alternative)
- [Quitter EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)
- [Remplacer les services de webhook dans le cloud](https://nexuscore-store.whop.site/guides/replace-cloud-webhooks)
- [Routage de webhooks en SQLite WAL](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)
- [Pipeline auto-hébergé](https://nexuscore-store.whop.site/guides/self-hosted-pipeline)
- [Admin auto-hébergé](https://nexuscore-store.whop.site/guides/self-hosted-admin)
- [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream)
- [EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)
- [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## L'obtenir

[Acheter des licences à vie → nexuscore-store.whop.site](https://nexuscore-store.whop.site)

Utilisez le code `DEVLAUNCH` pour 20 % de réduction.

[Acheter API Proxy](https://nexuscore-store.whop.site) · [Acheter Ops Microservices ($199.99)](https://nexuscore-store.whop.site) · [Acheter Complete Stack ($399.99)](https://nexuscore-store.whop.site)

NexusCore est un logiciel commercial auto-hébergé. Les licences sont à vie, payées une seule fois, et incluent le code source. Exécutez-le sur du matériel que vous contrôlez.
