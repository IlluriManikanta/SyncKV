import requests

BASE_URL = "http://localhost:8001"

headers = {"Content-Type": "application/json"}

def test_admin_view():
    print("Setting node view...")
    res = requests.put(f"{BASE_URL}/kvs/admin/view", json={"view": ["localhost:8001"]})
    print(res.status_code, res.json())

def test_put_key():
    print("Storing key 'greeting'...")
    res = requests.put(f"{BASE_URL}/kvs/data/greeting", json={"val": "hello", "causal-metadata": {}})
    print(res.status_code, res.json())
    return res.json().get("causal-metadata", {})

def test_get_key(metadata):
    print("Retrieving key 'greeting'...")
    res = requests.get(f"{BASE_URL}/kvs/data/greeting", json={"causal-metadata": metadata})
    print(res.status_code, res.json())

def test_delete_key(metadata):
    print("Deleting key 'greeting'...")
    res = requests.delete(f"{BASE_URL}/kvs/data/greeting", json={"causal-metadata": metadata})
    print(res.status_code, res.json())

def test_get_deleted_key(metadata):
    print("Trying to get deleted key 'greeting'...")
    res = requests.get(f"{BASE_URL}/kvs/data/greeting", json={"causal-metadata": metadata})
    print(res.status_code, res.json())

if __name__ == "__main__":
    test_admin_view()
    clock = test_put_key()
    test_get_key(clock)
    test_delete_key(clock)
    test_get_deleted_key(clock)