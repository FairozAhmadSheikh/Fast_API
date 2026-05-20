from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
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
    
# HomePage
@app.get('/')
def welcome():
    return "If you see this Server is Running and is Made with 💖"


# Displays all patients
@app.get('/viewall')
def view():
    data=load_data()
    return data

# Diplay a Specific Patient 
@app.get('/patient/{patient_id}')
def view_specific(patient_id):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404,detail="Patient with provide ID is not found")

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

# Lets now work on update route


# Creating an pydantic schema wiith all optional feilds 
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    city:Annotated[Optional[str],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female','others']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]

@app.put('/update/{patient_id}')
def update(patient_id:str,update_patient:PatientUpdate):
    data=load_data()

    # Incase of invalide id 
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='No user with that id ')
    
    # obtained existing info 
    existing_patient_info=data[patient_id]   

    # Updated info
    updated_patient_info=update_patient.model_dump(exclude_unset=True)

    # Placing updated key value pairs in the existing data
    for key , value in updated_patient_info.items():
        existing_patient_info[key]=value

    existing_patient_info['id']=patient_id

    patient_pydantic_obj=Patient(**existing_patient_info)

    existing_patient_info=patient_pydantic_obj.model_dump(exclude=['id'])

    data[patient_id]=existing_patient_info

    return JSONResponse(status_code=200, content={'message':"Patient Updated"})
    
    
# Delete Route 
@app.delete('/delete/{patient_id}')
def delete(pateint_id):
    data=load_data()

    if pateint_id not in data:
        raise HTTPException(status_code=404,detail="User not found")
    del data[pateint_id]
    save_data(data)
    return JSONResponse(status_code=200,content="Deleted Successfully")