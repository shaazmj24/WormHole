from app.models import Task, NewTask, UpdateTask
from app.repository.interface import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def list_tasks(self, user_id: str) -> list[Task]:
        return self.repository.list_tasks(user_id) 
    
    def get_task(self, id : int, user_id: str) -> Task: 
        return self.repository.get_task(id, user_id)

    def add_task(self, task: NewTask, user_id:str) -> Task:
        return self.repository.add_task(task, user_id)   
    
    def replace_task(self, id : int , update: UpdateTask, user_id: str) -> Task: 
        return self.repository.replace_task(id, update, user_id) 
    
    def delete_task(self, id : int, user_id: str) -> None: 
        self.repository.delete_task(id, user_id) 


    
    
    