import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
import re

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///finance.db")

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
    """Show portfolio"""
    portfolio = db.execute("""
        SELECT symbol, SUM(shares) as shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
    """, session["user_id"])

    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
    total = user["cash"]

    for stock in portfolio:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["total"] = stock["shares"] * quote["price"]
        total += stock["total"]

    return render_template("index.html", portfolio=portfolio, cash=user["cash"], total=total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Invalid shares", 400)

        if not symbol:
            return apology("Missing symbol", 400)
        if shares < 1:
            return apology("Invalid shares", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]
        cost = stock["price"] * shares

        if user["cash"] < cost:
            return apology("Can't afford", 400)

        db.execute("""
            INSERT INTO transactions
            (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, 'buy')
        """, session["user_id"], symbol, shares, stock["price"])

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"])

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history"""
    transactions = db.execute("""
        SELECT * FROM transactions
        WHERE user_id = ?
        ORDER BY transacted DESC
    """, session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username/password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Missing symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol", 400)

        return render_template("quoted.html", stock=stock)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username", 400)
        if not password:
            return apology("Must provide password", 400)
        if password != confirmation:
            return apology("Passwords don't match", 400)
        if len(password) < 6:
            return apology("Password too short", 400)
        if not re.search(r"\d", password):
            return apology("Password needs digit", 400)
        if not re.search(r"\W", password):
            return apology("Password needs special char", 400)

        try:
            db.execute("""
                INSERT INTO users (username, hash)
                VALUES (?, ?)
            """, username, generate_password_hash(password))
        except:
            return apology("Username taken", 400)

        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares"""
    if request.method == "GET":
        stocks = db.execute("""
            SELECT symbol FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, session["user_id"])
        return render_template("sell.html", stocks=stocks)
    else:
        symbol = request.form.get("symbol").upper()
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Invalid shares", 400)

        if not symbol:
            return apology("Missing symbol", 400)
        if shares < 1:
            return apology("Invalid shares", 400)

        available = db.execute("""
            SELECT SUM(shares) as total
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol)[0]["total"]

        if not available or shares > available:
            return apology("Not enough shares", 400)

        stock = lookup(symbol)
        value = stock["price"] * shares

        db.execute("""
            INSERT INTO transactions
            (user_id, symbol, shares, price, type)
            VALUES (?, ?, ?, ?, 'sell')
        """, session["user_id"], symbol, -shares, stock["price"])

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", value, session["user_id"])

        flash("Sold!")
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
