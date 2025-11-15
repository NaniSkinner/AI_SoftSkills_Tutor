FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit with production flags
# Note: Most settings are in .streamlit/config.toml, but these ensure production mode
CMD ["streamlit", "run", "Home.py", \
    "--server.port", "8501", \
    "--server.address", "0.0.0.0", \
    "--server.headless", "true", \
    "--server.enableCORS", "false", \
    "--server.enableXsrfProtection", "false", \
    "--browser.gatherUsageStats", "false", \
    "--server.fileWatcherType", "none"]
