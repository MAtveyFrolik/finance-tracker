import tkinter as tk
from tkinter import ttk, messagebox
from services.data_manager import DataManager

class LoginWindow(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        self.data_manager = DataManager()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self, text="Учет домашних финансов", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Фрейм для формы
        form_frame = ttk.Frame(self)
        form_frame.pack(pady=20)
        
        # Поля ввода
        ttk.Label(form_frame, text="Логин:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Label(form_frame, text="Пароль:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Кнопки
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        self.login_btn = ttk.Button(button_frame, text="Войти", command=self.login)
        self.login_btn.pack(side="left", padx=5)
        
        self.register_btn = ttk.Button(button_frame, text="Регистрация", command=self.register)
        self.register_btn.pack(side="left", padx=5)
        
        # Привязка Enter к кнопке входа
        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = self.data_manager.load_user(username)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if self.data_manager.user_exists(username):
            messagebox.showerror("Ошибка", "Пользователь уже существует")
            return
        
        # Создаем нового пользователя
        from models.user import User
        new_user = User(username)
        self.data_manager.save_user(new_user)
        
        messagebox.showinfo("Успех", "Пользователь зарегистрирован!")
        self.on_login_success(new_user)