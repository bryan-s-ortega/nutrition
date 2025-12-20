import requests

url = "http://localhost:8000/onboarding"
data = {
    "age": 30,
    "weight": 80,
    "height": 180,
    "gender": "male",
    "goal": "weight_loss",
    "activity_level": 1.2
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
