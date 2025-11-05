FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Copy application code
COPY fastapi_swarms_backend.py .
COPY customer_api_keys.md .
COPY production_config.md .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "fastapi_swarms_backend:app", "--host", "0.0.0.0", "--port", "8000"]