import os
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "database": os.getenv("POSTGRES_DB", "expenses"),
    "user": os.getenv("POSTGRES_USER", "expenseuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "expensepass"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(120) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    amount NUMERIC(10,2) NOT NULL CHECK (amount > 0),
                    expense_date DATE NOT NULL
                );
            """)
            cur.execute("SELECT COUNT(*) FROM expenses;")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    """INSERT INTO expenses
                       (title, category, amount, expense_date)
                       VALUES (%s, %s, %s, %s)""",
                    [
                        ("Lunch", "Food", 180, date.today()),
                        ("Bus fare", "Transport", 60, date.today()),
                        ("Internet bill", "Bills", 850, date.today()),
                    ],
                )
        conn.commit()
    finally:
        conn.close()


@app.route("/")
def index():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT COALESCE(SUM(amount), 0) AS total,
                       COUNT(*) AS count
                FROM expenses;
            """)
            summary = cur.fetchone()

            cur.execute("""
                SELECT category, COALESCE(SUM(amount), 0) AS total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC;
            """)
            categories = cur.fetchall()

            cur.execute("""
                SELECT id, title, category, amount, expense_date
                FROM expenses
                ORDER BY expense_date DESC, id DESC
                LIMIT 20;
            """)
            expenses = cur.fetchall()
    finally:
        conn.close()

    return render_template(
        "index.html", current_date=date.today().isoformat(),
        summary=summary,
        categories=categories,
        expenses=expenses,
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "").strip()
    expense_date = request.form.get("expense_date", "").strip()

    if not all([title, category, amount, expense_date]):
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))

    try:
        amount_value = float(amount)
        if amount_value <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "error")
        return redirect(url_for("index"))

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """INSERT INTO expenses
                   (title, category, amount, expense_date)
                   VALUES (%s, %s, %s, %s)""",
                (title, category, amount_value, expense_date),
            )
        conn.commit()
    finally:
        conn.close()

    flash("Expense added successfully.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        conn.commit()
    finally:
        conn.close()

    flash("Expense deleted.", "success")
    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy", "database": "connected"}, 200
    except Exception:
        return {"status": "unhealthy", "database": "disconnected"}, 503


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
