# NeuroCode Docker Image
FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3-venv \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory for Ollama
RUN mkdir -p /root/.ollama

# Expose ports
# 8000 - NeuroCode API
# 11434 - Ollama API
EXPOSE 8000 11434

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting NeuroCode Services..."\n\
\n\
# Start Ollama in background\n\
echo "📡 Starting Ollama server..."\n\
ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
# Wait for Ollama to be ready\n\
echo "⏳ Waiting for Ollama to start..."\n\
sleep 5\n\
\n\
# Check if model exists, if not pull it\n\
if ! ollama list | grep -q "codellama:7b-instruct"; then\n\
    echo "📥 Pulling CodeLlama model (first run - this will take a few minutes)..."\n\
    ollama pull codellama:7b-instruct\n\
fi\n\
\n\
echo "✅ Ollama ready"\n\
\n\
# Start NeuroCode API\n\
echo "🌐 Starting NeuroCode API..."\n\
python3 main.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run startup script
CMD ["/app/start.sh"]
