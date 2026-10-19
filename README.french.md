<!-- language: French (fr) -->

# NexusCore

[English](https://github.com/alfredobustamante19/NexusCore/blob/main/README.md) · [Español](https://github.com/alfredobustamante19/NexusCore/blob/main/README.spanish.md) · [عربي](https://github.com/alfredobustamante19/NexusCore/blob/main/README.arabic.md) · [বাংলা](https://github.com/alfredobustamante19/NexusCore/blob/main/README.bengali.md) · [Français](https://github.com/alfredobustamante19/NexusCore/blob/main/README.french.md) · [हिंदी](https://github.com/alfredobustamante19/NexusCore/blob/main/README.hindi.md) · [Indonesia](https://github.com/alfredobustamante19/NexusCore/blob/main/README.indonesian.md) · [汉语](https://github.com/alfredobustamante19/NexusCore/blob/main/README.mandarin-chinese.md) · [Português](https://github.com/alfredobustamante19/NexusCore/blob/main/README.portuguese.md) · [русский](https://github.com/alfredobustamante19/NexusCore/blob/main/README.russian.md) · [اردو](https://github.com/alfredobustamante19/NexusCore/blob/main/README.urdu.md)

> Langue : **Français**

Ce dépôt GitHub est la documentation du produit et le demo gratuit. NexusCore est commercial. Le code sous licence est livré après paiement sur la [boutique](https://nexuscore-store.whop.site).

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
- Processus Node.js pour LogStream, EnvSync et API Proxy.
- Les services n'envoient pas de données d'usage. L'échantillon lite reste silencieux tant que `NEXUS_TELEMETRY` n'est pas défini.
- Pas de Kubernetes. Pas de boîte de réception d'un éditeur entre les sauts.

**Obtenir une licence → [nexuscore-store.whop.site](https://nexuscore-store.whop.site)**

---

## Démarrage rapide <a id="quick-start"></a>

Le demo gratuit est dans `NexusCore Developer Demo.zip`. Ouvrez le dossier `NexusCore Developer Demo` (`./start-demo.sh`, sous Windows `.\Start Demo.ps1`, console sur http://127.0.0.1:7400). Il faut Python 3.12 ou plus récent et Node.js 24 ou plus récent. `nexuscore_lite.py` écoute sur http://127.0.0.1:8000 après `pip install -r requirements.txt`. Le code sous licence est livré après le paiement. Les extraits ci-dessous sont ce que vous lancez à ce moment-là.

### Exemple Compose (après le paiement)

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

### Créer une tâche en REST

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

### Processus Node.js (Compose n'est pas requis)

```bash
npm start          # EnvSync, http://127.0.0.1:8787. synchro chiffrée des .env entre VPS, portable et services
npm start          # API Proxy, http://127.0.0.1:8080. nouvelles tentatives, limites de débit, circuit breaker, replis
npm start          # LogStream, http://127.0.0.1:8787. Set PORT if 8787 is already taken. ingestion HTTP + UDP, SQLite, tableau de bord en direct
```

EnvSync demande un mot de passe administrateur au premier démarrage (`NEXUSENV_ADMIN_PASSWORD`). LogStream attend `NEXUS_TOKEN` dans `.env`. Liez l'écoute à localhost et sauvegardez le répertoire de données avec le reste de la machine.

---

## Fonctionnement <a id="how-it-works"></a>

1. Entrée : Stripe, GitHub, des formulaires, ou un top de cron. Du HTTP simple vers un endpoint que vous hébergez.
2. Votre VPS : FastAPI + SQLite sur Docker, ou un processus Node.js. Tâches, secrets et charges utiles restent sur le disque que vous montez.
3. Des destinations qui vous appartiennent : votre API, Discord, un fichier. Aucune boîte de réception d'éditeur entre les sauts.

Le routage des webhooks tourne en SQLite WAL, avec nouvelles tentatives et rejeu. EnvSync conserve un magasin clé-valeur chiffré pour les valeurs de `.env`. API Proxy se place sur le chemin pour que votre application ne recopie pas des boucles de nouvelle tentative.

Agencement du cron et bascule depuis EasyCron : [architecture auto-hébergée](https://nexuscore-store.whop.site/guides/self-hosted-architecture-guide)

---

## La suite <a id="the-suite"></a>

| Outil | Ce qu'il remplace | Forme | Licence |
|------|------------------|-------|---------|
| [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron) | EasyCron, cron-job.org | FastAPI + SQLite + Docker | $94.99 à vie |
| [Webhook Router](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) | Hookdeck, Svix, routage Zapier | FastAPI + SQLite WAL + Docker | $94.99 à vie |
| [NexusPipeline](https://nexuscore-store.whop.site/guides/self-hosted-pipeline) | SaaS de workflows / workers dans le cloud | FastAPI + SQLModel + SQLite | $149.00 à vie |
| [NexusAdmin](https://nexuscore-store.whop.site/guides/self-hosted-admin) | Tableau de bord d'exploitation hébergé | Tableau de bord Docker à côté de Pipeline | $94.99 à vie |
| [LogStream](https://nexuscore-store.whop.site/guides/self-hosted-logstream) | SaaS d'observabilité | Processus Node.js, HTTP + UDP | $79.99 à vie |
| [EnvSync Agent](https://nexuscore-store.whop.site/guides/self-hosted-envsync) | Doppler / locataire de secrets supplémentaire | Agent zero-trust, KV chiffré, REST | $99 à vie |
| [API Proxy Service](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) | SaaS de passerelle pour les nouvelles tentatives | Processus Node.js : backoff, limites, breaker | $99 à vie |

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
| Télémétrie | Compteurs d'usage | Pas de compteur d'usage |
| Cluster | Leur plan multi-locataire | Un seul nœud. Pas de Kubernetes |

Un cron hébergé à $20–$50 par mois représente $240–$600 la première année. NexusCron coûte $94.99 une seule fois. Si le VPS est déjà dans le budget, le seul coût nouveau est la licence.

---

## Ce que vous lancez après le paiement <a id="what-you-run-after-checkout"></a>

### NexusCron. Du HTTP sur une minuterie qui vous appartient

```bash
curl -sS -X POST http://127.0.0.1:8000/api/tasks \
  -H "content-type: application/json" \
  -d '{"name":"health-ping","cron_expression":"*/5 * * * *","http_method":"GET","target_url":"https://app.internal/health"}'
```

[Configuration du cron](https://nexuscore-store.whop.site/guides/self-hosted-cron) · [Alternative à EasyCron](https://nexuscore-store.whop.site/guides/easycron-alternative) · [Quitter EasyCron](https://nexuscore-store.whop.site/guides/migrate-off-easycron)

### Webhook Router. Recevoir, transformer, transmettre

Stripe, formulaires, GitHub → votre API. SQLite WAL, nouvelles tentatives et rejeu.

[Configuration des webhooks](https://nexuscore-store.whop.site/guides/self-hosted-webhook-router) · [Routage SQLite](https://nexuscore-store.whop.site/guides/sqlite-webhook-routing)

### EnvSync. Arrêtez de copier les `.env` à la main

```bash
npm start
# http://127.0.0.1:8787
```

1. Téléchargez l'agent depuis les fichiers membre.
2. Initialisez le magasin chiffré et ajoutez le premier hôte cible.
3. Confirmez la synchronisation dans le tableau de bord. Branchez l'API REST si la CI en a besoin.

[Guide EnvSync](https://nexuscore-store.whop.site/guides/self-hosted-envsync)

### API Proxy. Les nouvelles tentatives sont sur le chemin, pas dans chaque service

```bash
npm start
# http://127.0.0.1:8080
```

Pointez vos services vers le proxy plutôt que vers l'amont. Réglez la nouvelle tentative, la limite de débit et le repli. Confirmez les métriques sur le tableau de bord local.

[Guide API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy)

---

## FAQ <a id="faq"></a>

### Est-ce open source ?

Non. NexusCore est commercial. Une licence à vie inclut le code source complet après paiement sur Whop. Ce GitHub contient la documentation et le demo gratuit, pas l'arbre des sources sous licence, et ce n'est pas du FOSS.

### Faut-il un nouveau VPS ?

Non. Lancez Compose sur un portable ou sur une machine que vous faites déjà tourner. Liez l'interface à 127.0.0.1.

### Faut-il Kubernetes ?

Non.

### Quelque chose contacte-t-il l'extérieur ?

Les services n'envoient pas de données d'usage. L'échantillon lite reste silencieux tant que `NEXUS_TELEMETRY` n'est pas défini.

### Où se trouvent les secrets et les journaux ?

Sur le volume que vous montez. Sauvegardez-le avec le reste de l'hôte.

### EnvSync remplace-t-il Vault ou Doppler ?

Si les non-ingénieurs vivent déjà dans un coffre partagé, gardez-le. Si la stack est déjà auto-hébergée et que vous voulez une configuration chiffrée sur les mêmes hôtes, lancez EnvSync.

### API Proxy est-il une passerelle d'API complète ?

Non. Ce sont des nouvelles tentatives, des limites de débit, un circuit breaker et un repli sur un hôte qui vous appartient. Utilisez un mesh si vous avez besoin d'une identité à l'échelle de l'organisation.

### Puis-je n'acheter qu'un outil ?

Oui. Commencez par [API Proxy](https://nexuscore-store.whop.site/guides/self-hosted-api-proxy) ou [NexusCron](https://nexuscore-store.whop.site/guides/self-hosted-cron). L'offre [Ops Microservices](https://nexuscore-store.whop.site) réunit LogStream + EnvSync + API Proxy pour $199.99.

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
