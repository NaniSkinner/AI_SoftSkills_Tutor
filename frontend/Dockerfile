FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port (Render will use PORT env var, typically 10000)
EXPOSE 8501

# Run Streamlit with production flags, using PORT environment variable
# Note: Most settings are in .streamlit/config.toml, but these ensure production mode
CMD ["sh", "-c", "streamlit run Home.py \
    --server.port ${PORT:-8501} \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false \
    --server.fileWatcherType none"]
