# 🛡️ NeuroCode - AI-Powered Security Scanner

Multi-layer security analysis tool for GitHub/GitLab PRs using Semgrep, Bandit, and CodeLlama AI.

## ✨ Features

- 🤖 **AI-Powered Analysis** - CodeLlama 7B for contextual vulnerability detection
- 🔍 **Multi-Layer Scanning** - Combines Semgrep, Bandit, and AI for comprehensive coverage
- 🔗 **GitHub/GitLab Integration** - Automatic PR reviews via webhooks
- ⚡ **Fast & Efficient** - Optimized for real-time code review
- 📊 **Detailed Reports** - Severity levels, CWE IDs, and fix recommendations

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Ollama installed (for CodeLlama model)
- Ubuntu/WSL2 or Linux environment

### Installation

1. **Clone/Setup Project**
cd /mnt/d/projects/neurocode
python3 -m venv venv
source venv/bin/activate

2. **Install Dependencies**
pip install -r requirements.txt

3. **Install Ollama & Model**
curl -fsSL https://ollama.com/install.sh | sh
ollama pull codellama:7b-instruct

4. **Configure Environment**
cp .env.example .env

Edit .env with your GitHub/GitLab tokens

5. **Start Services**

Terminal 1 - Ollama:
ollama serve

Terminal 2 - NeuroCode API:
source venv/bin/activate
python main.py

## 📡 API Endpoints

### Health Check
curl http://localhost:8000/health

### Manual Code Scan
curl -X POST http://localhost:8000/api/scan
-H "Content-Type: application/json"
-d '{
"code": "import os\nos.system(user_input)",
"language": "python"
}'

### GitHub Webhook
POST /webhook/github

Configure in GitHub: Settings → Webhooks → Add webhook
- Payload URL: `http://your-server:8000/webhook/github`
- Content type: `application/json`
- Events: Pull requests

### GitLab Webhook
POST /webhook/gitlab

Configure in GitLab: Settings → Webhooks → Add new webhook

## 🔧 Configuration

Edit `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub personal access token | - |
| `GITLAB_TOKEN` | GitLab personal access token | - |
| `OLLAMA_MODEL` | Ollama model name | codellama:7b-instruct |
| `ENABLE_SEMGREP` | Enable Semgrep scanner | true |
| `ENABLE_BANDIT` | Enable Bandit scanner | true |
| `MAX_FILES_PER_PR` | Max files to scan per PR | 50 |

## 🎯 Detection Capabilities

- ✅ SQL Injection
- ✅ Command Injection  
- ✅ Code Injection (eval, exec)
- ✅ Path Traversal
- ✅ SSRF
- ✅ Hardcoded Credentials
- ✅ Weak Cryptography
- ✅ Authentication Issues

## 📊 Example Scan Output

{
"total_issues": 3,
"severity_breakdown": {
"high": 1,
"medium": 2,
"low": 0
},
"semgrep_findings": [...],
"bandit_findings": [...],
"codellama_analysis": "..."
}

## 🛠️ Development

### Run Tests
python test_setup.py
python test_multi_scanner.py

### Project Structure
neurocode/
├── main.py # FastAPI application
├── security_scanner.py # Multi-layer scanner core
├── github_integration.py # GitHub API integration
├── config.py # Configuration management
├── test_setup.py # Basic setup test
├── test_multi_scanner.py # Multi-scanner test
├── .env.example # Configuration template
└── README.md # This file

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open issues or PRs.

## 📧 Support

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ using CodeLlama, Semgrep, and Bandit**
