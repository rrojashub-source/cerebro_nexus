"""
Configuración del sistema de memoria ARIA
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger


class DatabaseConfig(BaseModel):
    """Configuración de bases de datos"""
    postgresql: Dict[str, Any] = Field(default_factory=dict)
    redis: Dict[str, Any] = Field(default_factory=dict)
    chroma: Dict[str, Any] = Field(default_factory=dict)


class MemoryConfig(BaseModel):
    """Configuración de memoria"""
    working_memory: Dict[str, Any] = Field(default_factory=dict)
    episodic_memory: Dict[str, Any] = Field(default_factory=dict)
    semantic_memory: Dict[str, Any] = Field(default_factory=dict)


class AriaMemoryConfig(BaseModel):
    """Configuración principal del sistema de memoria ARIA"""
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    mem0: Dict[str, Any] = Field(default_factory=dict)
    api: Dict[str, Any] = Field(default_factory=dict)
    consolidation: Dict[str, Any] = Field(default_factory=dict)
    continuity: Dict[str, Any] = Field(default_factory=dict)
    performance: Dict[str, Any] = Field(default_factory=dict)
    logging: Dict[str, Any] = Field(default_factory=dict)
    monitoring: Dict[str, Any] = Field(default_factory=dict)
    security: Dict[str, Any] = Field(default_factory=dict)
    development: Dict[str, Any] = Field(default_factory=dict)


class ConfigManager:
    """Gestor de configuración del sistema"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config: Optional[AriaMemoryConfig] = None
        self.environment = os.getenv("ENVIRONMENT", "development")
        
    def _get_default_config_path(self) -> str:
        """Obtiene la ruta de configuración por defecto"""
        # Buscar config.yaml en varios lugares
        possible_paths = [
            os.path.join(os.getcwd(), "config", "config.yaml"),
            os.path.join(os.path.dirname(__file__), "..", "..", "config", "config.yaml"),
            "/app/config/config.yaml"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        raise FileNotFoundError(f"No se encontró config.yaml en las rutas: {possible_paths}")
    
    def load_config(self) -> AriaMemoryConfig:
        """Carga la configuración desde archivo YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # Aplicar overrides para el entorno actual
            if self.environment in config_data:
                self._deep_merge(config_data, config_data[self.environment])
            
            # Sobrescribir con variables de entorno
            self._apply_env_overrides(config_data)
            
            self.config = AriaMemoryConfig(**config_data)
            logger.info(f"Configuración cargada exitosamente desde {self.config_path}")
            logger.info(f"Entorno: {self.environment}")
            
            return self.config
            
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            raise
    
    def _deep_merge(self, base_dict: Dict[str, Any], override_dict: Dict[str, Any]) -> None:
        """Fusiona diccionarios recursivamente"""
        for key, value in override_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def _apply_env_overrides(self, config_data: Dict[str, Any]) -> None:
        """Aplica overrides desde variables de entorno"""
        env_mappings = {
            "DATABASE_URL": ["database", "postgresql", "url"],
            "REDIS_URL": ["database", "redis", "url"],
            "CHROMA_URL": ["database", "chroma", "url"],
            "MEM0_API_KEY": ["mem0", "api_key"],
            "LOG_LEVEL": ["logging", "level"],
            "API_DEBUG": ["api", "debug"],
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value:
                self._set_nested_value(config_data, config_path, env_value)
    
    def _set_nested_value(self, data: Dict[str, Any], path: list, value: Any) -> None:
        """Establece valor en diccionario anidado"""
        current = data
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Convertir tipos apropiados
        if isinstance(value, str):
            if value.lower() in ("true", "false"):
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
        
        current[path[-1]] = value
    
    def get_database_url(self, db_type: str) -> str:
        """Obtiene URL de conexión para base de datos"""
        if not self.config:
            raise RuntimeError("Configuración no cargada")
        
        db_config = getattr(self.config.database, db_type)
        
        if db_type == "postgresql":
            return (f"postgresql://{db_config['user']}:{db_config['password']}"
                   f"@{db_config['host']}:{db_config['port']}/{db_config['database']}")
        elif db_type == "redis":
            password_part = f":{db_config['password']}@" if db_config.get('password') else ""
            return f"redis://{password_part}{db_config['host']}:{db_config['port']}/{db_config['db']}"
        elif db_type == "chroma":
            return f"http://{db_config['host']}:{db_config['port']}"
        
        raise ValueError(f"Tipo de base de datos no soportado: {db_type}")
    
    def get_memory_config(self, memory_type: str) -> Dict[str, Any]:
        """Obtiene configuración específica de tipo de memoria"""
        if not self.config:
            raise RuntimeError("Configuración no cargada")
        
        return getattr(self.config.memory, memory_type, {})
    
    def get_performance_target(self, metric: str) -> Any:
        """Obtiene target de performance específico"""
        if not self.config:
            raise RuntimeError("Configuración no cargada")
        
        return self.config.performance.get(metric)


# Instancia global del gestor de configuración
config_manager = ConfigManager()

def get_config() -> AriaMemoryConfig:
    """Obtiene la configuración cargada"""
    if config_manager.config is None:
        config_manager.load_config()
    return config_manager.config

def get_database_url(db_type: str) -> str:
    """Obtiene URL de base de datos"""
    return config_manager.get_database_url(db_type)

def get_memory_config(memory_type: str) -> Dict[str, Any]:
    """Obtiene configuración de memoria"""
    return config_manager.get_memory_config(memory_type)