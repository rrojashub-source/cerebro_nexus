@echo off
REM ====================================
REM REINICIAR ARIA CEREBRO COMPLETO
REM Desde nueva ubicación D:\01_PROYECTOS_ACTIVOS
REM ====================================

echo 🧠 REINICIANDO ARIA CEREBRO COMPLETO...
echo.

cd "D:\01_PROYECTOS_ACTIVOS\ARIA_CEREBRO_COMPLETO\03_DEPLOYMENT_PRODUCTIVO"

echo 📋 Verificando estado actual...
docker-compose ps

echo.
echo 🔄 Deteniendo servicios existentes...
docker-compose down

echo.
echo 🚀 Iniciando servicios ARIA...
docker-compose up -d

echo.
echo ⏳ Esperando 10 segundos para que los servicios inicien...
timeout /t 10 /nobreak

echo.
echo 📊 Estado de servicios:
docker-compose ps

echo.
echo 🔍 Verificando API:
curl http://localhost:8001/health

echo.
echo 📚 Verificando recuerdos recientes:
curl "http://localhost:8001/memory/episodic/recent?limit=3"

echo.
echo ✅ ARIA reiniciado. 
echo.
echo VERIFICAR:
echo - API responde en http://localhost:8001
echo - PostgreSQL tiene volumen correcto montado
echo - Los recuerdos están disponibles
echo.
pause