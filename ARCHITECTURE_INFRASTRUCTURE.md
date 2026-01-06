# 🏗️ ForestGuard AI - Architecture Infrastructure

## 📋 Vue d'ensemble

Architecture infrastructure complète pour déployer ForestGuard AI en production avec haute disponibilité, scalabilité et sécurité.

---

## 🎯 Architecture Cible (Production)

```
                                    INTERNET
                                       │
                                       ▼
                            ┌──────────────────┐
                            │   CloudFlare CDN  │
                            │   + WAF + DDoS    │
                            └────────┬──────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  Load Balancer   │
                            │   (AWS ALB)      │
                            │  SSL/TLS Term.   │
                            └────────┬──────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │  Streamlit   │ │  Streamlit   │ │  Streamlit   │
            │  Instance 1  │ │  Instance 2  │ │  Instance 3  │
            │  (ECS/EC2)   │ │  (ECS/EC2)   │ │  (ECS/EC2)   │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │   Redis      │ │  PostgreSQL  │ │     S3       │
            │   Cache      │ │  + PostGIS   │ │  (GeoJSON)   │
            │ (ElastiCache)│ │    (RDS)     │ │   Storage    │
            └──────────────┘ └──────────────┘ └──────────────┘
                                    │
                                    ▼
                            ┌──────────────────┐
                            │   Monitoring     │
                            │  CloudWatch +    │
                            │  Datadog + Sentry│
                            └──────────────────┘
```

---

## 🌐 Architecture Multi-Région (Haute Disponibilité)

```
                                INTERNET
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │  Route 53 (DNS)      │
                        │  Geo-routing         │
                        └──────┬───────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │  REGION 1     │             │  REGION 2     │
        │  us-east-1    │             │  eu-west-1    │
        │  (Primaire)   │◄───────────►│  (Secondaire) │
        └───────────────┘  Réplication └───────────────┘
                │                             │
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │  Load Balancer│             │  Load Balancer│
        └───────┬───────┘             └───────┬───────┘
                │                             │
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │  App Cluster  │             │  App Cluster  │
        │  (3 instances)│             │  (3 instances)│
        └───────┬───────┘             └───────┬───────┘
                │                             │
                ▼                             ▼
        ┌───────────────┐             ┌───────────────┐
        │  RDS Primary  │────────────►│  RDS Replica  │
        │  + Read Rep.  │  Async Rep. │  + Read Rep.  │
        └───────────────┘             └───────────────┘
```

---

## 🔧 Composants Infrastructure

### 1. CDN & Sécurité

**CloudFlare**
- **Rôle** : CDN global, cache, protection DDoS
- **Configuration** :
  ```
  Cache TTL: 1 heure pour assets statiques
  WAF Rules: Protection OWASP Top 10
  Rate Limiting: 100 req/min par IP
  SSL: Full (strict)
  ```
- **Coût** : $20/mois (Pro plan)

**AWS WAF**
- **Rôle** : Web Application Firewall
- **Règles** :
  - Bloquer SQL injection
  - Bloquer XSS
  - Géo-blocking (pays à risque)
  - Rate limiting par endpoint
- **Coût** : $5/mois + $1 par million de requêtes

---

### 2. Load Balancing

**AWS Application Load Balancer (ALB)**
- **Rôle** : Distribution du trafic, SSL termination
- **Configuration** :
  ```yaml
  Type: Application Load Balancer
  Scheme: Internet-facing
  Listeners:
    - Port: 443 (HTTPS)
      Protocol: HTTPS
      Certificate: ACM (Let's Encrypt)
      Default Action: Forward to Target Group
    - Port: 80 (HTTP)
      Protocol: HTTP
      Default Action: Redirect to HTTPS
  
  Target Group:
    Protocol: HTTP
    Port: 8501
    Health Check:
      Path: /healthz
      Interval: 30s
      Timeout: 5s
      Healthy Threshold: 2
      Unhealthy Threshold: 3
  
  Stickiness: Enabled (1 hour)
  ```
- **Coût** : $16/mois + $0.008 per LCU-hour

---

### 3. Compute (Application)

#### Option A : AWS ECS (Recommandé)

**Amazon ECS Fargate**
- **Rôle** : Conteneurs serverless
- **Configuration** :
  ```yaml
  Cluster: forestguard-prod
  Service: streamlit-app
  
  Task Definition:
    CPU: 1 vCPU
    Memory: 2 GB
    Container:
      Image: forestguard/streamlit:latest
      Port: 8501
      Environment:
        - DATABASE_URL: ${RDS_ENDPOINT}
        - REDIS_URL: ${REDIS_ENDPOINT}
        - S3_BUCKET: forestguard-data
  
  Desired Count: 3
  Min Capacity: 2
  Max Capacity: 10
  
  Auto Scaling:
    Target CPU: 70%
    Target Memory: 80%
    Scale Out Cooldown: 60s
    Scale In Cooldown: 300s
  ```
- **Coût** : $30/mois par instance (1 vCPU, 2GB)

#### Option B : AWS EC2

**EC2 Instances**
- **Type** : t3.medium (2 vCPU, 4 GB RAM)
- **OS** : Ubuntu 22.04 LTS
- **Auto Scaling Group** :
  ```yaml
  Min Size: 2
  Desired: 3
  Max Size: 10
  
  Launch Template:
    AMI: ami-ubuntu-22.04
    Instance Type: t3.medium
    Security Group: streamlit-sg
    IAM Role: streamlit-role
    User Data: |
      #!/bin/bash
      apt-get update
      apt-get install -y docker.io
      docker run -d -p 8501:8501 \
        -e DATABASE_URL=${RDS_ENDPOINT} \
        forestguard/streamlit:latest
  ```
- **Coût** : $35/mois par instance

---

### 4. Base de Données

**Amazon RDS PostgreSQL + PostGIS**
- **Rôle** : Stockage des données géospatiales
- **Configuration** :
  ```yaml
  Engine: PostgreSQL 15
  Instance Class: db.t3.medium (2 vCPU, 4 GB)
  Storage: 100 GB SSD (gp3)
  Multi-AZ: Enabled
  
  Extensions:
    - PostGIS 3.3
    - pg_stat_statements
  
  Backup:
    Retention: 7 days
    Window: 03:00-04:00 UTC
  
  Maintenance Window: Sun 04:00-05:00 UTC
  
  Read Replicas: 1 (même région)
  
  Security:
    Encryption at rest: Enabled (KMS)
    Encryption in transit: SSL/TLS required
  ```
- **Coût** : $60/mois (primary) + $60/mois (replica)

**Schéma de base de données** :
```sql
-- Table des zones de déforestation
CREATE TABLE deforestation_zones (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100) NOT NULL,
    region VARCHAR(200),
    classification VARCHAR(20) CHECK (classification IN ('Légale', 'Illégale')),
    area_ha DECIMAL(10, 2) NOT NULL,
    year INTEGER NOT NULL,
    source VARCHAR(100),
    confidence DECIMAL(3, 2),
    verified BOOLEAN DEFAULT false,
    geometry GEOMETRY(Polygon, 4326) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index spatial
CREATE INDEX idx_zones_geometry ON deforestation_zones USING GIST (geometry);
CREATE INDEX idx_zones_country ON deforestation_zones (country);
CREATE INDEX idx_zones_year ON deforestation_zones (year);
CREATE INDEX idx_zones_classification ON deforestation_zones (classification);
```

---

### 5. Cache

**Amazon ElastiCache Redis**
- **Rôle** : Cache des requêtes, sessions utilisateurs
- **Configuration** :
  ```yaml
  Engine: Redis 7.0
  Node Type: cache.t3.medium (2 vCPU, 3.09 GB)
  Number of Nodes: 2 (primary + replica)
  Multi-AZ: Enabled
  
  Eviction Policy: allkeys-lru
  Max Memory: 3 GB
  
  Backup:
    Retention: 1 day
    Window: 02:00-03:00 UTC
  ```
- **Utilisation** :
  ```python
  # Cache des données GeoJSON
  redis.setex(f"geojson:{country}", 3600, json.dumps(data))
  
  # Cache des statistiques
  redis.setex(f"stats:{country}:{year}", 1800, json.dumps(stats))
  
  # Sessions utilisateurs
  redis.setex(f"session:{user_id}", 86400, session_data)
  ```
- **Coût** : $50/mois

---

### 6. Stockage

**Amazon S3**
- **Rôle** : Stockage des fichiers GeoJSON, assets statiques
- **Buckets** :
  ```yaml
  forestguard-data-prod:
    Purpose: Fichiers GeoJSON
    Versioning: Enabled
    Lifecycle:
      - Transition to IA after 30 days
      - Transition to Glacier after 90 days
    Encryption: AES-256
    Access: Private (IAM roles only)
  
  forestguard-assets-prod:
    Purpose: Assets statiques (images, CSS, JS)
    Versioning: Disabled
    CloudFront: Enabled
    Access: Public read
  
  forestguard-backups-prod:
    Purpose: Backups base de données
    Versioning: Enabled
    Lifecycle:
      - Delete after 30 days
    Encryption: KMS
    Access: Private
  ```
- **Coût** : $5/mois (50 GB)

---

### 7. Monitoring & Logging

**Amazon CloudWatch**
- **Métriques** :
  ```yaml
  Application:
    - CPU Utilization
    - Memory Utilization
    - Request Count
    - Response Time
    - Error Rate
  
  Database:
    - CPU Utilization
    - Connections
    - Read/Write IOPS
    - Storage Space
  
  Cache:
    - Hit Rate
    - Evictions
    - Memory Usage
  
  Alarms:
    - CPU > 80% for 5 minutes
    - Memory > 90% for 5 minutes
    - Error Rate > 5% for 2 minutes
    - Response Time > 3s for 5 minutes
  ```

**Datadog**
- **Rôle** : Monitoring avancé, APM, logs
- **Configuration** :
  ```yaml
  Integrations:
    - AWS (CloudWatch, ECS, RDS, S3)
    - PostgreSQL
    - Redis
    - Nginx
  
  Dashboards:
    - Application Performance
    - Infrastructure Health
    - User Analytics
    - Error Tracking
  
  Alerts:
    - Slack notifications
    - PagerDuty for critical
    - Email for warnings
  ```
- **Coût** : $15/host/mois

**Sentry**
- **Rôle** : Error tracking, performance monitoring
- **Configuration** :
  ```python
  import sentry_sdk
  
  sentry_sdk.init(
      dsn="https://xxx@sentry.io/xxx",
      environment="production",
      traces_sample_rate=0.1,
      profiles_sample_rate=0.1
  )
  ```
- **Coût** : $26/mois (50K events)

---

### 8. CI/CD Pipeline

**GitHub Actions**
- **Workflow** :
  ```yaml
  name: Deploy to Production
  
  on:
    push:
      branches: [main]
  
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Run tests
          run: |
            pip install -r requirements.txt
            pytest tests/
    
    build:
      needs: test
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Build Docker image
          run: |
            docker build -t forestguard/streamlit:${{ github.sha }} .
            docker tag forestguard/streamlit:${{ github.sha }} forestguard/streamlit:latest
        - name: Push to ECR
          run: |
            aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
            docker push forestguard/streamlit:${{ github.sha }}
            docker push forestguard/streamlit:latest
    
    deploy:
      needs: build
      runs-on: ubuntu-latest
      steps:
        - name: Deploy to ECS
          run: |
            aws ecs update-service \
              --cluster forestguard-prod \
              --service streamlit-app \
              --force-new-deployment
  ```

---

### 9. Sécurité

**AWS IAM Roles**
```yaml
StreamlitAppRole:
  Policies:
    - S3ReadAccess (forestguard-data-prod)
    - RDSConnect
    - ElastiCacheConnect
    - CloudWatchPutMetrics
    - SecretsManagerReadOnly

DatabaseAdminRole:
  Policies:
    - RDSFullAccess
    - S3BackupAccess

DeploymentRole:
  Policies:
    - ECSUpdateService
    - ECRPushImage
```

**AWS Secrets Manager**
```yaml
Secrets:
  - database-credentials:
      username: forestguard_admin
      password: ${RANDOM_PASSWORD}
  
  - redis-auth-token:
      token: ${RANDOM_TOKEN}
  
  - api-keys:
      mapbox: ${MAPBOX_API_KEY}
      stripe: ${STRIPE_SECRET_KEY}
```

**Security Groups**
```yaml
ALB-SG:
  Inbound:
    - Port 443 from 0.0.0.0/0 (HTTPS)
    - Port 80 from 0.0.0.0/0 (HTTP redirect)
  Outbound:
    - All traffic to App-SG

App-SG:
  Inbound:
    - Port 8501 from ALB-SG
  Outbound:
    - Port 5432 to RDS-SG (PostgreSQL)
    - Port 6379 to Redis-SG
    - Port 443 to 0.0.0.0/0 (HTTPS)

RDS-SG:
  Inbound:
    - Port 5432 from App-SG
  Outbound:
    - None

Redis-SG:
  Inbound:
    - Port 6379 from App-SG
  Outbound:
    - None
```

---

## 💰 Coûts Mensuels Estimés

### MVP (Phase 1)

| Service | Configuration | Coût/mois |
|---------|--------------|-----------|
| EC2 (1 instance) | t3.medium | $35 |
| RDS PostgreSQL | db.t3.small | $30 |
| S3 | 20 GB | $2 |
| CloudFront | 100 GB transfer | $10 |
| Route 53 | 1 hosted zone | $1 |
| **TOTAL MVP** | | **$78/mois** |

### Production (Phase 2)

| Service | Configuration | Coût/mois |
|---------|--------------|-----------|
| CloudFlare | Pro plan | $20 |
| AWS WAF | Basic rules | $10 |
| ALB | 1 load balancer | $20 |
| ECS Fargate | 3 tasks (1vCPU, 2GB) | $90 |
| RDS PostgreSQL | db.t3.medium + replica | $120 |
| ElastiCache Redis | cache.t3.medium | $50 |
| S3 | 100 GB | $5 |
| CloudFront | 500 GB transfer | $40 |
| Route 53 | 1 hosted zone | $1 |
| CloudWatch | Logs + metrics | $20 |
| Datadog | 3 hosts | $45 |
| Sentry | 50K events | $26 |
| **TOTAL PRODUCTION** | | **$447/mois** |

### Scale-up (Phase 3)

| Service | Configuration | Coût/mois |
|---------|--------------|-----------|
| CloudFlare | Business plan | $200 |
| AWS WAF | Advanced rules | $50 |
| ALB | 2 load balancers (multi-region) | $40 |
| ECS Fargate | 10 tasks (2vCPU, 4GB) | $600 |
| RDS PostgreSQL | db.r5.xlarge + 2 replicas | $800 |
| ElastiCache Redis | cache.r5.large cluster | $300 |
| S3 | 1 TB | $25 |
| CloudFront | 5 TB transfer | $150 |
| Route 53 | Geo-routing | $5 |
| CloudWatch | Advanced | $100 |
| Datadog | 10 hosts | $150 |
| Sentry | 500K events | $99 |
| **TOTAL SCALE-UP** | | **$2,519/mois** |

---

## 🚀 Plan de Déploiement

### Phase 1 : MVP (Mois 1-6)
```
✅ 1 EC2 instance
✅ 1 RDS PostgreSQL small
✅ S3 pour stockage
✅ CloudFront CDN
✅ Monitoring basique
```
**Capacité** : 50-100 utilisateurs simultanés
**Coût** : $78/mois

### Phase 2 : Production (Mois 6-12)
```
✅ Load Balancer
✅ 3 ECS Fargate tasks
✅ RDS avec replica
✅ Redis cache
✅ WAF + CloudFlare
✅ Monitoring avancé (Datadog, Sentry)
```
**Capacité** : 500-1000 utilisateurs simultanés
**Coût** : $447/mois

### Phase 3 : Scale-up (Mois 12-24)
```
✅ Multi-région (US + EU)
✅ 10 ECS tasks
✅ RDS xlarge + 2 replicas
✅ Redis cluster
✅ CDN global
✅ Monitoring enterprise
```
**Capacité** : 5000+ utilisateurs simultanés
**Coût** : $2,519/mois

---

## 📊 Métriques de Performance

### SLA (Service Level Agreement)

| Métrique | Cible | Mesure |
|----------|-------|--------|
| Uptime | 99.9% | CloudWatch |
| Response Time | < 2s (p95) | Datadog APM |
| Error Rate | < 0.1% | Sentry |
| Database Latency | < 100ms | RDS Metrics |
| Cache Hit Rate | > 80% | Redis INFO |

### Capacité

| Phase | Users/jour | Requests/sec | Data Transfer/mois |
|-------|------------|--------------|-------------------|
| MVP | 1,000 | 10 | 100 GB |
| Production | 10,000 | 100 | 1 TB |
| Scale-up | 100,000 | 1,000 | 10 TB |

---

## 🔐 Disaster Recovery

### Backup Strategy

**Base de données** :
```yaml
Automated Backups:
  Frequency: Daily
  Retention: 7 days
  Window: 03:00-04:00 UTC

Manual Snapshots:
  Frequency: Weekly
  Retention: 30 days
  Before: Major deployments

Point-in-Time Recovery:
  Enabled: Yes
  Retention: 7 days
```

**Fichiers S3** :
```yaml
Versioning: Enabled
Cross-Region Replication: us-east-1 → eu-west-1
Lifecycle:
  - Current version: Keep
  - Previous versions: Delete after 30 days
```

### Recovery Procedures

**RTO (Recovery Time Objective)** : 1 heure
**RPO (Recovery Point Objective)** : 5 minutes

**Procédure** :
1. Détecter l'incident (monitoring)
2. Basculer sur région secondaire (Route 53)
3. Restaurer base de données depuis snapshot
4. Vérifier intégrité des données
5. Rediriger le trafic
6. Post-mortem et amélioration

---

## 📝 Checklist Déploiement

### Avant le déploiement

- [ ] Tests unitaires passent (pytest)
- [ ] Tests d'intégration passent
- [ ] Code review approuvé
- [ ] Documentation à jour
- [ ] Secrets configurés (Secrets Manager)
- [ ] Backup base de données créé
- [ ] Monitoring configuré
- [ ] Alertes configurées

### Déploiement

- [ ] Build Docker image
- [ ] Push vers ECR
- [ ] Update ECS task definition
- [ ] Deploy new version (blue/green)
- [ ] Health checks passent
- [ ] Smoke tests passent
- [ ] Monitoring actif

### Après le déploiement

- [ ] Vérifier logs (CloudWatch)
- [ ] Vérifier métriques (Datadog)
- [ ] Vérifier erreurs (Sentry)
- [ ] Tester fonctionnalités critiques
- [ ] Communiquer aux utilisateurs
- [ ] Documenter le déploiement

---

## 🎓 Conclusion

Cette architecture infrastructure est :

✅ **Scalable** : De 100 à 100,000 utilisateurs
✅ **Résiliente** : Multi-AZ, backups, monitoring
✅ **Sécurisée** : WAF, encryption, IAM roles
✅ **Performante** : Cache, CDN, load balancing
✅ **Observable** : Logs, metrics, traces, alerts
✅ **Économique** : Coûts adaptés à chaque phase

**Prête pour la production ! 🚀**

---

**Document créé le** : 2024-12-03
**Version** : 1.0
**Auteur** : ForestGuard AI Team
