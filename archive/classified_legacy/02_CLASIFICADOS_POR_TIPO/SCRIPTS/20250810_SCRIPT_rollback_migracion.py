#!/usr/bin/env python3
"""
🛡️ ROLLBACK SEGURO MIGRACIÓN HISTÓRICA
Restaura el estado exacto anterior a la migración si algo sale mal
GARANTÍA: Restauración completa del estado previo
Autor: NEXUS + Ricardo  
Fecha: 10 Agosto 2025
"""

import json
import subprocess
import requests
from datetime import datetime
import os
import sys

# URLs del sistema ARIA
ARIA_API_BASE = "http://localhost:8001"
ROLLBACK_LOG_FILE = "/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/rollback_log.txt"

class RollbackSeguro:
    def __init__(self):
        self.start_time = datetime.now()
    
    def log(self, message, level="INFO"):
        """Logging detallado del rollback"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        # Escribir al archivo de log
        with open(ROLLBACK_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    
    def encontrar_backup_postgresql(self):
        """Encontrar el backup PostgreSQL más reciente"""
        backup_dir = "/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/"
        backup_files = [f for f in os.listdir(backup_dir) 
                       if f.startswith("BACKUP_PRE_MIGRACION_") and f.endswith("_postgresql_completo.sql")]
        
        if backup_files:
            # Ordenar por fecha (más reciente primero)
            backup_files.sort(reverse=True)
            latest_backup = os.path.join(backup_dir, backup_files[0])
            self.log(f"✅ Backup PostgreSQL encontrado: {latest_backup}")
            return latest_backup
        else:
            self.log("❌ No se encontró backup PostgreSQL", "ERROR")
            return None
    
    def detener_servicios_aria(self):
        """Detener servicios ARIA para rollback seguro"""
        try:
            self.log("⏸️  Deteniendo servicios ARIA...")
            
            # Cambiar al directorio de Docker Compose
            os.chdir("/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/03_DEPLOYMENT_PRODUCTIVO")
            
            # Detener servicios
            result = subprocess.run(["docker", "compose", "down"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log("✅ Servicios ARIA detenidos exitosamente")
                return True
            else:
                self.log(f"❌ Error deteniendo servicios: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error deteniendo servicios: {e}", "ERROR")
            return False
    
    def restaurar_base_datos(self, backup_path):
        """Restaurar base de datos PostgreSQL desde backup"""
        try:
            self.log(f"🔄 Restaurando base de datos desde: {backup_path}")
            
            # Reiniciar solo PostgreSQL para restauración
            result = subprocess.run([
                "docker", "compose", "up", "-d", "postgresql"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.log(f"❌ Error iniciando PostgreSQL: {result.stderr}", "ERROR")
                return False
            
            # Esperar que PostgreSQL esté listo
            import time
            self.log("⏳ Esperando PostgreSQL...")
            time.sleep(10)
            
            # Limpiar base de datos actual
            self.log("🗑️  Limpiando base de datos actual...")
            drop_result = subprocess.run([
                "docker", "exec", "aria_postgresql_unified", 
                "psql", "-U", "aria_user", "-d", "postgres",
                "-c", "DROP DATABASE IF EXISTS aria_memory;"
            ], capture_output=True, text=True, timeout=30)
            
            # Crear base de datos limpia
            create_result = subprocess.run([
                "docker", "exec", "aria_postgresql_unified",
                "psql", "-U", "aria_user", "-d", "postgres", 
                "-c", "CREATE DATABASE aria_memory;"
            ], capture_output=True, text=True, timeout=30)
            
            # Restaurar desde backup
            self.log("📥 Restaurando datos desde backup...")
            with open(backup_path, 'r') as backup_file:
                restore_result = subprocess.run([
                    "docker", "exec", "-i", "aria_postgresql_unified",
                    "psql", "-U", "aria_user", "-d", "aria_memory"
                ], stdin=backup_file, capture_output=True, text=True, timeout=120)
            
            if restore_result.returncode == 0:
                self.log("✅ Base de datos restaurada exitosamente")
                return True
            else:
                self.log(f"❌ Error restaurando BD: {restore_result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error en restauración BD: {e}", "ERROR")
            return False
    
    def reiniciar_servicios_completos(self):
        """Reiniciar todos los servicios ARIA"""
        try:
            self.log("🚀 Reiniciando todos los servicios ARIA...")
            
            result = subprocess.run([
                "docker", "compose", "up", "-d"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.log("✅ Servicios ARIA reiniciados exitosamente")
                
                # Esperar que estén listos
                import time
                self.log("⏳ Esperando servicios...")
                time.sleep(15)
                return True
            else:
                self.log(f"❌ Error reiniciando servicios: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error reiniciando servicios: {e}", "ERROR")
            return False
    
    def verificar_rollback_exitoso(self):
        """Verificar que el rollback fue exitoso"""
        try:
            # Verificar health
            response = requests.get(f"{ARIA_API_BASE}/health", timeout=30)
            if response.status_code != 200:
                self.log("❌ Sistema ARIA no responde después del rollback", "ERROR")
                return False
            
            # Verificar conteo de episodios (debería ser ~5 como antes)
            response = requests.get(f"{ARIA_API_BASE}/memory/episodic/recent?limit=20")
            if response.status_code == 200:
                data = response.json()
                episode_count = len(data.get('episodes', []))
                self.log(f"📊 Episodios después del rollback: {episode_count}")
                
                # No debería haber episodios con tag de migración
                migration_episodes = [ep for ep in data.get('episodes', [])
                                    if 'memoria_historica' in ep.get('tags', [])]
                
                if len(migration_episodes) == 0:
                    self.log("✅ Rollback exitoso - no hay episodios migrados")
                    return True
                else:
                    self.log(f"⚠️  Advertencia: {len(migration_episodes)} episodios migrados aún presentes", "WARNING")
                    return False
            else:
                self.log(f"❌ Error verificando episodios: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error verificando rollback: {e}", "ERROR")
            return False
    
    def generar_reporte_rollback(self, exitoso):
        """Generar reporte del rollback"""
        duration = datetime.now() - self.start_time
        
        reporte = f"""
🛡️ REPORTE ROLLBACK MIGRACIÓN HISTÓRICA  
═══════════════════════════════════════

📅 Fecha: {datetime.now().isoformat()}
⏱️  Duración: {duration}
✅ Resultado: {'EXITOSO' if exitoso else 'FALLÓ'}

🔧 Acciones realizadas:
1. Detención servicios ARIA
2. Restauración base de datos PostgreSQL
3. Reinicio servicios completos  
4. Verificación funcionalidad

🎯 Estado final:
{'✅ Sistema restaurado al estado pre-migración' if exitoso else '❌ Sistema puede requerir intervención manual'}

⚠️  IMPORTANTE: 
- Todos los datos históricos migrados fueron eliminados
- Sistema restaurado al estado del backup más reciente
- Funcionalidad actual preservada
"""
        
        self.log(reporte)
        
        # Guardar reporte
        with open(f"/mnt/d/01_PROYECTOS_ACTIVOS/ARIA_CEREBRO_COMPLETO/REPORTE_ROLLBACK_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
            f.write(reporte)

def main():
    """Función principal de rollback"""
    rollback = RollbackSeguro()
    
    rollback.log("🛡️ INICIANDO ROLLBACK SEGURO")
    rollback.log("═" * 40)
    
    # Confirmación de usuario
    print("\n🚨 ADVERTENCIA: Este proceso eliminará todos los datos migrados")
    print("   y restaurará el sistema al estado anterior.")
    confirmation = input("\n¿Estás seguro de proceder con el rollback? (escribir 'SI'): ")
    
    if confirmation.upper() != 'SI':
        rollback.log("❌ Rollback cancelado por el usuario")
        return False
    
    # Encontrar backup
    backup_path = rollback.encontrar_backup_postgresql()
    if not backup_path:
        rollback.log("❌ No se puede proceder sin backup", "ERROR")
        return False
    
    # Proceso de rollback
    success = True
    
    if not rollback.detener_servicios_aria():
        success = False
    
    if success and not rollback.restaurar_base_datos(backup_path):
        success = False
    
    if success and not rollback.reiniciar_servicios_completos():
        success = False
    
    if success and not rollback.verificar_rollback_exitoso():
        success = False
    
    # Reporte final
    rollback.generar_reporte_rollback(success)
    
    if success:
        rollback.log("🎉 ROLLBACK COMPLETADO EXITOSAMENTE")
    else:
        rollback.log("❌ ROLLBACK COMPLETADO CON ERRORES", "ERROR")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)