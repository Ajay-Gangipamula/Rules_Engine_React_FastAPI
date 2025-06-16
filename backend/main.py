from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_sample_transactions(num_transactions=50):
    merchants = ["Amazon", "Best Buy", "Walmart", "Target", "Apple Store", "Unknown"]
    for _ in range(num_transactions):
        amount = round(random.uniform(10, 2000), 2)
        merchant = random.choice(merchants)
        credit_card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
        yield {
            "amount": amount,
            "merchant": merchant,
            "credit_card_number": credit_card_number,
            "timestamp": timestamp
        }

@app.post("/generate-sample-data/")
def create_sample_data(db: Session = Depends(get_db)):
    for transaction in generate_sample_transactions():
        crud.create_transaction(db, schemas.TransactionCreate(**transaction))
    return {"message": "Sample data created"}

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_transactions(db, skip=skip, limit=limit)

@app.post("/rules/", response_model=schemas.Rule)
def create_rule(rule: schemas.RuleCreate, db: Session = Depends(get_db)):
    return crud.create_rule(db=db, rule=rule)

@app.get("/rules/", response_model=List[schemas.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rules(db, skip=skip, limit=limit)

@app.post("/apply-rules/")
def apply_rules(db: Session = Depends(get_db)):
    return crud.apply_rules(db)

@app.delete("/rules/{rule_id}")
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    return crud.delete_rule(db, rule_id)