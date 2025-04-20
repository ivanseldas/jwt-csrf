from fastapi import FastAPI
from auth_router import router 

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"JWT Authentication Test"}