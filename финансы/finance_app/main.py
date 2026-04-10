import tkinter as tk
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("💰 Учет домашних финансов")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        self.current_user = None
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        self.login_frame = LoginWindow(self, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)
    
    def show_main_window(self):
        self.clear_window()
        self.main_frame = MainWindow(self, self.current_user, self.on_logout)
        self.main_frame.pack(fill="both", expand=True)
    
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
    
    def on_login_success(self, user):
        self.current_user = user
        self.show_main_window()
    
    def on_logout(self):
        self.current_user = None
        self.show_login()

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()