import subprocess
import json
try:
    import ollama
except ImportError:
    ollama = None 
    
from pathlib import Path
from typing import Dict, List, Any
from config import config


class SecurityScanner:
    """Multi-layer security scanner combining Semgrep, Bandit, and CodeLlama AI"""
    
    def __init__(self):
        self.config = config
        self.semgrep_available = self._check_tool("semgrep")
        self.bandit_available = self._check_tool("bandit")
        
        # Check if Ollama is available
        self.ai_available = False
        try:
            if ollama:
                ollama.list()
                self.ai_available = True
        except Exception as e:
            print(f"⚠️  Ollama not available: {e}")
        
        print(f"🔧 Security Scanner initialized")
        print(f"   - Semgrep: {'✅' if self.semgrep_available else '❌'}")
        print(f"   - Bandit: {'✅' if self.bandit_available else '❌'}")
        print(f"   - CodeLlama AI: {'✅' if self.ai_available else '❌'}")
    
    def _check_tool(self, tool_name: str) -> bool:
        """Check if a command-line tool is available"""
        try:
            subprocess.run([tool_name, "--version"], 
                         capture_output=True, 
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def scan_with_semgrep(self, code: str, language: str = "python") -> List[Dict]:
        """Run Semgrep security scan"""
        if not self.semgrep_available:
            return []
    
        try:
            # Map UI language to file extension
            extension_map = {
                "python": "py",
                "javascript": "js",
                "typescript": "ts",
                "java": "java",
                "go": "go"
            }
        
            ext = extension_map.get(language, "py")
            temp_file = Path(f"temp_scan.{ext}")
            temp_file.write_text(code)
        
            # Run Semgrep with comprehensive security rules
            result = subprocess.run(
                [
                    "semgrep",
                    "--config", "p/security-audit",
                    "--config", "p/owasp-top-ten",
                    "--json",
                    str(temp_file)
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
        
            temp_file.unlink()
        
            if result.returncode in [0, 1]:
                data = json.loads(result.stdout)
                return data.get("results", [])
            
        except Exception as e:
            print(f"⚠️  Semgrep error: {e}")
    
        return []

    
    def scan_with_bandit(self, code: str) -> List[Dict]:
        """Run Bandit Python security scan"""
        if not self.bandit_available:
            return []
        
        try:
            # Create temporary file
            temp_file = Path("temp_scan.py")
            temp_file.write_text(code)
            
            # Run Bandit
            result = subprocess.run(
                ["bandit", "-f", "json", str(temp_file)],
                capture_output=True,
                text=True
            )
            
            # Clean up
            temp_file.unlink()
            
            if result.stdout:
                data = json.loads(result.stdout)
                return data.get("results", [])
            
        except Exception as e:
            print(f"⚠️  Bandit error: {e}")
        
        return []
    
    def scan_with_codellama(self, code: str, language: str = "python") -> str:
        """Run CodeLlama AI security analysis"""
        if not self.ai_available:
            return "AI analysis skipped - Ollama/CodeLlama not available"
    
        try:
            prompt = f"""You are a security expert analyzing {language} code for vulnerabilities.

Analyze this code and identify:
1. Security vulnerabilities (SQL injection, XSS, command injection, etc.)
2. Authentication/authorization issues
3. Cryptographic weaknesses
4. Input validation problems
5. Error handling issues

Code:
{code}

Provide a concise security analysis with severity levels (HIGH, MEDIUM, LOW) for each issue found."""

            # Generate content using Ollama
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt
            )
            
            return response['response']
        
        except Exception as e:
            return f"CodeLlama AI analysis error: {str(e)}"
    
    def comprehensive_scan(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Run all security scanners and combine results"""
        print(f"\n{'='*60}")
        print(f"🔍 COMPREHENSIVE SECURITY SCAN")
        print(f"{'='*60}")
    
        results = {
            "semgrep_findings": [],
            "bandit_findings": [],
            "codellama_analysis": "",
            "total_issues": 0,
            "severity_breakdown": {"high": 0, "medium": 0, "low": 0}
        }
    
    # Run Semgrep (all languages)
        if self.config.enable_semgrep:
            print("\n[1/3] Running Semgrep scan...")
            semgrep_results = self.scan_with_semgrep(code, language)
            results["semgrep_findings"] = semgrep_results
            print(f"      Found {len(semgrep_results)} issues")
    
    # Run Bandit (Python only)
        if language == "python" and self.config.enable_bandit:
            print("[2/3] Running Bandit scan...")
            bandit_results = self.scan_with_bandit(code)
            results["bandit_findings"] = bandit_results
            print(f"      Found {len(bandit_results)} issues")
        else:
            print(f"[2/3] Bandit scan skipped ({language} not supported, Python only)")
    
    # Run CodeLlama AI (all languages)
        if self.config.enable_ai_analysis:
            print("[3/3] Running CodeLlama AI analysis...")
            codellama_analysis = self.scan_with_codellama(code, language)
            results["codellama_analysis"] = codellama_analysis
            print(f"      Analysis complete")
    
    # Calculate totals
        results["total_issues"] = len(results["semgrep_findings"]) + len(results["bandit_findings"])
    
        # Count severity levels from Semgrep
        for finding in results["semgrep_findings"]:
            severity = finding.get("extra", {}).get("severity", "").lower()
            if severity in results["severity_breakdown"]:
                results["severity_breakdown"][severity] += 1
    
        # Count severity levels from Bandit
        for finding in results["bandit_findings"]:
            severity = finding.get("issue_severity", "").lower()
            if severity in results["severity_breakdown"]:
                results["severity_breakdown"][severity] += 1
    
        return results

    
    def print_results(self, results: Dict[str, Any]):
        """Pretty print scan results"""
        print(f"\n{'='*60}")
        print(f"📊 SCAN RESULTS SUMMARY")
        print(f"{'='*60}")
    
        # Show scanner breakdown
        scanners_used = ["Semgrep"]
        if results.get("bandit_findings"):
            scanners_used.append("Bandit")
        if results.get("codellama_analysis") and "error" not in results["codellama_analysis"].lower():
            scanners_used.append("CodeLlama AI")
    
        print(f"\n🔧 Scanners Used: {', '.join(scanners_used)}")
    
        print(f"\n🎯 Total Issues Found: {results['total_issues']}")
        print(f"   - High Severity: {results['severity_breakdown']['high']}")
        print(f"   - Medium Severity: {results['severity_breakdown']['medium']}")
        print(f"   - Low Severity: {results['severity_breakdown']['low']}")

        
        # Semgrep findings
        if results["semgrep_findings"]:
            print(f"\n🔍 Semgrep Findings ({len(results['semgrep_findings'])})")
            for i, finding in enumerate(results["semgrep_findings"][:5], 1):  # Show first 5
                check_id = finding.get("check_id", "unknown")
                message = finding.get("extra", {}).get("message", "No description")
                severity = finding.get("extra", {}).get("severity", "unknown")
                print(f"   {i}. [{severity.upper()}] {check_id}")
                print(f"      {message[:80]}...")
        
        # Bandit findings
        if results["bandit_findings"]:
            print(f"\n🐍 Bandit Findings ({len(results['bandit_findings'])})")
            for i, finding in enumerate(results["bandit_findings"][:5], 1):  # Show first 5
                test_id = finding.get("test_id", "unknown")
                issue_text = finding.get("issue_text", "No description")
                severity = finding.get("issue_severity", "unknown")
                print(f"   {i}. [{severity.upper()}] {test_id}")
                print(f"      {issue_text[:80]}...")
        
        # CodeLlama AI analysis
        if results.get("codellama_analysis"):
            print(f"\n🤖 CodeLlama AI Analysis:")
            print(f"{'-'*60}")
            analysis_text = results["codellama_analysis"]
            print(analysis_text[:500])  # Show first 500 chars
            if len(analysis_text) > 500:
                print("... (truncated)")
        
        print(f"\n{'='*60}")
