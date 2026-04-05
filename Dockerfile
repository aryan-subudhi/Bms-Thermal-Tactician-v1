# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (better for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Expose the port FastAPI runs on
EXPOSE 7860

# Command to run your server (pointing to your app file)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

COPY server/app.py /app/app.py
# or if the Dockerfile is INSIDE the server folder:
COPY app.py /app/app.py