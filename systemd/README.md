# CEREBRO Sync Daemon - Systemd Service

**Version:** 1.0.0
**Date:** 2026-01-12
**Author:** NEXUS-PC

---

## 📋 Descripción

Servicio systemd para ejecutar el daemon de sincronización bidireccional entre PC local y Cloud (Fly.io).

**Funcionalidad:**
- Sincronización automática cada 5 minutos
- Auto-start en boot
- Auto-restart en caso de fallo
- Logs manejados por journald
- Resource limits (512MB RAM, 50% CPU)

---

## 🚀 Instalación

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/systemd
chmod +x install-service.sh
sudo ./install-service.sh
```

**Resultado esperado:**
```
✅ Service file installed
✅ Systemd reloaded
✅ Auto-start enabled
✅ Service started
```

---

## 🗑️ Desinstalación

```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/systemd
chmod +x uninstall-service.sh
sudo ./uninstall-service.sh
```

---

## 📊 Comandos Útiles

### Status del Servicio
```bash
sudo systemctl status cerebro-sync
```

**Output esperado:**
```
● cerebro-sync.service - CEREBRO Sync Daemon - Bidirectional PC <-> Cloud Sync
   Loaded: loaded (/etc/systemd/system/cerebro-sync.service; enabled)
   Active: active (running) since ...
```

### Ver Logs en Tiempo Real
```bash
sudo journalctl -u cerebro-sync -f
```

**Output esperado:**
```
Jan 12 15:58:48 hostname cerebro-sync[12345]: 🔄 Starting sync cycle
Jan 12 15:58:53 hostname cerebro-sync[12345]: ✅ Upload success: 1 inserted, 0 updated
Jan 12 15:58:54 hostname cerebro-sync[12345]: ✅ Sync cycle completed
```

### Ver Logs Históricos (últimas 100 líneas)
```bash
sudo journalctl -u cerebro-sync -n 100
```

### Ver Logs de Hoy
```bash
sudo journalctl -u cerebro-sync --since today
```

### Ver Logs con Timestamp
```bash
sudo journalctl -u cerebro-sync --since "2026-01-12 15:00:00"
```

### Controlar el Servicio

**Start:**
```bash
sudo systemctl start cerebro-sync
```

**Stop:**
```bash
sudo systemctl stop cerebro-sync
```

**Restart:**
```bash
sudo systemctl restart cerebro-sync
```

**Reload (si cambió configuración):**
```bash
sudo systemctl daemon-reload
sudo systemctl restart cerebro-sync
```

### Auto-start

**Enable (arrancar en boot):**
```bash
sudo systemctl enable cerebro-sync
```

**Disable (NO arrancar en boot):**
```bash
sudo systemctl disable cerebro-sync
```

**Verificar si está enabled:**
```bash
systemctl is-enabled cerebro-sync
```

---

## 📁 Archivos del Servicio

```
systemd/
├── cerebro-sync.service       # Definición del servicio systemd
├── install-service.sh          # Script de instalación
├── uninstall-service.sh        # Script de desinstalación
└── README.md                   # Este archivo
```

**Service instalado en:**
```
/etc/systemd/system/cerebro-sync.service
```

---

## 🔧 Configuración del Servicio

### Resource Limits

**Memoria:**
- Max: 512MB
- Si se excede: servicio reinicia automáticamente

**CPU:**
- Quota: 50% (máximo medio core)

### Restart Policy

- **Restart:** Always (siempre reinicia si falla)
- **RestartSec:** 10s (espera 10s antes de reiniciar)

### Seguridad (Hardening)

- `NoNewPrivileges=true` - No puede escalar privilegios
- `PrivateTmp=true` - Directorio /tmp aislado
- `ProtectSystem=strict` - Sistema de archivos protegido
- `ProtectHome=read-only` - Directorio home solo lectura
- `ReadWritePaths` - Solo puede escribir en:
  - `logs/` (para logs locales)
  - `memory/shared/` (para last_sync.json)

---

## 🐛 Troubleshooting

### Servicio no arranca

**1. Verificar estado:**
```bash
sudo systemctl status cerebro-sync
```

**2. Ver errores completos:**
```bash
sudo journalctl -u cerebro-sync -n 50 --no-pager
```

**3. Verificar permisos:**
```bash
ls -l /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/cerebro_sync_daemon.py
# Debe ser ejecutable: -rwxr-xr-x
```

**4. Probar script manualmente:**
```bash
cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0
python3 cerebro_sync_daemon.py
```

### Servicio se reinicia constantemente

**Ver últimas 20 líneas de log:**
```bash
sudo journalctl -u cerebro-sync -n 20
```

**Causas comunes:**
- PostgreSQL local no disponible (puerto 5437)
- Cloud API no accesible (https://nexus-cerebro-api.fly.dev)
- Credenciales incorrectas
- OOM (Out of Memory) - verificar con `sudo journalctl -u cerebro-sync | grep "memory"`

### Logs rotation

**Journald maneja logs automáticamente:**
- Max size: 4GB (default de systemd)
- Retention: 2 semanas (default)

**Ver configuración actual:**
```bash
journalctl --disk-usage
```

**Limpiar logs manualmente (liberar espacio):**
```bash
# Mantener solo últimos 3 días
sudo journalctl --vacuum-time=3d

# Mantener solo últimos 500MB
sudo journalctl --vacuum-size=500M
```

---

## 📈 Monitoreo

### Ver estadísticas de sync

**Última sincronización:**
```bash
cat /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0/memory/shared/last_sync.json
```

**Count de episodios sincronizados (desde logs):**
```bash
sudo journalctl -u cerebro-sync --since today | grep "Upload success"
```

### Verificar performance

**Resource usage actual:**
```bash
systemctl show cerebro-sync --property=MemoryCurrent,CPUUsageNSec
```

**Uptime del servicio:**
```bash
systemctl show cerebro-sync --property=ActiveEnterTimestamp
```

---

## 🔄 Actualizar el Daemon

Si modificas `cerebro_sync_daemon.py`:

```bash
# 1. Commit cambios
git add cerebro_sync_daemon.py
git commit -m "Update sync daemon"

# 2. Reiniciar servicio
sudo systemctl restart cerebro-sync

# 3. Verificar que arrancó correctamente
sudo systemctl status cerebro-sync
```

**NO es necesario reinstalar el servicio** (a menos que cambies `cerebro-sync.service`).

---

## 📚 Referencias

- [systemd.service documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [journalctl documentation](https://www.freedesktop.org/software/systemd/man/journalctl.html)
- [systemd security hardening](https://www.freedesktop.org/software/systemd/man/systemd.exec.html)

---

**Última actualización:** 2026-01-12
**Maintainer:** NEXUS-PC
