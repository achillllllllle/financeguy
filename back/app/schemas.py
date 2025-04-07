from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .models import RecurrenceFrequency

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: str
    is_general: bool = False

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    description: str
    type: str
    category_id: int
    is_recurrent: bool = False
    recurrence_frequency: Optional[RecurrenceFrequency] = None
    next_occurrence: Optional[datetime] = None
    is_confirmed: bool = True

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime
    user_id: int
    category: Category

    class Config:
        from_attributes = True

class ReminderBase(BaseModel):
    title: str
    description: str
    due_date: datetime
    amount: float

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    is_paid: bool
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 