#!/bin/bash

# ====================================
# VERIFICAR VOLÚMENES Y RECUERDOS ARIA
# Diagnóstico completo del sistema
# ====================================

echo "🔍 DIAGNÓSTICO COMPLETO ARIA CEREBRO..."
echo ""

echo "📁 1. VERIFICAR VOLÚMENES DOCKER:"
echo "=================================="
docker volume ls | grep -E "(aria|postgres|memoria)" || echo "❌ No se encontraron volúmenes ARIA"
echo ""

echo "📊 2. INSPECCIONAR VOLUMEN POSTGRESQL:"
echo "======================================"
docker volume inspect proyecto_aria_memoria_persistente_postgres_data 2>/dev/null || echo "❌ Volumen PostgreSQL no encontrado"
echo ""

echo "🐘 3. CONECTAR A POSTGRESQL Y CONTAR RECUERDOS:"
echo "================================================"
docker exec aria_postgresql_unified psql -U aria_user -d aria_memory -c "
SELECT 
    'Episodes' as type, COUNT(*) as count FROM memory_system.episodes
UNION ALL
SELECT 
    'Semantic', COUNT(*) FROM memory_system.semantic_memory
UNION ALL
SELECT 
    'Working', COUNT(*) FROM memory_system.working_memory
UNION ALL
SELECT 
    'Sessions', COUNT(*) FROM memory_system.sessions;
" 2>/dev/null || echo "❌ No se pudo conectar a PostgreSQL"
echo ""

echo "📅 4. VERIFICAR RECUERDOS MÁS RECIENTES:"
echo "========================================="
docker exec aria_postgresql_unified psql -U aria_user -d aria_memory -c "
SELECT 
    timestamp,
    action_type,
    LEFT(action_details::text, 100) as preview
FROM memory_system.episodes 
ORDER BY timestamp DESC 
LIMIT 5;
" 2>/dev/null || echo "❌ No se pudieron leer episodios"
echo ""

echo "🔗 5. VERIFICAR API ENDPOINTS:"
echo "==============================="
echo "Health check:"
curl -s http://localhost:8001/health | jq '.' 2>/dev/null || echo "❌ API no responde"
echo ""
echo "Recent memories:"
curl -s "http://localhost:8001/memory/episodic/recent?limit=2" | jq '.' 2>/dev/null || echo "❌ No se pueden obtener memorias recientes"
echo ""

echo "📈 6. ESTADÍSTICAS SISTEMA:"
echo "============================"
curl -s http://localhost:8001/stats | jq '.' 2>/dev/null || echo "❌ No se pueden obtener estadísticas"
echo ""

echo "✅ DIAGNÓSTICO COMPLETADO"
echo ""
echo "INTERPRETACIÓN:"
echo "- Si los volúmenes existen pero están vacíos = recuerdos perdidos"
echo "- Si los volúmenes no existen = necesario recuperar backup"
echo "- Si la API no responde = servicios no iniciados correctamente"
echo ""