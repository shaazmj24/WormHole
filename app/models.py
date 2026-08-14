from pydantic import BaseModel, Field, field_validator , EmailStr


class TaskTitle(BaseModel):                             #data validation and serialization
    title: str = Field(min_length=1, max_length=200)

    @field_validator("title")                           #when validating title, call title_not_blank fucntion 
    @classmethod
    def title_not_blank(cls, value: str) -> str:         #object itself = cls (self)
        cleaned_title = value.strip()

        if not cleaned_title:
            raise ValueError("Title cannot be blank.")

        return cleaned_title


class NewTask(TaskTitle):
    done: bool = False


class UpdateTask(TaskTitle):
    done: bool


class Task(TaskTitle):
    id: int = Field(ge=1)
    done: bool 
    
    
class AuthRequest(BaseModel):
    email: EmailStr
    password: str
    
    
