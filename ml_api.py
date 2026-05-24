from fastapi import FastAPI,Path,HTTPException
from pydantic import BaseModel,Field,computed_field
from typing import Optional,Literal,Annotated
import pickle
from fastapi.responses import JSONResponse

app=FastAPI()

# Load Model first
with open('model.pkl','rb')as f:
    pickle.load(f)

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
    weight:Annotated[float,Field(...,description='Weight in Kgs')]
    height:Annotated[float,Field(...,description='Enter height in Meters')]
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
    income_lpa:Annotated[str,Field(...,description="What is your income in Lakhs per annum",examples=[12.5,3.2])]
    smoker:Annotated[bool,Field(...,description="Does the user Smoke True or False Only")]

    city:Annotated[str,Field(...,description='Enter the city of user')]
    
    @computed_field
    @property
    def bmi(self):
        return round(self.weight/(self.height**2),2)
    

    

@app.get('/')
def home():
    JSONResponse(status_code=200,content={"message":"This is a Insurance prediction API 💖"})