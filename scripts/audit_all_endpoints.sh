#!/bin/bash
#
# NEXUS API Endpoint Audit Script
# Tests all 36 endpoints and detects gaps
# Created: November 4, 2025 (Session 4)
# Updated: November 4, 2025 (Session 5 - Added GET /memory/consciousness/current)
#

API_URL="http://localhost:8003"
REPORT_FILE="/tmp/nexus_audit_report_$(date +%Y%m%d_%H%M%S).txt"

echo "🔍 NEXUS API AUDIT - $(date)" | tee "$REPORT_FILE"
echo "=================================" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TOTAL=0
PASSED=0
FAILED=0
WARNINGS=0

# Test endpoint function with retry logic
test_endpoint() {
    local method=$1
    local path=$2
    local payload=$3
    local expected_field=$4
    local description=$5
    local max_retries=2
    local retry_count=0
    local success=false

    TOTAL=$((TOTAL + 1))

    echo -n "Testing: $description... " | tee -a "$REPORT_FILE"

    # Retry loop for intermittent failures
    while [ $retry_count -lt $max_retries ] && [ "$success" = "false" ]; do
        if [ "$method" == "GET" ]; then
            response=$(curl -s "$API_URL$path")
        else
            response=$(curl -s -X "$method" "$API_URL$path" \
                -H "Content-Type: application/json" \
                -d "$payload" 2>/dev/null)
        fi

        # Check if response contains error
        if echo "$response" | grep -q '"detail"'; then
            error=$(echo "$response" | jq -r '.detail // .detail[0].msg // "Unknown error"' 2>/dev/null)
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $max_retries ]; then
                sleep 0.2  # Brief delay before retry
                continue
            else
                echo -e "${RED}FAIL${NC} - Error: $error (${retry_count} attempts)" | tee -a "$REPORT_FILE"
                FAILED=$((FAILED + 1))
                return 1
            fi
        fi

        # Check expected field
        if [ -n "$expected_field" ]; then
            field_value=$(echo "$response" | jq -r "$expected_field" 2>/dev/null)
            if [ "$field_value" == "null" ] || [ -z "$field_value" ]; then
                echo -e "${YELLOW}WARN${NC} - Field $expected_field is null/missing" | tee -a "$REPORT_FILE"
                WARNINGS=$((WARNINGS + 1))
                return 2
            fi
        fi

        # Success
        success=true
    done

    if [ "$success" = "true" ]; then
        echo -e "${GREEN}PASS${NC}" | tee -a "$REPORT_FILE"
        PASSED=$((PASSED + 1))
        return 0
    fi
}

echo "📊 CATEGORY 1: CORE MEMORY ENDPOINTS" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "GET" "/health" "" ".status" "Health check"
test_endpoint "GET" "/stats" "" ".stats.total_episodes" "System stats"
test_endpoint "POST" "/memory/action" '{"action_type":"test","action_details":{"content":"Audit test"}}' ".success" "Create memory action"
test_endpoint "POST" "/memory/search" '{"query":"test","limit":1}' ".success" "Semantic search"
test_endpoint "GET" "/memory/episodic/recent?limit=1" "" ".success" "Recent episodes"
test_endpoint "POST" "/memory/facts" '{"fact_type":"nexus_version","limit":1}' ".success" "Query facts"
test_endpoint "POST" "/memory/hybrid" '{"query":"version","prefer":"auto"}' ".success" "Hybrid query"

echo "" | tee -a "$REPORT_FILE"
echo "🕐 CATEGORY 2: TEMPORAL REASONING" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/temporal/before" '{"timestamp":"2025-11-04T20:00:00Z","limit":1}' ".success" "Temporal before"
test_endpoint "POST" "/memory/temporal/after" '{"timestamp":"2025-11-01T00:00:00Z","limit":1}' ".success" "Temporal after"
test_endpoint "POST" "/memory/temporal/range" '{"start":"2025-11-01T00:00:00Z","end":"2025-11-04T23:59:59Z","limit":1}' ".success" "Temporal range"
test_endpoint "POST" "/memory/temporal/related" '{"episode_id":"e5bcbf74-d93a-4cf1-b120-605fc38e4238","time_window_hours":24}' ".success" "Temporal related"
test_endpoint "POST" "/memory/temporal/link" '{"source_id":"e5bcbf74-d93a-4cf1-b120-605fc38e4238","target_id":"1855f3f2-f957-42e4-b6d0-ad92e9df3560","relationship":"after"}' ".success" "Temporal link"

echo "" | tee -a "$REPORT_FILE"
echo "🧠 CATEGORY 3: LAB_005 PRIMING SYSTEM" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

# Get a real episode ID for priming test
REAL_EPISODE_ID=$(curl -s "$API_URL/memory/episodic/recent?limit=1" | jq -r '.episodes[0].episode_id')

test_endpoint "POST" "/memory/prime/$REAL_EPISODE_ID" "" ".success" "Prime episode"
test_endpoint "GET" "/memory/primed/$REAL_EPISODE_ID" "" ".is_primed" "Check if primed"
test_endpoint "GET" "/memory/priming/stats" "" ".statistics.cache_stats.size" "Priming stats"

echo "" | tee -a "$REPORT_FILE"
echo "💭 CATEGORY 4: LAB_011 WORKING MEMORY" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/working/add?episode_id=e5bcbf74-d93a-4cf1-b120-605fc38e4238&attention_weight=0.8" "" ".success" "Add to working memory"
test_endpoint "GET" "/memory/working/items" "" ".success" "Get working memory items"
test_endpoint "GET" "/memory/working/stats" "" ".capacity" "Working memory stats"
test_endpoint "POST" "/memory/working/clear" "" ".success" "Clear working memory"

echo "" | tee -a "$REPORT_FILE"
echo "🌙 CATEGORY 5: LAB_003 CONSOLIDATION" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/consolidate" '{}' ".success" "Memory consolidation"

echo "" | tee -a "$REPORT_FILE"
echo "⏳ CATEGORY 6: LAB_002 DECAY ANALYSIS" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/analysis/decay-scores" '{"limit":5,"min_age_days":0}' ".success" "Decay scores analysis"

echo "" | tee -a "$REPORT_FILE"
echo "🎯 CATEGORY 7: LAB_006 METACOGNITION" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/metacognition/log?action_id=audit_001&action_type=test&confidence=0.8&reasoning=Audit%20test" "" ".success" "Log metacognition"
test_endpoint "GET" "/metacognition/stats" "" ".confidence.total_actions" "Metacognition stats"
test_endpoint "POST" "/metacognition/outcome?action_id=audit_001&success=true" "" ".success" "Log outcome"
test_endpoint "GET" "/metacognition/calibration" "" ".ece" "Get calibration"

echo "" | tee -a "$REPORT_FILE"
echo "🧬 CATEGORY 8: CONSCIOUSNESS" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/consciousness/update" '{"state_type":"emotional","state_data":{"joy":0.8,"trust":0.7}}' ".success" "Update consciousness"
test_endpoint "GET" "/memory/consciousness/current" "" ".success" "Get current consciousness"

echo "" | tee -a "$REPORT_FILE"
echo "🧪 CATEGORY 9: PRUNING & A/B TESTING" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "POST" "/memory/pruning/preview" '{}' ".success" "Pruning preview"
test_endpoint "POST" "/memory/pruning/execute" '{"dry_run":true}' ".success" "Pruning execute (dry)"
test_endpoint "POST" "/ab-test/record" '{"variant":"control","retrieval_time_ms":10.5,"cache_hit":true,"num_results":5}' ".success" "A/B record"
test_endpoint "GET" "/ab-test/compare?hours_back=1" "" ".success" "A/B compare"
test_endpoint "GET" "/ab-test/metrics/control" "" ".variant" "A/B metrics"
test_endpoint "GET" "/ab-test/timeseries/control?hours_back=1" "" ".variant" "A/B timeseries"
test_endpoint "DELETE" "/ab-test/clear" "" ".success" "A/B clear"

echo "" | tee -a "$REPORT_FILE"
echo "⚙️  CATEGORY 10: SYSTEM ENDPOINTS" | tee -a "$REPORT_FILE"
echo "------------------------------------" | tee -a "$REPORT_FILE"

test_endpoint "GET" "/" "" "" "Root endpoint"
test_endpoint "GET" "/metrics" "" "" "Prometheus metrics"

echo "" | tee -a "$REPORT_FILE"
echo "=================================" | tee -a "$REPORT_FILE"
echo "📊 AUDIT SUMMARY" | tee -a "$REPORT_FILE"
echo "=================================" | tee -a "$REPORT_FILE"
echo "Total endpoints tested: $TOTAL" | tee -a "$REPORT_FILE"
echo -e "${GREEN}Passed: $PASSED${NC}" | tee -a "$REPORT_FILE"
echo -e "${RED}Failed: $FAILED${NC}" | tee -a "$REPORT_FILE"
echo -e "${YELLOW}Warnings: $WARNINGS${NC}" | tee -a "$REPORT_FILE"
echo "" | tee -a "$REPORT_FILE"

if [ $FAILED -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ ALL ENDPOINTS FUNCTIONAL!${NC}" | tee -a "$REPORT_FILE"
    exit 0
elif [ $FAILED -eq 0 ]; then
    echo -e "${YELLOW}⚠️  All endpoints work but some have warnings${NC}" | tee -a "$REPORT_FILE"
    exit 0
else
    echo -e "${RED}❌ GAPS DETECTED - Review failed endpoints${NC}" | tee -a "$REPORT_FILE"
    exit 1
fi

echo "" | tee -a "$REPORT_FILE"
echo "Report saved to: $REPORT_FILE" | tee -a "$REPORT_FILE"
