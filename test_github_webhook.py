import requests
import json
import hmac
import hashlib

def test_github_webhook_locally():
    """Test GitHub webhook endpoint locally"""
    
    # Simulated GitHub PR webhook payload
    payload = {
        "action": "opened",
        "pull_request": {
            "number": 1,
            "head": {
                "sha": "abc123def456"
            },
            "base": {
                "ref": "main"
            }
        },
        "repository": {
            "full_name": "test-user/test-repo"
        }
    }
    
    # Convert to JSON
    payload_json = json.dumps(payload)
    
    # Optional: Generate signature (if webhook secret is set)
    webhook_secret = "test-secret-123"  # Change this to your actual secret
    signature = hmac.new(
        webhook_secret.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": f"sha256={signature}"
    }
    
    # Send request to local server
    url = "http://localhost:8000/webhook/github"
    
    print("=" * 60)
    print("🧪 Testing GitHub Webhook Endpoint")
    print("=" * 60)
    print(f"URL: {url}")
    print(f"Event: pull_request (opened)")
    print(f"PR Number: {payload['pull_request']['number']}")
    print(f"Repository: {payload['repository']['full_name']}")
    print("=" * 60)
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📄 Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Webhook test PASSED!")
            print("💡 Note: Actual scanning requires GitHub token and valid repo access")
        else:
            print(f"\n⚠️  Unexpected status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to NeuroCode API")
        print("Make sure the API server is running: python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    test_github_webhook_locally()
