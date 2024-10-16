# Persist Ventures Dashboard

## Overview
This dashboard provides an interactive interface to explore CO2 emissions, capital catalyzed, and company locations using the provided dataset. The application is built with a FastAPI backend and a Streamlit frontend.

## Project Structure

```plaintext
.
├── backend
│   ├── data_processing.py   # Contains data loading and processing functions
│   └── main.py              # FastAPI app definition and route endpoints
├── frontend
│   └── app.py               # Streamlit frontend application
├── data
│   └── dataset.csv          # The dataset used for company metrics
├── requirements.txt         # Python dependencies
└── Dockerfile               # Dockerfile to build the image
```

## How to Run the Application (Locally)

Follow these steps to set up and run the application locally (without Docker).

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.9+
- Pip

### Steps to Run Locally

1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Start the FastAPI backend:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The backend will be available at: `http://localhost:8000`

6. Start the Streamlit frontend: Open a new terminal (keeping the backend running in the first terminal):
    ```bash
    streamlit run frontend/app.py
    ```
    The frontend will be available at: `http://localhost:8502`

## How to Run the Application (with Docker)

This project uses Docker to containerize the application, making it easy to set up and run on any machine. Follow the steps below to run the dashboard using Docker.

### Prerequisites

Make sure you have Docker installed. You can download it from [here](https://www.docker.com/products/docker-desktop) if you don't already have it.

### Steps to Run the Application

1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Build the Docker image by running the following command in the root directory of the project:
    ```bash
    docker build -t persist_dashboard .
    ```

3. Run the Docker container:
    ```bash
    docker run -p 8000:8000 -p 8502:8502 persist_dashboard
    ```
    This will start the FastAPI backend on port 8000 and the Streamlit frontend on port 8502.

4. Access the application in your web browser:
    - **Streamlit Frontend**: `http://localhost:8502`
    - **FastAPI Backend**: `http://localhost:8000`

## Streamlit Dashboard Features

- Use the radio button in the sidebar to select a company from the list of available companies.
- Explore various metrics such as CO2 emissions, capital catalyzed, and the company's location.
- Press buttons to display the respective charts and map views for CO2 emissions, capital catalyzed, and the company's location.

## Stopping the Application

- To stop the application, simply press `CTRL + C` in the terminal where the Docker container or local server is running.
- Alternatively, you can stop the Docker container using:
    ```bash
    docker ps
    docker stop <CONTAINER_ID>
    ```

## Troubleshooting

- **Port Conflict**: If you get a port conflict error, ensure no other applications are running on ports 8000 or 8502. You can change the ports when running the Docker container:
    ```bash
    docker run -p 8001:8000 -p 8503:8502 persist_dashboard
    ```

- **File Not Found (dataset.csv)**: Ensure the `data` directory containing `dataset.csv` is included in the project and copied into the Docker container or accessible from the local environment.

By following these steps, you should be able to successfully set up and run the dashboard.
