# NeuroCode - Python Security Scanner

# NeuroCode - Python Security Scanner

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://web-production-15a1.up.railway.app)
[![Deployment](https://img.shields.io/badge/deployment-active-success)](https://railway.app)
[![Platform](https://img.shields.io/badge/platform-Railway-blueviolet)](https://railway.app)

**Live Demo:** [https://web-production-15a1.up.railway.app](https://web-production-15a1.up.railway.app)

A static application security testing (SAST) tool that analyzes Python code for security vulnerabilities using industry-standard scanning engines (Semgrep and Bandit)

## Overview

NeuroCode combines Semgrep and Bandit to provide comprehensive security analysis of Python codebases. The tool can be used as a standalone web application for manual code review or integrated into CI/CD pipelines via GitHub webhooks for automated pull request security scanning.

## Features

**Multi-Engine Scanning**
- Semgrep for pattern-based vulnerability detection across 166+ security rules
- Bandit for Python-specific security issue identification (68 built-in checks)
- Combined analysis providing broader coverage than single-tool approaches

**Web Interface**
- Real-time code analysis with instant feedback
- Dark-themed responsive UI
- Severity-based categorization (HIGH, MEDIUM, LOW)
- Line-level precision for identified issues

**CI/CD Integration**
- GitHub webhook support for automated PR scanning
- GitLab webhook support (experimental)
- REST API for programmatic access
- Background task processing for large codebases

**Detection Capabilities**
- SQL Injection (CWE-89)
- Command Injection (CWE-78)
- Code Injection via eval/exec (CWE-94)
- Hardcoded Credentials (CWE-798)
- Weak Cryptographic Functions (CWE-327)
- Insecure Deserialization (CWE-502)
- Path Traversal (CWE-22)
- Flask Debug Mode Issues

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git

### Local Setup

Clone the repository:

git clone https://github.com/YOUR_USERNAME/neurocode.git
cd neurocode

Create and activate virtual environment:

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the application:

python main.py


Access the web interface at `http://localhost:8000`

## Configuration

Create a `.env` file in the project root (use `.env.example` as template):

Scanner Settings
ENABLE_SEMGREP=true
ENABLE_BANDIT=true
ENABLE_AI_ANALYSIS=false

API Server
API_HOST=0.0.0.0
API_PORT=8000

GitHub Integration (Optional)
GITHUB_TOKEN=your_token_here
GITHUB_WEBHOOK_SECRET=your_secret_here

GitLab Integration (Optional)
GITLAB_TOKEN=your_token_here
GITLAB_URL=https://gitlab.com
GITLAB_WEBHOOK_SECRET=your_secret_here

Performance
MAX_FILE_SIZE_KB=500
MAX_FILES_PER_PR=50
SCAN_TIMEOUT_SECONDS=300


## Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Paste Python code in the editor
3. Click "Scan Python Code"
4. Review identified vulnerabilities with severity levels and line numbers

### API Endpoints

**Health Check**
curl http://localhost:8000/api/health

**Manual Code Scan**
curl -X POST http://localhost:8000/api/scan
-H "Content-Type: application/json"
-d '{
"code": "query = "SELECT * FROM users WHERE id = " + user_id",
"language": "python"
}'

**Response Format**
{
"success": true,
"results": {
"total_issues": 1,
"severity_breakdown": {
"high": 0,
"medium": 1,
"low": 0
},
"semgrep_findings": [],
"bandit_findings": [
{
"test_id": "B608",
"issue_severity": "MEDIUM",
"issue_text": "Possible SQL injection vector",
"line_number": 1
}
]
}
}

### GitHub Integration

Configure webhook in your repository:

1. Go to Settings → Webhooks → Add webhook
2. Set Payload URL: `https://your-domain.com/webhook/github`
3. Content type: `application/json`
4. Select events: Pull requests
5. Add webhook secret (match GITHUB_WEBHOOK_SECRET in .env)

NeuroCode will automatically scan code changes in pull requests and post results as PR comments.

### GitLab Integration

Configure webhook in your project:

1. Go to Settings → Webhooks
2. Set URL: `https://your-domain.com/webhook/gitlab`
3. Add Secret Token (match GITLAB_WEBHOOK_SECRET in .env)
4. Select trigger: Merge request events

## Architecture

neurocode/
├── main.py # FastAPI application entry point
├── security_scanner.py # Core scanning logic (Semgrep + Bandit)
├── github_integration.py # GitHub API integration
├── config.py # Configuration management
├── static/ # Frontend assets
│ ├── css/
│ ├── js/
│ └── index.html
├── requirements.txt # Python dependencies
├── Procfile # Railway deployment configuration
└── README.md


## Testing

Run the test suite:

python test_multi_scanner.py

Expected output shows detection of 8+ vulnerabilities in test code samples.

## Deployment

### Railway

1. Push code to GitHub
2. Connect repository to Railway
3. Configure environment variables:
   - ENABLE_SEMGREP=true
   - ENABLE_BANDIT=true
   - ENABLE_AI_ANALYSIS=false
4. Railway automatically detects Python and deploys

### Docker (Alternative)

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]


## Performance Considerations

- Semgrep scans typically complete in 2-5 seconds for <500 lines of code
- Bandit analysis adds 1-3 seconds overhead
- Large PRs (50+ files) may take 30-60 seconds
- Configure MAX_FILES_PER_PR to limit scan scope

## Security Notes

- GitHub/GitLab tokens should have minimal required permissions
- Use webhook secrets to verify request authenticity
- Never commit .env files to version control
- Review scan results for false positives before taking action

## Limitations

- Currently supports Python only (JavaScript/TypeScript support planned)
- AI analysis requires local Ollama installation (optional feature)
- Maximum file size: 500KB per file
- Webhook endpoints require public URL (use ngrok for local testing)

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request with clear description

## License

MIT License - see LICENSE file for details

## References

- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Common Weakness Enumeration](https://cwe.mitre.org/)

## Author

Yashwanth Balaji
- GitHub: [@yashwanth2408](https://github.com/Yashwanth2408)
- LinkedIn: [yashwanth-balaji](https://www.linkedin.com/in/yashwanthbalaji/)

---

Built with FastAPI, Semgrep, and Bandit
