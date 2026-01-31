from flask import Flask, render_template, request, redirect, url_for, session, flash
from expense import Expense
import storage
import users
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# Initialize tables
storage.create_table()
users.create_users_table()


# 🔐 Login-required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


# ================= AUTH ROUTES =================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        existing_user = users.get_user_by_email(email)
        if existing_user:
            flash("User already exists. Please login.", "error")
            return redirect(url_for("login"))

        password_hash = generate_password_hash(password)
        user_id = users.create_user(email, password_hash)

        # store user in session
        session["user_id"] = user_id
        session["user_email"] = email

        flash("Account created successfully 🎉", "success")
        return redirect(url_for("index"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = users.get_user_by_email(email)

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_email"] = user["email"]
            flash("Login successful 🎉", "success")
            return redirect(url_for("index"))

        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully 👋", "success")
    return redirect(url_for("index"))


# ================= MAIN APP =================

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    summary_result = None
    summary_type = None

    if request.method == "POST":

        # 📊 Summary dropdown
        if "summary_type" in request.form:
            summary_type = request.form["summary_type"]
            today = date.today()

            if summary_type == "daily":
                value = today.strftime("%Y-%m-%d")
            elif summary_type == "monthly":
                value = today.strftime("%Y-%m")
            else:
                value = today.strftime("%Y")

            summary_result = storage.get_total_by_type_and_user(
                summary_type, value, user_id
            )

        # ➕ Add expense
        else:
            date_val = request.form["date"]
            category = request.form["category"]
            amount = float(request.form["amount"])
            description = request.form["description"] or "-"

            expense = Expense(
                user_id,          # ✅ CORRECT USER ID
                date_val,
                category,
                amount,
                description
            )

            storage.add_expense(expense)
            flash("Expense added ✅", "success")
            return redirect(url_for("index"))

    expenses = storage.get_expenses_by_user(user_id)
    category_totals = storage.get_category_totals_by_user(user_id)

    return render_template(
        "index.html",
        expenses=expenses,
        edit_expense=None,
        category_totals=category_totals,
        summary_result=summary_result,
        summary_type=summary_type
    )


# ================= EDIT / DELETE (STRICT OWNERSHIP) =================

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
@login_required
def edit(expense_id):
    user_id = session["user_id"]

    expense = storage.get_expense_by_id_and_user(expense_id, user_id)
    if not expense:
        flash("Unauthorized access ❌", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        date_val = request.form["date"]
        category = request.form["category"]
        amount = float(request.form["amount"])
        description = request.form["description"] or "-"

        storage.update_expense(
            expense_id,
            user_id,
            date_val,
            category,
            amount,
            description
        )

        flash("Expense updated successfully ✅", "success")
        return redirect(url_for("index"))

    expenses = storage.get_expenses_by_user(user_id)
    category_totals = storage.get_category_totals_by_user(user_id)

    return render_template(
        "index.html",
        expenses=expenses,
        edit_expense=expense,
        category_totals=category_totals,
        summary_result=None,
        summary_type=None
    )


@app.route("/delete/<int:expense_id>", methods=["POST"])
@login_required
def delete(expense_id):
    user_id = session["user_id"]

    expense = storage.get_expense_by_id_and_user(expense_id, user_id)
    if not expense:
        flash("Unauthorized delete attempt ❌", "error")
        return redirect(url_for("index"))

    storage.delete_expense(expense_id, user_id)  # ✅ FIX HERE
    flash("Expense deleted 🗑", "success")
    return redirect(url_for("index"))



# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)
