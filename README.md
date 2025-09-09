# Scanimal

Scanimal is an AI-powered service for analyzing cat X-ray images. This repository
contains a minimal proof-of-concept implementation with a Next.js frontend and a
FastAPI backend.

## Structure

- `frontend` – React/Next.js application using Material-UI
- `backend` – FastAPI application for inference (dummy model)

## Development

Start the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser.

Both services include Dockerfiles for containerization.
