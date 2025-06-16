from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    amount: float
    merchant: str
    credit_card_number: str
    timestamp: datetime

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    is_fraudulent: bool

    class Config:
        orm_mode = True

class RuleBase(BaseModel):
    name: str
    condition: str
    action: str

class RuleCreate(RuleBase):
    pass

class Rule(RuleBase):
    id: int

    class Config:
        orm_mode = True