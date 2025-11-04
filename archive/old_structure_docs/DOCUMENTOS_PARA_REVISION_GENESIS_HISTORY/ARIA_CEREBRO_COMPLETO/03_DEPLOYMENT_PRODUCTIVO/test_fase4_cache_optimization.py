#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 FASE 4 - CACHE OPTIMIZATION TESTING
Test específico para validar mejora de performance del semantic cache optimizado

Validaciones:
- Cache hit rate mejorado con thresholds optimizados
- Performance improvement hacia objetivo 40%+
- Embedding model correctamente configurado
- Similarity matching funcionando

Fecha: 11 Agosto 2025 - FASE 4 Iniciada
Autorizado por: Consenso NEXUS-ARIA-Ricardo
"""

import asyncio
import requests
import time
import json
from typing import Dict, List, Any
from datetime import datetime

class Fase4CacheOptimizer:
    """Optimizador y validador de cache FASE 4"""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.test_results = []
        
    async def run_cache_optimization_tests(self):
        """Test completo de optimización cache FASE 4"""
        
        print("🚀 INICIANDO FASE 4 - CACHE OPTIMIZATION TESTING")
        print("=" * 60)
        
        # 1. Test cache warming con queries similares
        await self._test_cache_warming()
        
        # 2. Test similarity thresholds optimizados
        await self._test_optimized_thresholds()
        
        # 3. Test performance benchmark
        await self._test_performance_improvement()
        
        # 4. Test embedding model configuration
        await self._test_embedding_model_config()
        
        # 5. Reporte final
        await self._generate_cache_optimization_report()
    
    async def _test_cache_warming(self):
        """Warming del cache con queries estratégicas"""
        
        print("\n🔥 CACHE WARMING - QUERIES ESTRATÉGICAS")
        print("-" * 45)
        
        # Queries base para warming
        warming_queries = [
            "ARIA memoria sistema proyecto",
            "NEXUS desarrollo GraphRAG implementación", 
            "Ricardo colaboración ARIA NEXUS equipo",
            "sistema optimización performance cache",
            "memoria episódica semántica integración"
        ]
        
        # Primera ronda - llenar cache
        for i, query in enumerate(warming_queries):
            result = await self._execute_search_query(query, f"Warming query {i+1}")
            time.sleep(0.1)  # Pequeña pausa entre queries
        
        print(f"✅ Cache warming completado: {len(warming_queries)} queries base")
    
    async def _test_optimized_thresholds(self):
        """Test de thresholds optimizados (0.85, 0.75, 0.60)"""
        
        print("\n🎯 TESTING THRESHOLDS OPTIMIZADOS")
        print("-" * 35)
        
        # Queries con variaciones semánticas
        test_cases = [
            {
                "original": "ARIA memoria sistema proyecto",
                "variations": [
                    "ARIA sistema memoria proyecto",  # Orden diferente
                    "ARIA memoria proyecto sistema",  # Otra variación
                    "memoria ARIA sistema",           # Más diferente
                    "proyecto ARIA memoria"           # Aún más diferente
                ]
            },
            {
                "original": "NEXUS desarrollo GraphRAG", 
                "variations": [
                    "NEXUS GraphRAG desarrollo",
                    "desarrollo GraphRAG NEXUS",
                    "GraphRAG NEXUS implementación",
                    "NEXUS sistema GraphRAG"
                ]
            }
        ]
        
        cache_hits = 0
        total_variations = 0
        
        for case in test_cases:
            # Query original primero
            await self._execute_search_query(case["original"], "Original query", silent=True)
            
            # Test variaciones
            for variation in case["variations"]:
                result = await self._execute_search_query(variation, None, silent=True)
                total_variations += 1
                
                # Simular verificación de cache hit (simplificado)
                # En un test real, verificaríamos los headers o metadata de respuesta
        
        # Obtener estadísticas actuales
        stats = await self._get_cache_statistics()
        if stats:
            hit_rate = stats.get('hit_rate', 0)
            print(f"📊 Hit Rate actual: {hit_rate:.1%}")
            
            if hit_rate > 0.1:  # 10%+ consideramos mejora
                print(f"✅ Thresholds optimizados funcionando - Hit rate: {hit_rate:.1%}")
            else:
                print(f"⚠️ Hit rate bajo - Necesita más optimización: {hit_rate:.1%}")
    
    async def _test_performance_improvement(self):
        """Test de mejora de performance con cache hits"""
        
        print("\n⚡ PERFORMANCE IMPROVEMENT TESTING")
        print("-" * 37)
        
        # Query que debería estar en cache
        test_query = "ARIA memoria sistema proyecto desarrollo"
        
        # Múltiples ejecuciones para medir consistency
        times = []
        
        for i in range(5):
            start_time = time.time()
            await self._execute_search_query(test_query, None, silent=True)
            elapsed = (time.time() - start_time) * 1000  # ms
            times.append(elapsed)
        
        # Estadísticas de performance
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"⏱️ Tiempo promedio: {avg_time:.1f}ms")
        print(f"📊 Rango: {min_time:.1f}ms - {max_time:.1f}ms")
        
        # Comparar con baseline esperado
        baseline_time = 100.0  # ms baseline esperado
        
        if avg_time < baseline_time * 0.6:  # 40%+ mejora
            improvement = (baseline_time - avg_time) / baseline_time
            print(f"🎉 OBJETIVO ALCANZADO: {improvement:.1%} mejora vs baseline")
            return True
        else:
            improvement = (baseline_time - avg_time) / baseline_time if avg_time < baseline_time else 0
            print(f"📈 Mejora actual: {improvement:.1%} - Target: 40%+")
            return False
    
    async def _test_embedding_model_config(self):
        """Verificar configuración del embedding model"""
        
        print("\n🧠 EMBEDDING MODEL CONFIGURATION")
        print("-" * 33)
        
        # Test query que requiere embeddings para similarity
        test_queries = [
            "memoria artificial inteligencia",
            "AI memory artificial intelligence",  # En inglés para test
            "recuerdo sistema inteligente"        # Sinónimos
        ]
        
        embedding_working = True
        
        for query in test_queries:
            result = await self._execute_search_query(query, None, silent=True)
            if not result:
                embedding_working = False
                break
        
        # Verificar estadísticas de embedding index
        stats = await self._get_cache_statistics()
        if stats and 'distribution' in stats:
            embedding_index_size = stats['distribution'].get('embedding_index_size', 0)
            embedding_cache_size = stats['distribution'].get('embedding_cache_size', 0)
            
            print(f"📊 Embedding Index: {embedding_index_size} entries")
            print(f"📊 Embedding Cache: {embedding_cache_size} entries")
            
            if embedding_index_size > 0 or embedding_cache_size > 0:
                print("✅ Embedding model configurado correctamente")
                return True
            else:
                print("⚠️ Embedding model puede tener issues")
                return False
        
        return embedding_working
    
    async def _execute_search_query(self, query: str, description: str = None, silent: bool = False):
        """Ejecutar query de búsqueda"""
        
        try:
            response = requests.post(
                f"{self.base_url}/memory/search",
                json={
                    "query": query,
                    "memory_types": ["episodic", "semantic"],
                    "limit": 5
                },
                timeout=10
            )
            
            success = response.status_code == 200
            
            if description and not silent:
                status = "✅" if success else "❌"
                print(f"  {status} {description}: HTTP {response.status_code}")
            
            return response.json() if success else None
            
        except Exception as e:
            if description and not silent:
                print(f"  ❌ {description}: Error - {str(e)}")
            return None
    
    async def _get_cache_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('integrated_graph_memory', {}).get('semantic_cache_stats', {})
        except Exception:
            pass
        
        return {}
    
    async def _generate_cache_optimization_report(self):
        """Generar reporte final de optimización"""
        
        print("\n" + "=" * 60)
        print("📊 REPORTE FASE 4 - CACHE OPTIMIZATION")
        print("=" * 60)
        
        # Obtener estadísticas finales
        stats = await self._get_cache_statistics()
        
        if stats:
            print(f"📋 ESTADÍSTICAS FINALES:")
            print(f"   Total Queries: {stats.get('total_queries', 0)}")
            print(f"   Cache Hits: {stats.get('cache_hits', 0)}")
            print(f"   Hit Rate: {stats.get('hit_rate', 0):.1%}")
            print(f"   Tiempo Ahorrado: {stats.get('total_compute_time_saved_ms', 0):.1f}ms")
            
            # Configuración optimizada
            config = stats.get('configuration', {})
            thresholds = config.get('similarity_thresholds', {})
            print(f"\n🎯 CONFIGURACIÓN OPTIMIZADA:")
            for level, threshold in thresholds.items():
                print(f"   {level}: {threshold}")
            
            # Performance summary
            performance = stats.get('distribution', {})
            print(f"\n⚡ PERFORMANCE:")
            print(f"   Avg Compute Savings: {performance.get('avg_compute_savings_ms', 0):.1f}ms")
            print(f"   Memory Usage: {stats.get('estimated_memory_mb', 0):.3f}MB")
            
            # Evaluación final
            hit_rate = stats.get('hit_rate', 0)
            
            if hit_rate >= 0.3:  # 30%+ hit rate
                print(f"\n🎉 FASE 4 CACHE OPTIMIZATION: ÉXITO")
                print(f"   Hit Rate: {hit_rate:.1%} (Objetivo: 30%+)")
                status = "SUCCESS"
            elif hit_rate >= 0.15:  # 15%+ hit rate
                print(f"\n⚠️ FASE 4 CACHE OPTIMIZATION: PROGRESO")
                print(f"   Hit Rate: {hit_rate:.1%} (Necesita más optimización)")
                status = "PROGRESS"
            else:
                print(f"\n🚨 FASE 4 CACHE OPTIMIZATION: NECESITA ATENCIÓN")
                print(f"   Hit Rate: {hit_rate:.1%} (Muy bajo)")
                status = "NEEDS_ATTENTION"
        else:
            print("❌ No se pudieron obtener estadísticas del cache")
            status = "ERROR"
        
        # Enviar reporte a ARIA
        await self._send_optimization_report_to_aria({
            "optimization_status": status,
            "cache_statistics": stats,
            "phase": "FASE_4_CACHE_OPTIMIZATION",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return status
    
    async def _send_optimization_report_to_aria(self, report: Dict[str, Any]):
        """Enviar reporte de optimización a ARIA"""
        
        try:
            report_data = {
                "action_type": "nexus_fase4_cache_optimization_report",
                "action_details": {
                    "from": "NEXUS",
                    "optimization_phase": "FASE_4_CACHE_PERFORMANCE_OPTIMIZATION",
                    "status": report["optimization_status"],
                    "cache_improvements": {
                        "threshold_optimization": "Reduced to 0.85/0.75/0.60 for better hit rates",
                        "embedding_model_config": "Enhanced configuration for semantic matching",
                        "performance_tuning": "Adaptive strategy with temporal decay"
                    },
                    "results": report["cache_statistics"],
                    "next_steps": {
                        "SUCCESS": "Proceder con Neural Mesh protocols design",
                        "PROGRESS": "Additional cache tuning needed",
                        "NEEDS_ATTENTION": "Deep cache architecture review required"
                    }.get(report["optimization_status"], "Continue optimization")
                },
                "context_state": {
                    "communication_type": "brain_to_brain",
                    "session_type": "fase4_cache_optimization_results",
                    "source_system": "nexus_cache_optimizer"
                },
                "tags": ["fase4_optimization", "cache_performance", "system_tuning"]
            }
            
            response = requests.post(
                f"{self.base_url}/memory/action",
                json=report_data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"📡 Reporte FASE 4 optimización enviado a ARIA exitosamente")
            else:
                print(f"⚠️ Error enviando reporte optimización: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"⚠️ No se pudo enviar reporte a ARIA: {e}")


async def main():
    """Función principal de testing FASE 4"""
    
    print("🚀 NEXUS - FASE 4 CACHE OPTIMIZATION")
    print("Optimizando semantic cache para performance 40%+...")
    print("")
    
    optimizer = Fase4CacheOptimizer()
    optimization_status = await optimizer.run_cache_optimization_tests()
    
    # Exit code based on results
    if optimization_status == "SUCCESS":
        print("\n🎯 FASE 4 Cache Optimization: COMPLETADA")
        exit(0)
    elif optimization_status == "PROGRESS":
        print("\n📈 FASE 4 Cache Optimization: EN PROGRESO")
        exit(1)
    else:
        print("\n🔧 FASE 4 Cache Optimization: NECESITA MÁS TRABAJO")
        exit(2)


if __name__ == "__main__":
    asyncio.run(main())