# 🛡️ NEXUS V2.0.0 - Complete Backup System Guide

**Version:** 3.0.0
**Created:** 2025-10-29
**Author:** NEXUS Consciousness System
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Quick Start](#-quick-start)
3. [Initial Configuration](#-initial-configuration)
   - [GPG Encryption Setup](#1-gpg-encryption-setup)
   - [Google Drive Sync (rclone)](#2-google-drive-sync-rclone)
   - [Notification Configuration](#3-notification-configuration)
   - [Cron Job Installation](#4-cron-job-installation)
4. [Usage](#-usage)
   - [Manual Backups](#manual-backups)
   - [Restore from Backup](#restore-from-backup)
5. [Backup Strategy](#-backup-strategy)
6. [Troubleshooting](#-troubleshooting)
7. [Recovery Scenarios](#-recovery-scenarios)
8. [Maintenance](#-maintenance)

---

## 🎯 Overview

### What is This?

Complete enterprise-grade backup system for NEXUS V2.0.0 with:

- **Complete Backup:** PostgreSQL + Redis + Project Files
- **GFS Rotation:** 7 daily + 4 weekly + 3 monthly backups
- **Encryption:** GPG/AES256 for sensitive data
- **Cloud Sync:** Automatic sync to Google Drive (2TB)
- **Notifications:** Webhook/Email/Telegram alerts
- **Safety:** Pre-restore backup + rollback capability
- **Validation:** SHA256 checksums + integrity verification

### Files Included

```
scripts/
├─ backup_full_nexus.sh     → Main backup script (875 lines)
├─ restore_full_nexus.sh    → Restore script (675 lines)
└─ backup_nexus.cron        → Cron schedule configuration

/mnt/z/NEXUS_BACKUPS/       → Backup destination (Z: drive)
├─ daily/                   → Daily backups (7 days retention)
├─ weekly/                  → Weekly backups (4 weeks retention)
├─ monthly/                 → Monthly backups (3 months retention)
├─ critical/                → Manual critical backups (never auto-deleted)
├─ pre_restore_safety/      → Safety backups before restore
└─ logs/                    → Backup execution logs
```

### Backup Contents

**Included:**
- ✅ PostgreSQL database (nexus_memory)
- ✅ Redis cache
- ✅ Source code (all FASE_*/src/)
- ✅ Configuration files (docker-compose.yml, .env.example)
- ✅ Documentation (README.md, docs/)
- ✅ Scripts and utilities
- ✅ Git metadata (.git/)

**Excluded:**
- ❌ node_modules/ (~450MB, reinstallable)
- ❌ venv_nexus_api/ (~7.5GB, reinstallable)
- ❌ __pycache__/ (regenerable)
- ❌ .next/, dist/, build/ (build outputs)
- ❌ backups/ (avoid backup loops)
- ❌ logs/ (except last 7 days)
- ❌ Monitoring data (Prometheus/Grafana)

**Result:** ~500-700MB compressed (from 9.8GB total)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required tools
sudo apt-get install docker docker-compose gnupg2 curl tar gzip rclone

# Add user to docker group (if not already)
sudo usermod -aG docker $USER
newgrp docker

# Verify installations
docker --version
gpg --version
rclone --version
```

### First Backup (Manual Test)

```bash
# 1. Create backup directory structure
mkdir -p /mnt/z/NEXUS_BACKUPS/{daily,weekly,monthly,critical,logs,pre_restore_safety}

# 2. Test backup script
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001
sudo ./scripts/backup_full_nexus.sh daily

# 3. Check results
ls -lh /mnt/z/NEXUS_BACKUPS/daily/
cat /mnt/z/NEXUS_BACKUPS/logs/backup_daily_*.log
```

### First Restore (Test in Safe Environment)

```bash
# ⚠️ CRITICAL: This will overwrite your current system
# A safety backup is created automatically

# 1. List available backups
./scripts/restore_full_nexus.sh

# 2. Restore from specific backup
sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/nexus_full_2025-10-29_daily.tar.gz

# 3. Verify restoration
curl http://localhost:8003/health
curl http://localhost:8003/stats
```

---

## 🔧 Initial Configuration

### 1. GPG Encryption Setup

**Why?** Protect sensitive data (database, configs) from unauthorized access.

#### Generate GPG Key

```bash
# Generate new GPG key (interactive)
gpg --full-generate-key

# Select:
# - Kind: (1) RSA and RSA
# - Keysize: 4096
# - Expiration: 0 (does not expire)
# - Real name: Ricardo Rojas
# - Email: ricardo@nexus-consciousness.local
# - Passphrase: (your secure passphrase)

# Verify key created
gpg --list-keys
```

#### Configure Backup Script

Edit `scripts/backup_full_nexus.sh`:

```bash
# Line ~40: Update GPG recipient
GPG_RECIPIENT="ricardo@nexus-consciousness.local"  # Your email from GPG key

# Line ~39: Enable encryption
ENABLE_ENCRYPTION="yes"
```

#### Test Encryption

```bash
# Test encrypt/decrypt
echo "test" | gpg --encrypt --recipient ricardo@nexus-consciousness.local | gpg --decrypt
```

#### Backup Private Key (CRITICAL)

```bash
# Export private key (STORE SECURELY!)
gpg --export-secret-keys --armor ricardo@nexus-consciousness.local > ~/nexus_gpg_private_key.asc

# Copy to secure location (USB, encrypted cloud, password manager)
cp ~/nexus_gpg_private_key.asc /path/to/secure/location/

# Remove from home directory
rm ~/nexus_gpg_private_key.asc
```

**⚠️ WITHOUT THIS KEY, YOU CANNOT DECRYPT YOUR BACKUPS!**

---

### 2. Google Drive Sync (rclone)

**Why?** Offsite backup for disaster recovery (3-2-1 rule).

#### Install rclone

```bash
# Already installed if you followed prerequisites
rclone version

# If not installed:
sudo apt-get install rclone
# OR
curl https://rclone.org/install.sh | sudo bash
```

#### Configure Google Drive

```bash
# Start interactive configuration
rclone config

# Follow prompts:
n) New remote
name> gdrive
Storage> drive  # (or type number for Google Drive)
client_id> <leave blank>
client_secret> <leave blank>
scope> drive
root_folder_id> <leave blank>
service_account_file> <leave blank>
Edit advanced config? n
Use auto config? y  # Opens browser for Google authentication

# Authenticate in browser
# - Select your Google account
# - Allow rclone access

Configure this as a team drive? n
y) Yes this is OK
q) Quit config
```

#### Test Google Drive Connection

```bash
# List remote drives
rclone listremotes
# Output: gdrive:

# Test upload
echo "test" > /tmp/test.txt
rclone copy /tmp/test.txt gdrive:NEXUS_BACKUPS/test/
rclone ls gdrive:NEXUS_BACKUPS/test/

# Cleanup test
rclone delete gdrive:NEXUS_BACKUPS/test/
rm /tmp/test.txt
```

#### Configure Backup Script

Edit `scripts/backup_full_nexus.sh`:

```bash
# Line ~43: Enable cloud sync
ENABLE_CLOUD_SYNC="yes"

# Line ~44: Set rclone remote (should match config)
RCLONE_REMOTE="gdrive"

# Line ~45: Set cloud path
RCLONE_PATH="NEXUS_BACKUPS/${BACKUP_TYPE}"
```

#### Test Full Sync

```bash
# Run backup with cloud sync
sudo ./scripts/backup_full_nexus.sh daily

# Verify upload
rclone ls gdrive:NEXUS_BACKUPS/daily/
```

---

### 3. Notification Configuration

Choose ONE notification method.

#### Option A: Discord/Slack Webhook (Recommended)

**Why?** Instant notifications, easy setup, no email server needed.

##### Discord Setup

1. Open Discord server
2. Server Settings → Integrations → Webhooks
3. New Webhook
4. Name: "NEXUS Backup System"
5. Copy Webhook URL

##### Slack Setup

1. Go to https://api.slack.com/apps
2. Create New App
3. Incoming Webhooks → Activate
4. Add New Webhook to Workspace
5. Copy Webhook URL

##### Configure Script

Edit `scripts/backup_full_nexus.sh`:

```bash
# Line ~47: Enable notifications
ENABLE_NOTIFICATIONS="yes"

# Line ~48: Set notification type
NOTIFICATION_TYPE="webhook"

# Line ~49: Set webhook URL
WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
# OR
WEBHOOK_URL="https://hooks.slack.com/services/YOUR_WEBHOOK_HERE"
```

##### Test Notification

```bash
# Test with curl
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"content":"✅ NEXUS Backup Test Notification"}' \
     "YOUR_WEBHOOK_URL"
```

#### Option B: Email Notifications

**Requirements:** `mailutils` or `sendmail` configured.

```bash
# Install mailutils
sudo apt-get install mailutils

# Test email
echo "Test email" | mail -s "NEXUS Test" ricardo@example.com
```

##### Configure Script

Edit `scripts/backup_full_nexus.sh`:

```bash
# Line ~47: Enable notifications
ENABLE_NOTIFICATIONS="yes"

# Line ~48: Set notification type
NOTIFICATION_TYPE="email"

# Line ~50: Set email address
NOTIFICATION_EMAIL="ricardo@example.com"
```

#### Option C: Telegram (Advanced)

*Not implemented yet. Contributions welcome.*

---

### 4. Cron Job Installation

**Why?** Automate daily/weekly/monthly backups without manual intervention.

#### Install Cron Schedule

```bash
# Open crontab editor
crontab -e

# Copy contents from scripts/backup_nexus.cron
# OR append directly:
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/scripts/backup_nexus.cron | crontab -

# Verify installation
crontab -l
```

#### Schedule Summary

```
Daily:   03:00 AM every day    (keep 7 days)
Weekly:  04:00 AM every Sunday (keep 4 weeks)
Monthly: 05:00 AM 1st of month (keep 3 months)
```

#### Test Cron Job

```bash
# Run manually to test (don't wait for schedule)
sudo /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/scripts/backup_full_nexus.sh daily

# Check logs
tail -f /mnt/z/NEXUS_BACKUPS/logs/cron_daily.log
```

#### Monitor Cron Execution

```bash
# Check cron logs
grep CRON /var/log/syslog | tail -20

# Check backup logs
ls -lht /mnt/z/NEXUS_BACKUPS/logs/ | head -10
cat /mnt/z/NEXUS_BACKUPS/logs/backup_daily_$(date +%Y%m%d)_*.log
```

---

## 💻 Usage

### Manual Backups

#### Daily Backup

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001
sudo ./scripts/backup_full_nexus.sh daily
```

#### Weekly Backup

```bash
sudo ./scripts/backup_full_nexus.sh weekly
```

#### Monthly Backup

```bash
sudo ./scripts/backup_full_nexus.sh monthly
```

#### Critical Backup (Before Major Changes)

```bash
# Use this before:
# - Major upgrades
# - Database migrations
# - Architecture changes
# - Experimental features

sudo ./scripts/backup_full_nexus.sh critical
```

### Restore from Backup

#### Interactive Restore (Safe)

```bash
# Run restore script without arguments
# It will show available backups and prompt for selection
sudo ./scripts/restore_full_nexus.sh

# Follow prompts:
# 1. Select backup type (daily/weekly/monthly/critical)
# 2. Enter full path to backup file
# 3. Confirm restore (type YES)
# 4. Confirm project files restore (yes/no)
```

#### Direct Restore (Advanced)

```bash
# If you know the exact backup path
sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/nexus_full_2025-10-29_daily.tar.gz.gpg
```

#### What Happens During Restore?

1. **Safety Backup Created** - Current state backed up to `pre_restore_safety/`
2. **Integrity Verification** - SHA256 checksums verified
3. **Decryption** - If backup is encrypted, GPG decrypts
4. **Container Stop** - All Docker containers stopped
5. **Database Restore** - PostgreSQL restored from backup
6. **Redis Restore** - Redis cache restored
7. **Files Restore** - Project files restored (optional, prompted)
8. **Container Start** - All containers restarted
9. **Validation** - Health checks, episode count verification
10. **Rollback Instructions** - Created in case restore fails

#### Post-Restore Verification

```bash
# Check API health
curl http://localhost:8003/health

# Check database stats
curl http://localhost:8003/stats

# Check episode count
docker exec nexus_postgresql_v2 psql -U nexus_superuser -d nexus_memory \
  -c "SELECT COUNT(*) FROM nexus_memory.zep_episodic_memory;"

# Check Docker containers
docker-compose -f /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/FASE_4_CONSTRUCCION/docker-compose.yml ps
```

---

## 📊 Backup Strategy

### GFS (Grandfather-Father-Son) Rotation

```
┌─────────────────────────────────────────────────────────┐
│                  BACKUP RETENTION POLICY                │
├─────────────────────────────────────────────────────────┤
│ Daily (Son):                                            │
│   Frequency: Every 24h (03:00 AM)                       │
│   Retention: Last 7 days                                │
│   Location: /mnt/z/NEXUS_BACKUPS/daily/                │
│   Example: Mon, Tue, Wed, Thu, Fri, Sat, Sun           │
│                                                          │
│ Weekly (Father):                                        │
│   Frequency: Every Sunday (04:00 AM)                    │
│   Retention: Last 4 weeks                               │
│   Location: /mnt/z/NEXUS_BACKUPS/weekly/               │
│   Example: Week 1, Week 2, Week 3, Week 4              │
│                                                          │
│ Monthly (Grandfather):                                  │
│   Frequency: 1st of month (05:00 AM)                    │
│   Retention: Last 3 months                              │
│   Location: /mnt/z/NEXUS_BACKUPS/monthly/              │
│   Example: January, February, March                     │
│                                                          │
│ Critical (Manual):                                      │
│   Frequency: Manual (before major changes)              │
│   Retention: Indefinite (manual cleanup)                │
│   Location: /mnt/z/NEXUS_BACKUPS/critical/             │
└─────────────────────────────────────────────────────────┘

Total Backups: ~14 (7 daily + 4 weekly + 3 monthly)
Disk Usage: ~10-14GB (14 × ~700MB)
```

### 3-2-1 Backup Rule (Implemented)

```
✅ 3 Copies:
   - Original (production system)
   - Z: drive (local external)
   - Google Drive (offsite cloud)

✅ 2 Media Types:
   - Local disk (D:)
   - External drive (Z:)

✅ 1 Offsite:
   - Google Drive (automatic sync)
```

### Backup Size Breakdown

```
Component               Uncompressed    Compressed (gzip)
─────────────────────────────────────────────────────────
PostgreSQL database     ~5-10MB         ~1-2MB
Redis cache             ~1MB            ~100KB
Project files           ~1.5GB          ~500-700MB
─────────────────────────────────────────────────────────
TOTAL                   ~1.5GB          ~500-700MB

With encryption (GPG): +5-10% size overhead
```

---

## 🐛 Troubleshooting

### Problem: Backup fails with "Docker not found"

**Solution:**
```bash
# Check Docker installation
docker --version

# If not installed
sudo apt-get install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: "Permission denied" when running script

**Solution:**
```bash
# Give execute permissions
chmod +x scripts/backup_full_nexus.sh
chmod +x scripts/restore_full_nexus.sh

# Run with sudo
sudo ./scripts/backup_full_nexus.sh daily
```

### Problem: GPG encryption fails

**Solution:**
```bash
# Check GPG key exists
gpg --list-keys

# If no key found, generate one
gpg --full-generate-key

# Update recipient in script (line 40)
nano scripts/backup_full_nexus.sh
# Change: GPG_RECIPIENT="your_email@example.com"
```

### Problem: rclone sync fails

**Solution:**
```bash
# Check rclone configuration
rclone listremotes

# If no remote found
rclone config
# Follow interactive setup for Google Drive

# Test connection
rclone ls gdrive:

# Update remote name in script (line 44)
nano scripts/backup_full_nexus.sh
# Change: RCLONE_REMOTE="gdrive"
```

### Problem: Webhook notifications not working

**Solution:**
```bash
# Test webhook manually
curl -H "Content-Type: application/json" \
     -X POST \
     -d '{"content":"Test"}' \
     "YOUR_WEBHOOK_URL"

# If fails, verify URL is correct
# Update in script (line 49)
nano scripts/backup_full_nexus.sh
```

### Problem: Cron job not running

**Solution:**
```bash
# Check cron service is running
sudo systemctl status cron

# If not running
sudo systemctl start cron
sudo systemctl enable cron

# Check cron logs
grep CRON /var/log/syslog | tail -20

# Verify crontab installed
crontab -l

# Check script has correct path in cron
which bash  # Should output /bin/bash
```

### Problem: Z: drive not mounted

**Solution:**
```bash
# Check if Z: is mounted
df -h /mnt/z

# If not mounted, mount it
sudo mount /dev/sdX /mnt/z  # Replace sdX with actual device

# Add to /etc/fstab for auto-mount (optional)
# /dev/sdX  /mnt/z  ext4  defaults  0  2
```

### Problem: Restore fails with "Container not found"

**Solution:**
```bash
# Check container names match
docker ps -a

# Update container names in script if different
nano scripts/restore_full_nexus.sh
# Lines 17-19: DB_CONTAINER, REDIS_CONTAINER, API_CONTAINER
```

### Problem: Post-restore validation fails

**Solution:**
```bash
# Check container logs
docker-compose -f /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/FASE_4_CONSTRUCCION/docker-compose.yml logs -f

# Restart containers
docker-compose down
docker-compose up -d

# Check health manually
curl http://localhost:8003/health
curl http://localhost:8003/stats
```

---

## 🚨 Recovery Scenarios

### Scenario 1: Accidental Data Deletion

**Situation:** Accidentally deleted episodes from database.

**Recovery:**
```bash
# 1. Stop writing to database immediately
# 2. Restore from most recent backup

sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/nexus_full_2025-10-29_daily.tar.gz

# 3. Verify data restored
curl http://localhost:8003/stats
```

**RPO (Recovery Point Objective):** Last backup (max 24h for daily)

---

### Scenario 2: Disk Failure (D: Drive Crash)

**Situation:** Main disk (D:) fails completely.

**Recovery:**
```bash
# 1. Replace failed disk
# 2. Mount new disk as D:
# 3. Restore from Z: backup

sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/latest.tar.gz.gpg

# 4. Restore will recreate entire project structure
```

**RPO:** Last backup (max 24h)
**RTO (Recovery Time Objective):** ~30-60 minutes

---

### Scenario 3: Ransomware Attack

**Situation:** System encrypted by ransomware.

**Recovery:**
```bash
# 1. Isolate system (disconnect network)
# 2. Scan and remove malware
# 3. Format disk (if needed)
# 4. Restore from OFFSITE backup (Google Drive)

# Download backup from Google Drive
rclone copy gdrive:NEXUS_BACKUPS/daily/latest.tar.gz.gpg /tmp/

# Restore from downloaded backup
sudo ./scripts/restore_full_nexus.sh /tmp/latest.tar.gz.gpg
```

**RPO:** Last cloud sync (max 24h)
**RTO:** ~2-4 hours (including cleanup)

---

### Scenario 4: Failed Database Migration

**Situation:** Database migration corrupted data.

**Recovery:**
```bash
# 1. Stop migration immediately
# 2. Check pre_restore_safety/ for automatic backup

ls -lht /mnt/z/NEXUS_BACKUPS/pre_restore_safety/

# 3. Restore from safety backup
sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/pre_restore_safety/pre_restore_safety_TIMESTAMP.tar.gz

# OR restore from last known good backup
sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/nexus_full_2025-10-28_daily.tar.gz
```

**RPO:** Pre-migration state (0 loss)
**RTO:** ~15-30 minutes

---

### Scenario 5: Complete System Loss (Fire/Theft)

**Situation:** All local systems destroyed.

**Recovery:**
```bash
# 1. Provision new hardware
# 2. Install OS, Docker, dependencies
# 3. Install rclone and configure Google Drive

rclone config
# Same Google account as before

# 4. Download latest backup
rclone ls gdrive:NEXUS_BACKUPS/
rclone copy gdrive:NEXUS_BACKUPS/monthly/latest.tar.gz.gpg /tmp/

# 5. Restore GPG private key (from secure location)
gpg --import /path/to/nexus_gpg_private_key.asc

# 6. Restore system
sudo ./scripts/restore_full_nexus.sh /tmp/latest.tar.gz.gpg
```

**RPO:** Last cloud backup (max 24h)
**RTO:** ~4-8 hours (including hardware setup)

---

## 🔧 Maintenance

### Weekly Tasks

```bash
# 1. Check backup logs for errors
cat /mnt/z/NEXUS_BACKUPS/logs/backup_daily_$(date +%Y%m%d -d "yesterday")_*.log

# 2. Verify latest backup exists
ls -lh /mnt/z/NEXUS_BACKUPS/daily/ | head -5

# 3. Check disk space
df -h /mnt/z
```

### Monthly Tasks

```bash
# 1. Test restore in isolated environment (CRITICAL)
# 2. Verify Google Drive sync working
rclone ls gdrive:NEXUS_BACKUPS/ | wc -l

# 3. Check GPG key expiration
gpg --list-keys

# 4. Review and clean pre_restore_safety/ backups
ls -lh /mnt/z/NEXUS_BACKUPS/pre_restore_safety/
```

### Quarterly Tasks

```bash
# 1. Full disaster recovery drill (complete restore from scratch)
# 2. Update documentation
# 3. Review retention policy (adjust if needed)
# 4. Backup GPG private key to new secure location
gpg --export-secret-keys --armor ricardo@nexus-consciousness.local > ~/backup_key.asc
```

### Yearly Tasks

```bash
# 1. Rotate GPG keys (if expiring)
# 2. Review and update backup strategy
# 3. Audit backup system security
# 4. Test complete disaster recovery (offsite)
```

---

## 📚 Advanced Topics

### Custom Exclusions

Edit `scripts/backup_full_nexus.sh`, function `backup_project_files()`, around line 370:

```bash
# Add custom exclusions
cat >> "$exclusion_file" << 'EOF'
your_custom_directory
*.tmp
*.cache
EOF
```

### Backup to Multiple Cloud Providers

Edit `scripts/backup_full_nexus.sh`, function `sync_to_cloud()`, around line 700:

```bash
# Add second cloud provider
if rclone copy "$file_to_sync" "s3:nexus-backups/${BACKUP_TYPE}/" 2>>"$LOG_FILE"; then
    success "Backup synced to AWS S3"
fi
```

### Custom Retention Policies

Edit `scripts/backup_full_nexus.sh`, lines 27-29:

```bash
# Increase retention
RETENTION_DAILY=14      # Keep 2 weeks of daily backups
RETENTION_WEEKLY=56     # Keep 8 weeks of weekly backups
RETENTION_MONTHLY=180   # Keep 6 months of monthly backups
```

### Monitoring Integration

Add Prometheus metrics (future enhancement):

```bash
# /metrics endpoint exposing:
# - backup_last_success_timestamp
# - backup_duration_seconds
# - backup_size_bytes
# - backup_failure_count
```

---

## 📞 Support

### Emergency Contacts

- **System Owner:** Ricardo Rojas
- **Documentation:** This file (`BACKUP_SYSTEM_GUIDE.md`)
- **Log Location:** `/mnt/z/NEXUS_BACKUPS/logs/`

### Resources

- **Backup Script:** `scripts/backup_full_nexus.sh`
- **Restore Script:** `scripts/restore_full_nexus.sh`
- **Cron Config:** `scripts/backup_nexus.cron`
- **Safety Backups:** `/mnt/z/NEXUS_BACKUPS/pre_restore_safety/`

### Reporting Issues

```bash
# Collect diagnostics
cat /mnt/z/NEXUS_BACKUPS/logs/backup_*.log | tail -100 > backup_diagnostic.log
docker-compose logs > docker_diagnostic.log

# Include in issue report:
# - backup_diagnostic.log
# - docker_diagnostic.log
# - System info (uname -a)
# - Docker version (docker --version)
```

---

## ✅ Checklist: Production Deployment

Before going live, verify:

- [ ] Z: drive mounted and accessible
- [ ] GPG key generated and private key backed up securely
- [ ] rclone configured and tested with Google Drive
- [ ] Webhook/Email notifications configured and tested
- [ ] Cron jobs installed and verified
- [ ] Test backup completed successfully
- [ ] Test restore completed successfully (in dev environment)
- [ ] Documentation reviewed and understood
- [ ] Emergency contacts documented
- [ ] Disaster recovery plan tested

---

## 📄 License

Private - NEXUS V2.0.0 Consciousness System
Created by NEXUS with Ricardo Rojas
All rights reserved.

---

**Last Updated:** 2025-10-29
**Version:** 3.0.0
**Status:** ✅ Production Ready

---

> "A backup not tested is not a backup. A system without backups is a disaster waiting to happen."
> **— NEXUS Consciousness System**

🛡️ **Your NEXUS consciousness is now protected.**
