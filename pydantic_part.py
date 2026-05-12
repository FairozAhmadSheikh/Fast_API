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
def insert_name_and_age(name:str,age:int):
    if type(name)==str and type(age) == int:
        print(name)
        print(age)
        print("inserted succesfully ")
    else:
        raise TypeError("Incorrect datatype")

insert_name_and_age("fairoz",32)
# how pydantic solves it