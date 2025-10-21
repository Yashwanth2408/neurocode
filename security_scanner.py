import subprocess
import json
import ollama
from pathlib import Path
from typing import Dict, List, Any

class SecurityScanner:
    """Multi-layer security scanner combining Semgrep, Bandit, and CodeLlama"""
    
    def __init__(self):
        self.semgrep_available = self._check_tool("semgrep")
        self.bandit_available = self._check_tool("bandit")
        print(f"🔧 Security Scanner initialized")
        print(f"   - Semgrep: {'✅' if self.semgrep_available else '❌'}")
        print(f"   - Bandit: {'✅' if self.bandit_available else '❌'}")
        print(f"   - CodeLlama: ✅")
    
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
            # Create temporary file
            temp_file = Path(f"temp_scan.{language}")
            temp_file.write_text(code)
            
            # Run Semgrep with security rules
            result = subprocess.run(
                ["semgrep", "--config=auto", "--json", str(temp_file)],
                capture_output=True,
                text=True
            )
            
            # Clean up
            temp_file.unlink()
            
            if result.returncode in [0, 1]:  # 0 = no findings, 1 = findings
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
        """Run CodeLlama AI analysis"""
        try:
            prompt = f"""Analyze this {language} code for security vulnerabilities.
Focus on:
1. Injection vulnerabilities (SQL, command, code)
2. Authentication/authorization issues
3. Cryptographic weaknesses
4. Input validation problems
5. Error handling issues

Code:
{code}

Provide a concise analysis with severity levels."""

            response = ollama.generate(
                model='codellama:7b-instruct',
                prompt=prompt
            )
            
            return response['response']
            
        except Exception as e:
            return f"CodeLlama error: {e}"
    
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
        
        # Run Semgrep
        print("\n[1/3] Running Semgrep scan...")
        semgrep_results = self.scan_with_semgrep(code, language)
        results["semgrep_findings"] = semgrep_results
        print(f"      Found {len(semgrep_results)} issues")
        
        # Run Bandit (Python only)
        if language == "python":
            print("[2/3] Running Bandit scan...")
            bandit_results = self.scan_with_bandit(code)
            results["bandit_findings"] = bandit_results
            print(f"      Found {len(bandit_results)} issues")
        
        # Run CodeLlama
        print("[3/3] Running CodeLlama AI analysis...")
        codellama_analysis = self.scan_with_codellama(code, language)
        results["codellama_analysis"] = codellama_analysis
        print(f"      Analysis complete")
        
        # Calculate totals
        results["total_issues"] = len(semgrep_results) + len(bandit_results)
        
        # Count severity levels (simplified)
        for finding in semgrep_results:
            severity = finding.get("extra", {}).get("severity", "").lower()
            if severity in results["severity_breakdown"]:
                results["severity_breakdown"][severity] += 1
        
        for finding in bandit_results:
            severity = finding.get("issue_severity", "").lower()
            if severity in results["severity_breakdown"]:
                results["severity_breakdown"][severity] += 1
        
        return results
    
    def print_results(self, results: Dict[str, Any]):
        """Pretty print scan results"""
        print(f"\n{'='*60}")
        print(f"📊 SCAN RESULTS SUMMARY")
        print(f"{'='*60}")
        
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
        
        # CodeLlama analysis
        print(f"\n🤖 CodeLlama AI Analysis:")
        print(f"{'-'*60}")
        print(results["codellama_analysis"][:500])  # Show first 500 chars
        if len(results["codellama_analysis"]) > 500:
            print("... (truncated)")
        
        print(f"\n{'='*60}")
