
import os

from flask import Flask, flash, redirect, render_template, request, url_for

import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "dev-secret-change-me"
)


# =========================
# Database Configuration
# =========================

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "database": os.getenv("POSTGRES_DB", "expenses"),
    "user": os.getenv("POSTGRES_USER", "expenseuser"),
    "password": os.getenv("POSTGRES_PASSWORD", "expensepass"),
}


# =========================
# Database Connection
# =========================

def get_connection():
    return psycopg2.connect(**DB_CONFIG)


# =========================
# Initialize Database
# =========================

def init_db():

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS expenses (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(120) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
                    expense_date DATE NOT NULL
                );
                """
            )

            cur.execute("SELECT COUNT(*) FROM expenses;")

            count = cur.fetchone()[0]

            if count == 0:

                sample_data = [
                    ("Lunch", "Food", 180),
                    ("Bus fare", "Transport", 60),
                    ("Internet bill", "Bills", 850),
                ]

                cur.executemany(
                    """
                    INSERT INTO expenses
                    (title, category, amount, expense_date)
                    VALUES (%s, %s, %s, CURRENT_DATE);
                    """,
                    sample_data
                )

        conn.commit()

    finally:

        conn.close()


# =========================
# Home Page
# =========================

@app.route("/")
def index():

    conn = get_connection()

    try:

        with conn.cursor(cursor_factory=RealDictCursor) as cur:

            # Total expense and number of expenses

            cur.execute(
                """
                SELECT
                    COALESCE(SUM(amount), 0) AS total,
                    COUNT(*) AS count
                FROM expenses;
                """
            )

            summary = cur.fetchone()


            # Category summary

            cur.execute(
                """
                SELECT
                    category,
                    SUM(amount) AS total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC;
                """
            )

            categories = cur.fetchall()


            # Expense list

            cur.execute(
                """
                SELECT
                    id,
                    title,
                    category,
                    amount,
                    expense_date
                FROM expenses
                ORDER BY expense_date DESC, id DESC;
                """
            )

            expenses = cur.fetchall()

    finally:

        conn.close()


    return render_template(
        "index.html",
        summary=summary,
        categories=categories,
        expenses=expenses
    )


# =========================
# Add Expense
# =========================

@app.route("/add", methods=["POST"])
def add_expense():

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    amount = request.form.get("amount", "").strip()
    expense_date = request.form.get("expense_date", "").strip()


    if not title or not category or not amount or not expense_date:

        flash(
            "Please fill in all fields.",
            "error"
        )

        return redirect(url_for("index"))


    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        flash(
            "Amount must be a positive number.",
            "error"
        )

        return redirect(url_for("index"))


    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO expenses
                (title, category, amount, expense_date)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    title,
                    category,
                    amount,
                    expense_date
                )
            )

        conn.commit()

    finally:

        conn.close()


    flash(
        "Expense added successfully.",
        "success"
    )

    return redirect(url_for("index"))


# =========================
# Delete Expense
# =========================

@app.route(
    "/delete/<int:expense_id>",
    methods=["POST"]
)
def delete_expense(expense_id):

    conn = get_connection()

    try:

        with conn.cursor() as cur:

            cur.execute(
                "DELETE FROM expenses WHERE id = %s;",
                (expense_id,)
            )

        conn.commit()

    finally:

        conn.close()


    flash(
        "Expense deleted successfully.",
        "success"
    )

    return redirect(url_for("index"))


# =========================
# Health Check
# =========================

@app.route("/health")
def health():

    try:

        conn = get_connection()

        try:

            with conn.cursor() as cur:

                cur.execute("SELECT 1;")

            return {
                "status": "healthy",
                "database": "connected"
            }

        finally:

            conn.close()

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }, 500


# =========================
# Run Application
# =========================

if __name__ == "__main__":

    # Create database table before starting Flask
    init_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

