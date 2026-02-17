from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "job_tracker.db")

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


# ✅ This runs once when the app starts (works with Gunicorn)
with app.app_context():
    init_db()


@app.route("/")
def index():
    status = request.args.get("status", "All")
    conn = get_db()

    if status == "All":
        rows = conn.execute("SELECT * FROM applications ORDER BY id DESC").fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM applications WHERE status = ? ORDER BY id DESC",
            (status,),
        ).fetchall()

    conn.close()
    return render_template("index.html", apps=rows, status=status)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        company = request.form["company"].strip()
        role = request.form["role"].strip()
        location = request.form["location"].strip()
        status = request.form["status"].strip()
        notes = request.form.get("notes", "").strip()

        conn = get_db()
        conn.execute(
            """
            INSERT INTO applications (company, role, location, status, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company, role, location, status, notes),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:app_id>", methods=["POST"])
def delete(app_id):
    conn = get_db()
    conn.execute("DELETE FROM applications WHERE id = ?", (app_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
