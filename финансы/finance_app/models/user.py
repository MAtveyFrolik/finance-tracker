import pandas as pd
from typing import List
from models.transaction import Transaction

class User:
    def __init__(self, username: str):
        self.username = username
        self.transactions: List[Transaction] = []
        self.budgets = {}
    
    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
    
    def get_transactions_dataframe(self) -> pd.DataFrame:
        """Конвертирует транзакции в Pandas DataFrame для анализа"""
        if not self.transactions:
            return pd.DataFrame()
        
        data = [t.to_dict() for t in self.transactions]
        df = pd.DataFrame(data)
        
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['amount'] = pd.to_numeric(df['amount'])
            # Для расходов делаем отрицательные значения
            df['signed_amount'] = df.apply(
                lambda x: -abs(x['amount']) if x['type'] == 'expense' else abs(x['amount']), 
                axis=1
            )
        
        return df
    
    def get_financial_summary(self) -> dict:
        """Возвращает финансовую сводку используя Pandas"""
        df = self.get_transactions_dataframe()
        
        if df.empty:
            return {"total_income": 0, "total_expense": 0, "balance": 0}
        
        income = df[df['type'] == 'income']['amount'].sum()
        expense = df[df['type'] == 'expense']['amount'].sum()
        
        return {
            "total_income": income,
            "total_expense": expense,
            "balance": income - expense
        }
    
    def save_data(self):
        from services.data_manager import DataManager
        data_manager = DataManager()
        data_manager.save_user(self)