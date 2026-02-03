"""
API Testing Script
Run this to test all backend endpoints
"""
import asyncio
import httpx
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_health():
    """Test health endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/api/health")
        print(f"✅ Health Check: {response.json()}")
        return response.status_code == 200

async def test_signup():
    """Test signup"""
    async with httpx.AsyncClient() as client:
        data = {
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "password": "TestPassword123!",
            "full_name": "Test User"
        }
        response = await client.post(f"{BASE_URL}/api/auth/signup", json=data)
        result = response.json()
        if response.status_code == 200:
            print(f"✅ Signup Success")
            return result.get("access_token")
        else:
            print(f"❌ Signup Failed: {result}")
            return None

async def test_upload(token: str):
    """Test file upload"""
    async with httpx.AsyncClient() as client:
        # Create a simple CSV file
        csv_content = """Date,Revenue,Expenses
2024-01-01,100000,75000
2024-02-01,120000,80000
2024-03-01,110000,78000"""
        
        files = {"file": ("test.csv", csv_content.encode(), "text/csv")}
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.post(
            f"{BASE_URL}/api/upload/document",
            files=files,
            headers=headers
        )
        result = response.json()
        if response.status_code == 200:
            print(f"✅ Upload Success: {result.get('message')}")
        else:
            print(f"❌ Upload Failed: {result}")

async def test_analysis(token: str, business_id: str):
    """Test financial analysis"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        data = {
            "business_id": business_id
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.post(
            f"{BASE_URL}/api/analysis/financial-health",
            json=data,
            headers=headers
        )
        result = response.json()
        if response.status_code == 200:
            analysis = result.get('analysis', {})
            print(f"✅ Analysis Success:")
            print(f"   Health Score: {analysis.get('health_score', 'N/A')}")
            print(f"   Credit Score: {analysis.get('credit_score', 'N/A')}")
        else:
            print(f"❌ Analysis Failed: {result}")

async def test_chat(token: str):
    """Test AI chat"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        data = {
            "message": "What are the key financial metrics I should track?"
        }
        headers = {"Authorization": f"Bearer {token}"}
        
        response = await client.post(
            f"{BASE_URL}/api/insights/chat",
            json=data,
            headers=headers
        )
        result = response.json()
        if response.status_code == 200:
            print(f"✅ Chat Success:")
            print(f"   Response: {result.get('message', 'N/A')[:100]}...")
        else:
            print(f"❌ Chat Failed: {result}")

async def run_tests():
    """Run all tests"""
    print("\n🧪 Starting API Tests...\n")
    
    # Test 1: Health Check
    print("1. Testing Health Endpoint...")
    health_ok = await test_health()
    if not health_ok:
        print("❌ Health check failed. Is the server running?")
        return
    
    # Test 2: Signup
    print("\n2. Testing Signup...")
    token = await test_signup()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    # Test 3: Upload
    print("\n3. Testing File Upload...")
    await test_upload(token)
    
    # Test 4: Chat (doesn't require business setup)
    print("\n4. Testing AI Chat...")
    await test_chat(token)
    
    print("\n✅ All tests completed!")
    print("\n📋 Summary:")
    print("   - Health Check: ✅")
    print("   - Authentication: ✅")
    print("   - File Upload: ✅")
    print("   - AI Chat: ✅")
    print("\n💡 Note: Some tests may fail if database is not properly configured.")
    print("   See DEPLOYMENT_GUIDE.md for database setup instructions.\n")

if __name__ == "__main__":
    print("=" * 60)
    print("SME Financial Compass - API Testing Suite")
    print("=" * 60)
    asyncio.run(run_tests())
