from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
import json
from fastapi.responses import JSONResponse

app=FastAPI()

# Create a Patient Model 
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Provide a Patient Id ',examples=['P001','P002'])]
    name:Annotated[str,Field(...,description='Provide Name of a patient ')]
    city:Annotated[str,Field(...,description='City a patient lives in  ')]
    age:Annotated[int,Field(...,description='Enter your Age ',gt=0,lt=120)]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,description="Height of patient in meters")]
    weight:Annotated[float,Field(...,description="Weight of patient in kgs")]

    @computed_field
    @property
    def bmi(self)->float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18:
            return 'underweight'
        elif self.bmi<25:
            return 'normall'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'
    

# Load data from json
def load_data():
    with open('patient.json','r')as f:
        data=json.load(f)
        return data
    
# Save data function
def save_data(data):
    with open ('patient.json','w')as f:
        data=json.dump(data,f)
        return data
    

@app.get('/')
def welcome():
    return "Made with 💖"

@app.get('/viewall')
def view():
    data=load_data()
    return data


# Route for post or saving the data 
@app.post('/create')
def create_patient(patient:Patient):
    # Load saved Data first
    data=load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")
    
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=200,content="Patient Created Successfully")