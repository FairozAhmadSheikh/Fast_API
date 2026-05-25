from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Optional,Literal,Annotated
import pickle
from fastapi.responses import JSONResponse
import pandas as pd

app=FastAPI()

# Load Model first
with open('model.pkl','rb')as f:
    model=pickle.load(f)

# Tier cities
tier_1_cities = [
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Pune",
    "Ahmedabad"
]


tier_2_cities = [
    "Jaipur",
    "Lucknow",
    "Chandigarh",
    "Indore",
    "Bhopal",
    "Patna",
    "Surat",
    "Nagpur",
    "Vadodara",
    "Coimbatore",
    "Visakhapatnam",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Kanpur",
    "Mysore",
    "Raipur",
    "Noida",
    "Guwahati",
    "Kochi"
]

class UserInput(BaseModel):
    age:Annotated[int,Field(...,description="Enter Age here ")]
    weight:Annotated[float,Field(...,gt=0,description='Weight in Kgs')]
    height:Annotated[float,Field(...,gt=0,description='Enter height in Meters')]
    occupation:Annotated[Literal
    [     'Factory Worker',         'Businessman',       'Sales Manager',
              'Banker',   'Marketing Manager',     'Insurance Agent',
          'HR Manager',          'Pharmacist',             'Teacher',
   'Software Engineer',          'Consultant',              'Driver',
          'Shop Owner',               'Nurse',          'Accountant',
 'Government Employee',           'Architect',            'Engineer',
   'Real Estate Agent',       'Civil Servant',             'Plumber',
      'Retail Manager',                'Chef',         'Electrician',
           'Carpenter',              'Doctor',      'Lab Technician',
        'Data Analyst',              'Lawyer',      'Content Writer'],Field(...,description="What is your Occupation",examples=['Businessman','Banker'])]
    income_lpa:Annotated[float,Field(...,description="What is your income in Lakhs per annum",examples=[12.5,3.2])]
    smoker:Annotated[bool,Field(...,description="Does the user Smoke True or False Only")]

    city:Annotated[str,Field(...,description='Enter the city of user')]
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker or self.bmi > 27:
            return "Medium"

        return "Low"
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age<25:
            return "Young"
        elif self.age<30:
            return "Adult"
        elif self.age<60:
            return "Middle_aged"
        return "Senior"
    
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1 
        elif self.city in tier_2_cities:
            return 2 
        else:
            return 3
    

@app.get('/')
def home():
    return JSONResponse(status_code=200,content={"message":"This is a Insurance prediction API 💖"})

@app.post('/predict')
def predict_premium(data: UserInput):

    input_data = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    prediction = model.predict(input_data)

    return JSONResponse(
        status_code=200,
        content={
            "Prediction":prediction.tolist()
        }
    )