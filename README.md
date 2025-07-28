# Video Streaming using Kafka

A full-stack web application for secure video upload, AES-256 encryption, and real-time video playback using Apache Kafka.


## Steps to Run the Project

### 1. Run Docker Images
Start Zookeeper and Kafka using Docker:

```bash
docker-compose up -d
```
This command will start Apache Kafka and its required services.

### 2. Run Backend Service
Use PostgreSQL DB and update configurations with your local database credentials.

```python
cd backend
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python run.py
```
This will start the FastAPI backend service.


### 3. Run Frontend
Navigate to the frontend directory and start the React app:
```bash
cd frontend/video-streamer
npm install
npm start
```
This will launch the frontend application in your browser.


# Note
You must have Node.js, Python, and Docker installed on your system to run this project.
Ensure Kafka and Zookeeper are running before starting the backend.
