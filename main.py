from fastapi import FastAPI
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


@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient Records "}


def load_data():
    with open ('patient.json','r') as f :
        data=json.load(f)
    return data

@app.get('/view')    
def view():
    data=load_data()

    return data
