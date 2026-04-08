"""
Test script for JWT authentication endpoints
Executes all requests and saves results to a file
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
RESULTS_FILE = "jwt_requests_results.json"

# Test credentials
TEST_USERS = [
    {"username": "JaguarEW", "password": "password123"},
    {"username": "Jaguarking", "password": "password456"},
]

def log_result(action, method, endpoint, status_code, response_data, error=None):
    """Log request result"""
    result = {
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "method": method,
        "endpoint": endpoint,
        "status_code": status_code,
        "response": response_data,
        "error": error
    }
    print(f"\n{'='*60}")
    print(f"[{method}] {endpoint}")
    print(f"Status: {status_code}")
    print(f"Response: {json.dumps(response_data, indent=2)}")
    if error:
        print(f"Error: {error}")
    print(f"{'='*60}")
    
    return result

def test_jwt_endpoints():
    """Execute all JWT endpoint tests"""
    all_results = []
    tokens = {}
    
    print("\n" + "="*60)
    print("INICIANDO PRUEBAS DE JWT AUTHENTICATION")
    print("="*60)
    
    # Test 1: Login endpoint for each user
    print("\n1. PROBANDO LOGIN (POST /jwt-auth/token)")
    for user in TEST_USERS:
        try:
            response = requests.post(
                f"{BASE_URL}/jwt-auth/token",
                data=user
            )
            result_data = response.json() if response.status_code == 200 else {"error": response.text}
            
            result = log_result(
                "Login",
                "POST",
                f"/jwt-auth/token (user: {user['username']})",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
            # Save token for authenticated requests
            if response.status_code == 200:
                tokens[user['username']] = response.json()['access_token']
                
        except Exception as e:
            result = log_result(
                "Login",
                "POST",
                f"/jwt-auth/token (user: {user['username']})",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 2: Get current user info (/me)
    if tokens:
        print("\n2. PROBANDO GET CURRENT USER (GET /jwt-auth/me)")
        username = list(tokens.keys())[0]
        token = tokens[username]
        
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{BASE_URL}/jwt-auth/me",
                headers=headers
            )
            result_data = response.json() if response.status_code == 200 else {"error": response.text}
            
            result = log_result(
                "Get Current User",
                "GET",
                "/jwt-auth/me",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
        except Exception as e:
            result = log_result(
                "Get Current User",
                "GET",
                "/jwt-auth/me",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 3: Get other user info
    if tokens:
        print("\n3. PROBANDO GET OTHER USER (GET /jwt-auth/users/{username})")
        username = list(tokens.keys())[0]
        token = tokens[username]
        other_user = "Jaguarking" if username == "JaguarEW" else "JaguarEW"
        
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{BASE_URL}/jwt-auth/users/{other_user}",
                headers=headers
            )
            result_data = response.json() if response.status_code == 200 else {"error": response.text}
            
            result = log_result(
                "Get User Info",
                "GET",
                f"/jwt-auth/users/{other_user}",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
        except Exception as e:
            result = log_result(
                "Get User Info",
                "GET",
                f"/jwt-auth/users/{other_user}",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 4: Validate token
    if tokens:
        print("\n4. PROBANDO VALIDAR TOKEN (POST /jwt-auth/token/validate)")
        token = list(tokens.values())[0]
        
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(
                f"{BASE_URL}/jwt-auth/token/validate",
                headers=headers
            )
            result_data = response.json() if response.status_code == 200 else {"error": response.text}
            
            result = log_result(
                "Validate Token",
                "POST",
                "/jwt-auth/token/validate",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
        except Exception as e:
            result = log_result(
                "Validate Token",
                "POST",
                "/jwt-auth/token/validate",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 5: Invalid token (should fail)
    print("\n5. PROBANDO CON TOKEN INVÁLIDO (debe fallar)")
    try:
        headers = {"Authorization": "Bearer invalid_token_here"}
        response = requests.get(
            f"{BASE_URL}/jwt-auth/me",
            headers=headers
        )
        result_data = response.json() if response.status_code != 401 else {"error": "Unauthorized"}
        
        result = log_result(
            "Invalid Token Test",
            "GET",
            "/jwt-auth/me (with invalid token)",
            response.status_code,
            result_data
        )
        all_results.append(result)
        
    except Exception as e:
        result = log_result(
            "Invalid Token Test",
            "GET",
            "/jwt-auth/me (with invalid token)",
            0,
            None,
            str(e)
        )
        all_results.append(result)
    
    return all_results

def save_results(results):
    """Save results to JSON file"""
    with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Resultados guardados en: {RESULTS_FILE}")

if __name__ == "__main__":
    try:
        print("⏳ Conectando a servidor en", BASE_URL)
        results = test_jwt_endpoints()
        save_results(results)
        
        print("\n" + "="*60)
        print("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor.")
        print(f"   Asegúrate de que FastAPI esté ejecutándose en {BASE_URL}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
