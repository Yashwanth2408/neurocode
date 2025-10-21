from security_scanner import SecurityScanner
import time

def main():
    """Test the multi-layer security scanner"""
    
    # Vulnerable test code with multiple security issues
    vulnerable_code = """
import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Vulnerability 1: SQL Injection
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    query = "SELECT * FROM users WHERE id = " + user_id
    return execute_query(query)

# Vulnerability 2: Command Injection
@app.route('/ping')
def ping_server():
    host = request.args.get('host')
    result = os.system(f"ping -c 1 {host}")
    return str(result)

# Vulnerability 3: Code Injection
@app.route('/calc')
def calculate():
    expression = request.args.get('expr')
    result = eval(expression)
    return str(result)

# Vulnerability 4: Arbitrary Code Execution
@app.route('/execute')
def execute_code():
    code = request.args.get('code')
    exec(code)
    return "Executed"

# Vulnerability 5: Weak Crypto
def hash_password(password):
    import md5
    return md5.new(password).hexdigest()

# Vulnerability 6: Hardcoded Credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# Vulnerability 7: Path Traversal
@app.route('/file')
def read_file():
    filename = request.args.get('name')
    with open(f"/var/data/{filename}", 'r') as f:
        return f.read()

# Vulnerability 8: SSRF
@app.route('/fetch')
def fetch_url():
    import requests
    url = request.args.get('url')
    response = requests.get(url)
    return response.text
"""
    
    print("=" * 80)
    print("🚀 NEUROCODE - MULTI-LAYER SECURITY SCANNER TEST")
    print("=" * 80)
    print("\n📝 Test Code:")
    print("-" * 80)
    print(vulnerable_code[:300] + "...")
    print("-" * 80)
    
    # Initialize scanner
    scanner = SecurityScanner()
    
    # Run comprehensive scan
    start_time = time.time()
    results = scanner.comprehensive_scan(vulnerable_code, language="python")
    elapsed = time.time() - start_time
    
    # Print results
    scanner.print_results(results)
    
    # Performance metrics
    print(f"\n⏱️  Total Scan Time: {elapsed:.2f} seconds")
    print(f"📊 Scanners Used: Semgrep + Bandit + CodeLlama")
    
    # Success message
    print("\n" + "=" * 80)
    if results["total_issues"] > 0:
        print("✅ STEP 2 COMPLETE - Multi-Layer Scanner Working!")
    else:
        print("⚠️  Scanner working but no issues detected (check scanner config)")
    print("=" * 80)
    print("\n🎯 Next: Step 3 will build the GitHub/GitLab integration for PR reviews")

if __name__ == "__main__":
    main()
