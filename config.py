import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration for NeuroCode Security Scanner"""
    
    # GitHub Integration
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    github_webhook_secret: Optional[str] = os.getenv("GITHUB_WEBHOOK_SECRET")
    
    # GitLab Integration
    gitlab_token: Optional[str] = os.getenv("GITLAB_TOKEN")
    gitlab_url: str = os.getenv("GITLAB_URL", "https://gitlab.com")
    gitlab_webhook_secret: Optional[str] = os.getenv("GITLAB_WEBHOOK_SECRET")
    
    # Ollama/CodeLlama AI Settings
    ollama_model: str = os.getenv("OLLAMA_MODEL", "codellama:7b-instruct")
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # Scanner Settings
    enable_semgrep: bool = os.getenv("ENABLE_SEMGREP", "true").lower() == "true"
    enable_bandit: bool = os.getenv("ENABLE_BANDIT", "true").lower() == "true"
    enable_ai_analysis: bool = os.getenv("ENABLE_AI_ANALYSIS", "true").lower() == "true"
    
    # API Server Settings
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    
    # Performance Settings
    max_file_size_kb: int = int(os.getenv("MAX_FILE_SIZE_KB", "500"))
    max_files_per_pr: int = int(os.getenv("MAX_FILES_PER_PR", "50"))
    scan_timeout_seconds: int = int(os.getenv("SCAN_TIMEOUT_SECONDS", "300"))


config = Config()
