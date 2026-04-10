import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Простой класс для категорий
class Category:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

# Класс для транзакций
class Transaction:
    def __init__(self, amount, category, description=""):
        self.amount = amount
        self.category = category
        self.date = datetime.now()
        self.description = description
    
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category.name,
            "date": self.date.isoformat(),
            "description": self.description,
            "type": self.category.type
        }

# Класс пользователя
class User:
    def __init__(self, username):
        self.username = username
        self.transactions = []
    
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
    
    def get_balance(self):
        income = sum(t.amount for t in self.transactions if t.category.type == 'income')
        expense = sum(t.amount for t in self.transactions if t.category.type == 'expense')
        return income - expense

# Менеджер данных
class DataManager:
    def __init__(self):
        # Используем абсолютный путь к рабочему столу
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.data_file = os.path.join(desktop_path, "finance_data.json")
        self.categories = [
            Category("Зарплата", "income"),
            Category("Фриланс", "income"),
            Category("Продукты", "expense"),
            Category("Транспорт", "expense"),
            Category("Развлечения", "expense"),
            Category("Жилье", "expense")
        ]
    
    def save_user(self, user):
        try:
            data = {
                "username": user.username,
                "transactions": [t.to_dict() for t in user.transactions]
            }
            
            all_data = {}
            if os.path.exists(self.data_file):
                try:
                    with open(self.data_file, 'r', encoding='utf-8') as f:
                        all_data = json.load(f)
                except:
                    # Если файл поврежден, создаем новый
                    all_data = {}
            
            all_data[user.username] = data
            
            # Создаем папку если нужно
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            return False
    
    def load_user(self, username):
        if not os.path.exists(self.data_file):
            return None
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return None
        
        if username not in all_data:
            return None
        
        user_data = all_data[username]
        user = User(username)
        
        for t_data in user_data.get("transactions", []):
            category = next((c for c in self.categories if c.name == t_data["category"]), None)
            if category:
                transaction = Transaction(
                    amount=float(t_data["amount"]),
                    category=category,
                    description=t_data.get("description", "")
                )
                user.transactions.append(transaction)
        
        return user

# Главное приложение
class FinanceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("💰 Учет финансов")
        self.root.geometry("600x500")
        
        self.data_manager = DataManager()
        self.current_user = None
        
        self.show_login_screen()
    
    def show_login_screen(self):
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Заголовок
        title = tk.Label(self.root, text="Учет домашних финансов", font=("Arial", 16, "bold"))
        title.pack(pady=20)
        
        # Фрейм для формы
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        # Логин
        tk.Label(form_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = tk.Entry(form_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Пароль (для совместимости, но не используется)
        tk.Label(form_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = tk.Entry(form_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Кнопки
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Войти", command=self.login, width=10).pack(side="left", padx=5)
        tk.Button(button_frame, text="Регистрация", command=self.register, width=10).pack(side="left", padx=5)
        
        # Фокус на поле логина
        self.username_entry.focus()
    
    def login(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Ошибка", "Введите логин")
            return
        
        user = self.data_manager.load_user(username)
        if user:
            self.current_user = user
            self.show_main_screen()
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")
    
    def register(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Ошибка", "Введите логин")
            return
        
        # Проверяем, существует ли пользователь
        if self.data_manager.load_user(username):
            messagebox.showerror("Ошибка", "Пользователь уже существует")
            return
        
        try:
            # Создаем нового пользователя
            user = User(username)
            
            # Сохраняем пользователя
            if self.data_manager.save_user(user):
                self.current_user = user
                messagebox.showinfo("Успех", "Пользователь создан!")
                self.show_main_screen()
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить пользователя")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при регистрации: {str(e)}")
    
    def show_main_screen(self):
        # Очищаем окно
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Верхняя панель
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(top_frame, text=f"Пользователь: {self.current_user.username}", 
                font=("Arial", 10, "bold")).pack(side="left")
        
        self.balance_label = tk.Label(top_frame, text="", font=("Arial", 10, "bold"))
        self.balance_label.pack(side="right")
        
        tk.Button(top_frame, text="Выйти", command=self.show_login_screen).pack(side="right", padx=5)
        
        # Вкладки
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка транзакций
        transaction_frame = ttk.Frame(notebook)
        notebook.add(transaction_frame, text="Добавить транзакцию")
        self.create_transaction_tab(transaction_frame)
        
        # Вкладка отчета
        report_frame = ttk.Frame(notebook)
        notebook.add(report_frame, text="Отчет")
        self.create_report_tab(report_frame)
        
        self.update_balance()
        self.update_report()
    
    def create_transaction_tab(self, parent):
        # Очищаем фрейм
        for widget in parent.winfo_children():
            widget.destroy()
            
        tk.Label(parent, text="Тип:").pack(anchor="w", pady=5)
        
        self.type_var = tk.StringVar(value="expense")
        type_frame = tk.Frame(parent)
        type_frame.pack(fill="x", pady=5)
        
        tk.Radiobutton(type_frame, text="Расход", variable=self.type_var, value="expense").pack(side="left")
        tk.Radiobutton(type_frame, text="Доход", variable=self.type_var, value="income").pack(side="left")
        
        tk.Label(parent, text="Категория:").pack(anchor="w", pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(parent, textvariable=self.category_var, state="readonly")
        
        # Обновляем категории при смене типа
        def update_categories(*args):
            categories = [c.name for c in self.data_manager.categories if c.type == self.type_var.get()]
            self.category_combo['values'] = categories
            if categories:
                self.category_combo.set(categories[0])
        
        self.type_var.trace('w', update_categories)
        update_categories()  # Инициализация
        
        self.category_combo.pack(fill="x", pady=5)
        
        tk.Label(parent, text="Сумма:").pack(anchor="w", pady=5)
        self.amount_entry = tk.Entry(parent)
        self.amount_entry.pack(fill="x", pady=5)
        
        tk.Label(parent, text="Описание:").pack(anchor="w", pady=5)
        self.desc_entry = tk.Entry(parent)
        self.desc_entry.pack(fill="x", pady=5)
        
        tk.Button(parent, text="Добавить", command=self.add_transaction, bg="lightblue").pack(pady=10)
    
    def create_report_tab(self, parent):
        self.report_text = tk.Text(parent, wrap="word", height=15)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar.set)
        
        self.report_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        tk.Button(parent, text="Обновить отчет", command=self.update_report).pack(pady=5)
    
    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category_name = self.category_var.get()
            description = self.desc_entry.get()
            
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительной")
                return
            
            if not category_name:
                messagebox.showerror("Ошибка", "Выберите категорию")
                return
            
            category = next((c for c in self.data_manager.categories if c.name == category_name), None)
            if not category:
                messagebox.showerror("Ошибка", "Выберите категорию")
                return
            
            transaction = Transaction(amount, category, description)
            self.current_user.add_transaction(transaction)
            
            # Сохраняем данные
            if self.data_manager.save_user(self.current_user):
                self.amount_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
                messagebox.showinfo("Успех", "Транзакция добавлена!")
                
                self.update_balance()
                self.update_report()
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить транзакцию")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")
    
    def update_balance(self):
        balance = self.current_user.get_balance()
        balance_text = f"Баланс: {balance:.2f} руб."
        if balance >= 0:
            self.balance_label.config(text=balance_text, fg="green")
        else:
            self.balance_label.config(text=balance_text, fg="red")
    
    def update_report(self):
        self.report_text.delete(1.0, tk.END)
        
        balance = self.current_user.get_balance()
        income = sum(t.amount for t in self.current_user.transactions if t.category.type == 'income')
        expense = sum(t.amount for t in self.current_user.transactions if t.category.type == 'expense')
        
        report = f"""📊 ФИНАНСОВЫЙ ОТЧЕТ

Доходы: {income:.2f} руб.
Расходы: {expense:.2f} руб.
Баланс: {balance:.2f} руб.

ПОСЛЕДНИЕ ТРАНЗАКЦИИ:
"""
        
        # Показываем транзакции в обратном порядке (последние сначала)
        recent_transactions = self.current_user.transactions[-10:]  # Последние 10 транзакций
        for t in reversed(recent_transactions):
            type_icon = "⬆️" if t.category.type == 'income' else "⬇️"
            report += f"{type_icon} {t.date.strftime('%d.%m %H:%M')} - {t.category.name}: {t.amount:.2f} руб."
            if t.description:
                report += f" ({t.description})"
            report += "\n"
        
        # Советы
        report += "\n💡 СОВЕТЫ:\n"
        if balance < 0:
            report += "• Внимание! Расходы превышают доходы\n"
        if expense > income * 0.7 and income > 0:
            report += "• Слишком высокие расходы (>70% доходов)\n"
        if len(self.current_user.transactions) < 3:
            report += "• Добавьте больше транзакций для точного анализа\n"
        
        if balance >= 0 and (income == 0 or expense <= income * 0.7):
            report += "• Отличная работа! Финансы в порядке\n"
        
        self.report_text.insert(1.0, report)
    
    def run(self):
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = FinanceApp()
    app.run()