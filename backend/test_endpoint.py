import requests
import sys

try:
    print("Testing /api/chat/check/ endpoint...")
    response = requests.post('http://127.0.0.1:8000/api/chat/check/', 
                            json={'sid': 'test', 'rid': 'test2'})
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Also test if the endpoint is registered in BluePrint correctly
    print("\nTesting Blueprint router check endpoint...")
    response = requests.post('http://127.0.0.1:8000/check/', 
                            json={'sid': 'test', 'rid': 'test2'})
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error testing endpoint: {e}")
    sys.exit(1) 