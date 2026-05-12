from fastapi import FastAPI,Path,HTTPException

app= FastAPI()

@app.get('/')
def home():
    return "API is Made with 💖"

# what issue looks like 


# how we can solve issue 


# how pydantic solves it