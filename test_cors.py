"""
Quick CORS test script to verify API connectivity from different origins
"""

import requests
import json

def test_cors():
    """Test CORS configuration"""
    api_url = "https://swarm-api-smzv.onrender.com"
    test_key = "biobot-alpha-2025-xk9f"
    
    headers = {
        "Authorization": f"Bearer {test_key}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:8888"  # Simulate request from local server
    }
    
    print("🧪 Testing CORS Configuration...")
    print(f"🌐 API URL: {api_url}")
    print(f"🔑 Test Key: {test_key}")
    print(f"📡 Origin: {headers['Origin']}")
    print("=" * 50)
    
    try:
        # Test auth endpoint
        print("1. Testing /auth/info endpoint...")
        response = requests.get(f"{api_url}/auth/info", headers=headers)
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"     {header}: {value}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {data['api_key_name']}")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
    
    print("\n" + "=" * 50)
    
    try:
        # Test swarms endpoint
        print("2. Testing /swarms endpoint...")
        response = requests.get(f"{api_url}/swarms", headers=headers)
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: Found {len(data)} swarms")
        else:
            print(f"   ❌ Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

    print("\n🏁 CORS test completed!")

if __name__ == "__main__":
    test_cors()