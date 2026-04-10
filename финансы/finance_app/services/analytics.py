import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from models.user import User
from typing import List, Dict
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsService:
    def __init__(self, user: User):
        self.user = user
    
    def get_spending_by_category(self, period: str = 'month') -> pd.Series:
        """Анализ расходов по категориям с использованием Pandas"""
        df = self.user.get_transactions_dataframe()
        
        if df.empty:
            return pd.Series()
        
        # Фильтрация по периоду
        now = datetime.now()
        if period == 'month':
            start_date = now - timedelta(days=30)
        elif period == 'week':
            start_date = now - timedelta(days=7)
        else:
            start_date = df['date'].min()
        
        filtered_df = df[df['date'] >= start_date]
        expense_df = filtered_df[filtered_df['type'] == 'expense']
        
        if expense_df.empty:
            return pd.Series()
        
        return expense_df.groupby('category')['amount'].sum()
    
    def get_income_vs_expense(self) -> Dict[str, float]:
        """Сравнение доходов и расходов"""
        df = self.user.get_transactions_dataframe()
        
        if df.empty:
            return {"income": 0, "expense": 0}
        
        income = df[df['type'] == 'income']['amount'].sum()
        expense = df[df['type'] == 'expense']['amount'].sum()
        
        return {"income": income, "expense": expense}
    
    def create_pie_chart(self, parent, period: str = 'month'):
        """Создает круговую диаграмму расходов в Tkinter"""
        spending_data = self.get_spending_by_category(period)
        
        if spending_data.empty:
            # Создаем пустой график если нет данных
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, 'Нет данных о расходах', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, fontsize=12)
            ax.set_title('Расходы по категориям')
        else:
            fig, ax = plt.subplots(figsize=(6, 4))
            colors = ['#e74c3c', '#e67e22', '#f39c12', '#d35400', '#c0392b', '#8e44ad']
            
            wedges, texts, autotexts = ax.pie(
                spending_data.values, 
                labels=spending_data.index,
                autopct='%1.1f%%',
                colors=colors[:len(spending_data)]
            )
            
            ax.set_title(f'Расходы по категориям ({period})')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas.get_tk_widget()
    
    def create_income_expense_chart(self, parent):
        """Создает столбчатую диаграмму доходов vs расходов"""
        data = self.get_income_vs_expense()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        
        categories = ['Доходы', 'Расходы']
        values = [data['income'], data['expense']]
        colors = ['#2ecc71', '#e74c3c']
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        ax.set_title('Доходы vs Расходы')
        ax.set_ylabel('Сумма (руб)')
        
        # Добавляем подписи значений
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                   f'{value:.2f}', ha='center', va='bottom')
        
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        return canvas.get_tk_widget()
    
    def generate_economy_tips(self) -> List[str]:
        """Генерирует советы по экономии на основе анализа данных"""
        tips = []
        summary = self.user.get_financial_summary()
        spending = self.get_spending_by_category()
        
        # Анализ с использованием Pandas
        df = self.user.get_transactions_dataframe()
        
        if not df.empty:
            # Анализ баланса
            if summary['balance'] < 0:
                tips.append("🚨 Внимание! Ваши расходы превышают доходы. Срочно пересмотрите бюджет!")
            
            # Анализ крупнейших категорий расходов
            if not spending.empty:
                max_spending = spending.nlargest(2)
                for category, amount in max_spending.items():
                    tips.append(f"💰 Самые большие расходы: {category} - {amount:.2f} руб.")
            
            # Анализ регулярности доходов
            income_dates = df[df['type'] == 'income']['date']
            if len(income_dates) > 1:
                date_diff = (income_dates.max() - income_dates.min()).days
                if date_diff > 60 and len(income_dates) < 3:
                    tips.append("💡 Рекомендуем найти дополнительные источники дохода")
        
        # Общие советы
        if not tips:
            tips.extend([
                "✅ Отличная работа! Ваши финансы в порядке.",
                "💡 Совет: Откладывайте 10-20% от каждого дохода",
                "💡 Совет: Планируйте бюджет на месяц вперед"
            ])
        else:
            tips.extend([
                "💡 Совет: Ведите учет всех ежедневных расходов",
                "💡 Совет: Установите лимиты по категориям расходов"
            ])
        
        return tips