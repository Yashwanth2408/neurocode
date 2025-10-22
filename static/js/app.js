// NeuroCode Scanner JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const scanBtn = document.getElementById('scanBtn');
    const codeInput = document.getElementById('codeInput');
    const resultsSection = document.getElementById('resultsSection');
    const loadingSection = document.getElementById('loadingSection');
    const resultsContent = document.getElementById('resultsContent');
    const scanSummary = document.getElementById('scanSummary');

    scanBtn.addEventListener('click', async () => {
        const code = codeInput.value.trim();
        const language = "python";  // Always Python

        if (!code) {
            alert('Please paste some Python code to scan!');
            return;
        }

        // Show loading
        resultsSection.style.display = 'none';
        loadingSection.style.display = 'block';

        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language })
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data.results);
            } else {
                throw new Error('Scan failed');
            }
        } catch (error) {
            console.error('Error:', error);
            resultsContent.innerHTML = `
                <div class="finding-card" style="border-left-color: #ef4444;">
                    <div class="finding-title" style="color: #ef4444;">
                        ❌ Scan Error
                    </div>
                    <div class="finding-description">
                        Failed to scan code. Please make sure the API server is running.
                    </div>
                </div>
            `;
            loadingSection.style.display = 'none';
            resultsSection.style.display = 'block';
        }
    });

    function displayResults(results) {
        // Hide loading
        loadingSection.style.display = 'none';

        // Show results
        resultsSection.style.display = 'block';

        // Display summary
        const { total_issues, severity_breakdown } = results;
        scanSummary.innerHTML = `
            <span class="severity-badge severity-high">High: ${severity_breakdown.high}</span>
            <span class="severity-badge severity-medium">Medium: ${severity_breakdown.medium}</span>
            <span class="severity-badge severity-low">Low: ${severity_breakdown.low}</span>
        `;

        // Clear previous results
        resultsContent.innerHTML = '';

        // Display findings
        if (total_issues === 0) {
            resultsContent.innerHTML = `
                <div class="finding-card" style="border-left-color: #00ff88;">
                    <div class="finding-title" style="color: #00ff88;">
                        ✅ No Issues Found
                    </div>
                    <div class="finding-description">
                        Great job! No security vulnerabilities detected in your code.
                    </div>
                </div>
            `;
            return;
        }

        // Display Bandit findings
        results.bandit_findings.forEach((finding, index) => {
            const severity = finding.issue_severity.toLowerCase();
            const color = severity === 'high' ? '#ef4444' :
                severity === 'medium' ? '#f59e0b' : '#06b6d4';

            const card = document.createElement('div');
            card.className = 'finding-card';
            card.style.borderLeftColor = color;
            card.innerHTML = `
                <div class="finding-header">
                    <div class="finding-title">${finding.test_id}</div>
                    <span class="severity-badge severity-${severity}">${finding.issue_severity}</span>
                </div>
                <div class="finding-description">${finding.issue_text}</div>
                <div class="finding-code">Line ${finding.line_number}: ${finding.code || 'N/A'}</div>
            `;
            resultsContent.appendChild(card);
        });

        // Display CodeLlama analysis
        if (results.codellama_analysis && results.codellama_analysis !== "AI analysis skipped - Ollama/CodeLlama not available") {
            const aiCard = document.createElement('div');
            aiCard.className = 'finding-card';
            aiCard.style.borderLeftColor = '#7c3aed';
            aiCard.innerHTML = `
                <div class="finding-header">
                    <div class="finding-title">🤖 AI Security Analysis</div>
                </div>
                <div class="finding-description" style="white-space: pre-wrap;">${results.codellama_analysis}</div>
            `;
            resultsContent.appendChild(aiCard);
        }
    }
});
