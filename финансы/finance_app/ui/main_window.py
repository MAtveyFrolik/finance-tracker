import tkinter as tk
from tkinter import ttk
from ui.transaction_frame import TransactionFrame
from ui.reports_frame import ReportsFrame

class MainWindow(tk.Frame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user = user
        self.on_logout = on_logout
        
        self.create_widgets()
        self.show_summary()
    
    def create_widgets(self):
        # Верхняя панель с информацией о пользователе и балансом
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Информация о пользователе
        user_info = ttk.Label(top_frame, text=f"Пользователь: {self.user.username}", 
                             font=("Arial", 10, "bold"))
        user_info.pack(side="left")
        
        # Баланс
        self.balance_label = ttk.Label(top_frame, text="", font=("Arial", 10, "bold"))
        self.balance_label.pack(side="right")
        
        # Кнопка выхода
        logout_btn = ttk.Button(top_frame, text="Выйти", command=self.on_logout)
        logout_btn.pack(side="right", padx=5)
        
        # Вкладки основного функционала
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка добавления транзакций
        self.transaction_tab = TransactionFrame(self.notebook, self.user, self.on_transaction_added)
        self.notebook.add(self.transaction_tab, text="Добавить транзакцию")
        
        # Вкладка отчетов
        self.reports_tab = ReportsFrame(self.notebook, self.user)
        self.notebook.add(self.reports_tab, text="Отчеты и аналитика")
    
    def show_summary(self):
        """Показывает текущий баланс"""
        summary = self.user.get_financial_summary()
        balance_text = f"Баланс: {summary['balance']:.2f} руб."
        
        # Разный цвет для положительного и отрицательного баланса
        if summary['balance'] >= 0:
            self.balance_label.config(text=balance_text, foreground="green")
        else:
            self.balance_label.config(text=balance_text, foreground="red")
    
    def on_transaction_added(self):
        """Обновляет интерфейс после добавления транзакции"""
        self.show_summary()
        # Обновляем отчеты
        if hasattr(self, 'reports_tab'):
            self.reports_tab.update_reports()