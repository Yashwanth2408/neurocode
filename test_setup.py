import ollama
import time

def test_neurocode_setup():
    """Test if Ollama and CodeLlama are working"""
    
    print("=" * 60)
    print("NEUROCODE - STEP 1 FINAL TEST")
    print("=" * 60)
    
    # Test code with multiple security vulnerabilities
    test_code = """
# Vulnerable Python code example
password = input("Enter password: ")
exec(password)  # Code injection vulnerability

user_input = request.args.get('id')
query = "SELECT * FROM users WHERE id = " + user_input  # SQL injection

eval(user_data)  # Arbitrary code execution

os.system("rm -rf " + filename)  # Command injection
"""
    
    print("\n📝 Analyzing Code for Security Vulnerabilities...")
    print(f"Test Code:\n{test_code}\n")
    
    # Start timer
    start_time = time.time()
    
    # Call Ollama CodeLlama model
    try:
        print("⏳ Calling CodeLlama 7B model...")
        response = ollama.generate(
            model='codellama:7b-instruct',
            prompt=f'''Analyze this Python code for security vulnerabilities.
List each vulnerability found with:
1. Vulnerability type
2. Line of code
3. Risk level (High/Medium/Low)
4. Fix recommendation

Code to analyze:
{test_code}
'''
        )
        
        elapsed = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS - NeuroCode AI is Working!")
        print("=" * 60)
        print(f"⏱️  Response Time: {elapsed:.2f} seconds")
        print(f"💾 Model: CodeLlama 7B Instruct")
        print(f"🔍 Security Analysis Results:\n")
        print(response['response'])
        print("\n" + "=" * 60)
        print("🎉 STEP 1 COMPLETE - Ready for Step 2!")
        print("=" * 60)
        print("\nNext: We'll integrate Semgrep + Bandit for multi-layer scanning")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n🔧 Troubleshooting Steps:")
        print("1. Is Terminal 1 still running 'ollama serve'?")
        print("2. Check: ollama list (should show codellama:7b-instruct)")
        print("3. Try: ollama run codellama:7b-instruct 'hello'")

if __name__ == "__main__":
    test_neurocode_setup()
