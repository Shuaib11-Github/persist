# Base image for Python
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend, frontend, and data folders into the container
COPY ./backend /app/backend
COPY ./frontend /app/frontend
COPY ./data /app/data

# Expose ports for FastAPI (8000) and Streamlit (8502)
EXPOSE 8000 8502

# Start both FastAPI and Streamlit using a single command
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8502 --server.address 0.0.0.0"]
