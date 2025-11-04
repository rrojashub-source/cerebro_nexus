# 🛡️ NEXUS Backup System - Quick Reference Card

**Version:** 3.0.0 | **Status:** Production Ready

---

## 📋 Common Commands

### Backups

```bash
# Manual daily backup
sudo ./scripts/backup_full_nexus.sh daily

# Manual weekly backup
sudo ./scripts/backup_full_nexus.sh weekly

# Critical backup (before major changes)
sudo ./scripts/backup_full_nexus.sh critical

# Check last backup log
cat /mnt/z/NEXUS_BACKUPS/logs/backup_daily_$(date +%Y%m%d)_*.log
```

### Restore

```bash
# Interactive restore (shows menu)
sudo ./scripts/restore_full_nexus.sh

# Direct restore from specific backup
sudo ./scripts/restore_full_nexus.sh /mnt/z/NEXUS_BACKUPS/daily/nexus_full_2025-10-29_daily.tar.gz.gpg
```

### Monitoring

```bash
# List recent backups
ls -lht /mnt/z/NEXUS_BACKUPS/daily/ | head -10

# Check disk space
df -h /mnt/z

# View cron jobs
crontab -l

# Check backup logs
tail -f /mnt/z/NEXUS_BACKUPS/logs/cron_daily.log

# Verify system health
curl http://localhost:8003/health
curl http://localhost:8003/stats
```

---

## 🗂️ File Locations

```
Backup Scripts:
  /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/scripts/backup_full_nexus.sh
  /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/scripts/restore_full_nexus.sh

Backups:
  /mnt/z/NEXUS_BACKUPS/daily/     (last 7 days)
  /mnt/z/NEXUS_BACKUPS/weekly/    (last 4 weeks)
  /mnt/z/NEXUS_BACKUPS/monthly/   (last 3 months)
  /mnt/z/NEXUS_BACKUPS/critical/  (manual, indefinite)

Logs:
  /mnt/z/NEXUS_BACKUPS/logs/

Safety Backups:
  /mnt/z/NEXUS_BACKUPS/pre_restore_safety/

Documentation:
  BACKUP_SYSTEM_GUIDE.md (complete guide)
  BACKUP_QUICK_REFERENCE.md (this file)
```

---

## ⏰ Automated Schedule

```
03:00 AM daily    → Daily backup   (keep 7 days)
04:00 AM Sunday   → Weekly backup  (keep 4 weeks)
05:00 AM 1st day  → Monthly backup (keep 3 months)
```

---

## 🚨 Emergency Procedures

### Data Loss

```bash
# 1. Stop system immediately
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_MASTER_NEXUS_001/FASE_4_CONSTRUCCION
docker-compose down

# 2. Restore from latest backup
sudo ./scripts/restore_full_nexus.sh

# 3. Verify restoration
curl http://localhost:8003/stats
```

### Ransomware

```bash
# 1. Disconnect network
# 2. Download backup from Google Drive
rclone copy gdrive:NEXUS_BACKUPS/daily/latest.tar.gz.gpg /tmp/

# 3. Restore from offsite backup
sudo ./scripts/restore_full_nexus.sh /tmp/latest.tar.gz.gpg
```

---

## 🔑 Key Configurations

### Enable/Disable Features

Edit `scripts/backup_full_nexus.sh`:

```bash
ENABLE_ENCRYPTION="yes"     # Line 39
ENABLE_CLOUD_SYNC="yes"     # Line 43
ENABLE_NOTIFICATIONS="yes"  # Line 47
```

### Change Retention

```bash
RETENTION_DAILY=7      # Line 27 (days)
RETENTION_WEEKLY=28    # Line 28 (days)
RETENTION_MONTHLY=90   # Line 29 (days)
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Permission denied | `chmod +x scripts/*.sh && sudo ./script.sh` |
| Docker not found | `sudo usermod -aG docker $USER && newgrp docker` |
| GPG fails | `gpg --list-keys` (generate if missing) |
| rclone fails | `rclone config` (setup Google Drive) |
| Webhook fails | Verify URL in script line 49 |
| Cron not running | `sudo systemctl start cron` |

---

## ✅ Pre-Launch Checklist

- [ ] GPG key generated and backed up
- [ ] rclone configured for Google Drive
- [ ] Notifications tested
- [ ] Cron jobs installed
- [ ] Test backup completed
- [ ] Test restore completed
- [ ] Documentation reviewed

---

## 📞 Support

**Full Documentation:** `BACKUP_SYSTEM_GUIDE.md`
**System Owner:** Ricardo Rojas
**Emergency Rollback:** Check `/mnt/z/NEXUS_BACKUPS/pre_restore_safety/ROLLBACK_INSTRUCTIONS_*.txt`

---

**Quick Help:**
```bash
# Show this file
cat BACKUP_QUICK_REFERENCE.md

# Show full guide
cat BACKUP_SYSTEM_GUIDE.md
```
