from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field
from typing import Annotated,Literal


# Create a Patient Model 
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Provide a Patient Id ',examples=['P001','P002'])]
    name:Annotated[str,Field(...,description='Provide Name of a patient ')]
    city:Annotated[str,Field(...,description='City a patient lives in  ')]
    age:Annotated[int,Field(...,description='Enter your Age ',gt=0,lt=120)]
    gender:Annotated[Literal['male','female','others'],Field(...,description="Gender of the patient")]
    height:Annotated[float,Field(...,description="Height of patient in meters")]
    weight:Annotated[float,Field(...,description="Weight of patient in kgs")]
    
    

