from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.auth.dependencies import get_current_user
from app.models import NewTask, Task, UpdateTask
from app.repository.postgres import PostgresTaskRepository
from app.service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"], 
    dependencies=[Depends(get_current_user)],        #verify authentication first before rnning route
)

repository = PostgresTaskRepository()
service = TaskService(repository)


@router.get("", response_model=list[Task])
def list_tasks(current_user=Depends(get_current_user)) -> list[Task]:
    return service.list_tasks(str(current_user.id))


@router.get("/{id}", response_model=Task)
def get_task(id: int, current_user=Depends(get_current_user)) -> Task:
    try:
        return service.get_task(
            id,
            str(current_user.id),
        )
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found",
        )


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def add_task(new_task: NewTask, current_user=Depends(get_current_user)) -> Task:
    return service.add_task(
        new_task,
        str(current_user.id),
    )


@router.put("/{id}", response_model=Task)
def replace_task(id: int, update: UpdateTask, current_user=Depends(get_current_user)) -> Task:
    try:
        return service.replace_task(
            id,
            update,
            str(current_user.id),
        )
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found",
        )


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, current_user=Depends(get_current_user)):
    try:
        service.delete_task(
            id,
            str(current_user.id),
        )
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {id} not found",
        )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    ) 
    
    
    
    
    
    
    
    