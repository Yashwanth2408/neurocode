import os
from typing import Optional
from pydantic import BaseModel

class NeurocodeConfig(BaseModel):
    """NeuroCode configuration settings"""
    
    # API Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Ollama Settings
    ollama_model: str = "codellama:7b-instruct"
    ollama_host: str = "http://localhost:11434"
    
    # GitHub Settings
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")
    github_webhook_secret: Optional[str] = os.getenv("GITHUB_WEBHOOK_SECRET")
    
    # GitLab Settings
    gitlab_token: Optional[str] = os.getenv("GITLAB_TOKEN")
    gitlab_url: str = os.getenv("GITLAB_URL", "https://gitlab.com")
    gitlab_webhook_secret: Optional[str] = os.getenv("GITLAB_WEBHOOK_SECRET")
    
    # Scanner Settings
    enable_semgrep: bool = True
    enable_bandit: bool = True
    enable_codellama: bool = True
    
    # Performance Settings
    max_file_size_kb: int = 500  # Skip files larger than 500KB
    max_files_per_pr: int = 50   # Limit analysis to 50 files per PR
    scan_timeout_seconds: int = 300  # 5 minute timeout
    
    # Security Settings
    min_severity_to_report: str = "low"  # Report low, medium, high
    auto_comment_on_pr: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global config instance
config = NeurocodeConfig()

def get_config() -> NeurocodeConfig:
    """Get configuration instance"""
    return config

def update_config(**kwargs):
    """Update configuration at runtime"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
    return config
