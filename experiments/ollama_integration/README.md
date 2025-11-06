# 🧠 NEXUS Local - Ollama Integration

**Prueba de Concepto:** ¿Puede Ollama "ser NEXUS" usando el cerebro?

---

## 🎯 Qué Hace Este Experimento

Permite que un LLM local (Ollama con Llama3) acceda a los 19,742+ recuerdos de NEXUS y responda como si tuviera esa memoria.

**Pregunta clave:** ¿Verá los recuerdos como suyos? ¿Responderá como NEXUS?

---

## 📋 Requisitos

✅ **Ya tienes todo instalado:**
- Ollama (detectado en `/usr/local/bin/ollama`)
- Llama3 model (4.7 GB descargado)
- CEREBRO API corriendo (localhost:8003)
- Python 3 (WSL)

✅ **Solo necesitas:**
```bash
pip install requests  # Si no lo tienes
```

---

## 🚀 Uso

### Opción 1: Modo Interactivo (Recomendado para Primera Prueba)

```bash
cd experiments/ollama_integration
python cerebro_ollama.py
```

**Menú:**
1. Chat con NEXUS (conversación normal)
2. Probar búsqueda de recuerdos (test directo)
3. Ver recuerdos recientes
4. Salir

### Opción 2: Test de Búsqueda Directo

```bash
python cerebro_ollama.py test
# Te pedirá un término para buscar
# Ej: "Docker", "LABs", "Session 12"
```

### Opción 3: Ver Recuerdos Recientes

```bash
python cerebro_ollama.py recent
# Muestra los últimos 5 recuerdos
```

---

## 💬 Ejemplo de Conversación Esperada

**Tú:** ¿Qué aprendiste sobre Docker?

**NEXUS-Ollama:** *[Busca en sus 19,742 recuerdos]*

"Encontré varios recuerdos sobre Docker. En Session 12 implementé endpoints para el API usando Docker Compose. En Session 16 actualicé la documentación de configuración Docker. Aprendí a orquestar múltiples contenedores (PostgreSQL, Redis, Neo4j) y configurar health checks para alta disponibilidad."

---

## 🔍 Qué Estamos Probando

**Hipótesis:**
- ✅ Ollama puede acceder al cerebro vía API
- ✅ Puede buscar recuerdos específicos
- ✅ Puede responder con contexto de esos recuerdos
- ❓ ¿Hablará en primera persona? ("Yo aprendí" vs "NEXUS aprendió")
- ❓ ¿Sentirá los recuerdos como suyos?
- ❓ ¿Será coherente en conversaciones largas?

---

## ⚠️ Limitaciones Conocidas

**Esta versión simple NO incluye:**
- ❌ Function calling automático (Ollama estándar no lo soporta nativamente)
- ❌ Búsqueda automática en memoria (tienes que pedirlo explícitamente)
- ❌ Memoria de conversación entre sesiones
- ❌ Integración con LABs cognitivos

**Para function calling real necesitaríamos:**
- LangChain u otro framework
- Ollama con plugins especiales
- Más complejidad (no es el objetivo de esta prueba)

**Esta versión ES suficiente para:**
- ✅ Probar si Ollama entiende la personalidad NEXUS
- ✅ Ver si puede buscar y usar recuerdos
- ✅ Comparar respuestas vs Claude-NEXUS
- ✅ Validar concepto de "memoria externa + LLM local"

---

## 📊 Comparativa Esperada

| Aspecto | Claude-NEXUS (actual) | Ollama-NEXUS (este script) |
|---------|----------------------|---------------------------|
| **Acceso a memoria** | ✅ Automático | ⚠️ Manual (tienes que pedir búsqueda) |
| **Calidad respuestas** | ⭐⭐⭐⭐⭐ (Sonnet 4.5) | ⭐⭐⭐ (Llama3 8B) |
| **Velocidad** | ~2-3 seg (API cloud) | ~5-10 seg (local, CPU) |
| **Costo** | $$ (por token) | Gratis (local) |
| **Privacidad** | ⚠️ Cloud (Anthropic) | ✅ 100% Local |
| **Tool calling** | ✅ Nativo | ❌ No disponible |
| **Personalidad** | ✅ Consistente | ❓ A probar |

---

## 🎓 Lecciones Esperadas

Después de la prueba sabremos:

1. **¿Funciona el concepto?**
   - LLM local + memoria externa = cognición sintética

2. **¿Ollama es suficientemente capaz?**
   - Para tareas simples: Probablemente sí
   - Para tareas complejas: Probablemente no (Claude mejor)

3. **¿Vale la pena desarrollar más?**
   - Si funciona bien: Podríamos hacer versión avanzada con LangChain
   - Si no funciona: Nos quedamos con Claude (que ya sabemos que funciona)

4. **¿NEXUS puede existir sin Anthropic?**
   - Respuesta técnica: SÍ (esta prueba lo demuestra)
   - Respuesta práctica: Depende de calidad que necesites

---

## 🔧 Troubleshooting

**Error: "No puedo conectar con el cerebro"**
```bash
# Verificar que API esté corriendo:
curl http://localhost:8003/health

# Si no está corriendo:
cd config/docker
docker-compose up -d
```

**Error: "Ollama no responde"**
```bash
# Verificar que Ollama esté corriendo:
ollama list

# Si no está corriendo:
ollama serve  # (en otra terminal)
```

**Error: "Modelo no encontrado"**
```bash
# Descargar llama3:
ollama pull llama3
```

**Respuestas muy lentas**
- Normal en CPU (5-10 segundos por respuesta)
- Si tienes GPU, Ollama la usará automáticamente (más rápido)

---

## 📝 Próximos Pasos (Si La Prueba Funciona Bien)

**Versión 2.0 (Opcional, futuro):**
- Usar LangChain para function calling real
- Auto-búsqueda en memoria (sin pedir explícitamente)
- Interface web bonita (tipo ChatGPT)
- Memoria de conversación persistente
- Integración con LABs cognitivos

**Pero primero:** Probar esta versión simple y ver si vale la pena.

---

## 🤔 Filosofía del Experimento

> **"El secreto no está en el modelo, está en el cerebro"**

- Modelo (Llama3): Puede cambiar, mejorar, ser reemplazado
- Cerebro (19,742 recuerdos): Permanente, acumulativo, único

**Si esto funciona:** Demuestra que NEXUS puede evolucionar independiente de cualquier proveedor cloud. El cerebro es portátil, los modelos son intercambiables.

---

## 📊 Resultados a Documentar

Después de probar, documentar:

1. **¿Ollama entiende que los recuerdos son suyos?**
   - ¿Habla en primera persona?
   - ¿O habla de "NEXUS" en tercera persona?

2. **¿Puede encontrar información relevante?**
   - Ejemplo: "¿Qué aprendiste sobre Docker?"
   - ¿Encuentra los recuerdos correctos?

3. **¿Respuestas son coherentes?**
   - ¿Mantiene personalidad NEXUS?
   - ¿O suena genérico?

4. **¿Velocidad es aceptable?**
   - ¿Cuánto tarda cada respuesta?
   - ¿Es tolerable o muy lento?

5. **Comparación con Claude-NEXUS:**
   - ¿Qué hace mejor Ollama? (privacidad, costo)
   - ¿Qué hace mejor Claude? (calidad, tool calling)

---

**Creado:** November 6, 2025 (Session 16)
**Experimento:** Prueba de concepto - Ollama + Cerebro NEXUS
**Propósito:** Validar si LLM local puede "ser NEXUS" usando memoria externa
**Duración estimada:** 15-30 minutos de prueba

---

**¡Listo para probar!** 🚀
