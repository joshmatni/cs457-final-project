import matplotlib.pyplot as plt

def plot_expense_breakdown(expenses):
    categories = [x[0] for x in expenses]
    amounts = [float(x[1]) for x in expenses if x[1] is not None]

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Breakdown by Category")
    plt.show()
