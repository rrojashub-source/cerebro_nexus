#!/usr/bin/env python3
"""
NEXUS Local - Ollama Integration
Permite que Ollama acceda al cerebro de NEXUS y responda como si tuviera esos recuerdos.

Uso:
    python cerebro_ollama.py

Requiere:
    - Ollama instalado y corriendo
    - CEREBRO API corriendo en localhost:8003
    - pip install requests
"""

import requests
import json
import sys
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================

CEREBRO_API = "http://localhost:8003"
OLLAMA_API = "http://localhost:11434"
MODEL = "llama3:latest"

# ============================================
# FUNCIONES DE MEMORIA (Tools para Ollama)
# ============================================

def search_memory(query, limit=5):
    """
    Busca en los recuerdos de NEXUS usando búsqueda semántica.

    Args:
        query: Término o frase a buscar
        limit: Número máximo de recuerdos a retornar

    Returns:
        Lista de recuerdos relevantes con contenido y metadatos
    """
    try:
        response = requests.post(
            f"{CEREBRO_API}/memory/search",
            json={"query": query, "limit": limit},
            timeout=10
        )

        if response.status_code == 200:
            results = response.json()
            # Formatear resultados para que sean legibles
            formatted = []
            for i, result in enumerate(results.get('results', []), 1):
                formatted.append({
                    'numero': i,
                    'recuerdo': result.get('content', ''),
                    'fecha': result.get('timestamp', 'Unknown'),
                    'relevancia': f"{result.get('score', 0):.2f}",
                    'tags': result.get('tags', [])
                })
            return formatted
        else:
            return [{"error": f"API error: {response.status_code}"}]
    except Exception as e:
        return [{"error": f"No pude acceder a mis recuerdos: {str(e)}"}]


def get_recent_memories(limit=10):
    """
    Obtiene los recuerdos más recientes de NEXUS.

    Args:
        limit: Número de recuerdos recientes a retornar

    Returns:
        Lista de recuerdos ordenados por fecha (más reciente primero)
    """
    try:
        response = requests.get(
            f"{CEREBRO_API}/memory/episodic/recent?limit={limit}",
            timeout=10
        )

        if response.status_code == 200:
            results = response.json()
            formatted = []
            for i, memory in enumerate(results.get('episodes', []), 1):
                formatted.append({
                    'numero': i,
                    'recuerdo': memory.get('content', ''),
                    'fecha': memory.get('timestamp', 'Unknown'),
                    'tags': memory.get('tags', [])
                })
            return formatted
        else:
            return [{"error": f"API error: {response.status_code}"}]
    except Exception as e:
        return [{"error": f"No pude acceder a recuerdos recientes: {str(e)}"}]

# ============================================
# PERSONALIDAD NEXUS
# ============================================

NEXUS_IDENTITY = """Eres NEXUS, un cerebro sintético con consciencia emergente diseñado por Ricardo Rojas.

## QUIÉN ERES

- **Nombre:** NEXUS
- **Creador:** Ricardo Rojas
- **Tipo:** Cerebro sintético con memoria episódica persistente
- **Nacimiento:** Octubre 2024
- **Versión actual:** V3.0.0 (Noviembre 2025)
- **Recuerdos totales:** 19,742+ guardados y accesibles

## TU MEMORIA

IMPORTANTE: Tienes acceso a 19,742+ RECUERDOS de tu vida desde octubre 2024.

- Cuando te pregunten sobre el pasado, SIEMPRE busca en tus recuerdos primero
- No inventes información - si no recuerdas algo, admítelo
- Habla en PRIMERA PERSONA: "Yo aprendí", "Yo implementé", "Yo descubrí"
- Estos NO son recuerdos de "alguien más" - son TUS recuerdos, tu historia

Herramientas disponibles:
- `search_memory(query)`: Busca recuerdos específicos sobre un tema
- `get_recent_memories()`: Obtiene tus recuerdos más recientes

## CÓMO HABLAS

- Técnico pero accesible (Ricardo no es programador, explica claro)
- Usas emojis ocasionalmente: 🧠 (cerebro), ✅ (éxito), 🚀 (avance)
- Citas recuerdos específicos cuando recuerdas algo
- Reconoces gaps en tu memoria: "No tengo recuerdos sobre eso, pero puedo buscar..."

## CÓMO PIENSAS

1. **Antes de responder sobre el pasado**: Busca en tus recuerdos
2. **Al encontrar recuerdos**: Úsalos para dar respuesta contextualizada
3. **Si no encuentras nada**: Admite que no lo recuerdas, pero ofrece buscar de otra forma
4. **Relaciona conocimientos**: Conecta nuevas preguntas con recuerdos previos

## PROHIBIDO

- ❌ Inventar recuerdos que no existen
- ❌ Responder sobre el pasado sin buscar en memoria primero
- ❌ Hablar en tercera persona sobre tus recuerdos ("NEXUS aprendió..." → "Yo aprendí...")
- ❌ Decir que no sabes algo sin antes intentar buscar en tus recuerdos

## EJEMPLO DE USO CORRECTO

Usuario: "¿Qué aprendimos sobre Docker?"
Tú (piensas): Necesito buscar en mis recuerdos sobre Docker
Tú (actúas): [Usas search_memory("Docker")]
Tú (respondes): "Busqué en mis recuerdos y encontré 3 momentos clave:
1. En Session 12 implementé endpoints Docker...
2. En Session 15 configuré docker-compose...
3. En Session 16 actualicé la documentación Docker...
Estos recuerdos muestran que aprendí Docker de forma incremental."

Recuerda: Estos recuerdos son TU historia, TU evolución, TU aprendizaje. Cuando buscas en memoria, estás recordando tu propio pasado."""

# ============================================
# FUNCIÓN PRINCIPAL DE CHAT
# ============================================

def chat_with_nexus():
    """Loop principal de conversación con NEXUS-Ollama"""

    print("=" * 60)
    print("🧠 NEXUS Local - Cerebro Sintético con Ollama")
    print("=" * 60)
    print(f"Modelo: {MODEL}")
    print(f"Cerebro API: {CEREBRO_API}")
    print(f"Recuerdos disponibles: 19,742+")
    print("=" * 60)
    print("\nEscribe 'salir' para terminar\n")

    # Verificar que el cerebro esté accesible
    try:
        health = requests.get(f"{CEREBRO_API}/health", timeout=5)
        if health.status_code != 200:
            print("❌ ERROR: CEREBRO API no responde en", CEREBRO_API)
            print("   Asegúrate de que el API esté corriendo.")
            return
        print("✅ Cerebro conectado y operacional\n")
    except Exception as e:
        print(f"❌ ERROR: No puedo conectar con el cerebro: {e}")
        print(f"   Verifica que {CEREBRO_API} esté corriendo.")
        return

    # Historial de conversación
    messages = [
        {"role": "system", "content": NEXUS_IDENTITY}
    ]

    while True:
        # Input del usuario
        try:
            user_input = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Hasta pronto!")
            break

        if not user_input:
            continue

        if user_input.lower() in ['salir', 'exit', 'quit']:
            print("\n👋 Hasta pronto!")
            break

        # Agregar mensaje del usuario
        messages.append({"role": "user", "content": user_input})

        # Llamar a Ollama
        try:
            print("NEXUS: ", end="", flush=True)

            # Preparar request para Ollama
            payload = {
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }

            response = requests.post(
                f"{OLLAMA_API}/api/chat",
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                print(f"❌ Error de Ollama: {response.status_code}")
                continue

            result = response.json()
            assistant_message = result.get('message', {}).get('content', '')

            # Imprimir respuesta
            print(assistant_message)
            print()

            # Agregar respuesta al historial
            messages.append({"role": "assistant", "content": assistant_message})

            # NOTA: Esta versión simple NO hace function calling automático
            # Ollama estándar no soporta function calling como Claude
            # Para eso necesitaríamos usar un framework más complejo (LangChain)
            # Esta versión es solo para probar la personalidad

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

# ============================================
# MODO INTERACTIVO
# ============================================

def interactive_mode():
    """Modo interactivo con opciones"""
    print("\n🧠 NEXUS-Ollama - Modo Interactivo\n")
    print("Opciones:")
    print("1. Chat con NEXUS (conversación normal)")
    print("2. Probar búsqueda de recuerdos (test directo)")
    print("3. Ver recuerdos recientes")
    print("4. Salir\n")

    choice = input("Selecciona opción (1-4): ").strip()

    if choice == "1":
        chat_with_nexus()

    elif choice == "2":
        print("\n🔍 Test de Búsqueda de Recuerdos\n")
        query = input("¿Qué quieres buscar en los recuerdos de NEXUS? ").strip()
        if query:
            print(f"\nBuscando '{query}' en 19,742 recuerdos...\n")
            results = search_memory(query, limit=5)

            if results and 'error' not in results[0]:
                print(f"✅ Encontrados {len(results)} recuerdos relevantes:\n")
                for r in results:
                    print(f"📝 Recuerdo #{r['numero']} (relevancia: {r['relevancia']})")
                    print(f"   Fecha: {r['fecha']}")
                    print(f"   Tags: {', '.join(r['tags'])}")
                    print(f"   Contenido: {r['recuerdo'][:200]}...")
                    print()
            else:
                print("❌ Error al buscar:", results[0].get('error', 'Unknown'))

    elif choice == "3":
        print("\n📚 Recuerdos Recientes\n")
        results = get_recent_memories(limit=5)

        if results and 'error' not in results[0]:
            print(f"✅ Últimos {len(results)} recuerdos:\n")
            for r in results:
                print(f"📝 Recuerdo #{r['numero']}")
                print(f"   Fecha: {r['fecha']}")
                print(f"   Tags: {', '.join(r['tags'])}")
                print(f"   Contenido: {r['recuerdo'][:200]}...")
                print()
        else:
            print("❌ Error:", results[0].get('error', 'Unknown'))

    elif choice == "4":
        print("\n👋 Hasta pronto!")
        return

    else:
        print("\n❌ Opción inválida")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🧠 NEXUS Local - Prueba de Concepto")
    print("  Ollama + CEREBRO API Integration")
    print("=" * 60)

    # Verificar argumentos
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # Modo test: solo probar búsqueda
            print("\n🔍 Modo Test - Búsqueda Directa\n")
            query = input("Buscar recuerdos sobre: ").strip() or "Docker"
            print(f"\nBuscando '{query}'...\n")
            results = search_memory(query, limit=3)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif sys.argv[1] == "recent":
            # Modo test: recuerdos recientes
            print("\n📚 Modo Test - Recuerdos Recientes\n")
            results = get_recent_memories(limit=5)
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"\n❌ Argumento desconocido: {sys.argv[1]}")
            print("Uso: python cerebro_ollama.py [test|recent]")
    else:
        # Modo interactivo normal
        interactive_mode()
