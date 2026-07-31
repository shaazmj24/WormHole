from fastapi import FastAPI, HTTPException, Response, status
from app.models import NewTask, Task, UpdateTask
from app.repository.postgres import PostgresTaskRepository
from app.service import TaskService  

app = FastAPI()   
repository = PostgresTaskRepository()
service = TaskService(repository) 


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

@app.get("/tasks", response_model=list[Task])    
def list_tasks() -> list[Task]: 
    return service.list_tasks()

@app.get("/tasks/{id}", response_model=Task)        #response_model validates output/response 
def get_task(id : int) -> Task:      
    try: 
        return service.get_task(id)                  #returns Task Object which fastapi converts it into json  
    except LookupError: 
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {id} not found" 
        )

@app.post("/tasks" , response_model=Task , status_code=status.HTTP_201_CREATED) 
def add_task(new_task : NewTask) -> Task:   
    return service.add_task(new_task)
    
@app.put("/tasks/{id}" , response_model=Task) 
def replace_task(id : int, update: UpdateTask) -> Task:       
    try: 
        return service.replace_task(id , update)
    except LookupError: 
        raise HTTPException(  
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {id} not found"
                            )

@app.delete("/tasks/{id}" , status_code=status.HTTP_204_NO_CONTENT) 
def delete_task(id : int):      
    try:
        service.delete_task(id)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    

