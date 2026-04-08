"""
Test script for creating users in MongoDB via API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
RESULTS_FILE = "mongodb_users_results.json"

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
    print(f"Response: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
    if error:
        print(f"Error: {error}")
    print(f"{'='*60}")
    
    return result

def test_user_endpoints():
    """Test user CRUD endpoints with MongoDB"""
    all_results = []
    created_users = {}
    
    print("\n" + "="*60)
    print("INICIANDO PRUEBAS DE USUARIOS CON MONGODB")
    print("="*60)
    
    # Test 1: Get all users
    print("\n1. OBTENIENDO TODOS LOS USUARIOS (GET /users)")
    try:
        response = requests.get(f"{BASE_URL}/users")
        result_data = response.json()
        
        result = log_result(
            "Get All Users",
            "GET",
            "/users",
            response.status_code,
            result_data
        )
        all_results.append(result)
        
    except Exception as e:
        result = log_result(
            "Get All Users",
            "GET",
            "/users",
            0,
            None,
            str(e)
        )
        all_results.append(result)
    
    # Test 2: Create new users
    new_users = [
        {"name": "Alejandro Lanchimba", "email": "alejandro.lanchimba@example.com"},
        {"name": "Jorge Vivas", "email": "jorge.vivas@example.com"},
        {"name": "Ana García", "email": "ana.garcia@example.com"},
        {"name": "Carlos López", "email": "carlos.lopez@example.com"},
    ]
    
    print("\n2. CREANDO NUEVOS USUARIOS (POST /users/)")
    for user_data in new_users:
        try:
            response = requests.post(
                f"{BASE_URL}/users/",
                json=user_data
            )
            result_data = response.json()
            
            result = log_result(
                "Create User",
                "POST",
                f"/users/ (user: {user_data['name']})",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
            # Save user ID for later tests
            if response.status_code == 201:
                created_users[user_data['email']] = result_data.get('id') or result_data.get('_id')
                
        except Exception as e:
            result = log_result(
                "Create User",
                "POST",
                f"/users/ (user: {user_data['name']})",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 3: Try to create duplicate user (should fail)
    print("\n3. INTENTANDO CREAR USUARIO DUPLICADO (debe fallar)")
    try:
        response = requests.post(
            f"{BASE_URL}/users/",
            json=new_users[0]
        )
        result_data = response.json()
        
        result = log_result(
            "Duplicate User Test",
            "POST",
            "/users/ (duplicate)",
            response.status_code,
            result_data
        )
        all_results.append(result)
        
    except Exception as e:
        result = log_result(
            "Duplicate User Test",
            "POST",
            "/users/ (duplicate)",
            0,
            None,
            str(e)
        )
        all_results.append(result)
    
    # Test 4: Get user by ID
    if created_users:
        user_id = list(created_users.values())[0]
        print(f"\n4. OBTENIENDO USUARIO POR ID (GET /users/{user_id})")
        try:
            response = requests.get(f"{BASE_URL}/users/{user_id}")
            result_data = response.json()
            
            result = log_result(
                "Get User by ID",
                "GET",
                f"/users/{user_id}",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
        except Exception as e:
            result = log_result(
                "Get User by ID",
                "GET",
                f"/users/{user_id}",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 5: Search user by name
    print("\n5. BUSCANDO USUARIO POR NOMBRE (GET /usersquery/)")
    try:
        response = requests.get(
            f"{BASE_URL}/usersquery/",
            params={"name": new_users[0]['name']}
        )
        result_data = response.json()
        
        result = log_result(
            "Search User by Name",
            "GET",
            f"/usersquery/?name={new_users[0]['name']}",
            response.status_code,
            result_data
        )
        all_results.append(result)
        
    except Exception as e:
        result = log_result(
            "Search User by Name",
            "GET",
            f"/usersquery/?name={new_users[0]['name']}",
            0,
            None,
            str(e)
        )
        all_results.append(result)
    
    # Test 6: Update user
    if created_users:
        user_id = list(created_users.values())[0]
        updated_data = {"name": "Alejandro Lanchimba (updated)", "email": "alejandro.updated@example.com"}
        print(f"\n6. ACTUALIZANDO USUARIO (PUT /users/{user_id})")
        try:
            response = requests.put(
                f"{BASE_URL}/users/{user_id}",
                json=updated_data
            )
            result_data = response.json()
            
            result = log_result(
                "Update User",
                "PUT",
                f"/users/{user_id}",
                response.status_code,
                result_data
            )
            all_results.append(result)
            
        except Exception as e:
            result = log_result(
                "Update User",
                "PUT",
                f"/users/{user_id}",
                0,
                None,
                str(e)
            )
            all_results.append(result)
    
    # Test 7: Get all users after operations
    print("\n7. OBTENIENDO TODOS LOS USUARIOS (DESPUÉS DE OPERACIONES)")
    try:
        response = requests.get(f"{BASE_URL}/users")
        result_data = response.json()
        
        result = log_result(
            "Get All Users (Final)",
            "GET",
            "/users",
            response.status_code,
            result_data
        )
        all_results.append(result)
        
    except Exception as e:
        result = log_result(
            "Get All Users (Final)",
            "GET",
            "/users",
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
        results = test_user_endpoints()
        save_results(results)
        
        print("\n" + "="*60)
        print("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor.")
        print(f"   Asegúrate de que FastAPI esté ejecutándose en {BASE_URL}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
