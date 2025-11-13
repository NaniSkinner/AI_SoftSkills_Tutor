#!/bin/bash

# Deployment Diagnostic Script
# Run this to check if your Render deployment is working

echo "=========================================="
echo "Flourish Skills Tracker - Deployment Test"
echo "=========================================="
echo ""

# Test backend health
echo "1. Testing Backend Health..."
echo "URL: https://flourish-skills-backend.onrender.com/health"
HEALTH=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "https://flourish-skills-backend.onrender.com/health" 2>&1)
HTTP_CODE=$(echo "$HEALTH" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE=$(echo "$HEALTH" | grep -v "HTTP_STATUS")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Backend Health: OK"
    echo "Response: $RESPONSE"
else
    echo "❌ Backend Health: FAILED (HTTP $HTTP_CODE)"
    echo "Response: $RESPONSE"
fi
echo ""

# Test backend root
echo "2. Testing Backend Root..."
echo "URL: https://flourish-skills-backend.onrender.com/"
ROOT=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "https://flourish-skills-backend.onrender.com/" 2>&1)
HTTP_CODE=$(echo "$ROOT" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE=$(echo "$ROOT" | grep -v "HTTP_STATUS")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Backend Root: OK"
    echo "Response: $RESPONSE"
else
    echo "❌ Backend Root: FAILED (HTTP $HTTP_CODE)"
    echo "Response: $RESPONSE"
fi
echo ""

# Test students endpoint
echo "3. Testing Students API..."
echo "URL: https://flourish-skills-backend.onrender.com/api/students/"
STUDENTS=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "https://flourish-skills-backend.onrender.com/api/students/" 2>&1)
HTTP_CODE=$(echo "$STUDENTS" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE=$(echo "$STUDENTS" | grep -v "HTTP_STATUS")

if [ "$HTTP_CODE" = "200" ]; then
    # Count students in response
    STUDENT_COUNT=$(echo "$RESPONSE" | grep -o '"id"' | wc -l | xargs)
    echo "✅ Students API: OK ($STUDENT_COUNT students found)"
    echo "Response: $RESPONSE"
else
    echo "❌ Students API: FAILED (HTTP $HTTP_CODE)"
    echo "Response: $RESPONSE"
fi
echo ""

# Test frontend
echo "4. Testing Frontend..."
echo "URL: https://flourish-skills-frontend.onrender.com"
FRONTEND=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "https://flourish-skills-frontend.onrender.com" 2>&1)
HTTP_CODE=$(echo "$FRONTEND" | grep "HTTP_STATUS" | cut -d: -f2)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: FAILED (HTTP $HTTP_CODE)"
    echo "Response (first 500 chars):"
    echo "$FRONTEND" | grep -v "HTTP_STATUS" | head -c 500
fi
echo ""

# Test API docs
echo "5. Testing API Documentation..."
echo "URL: https://flourish-skills-backend.onrender.com/docs"
DOCS=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "https://flourish-skills-backend.onrender.com/docs" 2>&1)
HTTP_CODE=$(echo "$DOCS" | grep "HTTP_STATUS" | cut -d: -f2)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ API Docs: OK"
    echo "You can view the API docs at: https://flourish-skills-backend.onrender.com/docs"
else
    echo "❌ API Docs: FAILED (HTTP $HTTP_CODE)"
fi
echo ""

echo "=========================================="
echo "Summary:"
echo "=========================================="
echo "If all tests pass with ✅, your deployment is working!"
echo "If you see ❌, check the Render logs for that service."
echo ""
echo "Next steps:"
echo "1. If backend is OK but students = 0: Run data initialization"
echo "2. If backend fails: Check Render backend logs"
echo "3. If frontend fails: Check Render frontend logs"
echo ""
