import sqlite3


def create_database():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY,
        amount REAL,
        name TEXT,
        city TEXT,
        date DATE
    )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY,
        amount REAL
    )"""
    )

    cur.execute("SELECT COUNT(*) FROM balance")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO balance (amount) VALUES (0.0)")

    conn.commit()
    conn.close()


def insert_expense(amount, name, city, date):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    date = date.strftime("%d/%m")
    cur.execute(
        "INSERT INTO expenses (amount, name, city, date) VALUES (?, ?, ?, ?)",
        (amount, name, city, date),
    )
    conn.commit()
    conn.close()


def update_expense(id, amount, name, city, date):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    date = date.strftime("%d/%m")
    cur.execute(
        "UPDATE expenses SET amount = ?, name = ?, city = ?, date = ? WHERE id = ?",
        (amount, name, city, date, id),
    )
    conn.commit()
    conn.close()


def delete_expense(id):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()


def fetch_expenses():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")
    expenses = cur.fetchall()
    conn.close()
    return expenses


def update_balance(new_balance):
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("UPDATE balance SET amount = ?", (new_balance,))
    conn.commit()
    conn.close()


def fetch_balance():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT amount FROM balance LIMIT 1")
    balance = cur.fetchone()
    conn.close()
    return balance[0] if balance else 0


def total_expenses():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()
    conn.close()
    return total[0] if total and total[0] else 0
