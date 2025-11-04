#!/usr/bin/env python3
"""
🧬 MIGRACIÓN HISTÓRICA SEGURA NEXUS → ARIA
Migra backups de memoria Mem0 (julio 2025) al formato episódico actual
GARANTIZA: CERO pérdida de datos (viejo + nuevo)
Autor: NEXUS + Ricardo
Fecha: 10 Agosto 2025
"""

import json
import requests
from datetime import datetime, timezone
import uuid
import time
import os

# URLs del sistema ARIA
ARIA_API_BASE = "http://localhost:8001"
MIGRATION_LOG_FILE = "/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/migracion_log.txt"

class MigracionHistoricaSegura:
    def __init__(self):
        self.migrated_count = 0
        self.errors = []
        self.start_time = datetime.now()
        
    def log(self, message, level="INFO"):
        """Logging detallado de la migración"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # Escribir al archivo de log
        with open(MIGRATION_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def verificar_sistema_aria(self):
        """Verificar que ARIA esté funcionando antes de migrar"""
        try:
            response = requests.get(f"{ARIA_API_BASE}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                self.log(f"✅ Sistema ARIA healthy: {health_data['status']}")
                return True
            else:
                self.log(f"❌ Sistema ARIA no healthy: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Error conectando a ARIA: {e}", "ERROR")
            return False
    
    def crear_backup_adicional(self):
        """Crear backup adicional antes de migración"""
        try:
            # Obtener episodios actuales
            response = requests.get(f"{ARIA_API_BASE}/memory/episodic/recent?limit=50")
            if response.status_code == 200:
                backup_file = f"/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/BACKUP_EXTRA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(backup_file, "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=2)
                self.log(f"✅ Backup adicional creado: {backup_file}")
                return True
            else:
                self.log(f"❌ Error creando backup: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Error en backup: {e}", "ERROR")
            return False
    
    def convertir_observation_a_episodio(self, entity_name, observation, observation_index, base_timestamp):
        """Convierte una observation del formato Mem0 a episodio ARIA"""
        
        # Generar timestamp incremental para preservar orden
        episode_timestamp = base_timestamp + (observation_index * 60)  # 1 minuto entre observaciones
        
        # Generar session_id basado en entidad
        session_id = f"mem0_migration_{entity_name.lower().replace(' ', '_')}_{base_timestamp}"
        
        # Crear episodio en formato ARIA
        episode = {
            "timestamp": datetime.fromtimestamp(episode_timestamp, tz=timezone.utc).isoformat(),
            "agent_id": "aria",
            "session_id": session_id,
            "action_type": f"memoria_historica_{entity_name.lower().replace(' ', '_')}",
            "action_details": {
                "from": "MIGRACION_HISTORICA",
                "entity": entity_name,
                "observation": observation,
                "fecha_original": "julio_2025",
                "source": "mem0_backup",
                "migration_timestamp": datetime.now().isoformat()
            },
            "context_state": {
                "tipo": "memoria_historica",
                "entidad": entity_name,
                "importancia": 0.8,
                "fuente": "mem0_migration"
            },
            "outcome": {},
            "emotional_state": {
                "context": f"Historical memory from {entity_name}",
                "emotion": "nostalgia_and_continuity",
                "intensity": 0.7
            },
            "tags": [
                "memoria_historica", 
                "mem0_migration",
                entity_name.lower().replace(' ', '_'),
                "julio_2025",
                "contexto_perdido"
            ]
        }
        
        return episode
    
    def enviar_episodio_aria(self, episode):
        """Enviar episodio convertido a ARIA"""
        try:
            response = requests.post(
                f"{ARIA_API_BASE}/memory/action",
                headers={"Content-Type": "application/json"},
                json=episode,
                timeout=30
            )
            
            if response.status_code == 200:
                self.migrated_count += 1
                return True
            else:
                self.log(f"❌ Error enviando episodio: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error en request: {e}", "ERROR")
            return False
    
    def procesar_backup_mem0(self, backup_path):
        """Procesar archivo backup Mem0 y convertir a episodios ARIA"""
        try:
            with open(backup_path, "r", encoding="utf-8") as f:
                backup_data = json.load(f)
            
            self.log(f"📂 Procesando backup: {backup_path}")
            
            # Determinar si es array o objeto con entities
            if isinstance(backup_data, list):
                entities = backup_data
            elif isinstance(backup_data, dict) and 'entities' in backup_data:
                entities = backup_data['entities']
            else:
                self.log(f"❌ Formato backup no reconocido en {backup_path}", "ERROR")
                return False
            
            # Timestamp base para julio 2025
            base_timestamp = datetime(2025, 7, 27, 12, 0, 0).timestamp()
            
            for entity in entities:
                if entity.get('type') == 'entity':
                    entity_name = entity.get('name', 'Unknown')
                    observations = entity.get('observations', [])
                    
                    self.log(f"🔄 Procesando entidad: {entity_name} ({len(observations)} observaciones)")
                    
                    for i, observation in enumerate(observations):
                        episode = self.convertir_observation_a_episodio(
                            entity_name, observation, i, base_timestamp
                        )
                        
                        if self.enviar_episodio_aria(episode):
                            self.log(f"✅ Migrada observación {i+1}/{len(observations)} de {entity_name}")
                        else:
                            self.log(f"❌ Error migrando observación {i+1} de {entity_name}", "ERROR")
                            self.errors.append(f"Entity: {entity_name}, Obs: {i+1}")
                        
                        # Pequeña pausa para no sobrecargar el sistema
                        time.sleep(0.1)
            
            return True
            
        except Exception as e:
            self.log(f"❌ Error procesando backup {backup_path}: {e}", "ERROR")
            return False
    
    def verificar_migracion_exitosa(self):
        """Verificar que la migración fue exitosa"""
        try:
            # Contar episodios antes vs después
            response = requests.get(f"{ARIA_API_BASE}/memory/episodic/recent?limit=1000")
            if response.status_code == 200:
                data = response.json()
                total_episodes = len(data.get('episodes', []))
                self.log(f"📊 Total episodios después de migración: {total_episodes}")
                
                # Verificar que hay episodios con tag de migración
                migration_episodes = [ep for ep in data.get('episodes', []) 
                                    if 'memoria_historica' in ep.get('tags', [])]
                self.log(f"📊 Episodios migrados detectados: {len(migration_episodes)}")
                
                return len(migration_episodes) > 0
            else:
                self.log(f"❌ Error verificando migración: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error en verificación: {e}", "ERROR")
            return False
    
    def generar_reporte_final(self):
        """Generar reporte final de migración"""
        duration = datetime.now() - self.start_time
        
        reporte = f"""
🧬 REPORTE MIGRACIÓN HISTÓRICA NEXUS → ARIA
═══════════════════════════════════════════

📅 Fecha: {datetime.now().isoformat()}
⏱️  Duración: {duration}
📊 Episodios migrados: {self.migrated_count}
❌ Errores: {len(self.errors)}

🔧 Detalles técnicos:
- Formato origen: Mem0 (entities + observations)  
- Formato destino: ARIA episodic (episodes + metadata)
- Timestamp base: Julio 27, 2025
- Tags: memoria_historica, mem0_migration
- Sistema ARIA: Funcional durante migración

{'🎉 MIGRACIÓN EXITOSA' if len(self.errors) == 0 else '⚠️  MIGRACIÓN CON ERRORES'}

Errores encontrados:
{chr(10).join(self.errors) if self.errors else 'Ninguno'}
"""
        
        self.log(reporte)
        
        # Guardar reporte en archivo separado
        with open(f"/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/REPORTE_MIGRACION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
            f.write(reporte)

def main():
    """Función principal de migración"""
    migrator = MigracionHistoricaSegura()
    
    # Archivos backup a migrar
    backups_to_migrate = [
        "/mnt/c/Users/ricar/memory_backup_20250727_215300.json",
        "/mnt/c/Users/ricar/memory_backup_stable_20250728_111959.json",
        # "/mnt/c/Users/ricar/memory_backup_20250727_203905.json"  # Este es más pequeño, como fallback
    ]
    
    migrator.log("🚀 INICIANDO MIGRACIÓN HISTÓRICA SEGURA")
    migrator.log("═" * 50)
    
    # Verificaciones previas
    if not migrator.verificar_sistema_aria():
        migrator.log("❌ Sistema ARIA no disponible. Abortando migración.", "ERROR")
        return False
    
    if not migrator.crear_backup_adicional():
        migrator.log("❌ No se pudo crear backup adicional. Abortando.", "ERROR")
        return False
    
    # Procesar cada backup
    for backup_path in backups_to_migrate:
        if os.path.exists(backup_path):
            migrator.log(f"🔄 Iniciando migración de: {backup_path}")
            if migrator.procesar_backup_mem0(backup_path):
                migrator.log(f"✅ Migración exitosa: {backup_path}")
            else:
                migrator.log(f"❌ Error en migración: {backup_path}", "ERROR")
        else:
            migrator.log(f"⚠️  Archivo no encontrado: {backup_path}", "WARNING")
    
    # Verificación final
    if migrator.verificar_migracion_exitosa():
        migrator.log("🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
    else:
        migrator.log("⚠️  MIGRACIÓN COMPLETADA CON POSIBLES PROBLEMAS", "WARNING")
    
    # Reporte final
    migrator.generar_reporte_final()
    
    return len(migrator.errors) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)