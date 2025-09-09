# Scanimal Backend

This is a minimal FastAPI backend for Scanimal. It exposes an `/analyze` endpoint
that accepts an X-ray image and returns dummy predictions.

## Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

The model currently uses a pretrained ResNet18 from `torchvision` as a placeholder.
Add your own model weights in `main.py` if needed.

## Docker

```bash
docker build -t scanimal-backend .
docker run -p 8000:8000 scanimal-backend
```
