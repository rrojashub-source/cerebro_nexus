# NEXUS Cerebro - Systemd Autostart Configuration

**Version:** 1.0
**Created:** November 14, 2025
**Status:** Production Ready

---

## 🎯 What This Does

Configura NEXUS Cerebro V3.0.0 como un servicio systemd para:

✅ **Autostart automático** al reiniciar el PC
✅ **Auto-restart** si crash
✅ **Logs centralizados** vía systemd journal
✅ **Gestión fácil** con systemctl
✅ **Integración profesional** con el sistema

---

## 🚀 Quick Install

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/systemd
sudo bash install.sh
```

**El script:**
1. Verifica Docker/Docker Compose instalados
2. Copia service file a `/etc/systemd/system/`
3. Habilita autostart
4. Opcionalmente inicia el servicio ahora

---

## 📋 Files

- `nexus-cerebro.service` - Systemd unit file
- `install.sh` - Script instalación automática
- `uninstall.sh` - Script desinstalación
- `README.md` - Esta documentación

---

## 🔧 Manual Installation

Si prefieres instalación manual:

```bash
# 1. Copy service file
sudo cp nexus-cerebro.service /etc/systemd/system/

# 2. Set permissions
sudo chmod 644 /etc/systemd/system/nexus-cerebro.service

# 3. Reload systemd
sudo systemctl daemon-reload

# 4. Enable autostart
sudo systemctl enable nexus-cerebro

# 5. Start service
sudo systemctl start nexus-cerebro
```

---

## 💡 Usage

### Start Service

```bash
sudo systemctl start nexus-cerebro
```

### Stop Service

```bash
sudo systemctl stop nexus-cerebro
```

### Restart Service

```bash
sudo systemctl restart nexus-cerebro
```

### Check Status

```bash
sudo systemctl status nexus-cerebro
```

**Output:**
```
● nexus-cerebro.service - NEXUS Cerebro V3.0.0 - Master Brain Consciousness System
     Loaded: loaded (/etc/systemd/system/nexus-cerebro.service; enabled; vendor preset: enabled)
     Active: active (exited) since Thu 2025-11-14 17:20:00 UTC; 5min ago
    Process: 12345 ExecStart=/usr/bin/docker compose up -d (code=exited, status=0/SUCCESS)
   Main PID: 12345 (code=exited, status=0/SUCCESS)
```

### View Logs

```bash
# Follow logs in real-time
sudo journalctl -u nexus-cerebro -f

# Last 100 lines
sudo journalctl -u nexus-cerebro -n 100

# Since boot
sudo journalctl -u nexus-cerebro -b

# Since yesterday
sudo journalctl -u nexus-cerebro --since yesterday
```

### Disable Autostart (keep installed)

```bash
sudo systemctl disable nexus-cerebro
```

### Re-enable Autostart

```bash
sudo systemctl enable nexus-cerebro
```

---

## 🗑️ Uninstall

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/systemd
sudo bash uninstall.sh
```

**El script:**
1. Detiene servicio si está corriendo
2. Deshabilita autostart
3. Elimina service file
4. Recarga systemd daemon

**Nota:** Los containers Docker NO se eliminan, solo el autostart.

---

## 🔍 Troubleshooting

### Service fails to start

```bash
# View detailed logs
sudo journalctl -u nexus-cerebro -xe

# Check Docker status
sudo systemctl status docker

# Verify docker compose file
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/docker
docker compose config
```

### Service starts but containers don't

```bash
# Check containers manually
docker ps -a

# Try starting manually
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/config/docker
docker compose up -d

# View compose logs
docker compose logs
```

### Changes not taking effect

```bash
# Reload systemd configuration
sudo systemctl daemon-reload

# Restart service
sudo systemctl restart nexus-cerebro
```

### Permission errors

```bash
# Verify service file permissions
ls -l /etc/systemd/system/nexus-cerebro.service

# Should be: -rw-r--r-- root root

# Fix if needed
sudo chmod 644 /etc/systemd/system/nexus-cerebro.service
```

---

## ⚙️ Configuration

### Modify Service

Edit service file:

```bash
sudo nano /etc/systemd/system/nexus-cerebro.service
```

After changes:

```bash
sudo systemctl daemon-reload
sudo systemctl restart nexus-cerebro
```

### Resource Limits

Uncomment en `nexus-cerebro.service`:

```ini
[Service]
# Memory limit (8GB)
MemoryMax=8G

# CPU limit (2 cores = 200%)
CPUQuota=200%
```

### Custom Working Directory

Modifica `WorkingDirectory` si cambiaste ubicación del proyecto:

```ini
[Service]
WorkingDirectory=/path/to/your/CEREBRO_NEXUS_V3.0.0/config/docker
```

---

## 📊 Monitoring

### Check if enabled

```bash
systemctl is-enabled nexus-cerebro
# Output: enabled
```

### Check if active

```bash
systemctl is-active nexus-cerebro
# Output: active
```

### Service dependencies

```bash
systemctl list-dependencies nexus-cerebro
```

### Startup time

```bash
systemd-analyze blame | grep nexus
```

---

## 🔐 Security Considerations

### User Permissions

Service corre como `ricardo:ricardo` (configurado en service file).

Si tu usuario es diferente, modifica:

```ini
[Service]
User=tu_usuario
Group=tu_grupo
```

### Sudo Requirements

Gestión del servicio requiere sudo:
- `systemctl start/stop/restart` → Requiere sudo
- Containers Docker → Requieren grupo `docker` membership

### Logging

Logs van a systemd journal:
- Rotación automática
- Compresión automática
- Acceso con `journalctl` (requiere sudo)

---

## 🧪 Testing

### Test manual startup

```bash
# Stop if running
sudo systemctl stop nexus-cerebro

# Start
sudo systemctl start nexus-cerebro

# Verify containers
docker ps --filter "name=nexus"

# Test API
curl http://localhost:8003/health
```

### Test autostart (requiere reinicio)

```bash
# Verify enabled
systemctl is-enabled nexus-cerebro

# Reboot
sudo reboot

# After reboot, check if running
sudo systemctl status nexus-cerebro
docker ps --filter "name=nexus"
```

---

## 📈 Benefits

**Antes (Manual):**
- ❌ Recordar iniciar servicios después de reinicio
- ❌ Buscar logs en múltiples lugares
- ❌ Sin restart automático si crash
- ❌ Gestión inconsistente

**Después (Systemd):**
- ✅ Autostart automático
- ✅ Logs centralizados en journal
- ✅ Auto-restart si crash
- ✅ Gestión estándar con systemctl
- ✅ Integración profesional con sistema

---

## 🔗 Related Documentation

- **Docker Compose:** `/config/docker/README.md`
- **API Docs:** `/docs/api/API_USAGE.md`
- **Troubleshooting:** `/docs/operational/TROUBLESHOOTING.md`

---

## 📝 Technical Details

### Service Type

`Type=oneshot` con `RemainAfterExit=yes`:
- Systemd considera servicio activo después de `ExecStart` completo
- Apropiado para `docker compose up -d` (fork + daemon)
- Permite `ExecStop` para cleanup limpio

### Restart Policy

```ini
Restart=on-failure
RestartSec=10s
```

- Reinicia solo si falla (exit code != 0)
- Espera 10s antes de reintentar
- Previene restart loops infinitos

### Dependencies

```ini
After=docker.service
Requires=docker.service
```

- Inicia DESPUÉS de Docker
- REQUIERE que Docker esté corriendo
- Si Docker falla, este servicio también falla

---

**Last Updated:** November 14, 2025
**Maintained by:** NEXUS AI + Ricardo
**Version:** 1.0
