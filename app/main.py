from fastapi import FastAPI 
from app.routers.tasks import router as tasks_router 
from app.routers.auth import router as auth_router 
from app.routers.protected import router as protected_router


app = FastAPI()   
app.include_router(tasks_router) 
app.include_router(auth_router) 

@app.get("/") 
def root():  
    ms = { 
          "name": "Task API", 
          "version": "1.0", 
          "endpoints": ["/tasks"]  
          } 
    return ms 

@app.get("/health") 
def health(): 
    return {"status" : "ok"} 


