import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, date
from helpers import apology, login_required
import re
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded during development
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///database.db")

# Email validation regex pattern
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


@app.after_request
def after_request(response):
    """No caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show dashboard with daily summary"""
    # Get user's daily summary
    summary = db.execute(
        """SELECT * FROM
        daily_summary
        WHERE user_id = ?""",
        session["user_id"]
    )

    # Get today's food logs
    food_logs = db.execute("""
        SELECT f.name, fl.quantity, f.calories, f.carbs, f.protein, f.fat, f.serving_size
        FROM food_log fl
        JOIN foods f ON fl.food_id = f.id
        WHERE fl.user_id = ? AND fl.date = DATE('now')
        ORDER BY fl.logged_at DESC
    """, session["user_id"])

    # Get today's workout logs
    workout_logs = db.execute("""
        SELECT w.name, wl.duration_minutes, wl.calories_burnt
        FROM workout_log wl
        JOIN workouts w ON wl.workout_id = w.id
        WHERE wl.user_id = ? AND wl.date = DATE('now')
        ORDER BY wl.logged_at DESC
    """, session["user_id"])

    # Calculate net calories
    if summary:
        net_calories = summary[0]["total_calories_consumed"] - summary[0]["total_calories_burnt"]
    else:
        net_calories = 0
        summary = [{"total_calories_consumed": 0, "total_calories_burnt": 0,
                   "current_weight": None, "current_bmi": None}]

    return render_template("index.html", summary=summary[0], food_logs=food_logs, workout_logs=workout_logs, net_calories=net_calories)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Validate username
        username = request.form.get("username")
        # Validate email
        email = request.form.get("email")
        # Validate password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)
        if not email or not EMAIL_REGEX.match(email):
            return apology("must provide valid email", 400)
        if not password:
            return apology("must provide password", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("username already exists", 400)



        # Insert new user into database
        hash = generate_password_hash(password)
        try:
            user_id = db.execute(
                "INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
                username, email, hash
            )

            # Log user in automatically
            session["user_id"] = user_id
            flash("Registered successfully!")
            return redirect("/")

        except Exception as e:
            return apology("registration failed", 500)

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username / password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to dashboard
        flash("Welcome back!")
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    return redirect("/")


@app.route("/food", methods=["GET", "POST"])
@login_required
def food():
    """Track food intake"""
    if request.method == "POST":
        food_id = request.form.get("food_id")
        quantity = request.form.get("quantity")

        if not food_id or not quantity:
            return apology("must select food and quantity", 400)

        try:
            quantity = float(quantity)
            if quantity <= 0:
                return apology("quantity must be positive", 400)
        except ValueError:
            return apology("invalid quantity", 400)

        # Insert food log
        db.execute(
            "INSERT INTO food_log (user_id, food_id, quantity) VALUES (?, ?, ?)",
            session["user_id"], food_id, quantity
        )

        flash("Food added successfully!")
        return redirect("/")

    else:
        foods = db.execute("SELECT * FROM foods ORDER BY name")
        return render_template("food.html", foods=foods)


@app.route("/workout", methods=["GET", "POST"])
@login_required
def workout():
    """Track workout activities"""
    if request.method == "POST":
        workout_id = request.form.get("workout_id")
        duration = request.form.get("duration")

        if not workout_id or not duration:
            return apology("must select workout and duration", 400)

        try:
            duration = float(duration)
            if duration <= 0:
                return apology("duration must be positive", 400)
        except ValueError:
            return apology("invalid duration", 400)

        # Calculate calories burnt
        workout_data = db.execute( "SELECT calories_per_minute FROM workouts WHERE id = ?", workout_id)
        calories_burnt = workout_data[0]["calories_per_minute"] * duration

        # Insert workout log
        db.execute(
            "INSERT INTO workout_log (user_id, workout_id, duration_minutes, calories_burnt) VALUES (?, ?, ?, ?)", session["user_id"], workout_id, duration, calories_burnt)

        flash(f"Workout added! You have burned {calories_burnt:.1f} calories!")
        return redirect("/")

    else:
        # Get workouts by category
        categories = ['abs', 'shoulder', 'legs', 'chest', 'cardio', 'others']
        workouts_by_category = {}

        for category in categories:
            workouts_by_category[category] = db.execute("SELECT * FROM workouts WHERE category = ? ORDER BY name", category)

        return render_template("workout.html", workouts_by_category=workouts_by_category)


@app.route("/metrics", methods=["POST"])
@login_required
def metrics():
    weight = request.form.get("weight")
    height = request.form.get("height")

    try:
        weight = float(weight)
        height = float(height)
        if weight <= 0 or height <= 0:
            return apology("invalid measurements", 400)
    except (ValueError, TypeError):
        return apology("invalid measurements", 400)

    db.execute("INSERT INTO body_metrics (user_id, weight, height) VALUES (?, ?, ?)", session["user_id"], weight, height)

    flash("Huuray, body metrics updated!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show historical data"""
    weight_history = db.execute(
        "SELECT date, weight, bmi FROM body_metrics WHERE user_id = ? ORDER BY date DESC LIMIT 30",
        session["user_id"]
    )

    all_dates = db.execute("""
        SELECT DISTINCT date FROM food_log WHERE user_id = ?
        UNION
        SELECT DISTINCT date FROM workout_log WHERE user_id = ?
        ORDER BY date DESC
        LIMIT 30
    """, session["user_id"], session["user_id"])

    # Build calorie history for each date
    calorie_history = []

    for date_row in all_dates:
        date = date_row["date"]

        # Get food calories for this date
        food_data = db.execute("""
            SELECT SUM(fl.quantity * f.calories / f.serving_size) as total
            FROM food_log fl
            JOIN foods f ON fl.food_id = f.id
            WHERE fl.user_id = ? AND fl.date = ?
        """, session["user_id"], date)

        # Get workout calories for this date
        workout_data = db.execute("""
            SELECT SUM(calories_burnt) as total
            FROM workout_log
            WHERE user_id = ? AND date = ?
        """, session["user_id"], date)

        # Add to history
        calorie_history.append({
            "date": date,
            "calories_consumed": food_data[0]["total"] if food_data[0]["total"] else 0,
            "calories_burnt": workout_data[0]["total"] if workout_data[0]["total"] else 0
        })

    return render_template("history.html",
                         weight_history=weight_history,
                         calorie_history=calorie_history)

if __name__ == "__main__":
    app.run(debug=True)
