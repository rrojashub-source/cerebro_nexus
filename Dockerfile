# NEXUS Cerebro API V3.0.0 - Distributed Architecture
# Multi-stage build para optimizar tamaño de imagen

# ============================================
# Stage 1: Builder (Dependencias)
# ============================================
FROM python:3.12-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-ml.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-ml.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY experiments/ ./experiments/
COPY scripts/ ./scripts/

# Create user for security (non-root)
RUN useradd -m -u 1000 nexus && \
    chown -R nexus:nexus /app

# Switch to non-root user
USER nexus

# Environment variables (overridable at runtime)
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_HOST=nexus_postgresql
ENV POSTGRES_PORT=5437
ENV POSTGRES_DB=nexus_memory
ENV POSTGRES_USER=nexus_superuser
ENV REDIS_HOST=nexus_redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0
ENV PORT=8003

# Expose API port
EXPOSE 8003

# Health check (llamada a /health endpoint)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

# Start command (uvicorn with proper workers)
CMD ["uvicorn", "src.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8003", \
     "--workers", "1", \
     "--log-level", "info", \
     "--access-log"]
