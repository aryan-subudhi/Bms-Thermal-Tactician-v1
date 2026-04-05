# Use a Python base image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ENTIRE project
COPY . .

# CRITICAL: Add the server directory to the Python path
ENV PYTHONPATH=/app/server

# Start the application pointing to the app object inside the server folder
# Since we added /app/server to PYTHONPATH, "app:app" works directly
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]