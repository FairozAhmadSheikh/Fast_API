from fastapi import FastAPI , Path , HTTPException
import json
"""
    The app would be designed something like a place where a doctor stores his patient data
    and he is able to :
                1 create a Record for a new patient
                2 retrieve a patients and all all patients 
                3 Modify existing patient 
                4 Delete the paient 
"""

app= FastAPI()

@app.get("/")
def hello():
    return {'message':"Patient Management System API ! "}

# route to display about page
@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient Records "}

# Load data from JSON
def load_data():
    with open ('patient.json','r') as f :
        data=json.load(f)
    return data

# Route to display all data
@app.get('/view')    
def view():
    data=load_data()

    return data

# Route to obtain patient data using patient id 

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        return{"error":"Patient not found "}
    
# Route with status code 

@app.get('/pateint/{patient_id}')
def get_pateint(patient_id:str=Path(...,description="ID Of the patient in the Database ",example='P001')):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404,detail="Patient not found")
