from github import Github, GithubException
from typing import List, Dict, Optional
import json
from config import config

class GitHubIntegration:
    """Handle GitHub API operations for PR reviews"""
    
    def __init__(self, token: Optional[str] = None):
        config = get_config()
        self.token = token or config.github_token
        
        if not self.token:
            print("⚠️  No GitHub token found. Set GITHUB_TOKEN environment variable.")
            self.client = None
        else:
            self.client = Github(self.token)
            print("✅ GitHub client initialized")
    
    def get_pr_files(self, repo_full_name: str, pr_number: int) -> List[Dict]:
        """Get list of changed files in a PR"""
        if not self.client:
            return []
        
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            
            files = []
            for file in pr.get_files():
                files.append({
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch if hasattr(file, 'patch') else None,
                    "raw_url": file.raw_url
                })
            
            return files
            
        except GithubException as e:
            print(f"❌ GitHub API error: {e}")
            return []
    
    def get_file_content(self, repo_full_name: str, file_path: str, ref: str = "main") -> Optional[str]:
        """Get content of a specific file"""
        if not self.client:
            return None
        
        try:
            repo = self.client.get_repo(repo_full_name)
            content = repo.get_contents(file_path, ref=ref)
            
            if isinstance(content, list):
                return None  # Directory, not a file
            
            return content.decoded_content.decode('utf-8')
            
        except GithubException as e:
            print(f"❌ Error fetching file content: {e}")
            return None
    
    def post_pr_comment(self, repo_full_name: str, pr_number: int, comment: str) -> bool:
        """Post a comment on a PR"""
        if not self.client:
            print("❌ Cannot post comment: No GitHub client")
            return False
        
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
            print(f"✅ Comment posted on PR #{pr_number}")
            return True
            
        except GithubException as e:
            print(f"❌ Error posting comment: {e}")
            return False
    
    def post_inline_comment(self, repo_full_name: str, pr_number: int, 
                          file_path: str, line: int, comment: str) -> bool:
        """Post an inline comment on specific line in PR"""
        if not self.client:
            return False
        
        try:
            repo = self.client.get_repo(repo_full_name)
            pr = repo.get_pull(pr_number)
            commit = pr.get_commits().reversed[0]  # Latest commit
            
            pr.create_review_comment(
                body=comment,
                commit=commit,
                path=file_path,
                line=line
            )
            print(f"✅ Inline comment posted on {file_path}:{line}")
            return True
            
        except GithubException as e:
            print(f"❌ Error posting inline comment: {e}")
            return False
    
    def format_scan_results_comment(self, results: Dict, pr_number: int) -> str:
        """Format scan results as a markdown comment"""
        
        total_issues = results.get("total_issues", 0)
        severity = results.get("severity_breakdown", {})
        
        comment = f"""## 🔍 NeuroCode Security Scan Results - PR #{pr_number}

### Summary
- **Total Issues Found:** {total_issues}
- **High Severity:** {severity.get('high', 0)} 🔴
- **Medium Severity:** {severity.get('medium', 0)} 🟡
- **Low Severity:** {severity.get('low', 0)} 🟢

---

"""
        
        # Semgrep findings
        semgrep_findings = results.get("semgrep_findings", [])
        if semgrep_findings:
            comment += f"### 🔍 Semgrep Findings ({len(semgrep_findings)})\n\n"
            for i, finding in enumerate(semgrep_findings[:10], 1):
                check_id = finding.get("check_id", "unknown")
                message = finding.get("extra", {}).get("message", "No description")
                severity_level = finding.get("extra", {}).get("severity", "unknown").upper()
                file_path = finding.get("path", "unknown")
                line = finding.get("start", {}).get("line", "?")
                
                comment += f"{i}. **[{severity_level}]** `{check_id}`\n"
                comment += f"   - **File:** `{file_path}:{line}`\n"
                comment += f"   - **Issue:** {message}\n\n"
        
        # Bandit findings
        bandit_findings = results.get("bandit_findings", [])
        if bandit_findings:
            comment += f"### 🐍 Bandit Findings ({len(bandit_findings)})\n\n"
            for i, finding in enumerate(bandit_findings[:10], 1):
                test_id = finding.get("test_id", "unknown")
                issue_text = finding.get("issue_text", "No description")
                severity_level = finding.get("issue_severity", "unknown").upper()
                filename = finding.get("filename", "unknown")
                line = finding.get("line_number", "?")
                
                comment += f"{i}. **[{severity_level}]** `{test_id}`\n"
                comment += f"   - **File:** `{filename}:{line}`\n"
                comment += f"   - **Issue:** {issue_text}\n\n"
        
        # CodeLlama summary
        codellama_analysis = results.get("codellama_analysis", "")
        if codellama_analysis:
            comment += f"### 🤖 AI Analysis Summary\n\n"
            comment += f"``````\n\n"
        
        comment += f"""---

*Scanned with NeuroCode | Powered by Semgrep, Bandit & CodeLlama*
"""
        
        return comment
    
    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """Verify GitHub webhook signature"""
        import hmac
        import hashlib
        
        if not secret:
            return True  # Skip verification if no secret set
        
        mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
        expected_signature = f"sha256={mac.hexdigest()}"
        
        return hmac.compare_digest(expected_signature, signature)
