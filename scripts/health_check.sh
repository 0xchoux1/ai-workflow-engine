#!/bin/bash
# Health check script for all services

set -e

echo "=== Service Health Check ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

check_service() {
    local name=$1
    local url=$2
    local expected_codes=$3
    
    echo -n "Checking $name... "
    http_code=$(curl -L -s -o /dev/null -w "%{http_code}" "$url" || echo "000")
    
    if [[ $expected_codes == *"$http_code"* ]]; then
        echo -e "${GREEN}✓${NC} HTTP $http_code"
        return 0
    else
        echo -e "${RED}✗${NC} HTTP $http_code (expected: $expected_codes)"
        return 1
    fi
}

# Check all services
failed=0

check_service "n8n" "http://localhost:5678" "200 401" || ((failed++))
check_service "Dify Web" "http://localhost:3000" "200" || ((failed++))
check_service "Dify API" "http://localhost:5001" "200 404" || ((failed++))
check_service "Weaviate Ready" "http://localhost:8080/v1/.well-known/ready" "200" || ((failed++))
check_service "Weaviate Meta" "http://localhost:8080/v1/meta" "200" || ((failed++))

echo ""
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}All services are healthy!${NC}"
    exit 0
else
    echo -e "${RED}$failed service(s) failed health check${NC}"
    exit 1
fi
