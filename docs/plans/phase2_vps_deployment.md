# Phase 2: VPS Deployment - Single Instance Validation

**Created:** January 7, 2026
**Status:** Planning
**Depends On:** Phase 1 Complete ✅
**Estimated Duration:** 1-2 sessions (~4 hours)

---

## 🎯 Objective

Deploy **single CEREBRO instance** to VPS for:
1. Cost validation ($30/month target)
2. Remote access testing (Claude Code → VPS)
3. Production readiness verification
4. Performance baseline measurement

**NOT deploying:** Multi-region, multiple replicas (that's Phase 3)

---

## 📊 Provider Analysis

### Option 1: Fly.io ⭐ RECOMMENDED

**Pros:**
- Docker-native deployment (uses our Dockerfile directly)
- Free PostgreSQL (1GB) + Redis (25MB) included
- Global regions (15+ locations)
- CLI deployment (`flyctl deploy`)
- Auto-scaling support
- Free tier: 3 VMs with 256MB RAM

**Cons:**
- Credit card required (even for free tier)
- Cold starts if inactive

**Cost Estimate:**
```
Shared CPU-1x, 256MB: Free (3 instances)
PostgreSQL (1GB):     Free
Redis (25MB):         Free
Total:                $0/month (free tier)
```

**If scaling:**
```
Dedicated CPU-1x, 2GB: $29/month
PostgreSQL (10GB):     $15/month
Redis (250MB):         $10/month
Total:                 $54/month
```

---

### Option 2: Railway

**Pros:**
- GitHub integration (auto-deploy on push)
- Simple UI
- Generous free tier ($5 credit/month)

**Cons:**
- More expensive at scale
- Less control than Fly.io

**Cost Estimate:**
```
Free tier: $5/month credit
After free: ~$20/month for basic setup
```

---

### Option 3: Hostinger VPS ⚠️ NOT RECOMMENDED for Phase 2

**Pros:**
- Already have account
- Full VM control
- biblioteca_moi VPS available

**Cons:**
- Manual Docker setup required
- No auto-scaling
- No managed PostgreSQL/Redis
- Higher maintenance overhead
- Better for Phase 3 (multi-region primary)

**Cost:** $30/month (biblioteca_moi VPS)

---

## ✅ Decision: Fly.io (Free Tier → Paid if needed)

**Reasoning:**
1. Zero cost to validate architecture
2. Docker-native (zero migration friction)
3. Easy to scale to Phase 3 (multi-region)
4. CLI deployment = automation-friendly
5. Managed databases = lower maintenance

---

## 🚀 Deployment Plan

### Prerequisites

1. **Fly.io Account**
   - Sign up: https://fly.io/app/sign-up
   - Install flyctl: `curl -L https://fly.sh/install.sh | sh`
   - Login: `flyctl auth login`

2. **Secrets Management**
   - Export from ~/.claude/secrets/credentials.json:
     - PostgreSQL password
     - Redis password
     - Any API keys needed

3. **Database Strategy Decision**

   **Option A: Fresh PostgreSQL (Recommended for Phase 2)**
   - Use Fly.io managed PostgreSQL (free 1GB)
   - Deploy empty, test without production data
   - PRO: Isolated testing environment
   - CON: No real data (can't test episodic memory)

   **Option B: Connect to Production PostgreSQL**
   - Point to existing CEREBRO database (port 5437)
   - PRO: Real data, full functionality
   - CON: Risk to production data
   - **NOT RECOMMENDED for Phase 2**

   **Selected: Option A** (isolated testing)

---

### Step-by-Step Deployment

#### 1. Prepare Fly.io Configuration

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0

# Initialize Fly app
flyctl launch --name nexus-cerebro-api \
              --region iad \
              --no-deploy

# This creates fly.toml
```

#### 2. Configure fly.toml

```toml
app = "nexus-cerebro-api"
primary_region = "iad"

[build]

[http_service]
  internal_port = 8003
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

[[services]]
  protocol = "tcp"
  internal_port = 8003

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[env]
  AGENT_ID = "nexus"
  INSTANCE_ID = "fly-iad-1"
  LOG_LEVEL = "info"
```

#### 3. Create PostgreSQL (Fly.io)

```bash
# Create Fly PostgreSQL
flyctl postgres create \
  --name nexus-cerebro-db \
  --region iad \
  --initial-cluster-size 1 \
  --vm-size shared-cpu-1x \
  --volume-size 1

# Attach to app
flyctl postgres attach nexus-cerebro-db
```

#### 4. Create Redis (Fly.io)

```bash
# Create Fly Redis (Upstash)
flyctl redis create \
  --name nexus-cerebro-redis \
  --region iad \
  --plan free

# Get connection string
flyctl redis status nexus-cerebro-redis
```

#### 5. Set Secrets

```bash
# Get secrets from local credentials
POSTGRES_PASSWORD=$(jq -r '.databases.nexus_v2.password' ~/.claude/secrets/credentials.json)

# Set in Fly.io
flyctl secrets set \
  POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  REDIS_PASSWORD="nexus_redis_secure_2025"
```

#### 6. Deploy

```bash
# Deploy to Fly.io
flyctl deploy

# Check status
flyctl status

# View logs
flyctl logs
```

#### 7. Test Remote Access

```bash
# Get app URL
APP_URL=$(flyctl info --json | jq -r '.Hostname')

# Test health endpoint
curl https://$APP_URL/health | jq '.'

# Test from Claude Code (this session)
# Should return: {status: "healthy", instance_id: "fly-iad-1"}
```

---

## 🧪 Testing Plan

### Functional Tests

1. **Health Check**
   ```bash
   curl https://nexus-cerebro-api.fly.dev/health
   # Expected: 200 OK, instance_id: "fly-iad-1"
   ```

2. **Database Connectivity**
   ```bash
   curl https://nexus-cerebro-api.fly.dev/health
   # Expected: database: "connected"
   ```

3. **Redis Connectivity**
   ```bash
   curl https://nexus-cerebro-api.fly.dev/health
   # Expected: redis: "connected"
   ```

4. **Episodic Memory** (if using production DB)
   ```bash
   curl https://nexus-cerebro-api.fly.dev/memory/search \
     -d '{"query": "distributed architecture"}'
   # Expected: Episodes returned
   ```

5. **Remote Access from Claude Code**
   ```bash
   # From this session:
   curl https://nexus-cerebro-api.fly.dev/api/brain/process \
     -d '{"query": "test deployment"}'
   # Expected: Brain processing response
   ```

### Performance Tests

1. **Latency Baseline**
   ```bash
   # Local (baseline)
   time curl http://localhost:8003/health

   # VPS
   time curl https://nexus-cerebro-api.fly.dev/health

   # Target: <200ms for health check
   ```

2. **Load Test (basic)**
   ```bash
   # 10 concurrent requests
   for i in {1..10}; do
     curl https://nexus-cerebro-api.fly.dev/health &
   done
   wait

   # Expected: All succeed, <500ms avg
   ```

---

## 📋 Success Criteria

- [ ] Fly.io account created and configured
- [ ] PostgreSQL deployed and accessible
- [ ] Redis deployed and accessible
- [ ] CEREBRO API deployed successfully
- [ ] Health check returns 200 OK
- [ ] Database connectivity confirmed
- [ ] Redis connectivity confirmed
- [ ] Remote access from Claude Code working
- [ ] Latency acceptable (<200ms health check)
- [ ] Cost validated ($0 on free tier)
- [ ] Logs accessible via `flyctl logs`
- [ ] Documentation updated with deployment URL

---

## 🔄 Rollback Strategy

If deployment fails or issues arise:

1. **Keep local instance running** (Phase 1 setup)
2. **Destroy Fly.io resources:**
   ```bash
   flyctl apps destroy nexus-cerebro-api
   flyctl postgres destroy nexus-cerebro-db
   flyctl redis destroy nexus-cerebro-redis
   ```
3. **Zero cost impact** (free tier)
4. **No data loss** (using isolated DB)

---

## 📊 Cost Tracking

**Phase 2 Budget:** $0-10/month

**Free Tier Usage:**
- 3 shared-cpu VMs (256MB each): $0
- PostgreSQL (1GB): $0
- Redis (25MB): $0

**If exceeds free tier:**
- Shared CPU-1x (512MB): ~$5/month
- Total estimated: ~$10/month

**Alert threshold:** If cost >$15/month, pause and review

---

## 🚀 Phase 3 Preview

After Phase 2 validates single instance:

**Phase 3 Goals:**
1. Deploy to 3 regions (US-East, EU-West, AP-Southeast)
2. Multi-instance in each region (failover)
3. Global load balancing (DNS-based)
4. Monitoring (Prometheus + Grafana)
5. Auto-scaling based on load

**Estimated Phase 3 Cost:** $50-150/month (depending on traffic)

---

## 📝 Next Session Action Items

1. Create Fly.io account
2. Install flyctl CLI
3. Review blueprint alignment with Fly.io architecture
4. Decide: Fresh DB vs Production DB connection
5. Execute deployment steps 1-7
6. Run testing plan
7. Update TRACKING.md with results
8. Git commit: Phase 2 deployment files (fly.toml)

---

**Plan Status:** Ready for Execution
**Ricardo Approval:** Pending
**Risk Level:** Low (free tier, isolated environment)
**Estimated Time:** 2-4 hours (including troubleshooting)
