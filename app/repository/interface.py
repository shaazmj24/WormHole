from abc import ABC , abstractmethod 
from app.models import UpdateTask, NewTask, Task

class TaskRepository(ABC): 
    @abstractmethod 
    def list_tasks(self , user_id: str) -> list[Task]: 
        pass   
    
    @abstractmethod
    def get_task(self, id : int , user_id: str) -> Task:
        pass
    
    @abstractmethod 
    def add_task(self, task: NewTask, user_id: str) -> Task: 
        pass 
    
    @abstractmethod 
    def replace_task(self, id : int , update: UpdateTask, user_id: str) -> Task: 
        pass
    
    @abstractmethod 
    def delete_task(self, id: int , user_id: str) -> None: 
        pass
    
    
    
    

