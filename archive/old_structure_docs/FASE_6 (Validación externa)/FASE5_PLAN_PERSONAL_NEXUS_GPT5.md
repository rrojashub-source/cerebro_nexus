
# Plan Técnico Simplificado – FASE 5 (Uso Personal)

**Generado por:** GPT-5 (modelo de inteligencia artificial de OpenAI, plataforma ChatGPT, empresa OpenAI)  
**Fecha:** 2025-10-16 22:26:28  

---

## Objetivo de la FASE 5 (personal)
- Que corra siempre, en una sola máquina (PC, mini-PC o VPS barato).
- Backups simples y verificados.
- Privacidad primero (exponer lo mínimo).
- Operación sin fricción: encender y usar.

---

## 1) Despliegue “mono-nodo” con Docker Compose
- Mantén Postgres+pgvector y Redis en el mismo docker-compose.yml.
- Fija versiones explícitas de imágenes y límites de recursos.
- Crea volúmenes persistentes (`postgres_data`, `redis_data`) para simplificar backups.

---

## 2) Arranque automático y recuperación
- Crea un servicio systemd que ejecute `docker compose up -d` al iniciar el sistema.
- Usa `restart: unless-stopped` y healthchecks para auto-recuperación.

---

## 3) Acceso: local por defecto; remoto solo si lo necesitas
- Local: API escuchando en 127.0.0.1.
- Remoto (opcional): Tailscale o Caddy con TLS automático y rate-limit básico.

---

## 4) Backups sin dolor
- Script diario con `pg_dump` comprimido.
- Snapshot de Redis solo si almacena datos críticos.
- Cifrado con age o gpg y rotación de 7–14 días.
- Restauración mensual probada en contenedor temporal.

---

## 5) Observabilidad ligera
- Logs rotativos (`max-size`).
- Métricas opcionales con Netdata o Prometheus+Grafana.
- Umbrales simples (CPU, RAM, disco).

---

## 6) Rendimiento práctico
- p95 búsqueda ≤ 120 ms, inserción ≤ 800 ms.
- Benchmark simple con script Python o k6.

---

## 7) Privacidad y gobernanza mínima
- Local-first, sin telemetría externa.
- Variables en `.env` (no subir al repo).
- Script `purge_episodios.py` y TTL opcional por tipo.

---

## 8) Seguridad pragmática
- Un solo rol con RLS.
- Secretos con `docker secrets` o `.env` (chmod 600).
- TLS y lista blanca de IP si se expone públicamente.

---

## 9) Documentación “de bolsillo”
- README_local.md: cómo levantar y hacer backup.
- CHEATSHEET.md: 10 comandos clave.
- TROUBLESHOOTING.md: errores frecuentes y soluciones.

---

## 10) Requisitos hardware sugeridos
- CPU: 4 vCPU  
- RAM: 8–16 GB  
- Disco: SSD 50–100 GB  
- SO: Linux estable (Debian/Ubuntu)

---

## Checklist entregable
- [ ] docker-compose.yml con restart y healthcheck  
- [ ] Servicio systemd  
- [ ] Scripts backup/restore con cifrado  
- [ ] Prueba de restauración  
- [ ] Modo local y proxy opcional  
- [ ] Mini-benchmark y resultados  
- [ ] Documentación de bolsillo  
- [ ] Script purge_episodios.py  
- [ ] .env.example completo

---

**Comentarios finales:**  
El objetivo es mantener NEXUS estable, privado y fácil de restaurar. Esta guía está optimizada para uso personal sin depender de infraestructura empresarial.

---

**Documento generado automáticamente por GPT-5 (OpenAI)**  
Modelo: GPT-5  
Plataforma: ChatGPT  
Empresa: OpenAI
