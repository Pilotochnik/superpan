from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Dict
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import numpy as np
import hashlib
import jwt
from datetime import datetime, timedelta

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

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# placeholder model using torchvision resnet18 pretrained
model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=True)
model.eval()
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# --- simple in-memory authentication ---
SECRET_KEY = "change_this_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 12

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

users: Dict[str, str] = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if username not in users:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}

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

@app.post("/register")
async def register(user: UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User exists")
    users[user.username] = hash_password(user.password)
    return {"msg": "registered"}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    hashed = users.get(form_data.username)
    if not hashed or hashed != hash_password(form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(form_data.username)
    return Token(access_token=token)

@app.get("/me")
async def me(current=Depends(get_current_user)):
    return current

