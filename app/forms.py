from pydantic import BaseModel, Field, ValidationError


class SignupForm(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class LoginForm(BaseModel):
    username: str
    password: str
