import json
import os
from models.user import User
from models.transaction import Transaction
from models.category import CategoryManager

class DataManager:
    def __init__(self):
        self.data_file = "finance_data.json"
        self.category_manager = CategoryManager()
    
    def load_users(self):
        if not os.path.exists(self.data_file):
            return {}
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def save_user(self, user):
        try:
            users_data = self.load_users()
            
            user_data = {
                "username": user.username,
                "transactions": [t.to_dict() for t in user.transactions],
                "budgets": user.budgets
            }
            
            users_data[user.username] = user_data
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
            return False
    
    def load_user(self, username):
        users_data = self.load_users()
        if username not in users_data:
            return None
        
        user_data = users_data[username]
        user = User(username)
        
        for t_data in user_data.get("transactions", []):
            category = self.category_manager.get_category_by_name(t_data["category"])
            if category:
                from datetime import datetime
                transaction = Transaction(
                    amount=float(t_data["amount"]),
                    category=category,
                    date=datetime.fromisoformat(t_data["date"]),
                    description=t_data.get("description", "")
                )
                user.add_transaction(transaction)
        
        user.budgets = user_data.get("budgets", {})
        return user
    
    def user_exists(self, username):
        return username in self.load_users()