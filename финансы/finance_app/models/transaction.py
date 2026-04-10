import pandas as pd
from datetime import datetime
from typing import Optional

class Transaction:
    def __init__(self, amount: float, category, date: Optional[datetime] = None, description: str = ""):
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now()
        self.description = description
    
    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category.name,
            "date": self.date.isoformat(),
            "description": self.description,
            "type": self.category.type
        }
    
    def __repr__(self):
        return f"Transaction({self.amount}, {self.category.name}, {self.date})"