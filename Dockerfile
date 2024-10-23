# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install the application in editable mode
COPY . .
RUN pip install -e .

# Expose the port your FastAPI app runs on
EXPOSE 8000

# Print environment variables for debugging before starting the app
CMD hyperlink-api
