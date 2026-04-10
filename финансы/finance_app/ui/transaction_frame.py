import tkinter as tk
from tkinter import ttk, messagebox
from models.transaction import Transaction
from services.data_manager import DataManager

class TransactionFrame(ttk.Frame):
    def __init__(self, parent, user, on_transaction_added):
        super().__init__(parent)
        self.user = user
        self.on_transaction_added = on_transaction_added
        self.data_manager = DataManager()
        self.category_manager = self.data_manager.category_manager
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title_label = ttk.Label(self, text="Добавить транзакцию", font=("Arial", 12, "bold"))
        title_label.pack(pady=10)
        
        # Фрейм формы
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=10, padx=20, fill="x")
        
        # Тип транзакции
        ttk.Label(form_frame, text="Тип:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.type_var = tk.StringVar(value="expense")
        type_frame = ttk.Frame(form_frame)
        type_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Radiobutton(type_frame, text="Расход", variable=self.type_var, 
                       value="expense", command=self.update_categories).pack(side="left")
        ttk.Radiobutton(type_frame, text="Доход", variable=self.type_var, 
                       value="income", command=self.update_categories).pack(side="left")
        
        # Категория
        ttk.Label(form_frame, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, width=25)
        self.category_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Сумма
        ttk.Label(form_frame, text="Сумма:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Описание
        ttk.Label(form_frame, text="Описание:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(form_frame)
        self.desc_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        
        # Кнопка добавления
        self.add_btn = ttk.Button(form_frame, text="Добавить транзакцию", command=self.add_transaction)
        self.add_btn.grid(row=4, column=1, padx=5, pady=10, sticky="e")
        
        # Обновляем категории при старте
        self.update_categories()
        
        # Привязка Enter
        self.amount_entry.bind('<Return>', lambda e: self.add_transaction())
        self.desc_entry.bind('<Return>', lambda e: self.add_transaction())
    
    def update_categories(self):
        """Обновляет список категорий в зависимости от типа транзакции"""
        current_type = self.type_var.get()
        categories = self.category_manager.get_categories_by_type(current_type)
        category_names = [cat.name for cat in categories]
        
        self.category_combo['values'] = category_names
        if category_names:
            self.category_combo.set(category_names[0])
    
    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category_name = self.category_var.get()
            description = self.desc_entry.get()
            
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительной")
                return
            
            category = self.category_manager.get_category_by_name(category_name)
            if not category:
                messagebox.showerror("Ошибка", "Выберите категорию")
                return
            
            # Создаем транзакцию
            transaction = Transaction(amount, category, description=description)
            self.user.add_transaction(transaction)
            self.data_manager.save_user(self.user)
            
            # Очищаем поля
            self.amount_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            
            messagebox.showinfo("Успех", "Транзакция добавлена!")
            self.on_transaction_added()
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму")