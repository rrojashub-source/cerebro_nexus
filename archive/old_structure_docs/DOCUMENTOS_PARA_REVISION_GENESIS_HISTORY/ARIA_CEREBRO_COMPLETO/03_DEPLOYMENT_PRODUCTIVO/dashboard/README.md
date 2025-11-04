# 🧠 ARIA Brain Dashboard

**Dashboard Web para Control del Cerebro Digital ARIA**  
**Versión:** 1.0  
**Fecha:** 20 Agosto 2025  
**Autores:** Ricardo + NEXUS

---

## 🎯 **DESCRIPCIÓN**

Dashboard web completo para monitoreo y control del cerebro digital ARIA. Incluye tanto backend como frontend para gestión visual del sistema completo.

### **🌟 CARACTERÍSTICAS PRINCIPALES:**

- **🚀 Control "Levantar Cerebro Completo"** - Botón único para iniciar todo el sistema
- **📊 Monitoreo en tiempo real** - WebSockets para actualizaciones automáticas
- **🔧 Control de servicios individuales** - Restart, logs, y estado detallado
- **💾 Gestión de backup/recovery** - Crear y restaurar backups con interfaz visual
- **🕵️ Explorador de episodios** - Búsqueda y análisis de memoria ARIA
- **📈 Estadísticas avanzadas** - Gráficos y métricas de rendimiento

---

## 🏗️ **ARQUITECTURA**

```
dashboard/
├── 📁 backend/              # FastAPI + WebSocket + Docker
│   ├── dashboard_api.py     # API principal del dashboard
│   ├── requirements.txt     # Dependencias Python
│   └── venv/                # Entorno virtual (auto-creado)
│
├── 📁 frontend/             # React + Recharts + Glass UI
│   ├── public/              # Archivos estáticos
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   │   ├── Dashboard.js          # Dashboard principal
│   │   │   ├── BrainControl.js       # Control cerebro completo
│   │   │   ├── ServiceControl.js     # Control servicios individual
│   │   │   ├── BackupRecovery.js     # Gestión backups
│   │   │   ├── EpisodeExplorer.js    # Explorador episodios
│   │   │   └── Statistics.js         # Estadísticas y gráficos
│   │   ├── services/
│   │   │   └── dashboardService.js   # Cliente API
│   │   ├── App.js           # Aplicación principal
│   │   ├── index.js         # Punto de entrada
│   │   └── index.css        # Estilos Glass Morphism
│   ├── package.json         # Dependencias Node.js
│   └── node_modules/        # Módulos (auto-creado)
│
├── 📁 logs/                 # Logs del sistema (auto-creado)
├── start_dashboard.sh       # Script de inicio automático
└── README.md               # Esta documentación
```

---

## 🚀 **INICIO RÁPIDO**

### **Método 1: Script Automático (RECOMENDADO)**

```bash
# Navegar al directorio del dashboard
cd /mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO/dashboard

# Ejecutar script de inicio
./start_dashboard.sh
```

El script se encarga de:
- ✅ Verificar dependencias del sistema
- ✅ Instalar dependencias Python y Node.js
- ✅ Crear entornos virtuales
- ✅ Iniciar backend en puerto 8002
- ✅ Iniciar frontend en puerto 3000
- ✅ Abrir navegador automáticamente

### **Método 2: Inicio Manual**

**Backend:**
```bash
cd dashboard/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python dashboard_api.py
```

**Frontend (en otra terminal):**
```bash
cd dashboard/frontend
npm install
npm start
```

---

## 🌐 **ACCESO AL DASHBOARD**

Una vez iniciado el sistema:

- **🎨 Dashboard Principal:** http://localhost:3000
- **🔧 API Backend:** http://localhost:8002
- **📖 Documentación API:** http://localhost:8002/docs
- **🧠 ARIA API:** http://localhost:8001 (debe estar corriendo)

---

## 📋 **FUNCIONALIDADES DETALLADAS**

### **1. 🏠 Dashboard Principal**
- Estado general del cerebro digital
- Métricas clave en tiempo real
- Resumen de servicios activos
- Actividad reciente de episodios

### **2. 🧠 Control del Cerebro**
- **Botón "Levantar Cerebro Completo"** con progreso visual
- Secuencia de arranque monitoreada
- Control de parada del sistema completo
- Estado de salud general

### **3. 🔧 Control de Servicios**
- Estado individual de cada servicio (PostgreSQL, Redis, ChromaDB, Neo4j, Qdrant, API)
- Restart de servicios específicos
- Visualización de logs en tiempo real
- Detalles técnicos por servicio

### **4. 💾 Backup y Recovery**
- Crear backups manuales inmediatos
- Visualizar backups existentes con metadata
- Restaurar desde backups específicos
- Programación de backups automáticos
- Métricas de integridad y tamaño

### **5. 🕵️ Explorador de Episodios**
- Búsqueda avanzada en memoria ARIA
- Filtros por tipo de acción, fecha, importancia
- Visualización detallada de episodios
- Análisis de patrones de actividad

### **6. 📊 Estadísticas y Analytics**
- Gráficos de actividad de episodios
- Distribución de tipos de acciones
- Métricas de salud de servicios
- Análisis de uso de memoria
- Tendencias de rendimiento

---

## 🔧 **CONFIGURACIÓN**

### **Puertos Utilizados:**
- **3000:** Frontend React
- **8002:** Backend FastAPI
- **8001:** ARIA API (externa, debe estar corriendo)

### **Dependencias del Sistema:**
- **Python 3.8+**
- **Node.js 16+**
- **npm 7+**
- **Docker** (para gestión de servicios ARIA)

### **Variables de Entorno (Opcionales):**
```bash
# Frontend
REACT_APP_API_URL=http://localhost:8002

# Backend
ARIA_API_URL=http://localhost:8001
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8002
```

---

## 🛠️ **DESARROLLO**

### **Estructura del Código Frontend:**

```javascript
// Ejemplo de uso del servicio API
import { dashboardService } from '../services/dashboardService';

// Obtener estado del sistema
const status = await dashboardService.getSystemStatus();

// Iniciar cerebro completo
const result = await dashboardService.startCompleteBrain();

// WebSocket en tiempo real
const ws = dashboardService.connectWebSocket(
  (data) => console.log('Update:', data),
  (error) => console.error('Error:', error)
);
```

### **API Endpoints Backend:**

```bash
# Estado del sistema
GET /api/system/status

# Control del cerebro
POST /api/system/start-complete
POST /api/system/stop-complete

# Control de servicios
POST /api/service/{service_name}/restart
GET /api/service/{service_name}/logs

# Backups
POST /api/backup/create

# WebSocket tiempo real
WS /ws
```

---

## 📊 **MONITOREO Y LOGS**

### **Ubicación de Logs:**
```bash
dashboard/logs/
├── backend.log       # Logs del backend FastAPI
├── frontend.log      # Logs del frontend React
└── dashboard.log     # Logs generales del sistema
```

### **Monitoreo en Tiempo Real:**
```bash
# Ver logs en vivo
tail -f dashboard/logs/backend.log
tail -f dashboard/logs/frontend.log

# Verificar procesos
ps aux | grep dashboard_api
ps aux | grep react-scripts
```

---

## 🚨 **TROUBLESHOOTING**

### **Problemas Comunes:**

**🔴 Backend no inicia (puerto 8002):**
```bash
# Verificar proceso ocupando puerto
lsof -i :8002
kill <PID>

# Verificar logs
cat dashboard/logs/backend.log
```

**🔴 Frontend no carga (puerto 3000):**
```bash
# Limpiar cache de npm
cd dashboard/frontend
rm -rf node_modules package-lock.json
npm install

# Verificar memoria disponible
free -h
```

**🔴 ARIA API no responde:**
```bash
# Verificar estado de contenedores ARIA
docker-compose ps

# Reiniciar cerebro digital
docker-compose restart
```

**🔴 WebSocket no conecta:**
- Verificar que el backend esté corriendo
- Comprobar configuración de proxy en package.json
- Revisar firewall/antivirus

---

## 🔄 **MANTENIMIENTO**

### **Actualizaciones:**
```bash
# Actualizar dependencias Python
cd dashboard/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Actualizar dependencias Node.js
cd dashboard/frontend
npm update
```

### **Limpieza:**
```bash
# Limpiar logs antiguos
find dashboard/logs -name "*.log" -mtime +7 -delete

# Limpiar cache de desarrollo
cd dashboard/frontend
rm -rf .next build node_modules/.cache
```

---

## 🤝 **COLABORACIÓN**

### **Para NEXUS Futuro:**
- **API Backend:** Totalmente funcional en `/api/...`
- **Componentes React:** Modulares y reutilizables
- **WebSocket:** Implementado para tiempo real
- **Estilos:** Glass Morphism moderno y responsive

### **Para Ricardo:**
- **Script de inicio:** Un comando y todo funciona
- **Interfaz intuitiva:** "For dummies" como pediste
- **Control completo:** "Levantar Cerebro Completo" implementado
- **Monitoreo visual:** Dashboard poderoso y funcional

---

## ✨ **PRÓXIMAS MEJORAS**

- [ ] Autenticación y seguridad
- [ ] Notificaciones push
- [ ] Temas oscuro/claro
- [ ] Exportación de reportes
- [ ] Integración con alertas
- [ ] Dashboard móvil responsivo
- [ ] Configuración visual de backups
- [ ] Analytics predictivo avanzado

---

**🎉 DASHBOARD ARIA BRAIN - CONTROL TOTAL DEL CEREBRO DIGITAL** ✨