import requests
import os

# You can set USDA_API_KEY env var before running this if you have one
# os.environ['USDA_API_KEY'] = 'YOUR_KEY_HERE' 

def verify_search():
    url = "http://localhost:8000/food/search"
    query = "snickers"
    
    print(f"Searching for '{query}'...")
    response = requests.get(url, params={"q": query})
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {len(data)} items.")
        for item in data[:3]:
            print(f"- [{item.get('source')}] {item.get('name')} ({item.get('calories')} kcal)")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    verify_search()
