# 🧠 ARIA CEREBRO UNIFICADO - DOCKERFILE
# Sistema completo: Fase 1 (Memoria Base) + Fase 2 (Continuidad Experiencial)
# Fecha: 9 Agosto 2025
# Unificado por: NEXUS

FROM python:3.11-slim

# Variables de entorno
ENV PYTHONPATH=/app
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de aplicación
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de aplicación
COPY memory_system/ ./memory_system/
COPY hybrid_layer/ ./hybrid_layer/
COPY config/ ./config/

# Crear directorios para logs
RUN mkdir -p /app/logs

# Exponer puertos
EXPOSE 8001

# Comando por defecto (API unificada)
CMD ["python", "-m", "memory_system.api.main"]