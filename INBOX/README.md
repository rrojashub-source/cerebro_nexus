# INBOX - Carpeta Temporal de Migración

**Propósito:** Carpeta temporal para staging de archivos durante migración de V2.0.0 → V3.0.0

**Status:** 🟡 ACTIVA durante migración (se eliminará al completar)

---

## 🔄 Workflow:

1. **Ricardo copia carpeta** de CEREBRO_MASTER_NEXUS_001 → `INBOX/[CARPETA]/`
2. **Ricardo avisa:** "Copiada: [NOMBRE_CARPETA]"
3. **NEXUS lee** estructura + contenido
4. **NEXUS mueve** archivos a ubicaciones lógicas en V3.0.0
5. **NEXUS documenta** en MIGRATION_MANIFEST.md
6. **NEXUS reporta:** "✅ Completado, INBOX vacía, listo para siguiente"
7. **Repetir** hasta completar todas las carpetas

---

## ⚠️ IMPORTANTE:

- Esta carpeta NO es parte de la estructura final de V3.0.0
- Se eliminará cuando migración esté completa
- NO committear contenidos grandes (solo estructura vacía)
- Mantener vacía entre carpetas (una a la vez)

---

## 📊 Estado Actual:

**Carpetas procesadas:** 0
**Carpeta actual:** Ninguna (esperando primera)
**Última actualización:** Session 1 (Nov 3, 2025)

---

**Cuando migración complete:** `rm -rf INBOX/`
