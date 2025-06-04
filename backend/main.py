from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import numpy as np

app = FastAPI(title="Scanimal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prediction(BaseModel):
    label: str
    probability: float

class AnalyzeResponse(BaseModel):
    top_class: str
    description: str
    predictions: List[Prediction]

# placeholder model using torchvision resnet18 pretrained
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Fake class names for demonstration
CLASSES = ['healthy', 'fracture', 'tumor']

def infer(image: Image.Image):
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        out = model(tensor)
        probs = torch.softmax(out, dim=1).numpy().flatten()
    # pick first 3 for demonstration
    preds = []
    for i, cls in enumerate(CLASSES):
        preds.append(Prediction(label=cls, probability=float(probs[i % len(probs)])))
    top = max(preds, key=lambda p: p.probability)
    return top.label, preds

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    top_class, predictions = infer(image)
    description = f"Detected condition: {top_class}"  # placeholder
    return AnalyzeResponse(
        top_class=top_class,
        description=description,
        predictions=predictions,
    )

