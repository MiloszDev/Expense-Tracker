import sqlite3

conn = sqlite3.connect('expense_tracker.db')

cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY,
        Date TEXT,
        amount REAL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        Date TEXT,
        description TEXT,
        category TEXT,
        price REAL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS category_budgets (
        id INTEGER PRIMARY KEY,
        category TEXT,
        budget REAL
    )
''')

conn.commit()
conn.close()