#!/bin/bash
# NEXUS Distributed Architecture - Phase 1 Simple Test
# Quick validation of multi-instance deployment

set -e

echo "==========================================="
echo "NEXUS Distributed - Phase 1 Simple Test"
echo "==========================================="
echo ""

cd /mnt/d/01_PROYECTOS_ACTIVOS/CEREBRO_NEXUS_V3.0.0

# Stop any existing instance
echo "1. Cleanup..."
docker compose -f docker-compose.distributed.yml down 2>/dev/null || true
echo "✅ Cleanup complete"
echo ""

# Build
echo "2. Building..."
docker compose -f docker-compose.distributed.yml build --quiet
echo "✅ Build complete"
echo ""

# Start
echo "3. Starting services..."
docker compose -f docker-compose.distributed.yml up -d
echo "✅ Services started"
echo ""

# Wait for health
echo "4. Waiting for system to be healthy (60s max)..."
for i in {1..30}; do
    if curl -s http://localhost:18000/health > /dev/null 2>&1; then
        echo "✅ System healthy after $((i*2))s"
        break
    fi
    echo -n "."
    sleep 2
done
echo ""
echo ""

# Test health from multiple requests
echo "5. Testing load balancer distribution (10 requests)..."
for i in {1..10}; do
    RESPONSE=$(curl -s http://localhost:18000/health 2>/dev/null)
    INSTANCE=$(echo "$RESPONSE" | jq -r '.instance_id' 2>/dev/null || echo "unknown")
    STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null || echo "unknown")
    echo "Request $i: $STATUS from $INSTANCE"
    sleep 0.1
done
echo ""

# Test failover
echo "6. Testing failover (stopping replica-1)..."
docker stop nexus-api-1
echo "Replica-1 stopped. Waiting 5s..."
sleep 5

echo "Testing if system still responds (should use replica-2 or replica-3)..."
for i in {1..5}; do
    RESPONSE=$(curl -s http://localhost:18000/health 2>/dev/null)
    if [ $? -eq 0 ]; then
        INSTANCE=$(echo "$RESPONSE" | jq -r '.instance_id' 2>/dev/null || echo "unknown")
        STATUS=$(echo "$RESPONSE" | jq -r '.status' 2>/dev/null || echo "unknown")
        echo "Failover test $i: $STATUS from $INSTANCE"
    else
        echo "❌ Request failed (system down)"
    fi
    sleep 0.5
done
echo ""

# Restart replica-1
echo "7. Restarting replica-1..."
docker start nexus-api-1
echo "Waiting 10s for replica to rejoin..."
sleep 10

for i in {1..5}; do
    RESPONSE=$(curl -s http://localhost:18000/health 2>/dev/null)
    INSTANCE=$(echo "$RESPONSE" | jq -r '.instance_id' 2>/dev/null || echo "unknown")
    echo "Recovery test $i: from $INSTANCE"
    sleep 0.3
done
echo ""

# Final status
echo "8. Final status:"
docker compose -f docker-compose.distributed.yml ps
echo ""

echo "==========================================="
echo "✅ PHASE 1 TEST COMPLETE"
echo "==========================================="
echo ""
echo "To view logs:"
echo "  docker compose -f docker-compose.distributed.yml logs -f"
echo ""
echo "To stop:"
echo "  docker compose -f docker-compose.distributed.yml down"
echo ""
