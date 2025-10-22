from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn
import json
from typing import Dict, Any
import asyncio
import os

from config import config
from security_scanner import SecurityScanner
from github_integration import GitHubIntegration


# Initialize FastAPI app
app = FastAPI(
    title="NeuroCode Security Scanner",
    description="AI-powered security scanner for GitHub/GitLab PRs",
    version="1.0.0"
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Global instances
scanner = SecurityScanner()


@app.get("/")
async def root():
    """Redirect to frontend"""
    return RedirectResponse(url="/static/index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        "service": "NeuroCode Security Scanner",
        "status": "running",
        "version": "1.0.0",
        "scanners": {
            "semgrep": scanner.semgrep_available,
            "bandit": scanner.bandit_available,
            "codellama_ai": scanner.ai_available
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ai_model": getattr(config, 'ollama_model', None) if scanner.ai_available else None,
        "scanners_enabled": {
            "semgrep": config.enable_semgrep and scanner.semgrep_available,
            "bandit": config.enable_bandit and scanner.bandit_available,
            "codellama_ai": config.enable_ai_analysis and scanner.ai_available
        }
    }


@app.post("/api/scan")
async def scan_code(request: Request):
    """Manual code scan endpoint"""
    try:
        data = await request.json()
        code = data.get("code", "")
        language = data.get("language", "python")
        
        if not code:
            raise HTTPException(status_code=400, detail="No code provided")
        
        # Run scan
        results = scanner.comprehensive_scan(code, language)
        
        return JSONResponse(content={
            "success": True,
            "results": results
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """GitHub webhook endpoint for PR events"""
    try:
        # Get webhook signature
        signature = request.headers.get("X-Hub-Signature-256", "")
        event_type = request.headers.get("X-GitHub-Event", "")
        
        # Get payload
        payload = await request.body()
        data = json.loads(payload)
        
        # Verify signature (if secret is configured)
        if config.github_webhook_secret:
            github_integration = GitHubIntegration()
            if not github_integration.verify_webhook_signature(
                payload, signature, config.github_webhook_secret
            ):
                raise HTTPException(status_code=401, detail="Invalid signature")
        
        # Handle pull request events
        if event_type == "pull_request":
            action = data.get("action", "")
            
            # Trigger scan on PR opened or synchronized (new commits)
            if action in ["opened", "synchronize", "reopened"]:
                pr_data = {
                    "repo": data["repository"]["full_name"],
                    "pr_number": data["pull_request"]["number"],
                    "head_sha": data["pull_request"]["head"]["sha"],
                    "base_ref": data["pull_request"]["base"]["ref"]
                }
                
                # Run scan in background
                background_tasks.add_task(process_github_pr, pr_data)
                
                return JSONResponse(content={
                    "success": True,
                    "message": f"Security scan queued for PR #{pr_data['pr_number']}"
                })
        
        return JSONResponse(content={
            "success": True,
            "message": "Event received but not processed"
        })
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def process_github_pr(pr_data: Dict[str, Any]):
    """Process GitHub PR security scan (background task)"""
    print(f"\n{'='*60}")
    print(f"🔍 Processing GitHub PR #{pr_data['pr_number']}")
    print(f"   Repository: {pr_data['repo']}")
    print(f"{'='*60}")
    
    try:
        github = GitHubIntegration()
        
        # Get PR files
        files = github.get_pr_files(pr_data["repo"], pr_data["pr_number"])
        print(f"📁 Found {len(files)} changed files")
        
        # Filter files to scan
        scannable_files = [
            f for f in files 
            if f["filename"].endswith((".py", ".js", ".ts", ".java", ".go"))
            and f["status"] != "removed"
        ]
        
        print(f"🎯 Scanning {len(scannable_files)} files")
        
        all_results = {
            "semgrep_findings": [],
            "bandit_findings": [],
            "codellama_analysis": "",
            "total_issues": 0,
            "severity_breakdown": {"high": 0, "medium": 0, "low": 0}
        }
        
        # Scan each file
        for file_info in scannable_files[:config.max_files_per_pr]:
            print(f"   Scanning: {file_info['filename']}")
            
            # Get file content
            content = github.get_file_content(
                pr_data["repo"], 
                file_info["filename"],
                ref=pr_data["head_sha"]
            )
            
            if content:
                # Scan file
                language = "python" if file_info["filename"].endswith(".py") else "generic"
                results = scanner.comprehensive_scan(content, language)
                
                # Aggregate results
                all_results["semgrep_findings"].extend(results["semgrep_findings"])
                all_results["bandit_findings"].extend(results["bandit_findings"])
                all_results["total_issues"] += results["total_issues"]
                
                for severity in ["high", "medium", "low"]:
                    all_results["severity_breakdown"][severity] += results["severity_breakdown"][severity]
        
        # Generate AI summary for all findings
        if all_results["total_issues"] > 0:
            all_results["codellama_analysis"] = f"Scanned {len(scannable_files)} files with {all_results['total_issues']} issues found."
        
        # Post comment on PR (if token is configured)
        if config.github_token:
            comment = github.format_scan_results_comment(all_results, pr_data["pr_number"])
            github.post_pr_comment(pr_data["repo"], pr_data["pr_number"], comment)
        
        print(f"✅ Scan complete: {all_results['total_issues']} issues found")
        
    except Exception as e:
        print(f"❌ Error processing PR: {e}")


@app.post("/webhook/gitlab")
async def gitlab_webhook(request: Request, background_tasks: BackgroundTasks):
    """GitLab webhook endpoint for merge request events"""
    try:
        # Get webhook token
        token = request.headers.get("X-Gitlab-Token", "")
        
        if config.gitlab_webhook_secret and token != config.gitlab_webhook_secret:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        data = await request.json()
        
        # Handle merge request events
        object_kind = data.get("object_kind", "")
        
        if object_kind == "merge_request":
            mr_data = data.get("object_attributes", {})
            action = mr_data.get("action", "")
            
            if action in ["open", "update", "reopen"]:
                return JSONResponse(content={
                    "success": True,
                    "message": "GitLab MR scan support coming soon"
                })
        
        return JSONResponse(content={
            "success": True,
            "message": "Event received"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def start_server():
    """Start the FastAPI server with Railway-compatible configuration"""
    # Railway provides PORT environment variable
    port = int(os.environ.get("PORT", config.api_port))
    host = os.environ.get("HOST", config.api_host)
    
    print("\n" + "="*60)
    print("🚀 Starting NeuroCode API Server")
    print("="*60)
    print(f"📡 Host: {host}:{port}")
    print(f"🌍 Environment: {'Production (Railway)' if os.environ.get('RAILWAY_ENVIRONMENT') else 'Development'}")
    print(f"🤖 AI Model: {getattr(config, 'ollama_model', 'Not configured') if scanner.ai_available else 'Disabled'}")
    print(f"✅ Scanners: Semgrep={'✓' if config.enable_semgrep else '✗'}, "
          f"Bandit={'✓' if config.enable_bandit else '✗'}, "
          f"AI Analysis={'✓' if config.enable_ai_analysis else '✗'}")
    print("="*60 + "\n")
    
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level="info"
    )


if __name__ == "__main__":
    start_server()
