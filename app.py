from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?", (u, p))
        user = cur.fetchone()
        con.close()

        if user:
            session["user"] = u
            return redirect("/dashboard")

    return render_template("index.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]
    con.close()

    return render_template("dashboard.html", total_students=total_students)


# ================= STUDENTS =================
@app.route("/students", methods=["GET", "POST"])
def students():
    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()

    # Add student
    if request.method == "POST":
        cur.execute(
            "INSERT INTO students (name, rollno, branch, year) VALUES (?, ?, ?, ?)",
            (
                request.form["name"],
                request.form["rollno"],
                request.form["branch"],
                request.form["year"]
            )
        )
        con.commit()

    # Search student
    search = request.args.get("search")
    if search:
        cur.execute("""
            SELECT * FROM students
            WHERE name LIKE ? OR rollno LIKE ?
        """, (f"%{search}%", f"%{search}%"))
    else:
        cur.execute("SELECT * FROM students")

    data = cur.fetchall()
    con.close()

    return render_template("students.html", students=data)


# ================= DELETE =================
@app.route("/delete/<int:id>")
def delete_student(id):
    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()

    return redirect("/students")


# ================= EDIT =================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if "user" not in session:
        return redirect("/")

    con = get_db()
    cur = con.cursor()

    if request.method == "POST":
        cur.execute("""
            UPDATE students
            SET name=?, rollno=?, branch=?, year=?
            WHERE id=?
        """, (
            request.form["name"],
            request.form["rollno"],
            request.form["branch"],
            request.form["year"],
            id
        ))

        con.commit()
        con.close()
        return redirect("/students")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    con.close()

    return render_template("edit.html", student=student)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)