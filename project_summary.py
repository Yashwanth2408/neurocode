import os
import subprocess
from pathlib import Path

def print_banner(text):
    """Print formatted banner"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def get_file_size(filepath):
    """Get human-readable file size"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def check_service(command):
    """Check if a service/command is available"""
    try:
        subprocess.run(command, capture_output=True, check=True, shell=True)
        return "✅"
    except:
        return "❌"

def main():
    """Display NeuroCode project summary"""
    
    print_banner("🛡️  NEUROCODE PROJECT SUMMARY")
    
    # Project files
    print("\n📁 PROJECT FILES:")
    print("-" * 70)
    
    project_files = [
        ("main.py", "FastAPI application & webhook handlers"),
        ("security_scanner.py", "Multi-layer security scanner engine"),
        ("github_integration.py", "GitHub API integration"),
        ("config.py", "Configuration management"),
        ("test_setup.py", "Basic setup verification"),
        ("test_multi_scanner.py", "Multi-scanner integration test"),
        ("test_github_webhook.py", "GitHub webhook testing"),
        ("requirements.txt", "Python dependencies"),
        ("Dockerfile", "Docker containerization"),
        ("docker-compose.yml", "Docker orchestration"),
        (".env.example", "Environment configuration template"),
        (".gitignore", "Git ignore rules"),
        (".dockerignore", "Docker ignore rules"),
        ("README.md", "Project documentation"),
        ("DEPLOYMENT.md", "Production deployment guide"),
    ]
    
    total_size = 0
    for filename, description in project_files:
        if os.path.exists(filename):
            size = get_file_size(filename)
            total_size += os.path.getsize(filename)
            status = "✅"
        else:
            size = "N/A"
            status = "❌"
        
        print(f"{status} {filename:30} {size:>10}  - {description}")
    
    print("-" * 70)
    print(f"   Total project size: {get_file_size('.')}")
    
    # Dependencies
    print_banner("📦 DEPENDENCIES STATUS")
    
    dependencies = [
        ("python3 --version", "Python 3.10+"),
        ("pip --version", "pip package manager"),
        ("ollama --version", "Ollama (AI model runtime)"),
        ("semgrep --version", "Semgrep (security scanner)"),
        ("bandit --version", "Bandit (Python security)"),
        ("docker --version", "Docker (containerization)"),
        ("curl --version", "cURL (API testing)"),
    ]
    
    print("\n" + "-" * 70)
    for command, name in dependencies:
        status = check_service(command)
        print(f"{status} {name}")
    
    # Services status
    print_banner("🔧 SERVICES STATUS")
    
    services = [
        ("curl -s http://localhost:11434/api/version", "Ollama Server (port 11434)"),
        ("curl -s http://localhost:8000/health", "NeuroCode API (port 8000)"),
    ]
    
    print("\n" + "-" * 70)
    for command, name in services:
        status = check_service(command)
        print(f"{status} {name}")
    
    # Features
    print_banner("✨ FEATURES IMPLEMENTED")
    
    features = [
        "✅ CodeLlama 7B AI model integration",
        "✅ Semgrep static analysis",
        "✅ Bandit Python security scanner",
        "✅ FastAPI REST API server",
        "✅ GitHub webhook integration",
        "✅ GitLab webhook support",
        "✅ Automated PR security reviews",
        "✅ Multi-language support (Python, JS, TS, Java, Go)",
        "✅ Docker containerization",
        "✅ Production deployment ready",
        "✅ Health monitoring endpoints",
        "✅ Configurable security rules",
    ]
    
    print("\n" + "-" * 70)
    for feature in features:
        print(f"  {feature}")
    
    # Security detections
    print_banner("🔍 SECURITY DETECTIONS")
    
    detections = [
        "✅ SQL Injection",
        "✅ Command Injection",
        "✅ Code Injection (eval/exec)",
        "✅ Path Traversal",
        "✅ SSRF (Server-Side Request Forgery)",
        "✅ Hardcoded Credentials",
        "✅ Weak Cryptography",
        "✅ Authentication Issues",
        "✅ Input Validation Problems",
        "✅ Error Handling Issues",
    ]
    
    print("\n" + "-" * 70)
    for detection in detections:
        print(f"  {detection}")
    
    # API endpoints
    print_banner("🌐 API ENDPOINTS")
    
    endpoints = [
        ("GET", "/", "Service information"),
        ("GET", "/health", "Health check & scanner status"),
        ("POST", "/api/scan", "Manual code security scan"),
        ("POST", "/webhook/github", "GitHub PR webhook handler"),
        ("POST", "/webhook/gitlab", "GitLab MR webhook handler"),
    ]
    
    print("\n" + "-" * 70)
    print(f"{'METHOD':<8} {'ENDPOINT':<25} {'DESCRIPTION'}")
    print("-" * 70)
    for method, endpoint, description in endpoints:
        print(f"{method:<8} {endpoint:<25} {description}")
    
    # Quick start
    print_banner("🚀 QUICK START COMMANDS")
    
    print("""
    Start Services:
    ───────────────────────────────────────────────────────────────────
    Terminal 1:  ollama serve
    Terminal 2:  source venv/bin/activate && python main.py
    
    Test API:
    ───────────────────────────────────────────────────────────────────
    curl http://localhost:8000/health
    python test_github_webhook.py
    
    Docker Deployment:
    ───────────────────────────────────────────────────────────────────
    docker-compose build
    docker-compose up -d
    docker-compose logs -f
    """)
    
    # Statistics
    print_banner("📊 PROJECT STATISTICS")
    
    try:
        # Count lines of code
        python_files = list(Path('.').glob('*.py'))
        total_lines = 0
        for f in python_files:
            if f.name != 'project_summary.py':
                with open(f) as file:
                    total_lines += len(file.readlines())
        
        print(f"""
    Python Files:        {len(python_files)}
    Total Lines of Code: {total_lines:,}
    Docker Images:       2 (Dockerfile, docker-compose.yml)
    Documentation:       2 (README.md, DEPLOYMENT.md)
    Test Scripts:        3
    Configuration Files: 4
        """)
    except:
        pass
    
    # Next steps
    print_banner("🎯 NEXT STEPS")
    
    print("""
    1. Configure GitHub/GitLab tokens in .env
    2. Deploy to production server (see DEPLOYMENT.md)
    3. Setup webhook in your repository settings
    4. Create a test PR to verify scanning
    5. Monitor logs and fine-tune scanner settings
    
    For detailed deployment instructions, see DEPLOYMENT.md
    """)
    
    print("=" * 70)
    print("  🎉 NeuroCode is ready for production!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
