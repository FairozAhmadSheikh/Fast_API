from fastapi import FastAPI,Path,HTTPException

app= FastAPI()

@app.get('/')
def home():
    return "API is Made with 💖"

# what issue looks like 
def insert_patient_data(name:str,age:int):
    """
    This function will accept age as a string also this means no type checking and validation
    """
    print(name)
    print(age)
    print("Insrted sUCcessfully")
    
insert_patient_data("feroz","thiry two")

# how we can solve issue 


# how pydantic solves it