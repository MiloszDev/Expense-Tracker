import sqlite3
import os
conn = sqlite3.connect('expense_tracker.db')

cur = conn.cursor()
def color_text(text, color):
    if color == 'green':
        return f"\033[92m{text}\033[0m"
    elif color == 'yellow':
        return f"\033[93m{text}\033[0m"
    elif color == 'red':
        return f"\033[91m{text}\033[0m"
    else:
        return text

# Function to add income
def add_income():
    date = input('Enter the date (YYYY-MM-DD):\n>> ')
    amount = float(input('Enter the amount of income:\n>> '))
    cur.execute('INSERT INTO income (Date, amount) VALUES (?, ?)', (date, amount))
    conn.commit()
    print(f'Income of {amount} added!')
    enter = input('Type Enter to continue...')
# Function to add an expense
def add_expense():
    date = input('Enter the date (YYYY-MM-DD):\n>> ')
    description = input('Enter the description of the expense:\n>> ')

    # Fetch and display categories
    cur.execute('SELECT DISTINCT category FROM category_budgets')
    categories = cur.fetchall()
    
    print('Select a category by number:')
    for idx, category in enumerate(categories):
        print(f'{idx + 1}. {category[0]}')
    print(f'{len(categories) + 1}. Create a new category')

    category_choice = int(input('>> '))
    if category_choice == len(categories) + 1:
        category = input('Enter a new category name:\n>> ')
        budget = float(input(f'Set a monthly budget for {category}:\n>> '))
        cur.execute('INSERT INTO category_budgets (category, budget) VALUES (?, ?)', (category, budget))
    else:
        category = categories[category_choice - 1][0]

    price = float(input('Enter the price of the expense:\n>> '))
    cur.execute('INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)', (date, description, category, price))
    
    conn.commit()
    print(f'Expense of {price} for {description} added to {category}!')
    enter = input('Type Enter to continue...')
def view_monthly_expenses():
    month = input('Enter the month (MM):\n>> ')
    year = input('Enter the year (YYYY):\n>> ')

    cur.execute("SELECT description, category, price FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
    expenses = cur.fetchall()
    os.system('cls')
    print("\n--- Monthly Expenses ---")
    for expense in expenses:
        print(f"{expense[0]} | Category: {expense[1]} | Price: {expense[2]}")

    cur.execute("SELECT category, SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ? GROUP BY category", (month, year))
    category_totals = cur.fetchall()
    print("\n--- Category Totals and Budgets ---")
    for category, total in category_totals:
        cur.execute('SELECT budget FROM category_budgets WHERE category = ?', (category,))
        budget = cur.fetchone()
        if budget:
            budget = budget[0]
            if total < 0.8 * budget:
                color = 'green'
            elif 0.8 * budget <= total <= budget:
                color = 'yellow'
            else:
                color = 'red'

            print(f"Category: {category} | Total Spent: {color_text(total, color)} | Budget: {budget}")
        else:
            print(f"Category: {category} | Total Spent: {total} (No budget set)")

    cur.execute("SELECT SUM(amount) FROM income WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
    total_income = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(price) FROM expenses WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?", (month, year))
    total_expenses = cur.fetchone()[0] or 0

    balance = total_income - total_expenses

    print("\n--- Income vs Expenses ---")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")

    if balance >= 0:
        print(f"Balance: {color_text(balance, 'green')}")
    else:
        print(f"Balance: {color_text(balance, 'red')}")
    enter = input('Type Enter to continue...')
while True:
    os.system('cls')
    print('\nSelect an option:')
    print('1. Add Income')
    print('2. Add Expense')
    print('3. View Monthly Expenses and Budgets')
    print('4. Exit')

    choice = int(input('\n>> '))

    if choice == 1:
        add_income()
    elif choice == 2:
        add_expense()
    elif choice == 3:
        view_monthly_expenses()
    elif choice == 4:
        print("Exiting the program.")
        break
    else:
        print("Invalid choice, please try again.")

cur.close()
conn.close()
