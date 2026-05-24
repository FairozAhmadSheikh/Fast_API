from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field
from typing import Optional,Literal,Annotated
import pickle
from fastapi.responses import JSONResponse

app=FastAPI()


class Prediction(BaseModel):
    age_group:Annotated[str,Field(...,description="Provide age group here ",examples=['Middle_aged','Young','Adult','Senior'])]
    city_tier:Annotated[str,Field(...,description="Provide city tier 1: for tier 1 cities upto 3  ",examples=[1,2,3])]
    occupation:Annotated[str,Field(...,description="What is your Occupation",examples=['Businessman','Banker'])]
    income_lpa:Annotated[str,Field(...,description="What is your income in Lakhs per annum",examples=[12.5,3.2])]


@app.get('/')
def home():
    JSONResponse(status_code=200,content={"message":"This is a Insurance prediction API 💖"})