import tkinter as tk
from tkinter import ttk
from services.analytics import AnalyticsService

class ReportsFrame(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.analytics = AnalyticsService(user)
        
        self.create_widgets()
        self.update_reports()
    
    def create_widgets(self):
        # Вкладки для разных отчетов
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Вкладка с графиками
        self.charts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_frame, text="Графики")
        
        # Вкладка с советами
        self.tips_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tips_frame, text="Советы по экономии")
        
        # Создаем содержимое вкладок
        self.create_charts_tab()
        self.create_tips_tab()
    
    def create_charts_tab(self):
        # Фрейм для управления периодом
        control_frame = ttk.Frame(self.charts_frame)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(control_frame, text="Период:").pack(side="left")
        self.period_var = tk.StringVar(value="month")
        period_combo = ttk.Combobox(control_frame, textvariable=self.period_var, 
                                   values=["week", "month", "all"], state="readonly")
        period_combo.pack(side="left", padx=5)
        period_combo.bind('<<ComboboxSelected>>', self.update_reports)
        
        # Фрейм для графиков
        charts_container = ttk.Frame(self.charts_frame)
        charts_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Левый график - расходы по категориям
        self.left_chart_frame = ttk.Frame(charts_container)
        self.left_chart_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Правый график - доходы vs расходы
        self.right_chart_frame = ttk.Frame(charts_container)
        self.right_chart_frame.pack(side="right", fill="both", expand=True, padx=5)
    
    def create_tips_tab(self):
        # Текстовая область для советов
        self.tips_text = tk.Text(self.tips_frame, wrap="word", width=80, height=20)
        scrollbar = ttk.Scrollbar(self.tips_frame, orient="vertical", command=self.tips_text.yview)
        self.tips_text.configure(yscrollcommand=scrollbar.set)
        
        self.tips_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка обновления советов
        update_btn = ttk.Button(self.tips_frame, text="Обновить советы", 
                               command=self.update_tips)
        update_btn.pack(pady=5)
    
    def update_reports(self, event=None):
        # Очищаем предыдущие графики
        for widget in self.left_chart_frame.winfo_children():
            widget.destroy()
        for widget in self.right_chart_frame.winfo_children():
            widget.destroy()
        
        # Создаем новые графики
        period = self.period_var.get()
        pie_chart = self.analytics.create_pie_chart(self.left_chart_frame, period)
        pie_chart.pack(fill="both", expand=True)
        
        bar_chart = self.analytics.create_income_expense_chart(self.right_chart_frame)
        bar_chart.pack(fill="both", expand=True)
        
        # Обновляем советы
        self.update_tips()
    
    def update_tips(self):
        tips = self.analytics.generate_economy_tips()
        
        self.tips_text.delete(1.0, tk.END)
        for tip in tips:
            self.tips_text.insert(tk.END, f"• {tip}\n\n")
        
        self.tips_text.config(state="normal")