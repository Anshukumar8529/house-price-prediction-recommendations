FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY Home.py .
COPY pages/ ./pages/
COPY backend/ ./backend/
COPY data/ ./data/

# Create startup script to launch FastAPI backend in background and Streamlit in foreground
RUN echo '#!/bin/bash\n\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &\n\
export API_URL=${API_URL:-http://127.0.0.1:8000}\n\
exec streamlit run Home.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.enableCORS=false\n\
' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8501 8000

CMD ["/app/start.sh"]
