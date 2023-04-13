import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax

app = FastAPI()

model_name = 'roberta-base-openai-detector'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class UserRequestIn(BaseModel):
    text: constr(min_length=10)

@app.post("/classificate")
def read_classification(user_request_in: UserRequestIn):
    encoded = tokenizer(user_request_in.text, return_tensors='pt')
    output = model(**encoded)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ai_score = scores[0]
    return JSONResponse(content={'ai_score': str(ai_score)})

