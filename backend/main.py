from fastapi import FastAPI
from backend.train import run_training
from backend.inference import predict
from pydantic import BaseModel

app = FastAPI()

class TrainRequest(BaseModel):
    run_name: str

class InferenceRequest(BaseModel):
    text_input: str

@app.post("/train")
def train_model(req: TrainRequest):
    result = run_training(req.run_name)
    return {"message": result}

@app.post("/predict")
def get_prediction(req: InferenceRequest):
    result = predict(req.text_input)
    return {"prediction": result}

