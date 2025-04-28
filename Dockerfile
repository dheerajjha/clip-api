FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
# Ensure we're using a compatible NumPy version first
RUN pip install --no-cache-dir "numpy<2.0.0" && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
