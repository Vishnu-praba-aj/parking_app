from pydantic import BaseModel, validator

class UserModel(BaseModel):
    email: str
    age: int

    @validator('email')
    def email_must_have_at(cls, v):
        if '@' not in v:
            raise ValueError('must contain @')
        return v

    @validator('age')
    def age_positive(cls, v):
        if v < 0:
            raise ValueError('must be positive')
        return v