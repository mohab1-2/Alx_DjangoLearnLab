#!/usr/bin/env python3
"""
Simple test script for the social media API endpoints
Run this after starting the Django development server
"""

import requests
import json

BASE_URL = 'http://localhost:8000/api/accounts'

def test_registration():
    """Test user registration endpoint"""
    print("Testing user registration...")
    
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User',
        'bio': 'This is a test user'
    }
    
    response = requests.post(f'{BASE_URL}/register/', json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token') if response.status_code == 201 else None

def test_login():
    """Test user login endpoint"""
    print("\nTesting user login...")
    
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    response = requests.post(f'{BASE_URL}/login/', json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json().get('token') if response.status_code == 200 else None

def test_profile(token):
    """Test profile endpoint with authentication"""
    print("\nTesting profile endpoint...")
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/profile/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_user_detail(token):
    """Test user detail endpoint"""
    print("\nTesting user detail endpoint...")
    
    headers = {'Authorization': f'Token {token}'}
    response = requests.get(f'{BASE_URL}/user/testuser/', headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def main():
    print("=== Social Media API Test ===\n")
    
    # Test registration
    token = test_registration()
    
    if token:
        print(f"\n✅ Registration successful! Token: {token[:20]}...")
        
        # Test login
        login_token = test_login()
        if login_token:
            print(f"✅ Login successful! Token: {login_token[:20]}...")
            
            # Test profile
            test_profile(login_token)
            
            # Test user detail
            test_user_detail(login_token)
        else:
            print("❌ Login failed!")
    else:
        print("❌ Registration failed!")

if __name__ == '__main__':
    main()
