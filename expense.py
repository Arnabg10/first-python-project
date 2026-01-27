class Expense:
    def __init__(self, user_id, date, category, amount, description=""):
        self.user_id = user_id
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
