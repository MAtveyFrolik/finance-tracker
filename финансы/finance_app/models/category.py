class Category:
    def __init__(self, name: str, type_: str, color: str = "#007acc"):
        self.name = name
        self.type = type_  # "income" или "expense"
        self.color = color

class CategoryManager:
    def __init__(self):
        self.income_categories = [
            Category("Зарплата", "income", "#2ecc71"),
            Category("Фриланс", "income", "#27ae60"),
            Category("Инвестиции", "income", "#3498db"),
            Category("Подарки", "income", "#9b59b6")
        ]
        
        self.expense_categories = [
            Category("Продукты", "expense", "#e74c3c"),
            Category("Транспорт", "expense", "#e67e22"),
            Category("Жилье", "expense", "#f39c12"),
            Category("Развлечения", "expense", "#d35400"),
            Category("Здоровье", "expense", "#c0392b"),
            Category("Одежда", "expense", "#8e44ad")
        ]
        
        self.all_categories = self.income_categories + self.expense_categories
    
    def get_categories_by_type(self, type_: str) -> list[Category]:
        return [cat for cat in self.all_categories if cat.type == type_]
    
    def get_category_by_name(self, name: str) -> Category:
        return next((cat for cat in self.all_categories if cat.name == name), None)