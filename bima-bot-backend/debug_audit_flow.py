import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def run_debug():
    print("1. Starting Audit...")
    try:
        resp = requests.post(f"{BASE_URL}/audit/start")
        if resp.status_code != 200:
            print(f"Failed to start: {resp.text}")
            return
        data = resp.json()
        audit_id = data["audit_id"]
        print(f"   Audit ID: {audit_id}")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    print("\n2. Triggering Completion...")
    try:
        # Trigger manually
        resp = requests.post(f"{BASE_URL}/audit/{audit_id}/complete")
        print(f"   Trigger Code: {resp.status_code}")
        print(f"   Response: {resp.text}")
    except Exception as e:
        print(f"Trigger failed: {e}")

    print("\n3. Polling Status...")
    for i in range(10):
        resp = requests.get(f"{BASE_URL}/audit/{audit_id}/status")
        status = resp.json().get("status")
        print(f"   Attempt {i+1}: Status = {status}")
        if status == "completed":
            print("\nSUCCESS: Audit Completed!")
            
            # Fetch result
            res_resp = requests.get(f"{BASE_URL}/audit/{audit_id}/result")
            print(f"   Result Flags: {len(res_resp.json().get('flags', []))}")
            return
        time.sleep(1)

    print("\nFAILURE: Timed out waiting for completion.")

if __name__ == "__main__":
    run_debug()
