from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field,computed_field
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

    @computed_field
    @property
    def bmi(self):
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self):
        if self.bmi<18:
            return 'underweight'
        elif self.bmi<25:
            return 'normall'
        elif self.bmi<30:
            return 'normal'
        else:
            return 'obese'
    

