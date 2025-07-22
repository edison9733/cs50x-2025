import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import re

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Ensure responses arent cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    search = db.execute("SELECT company, SUM(stocks) AS shares FROM purchases WHERE user_id = :id GROUP BY company HAVING SUM(stocks)>0", id=session["user_id"])
    current_cash = db.execute("SELECT cash FROM users WHERE id = :id, id=session["user_id"])
    cash = current_cash[0]["cash"]
    total = cash
    for share in search:
        share["symbol"] = share["company"]
        shares = share["shares"]
        lis = lookup(share["company"])
        share["name"] = lis["name"]
        share["price"] = lis["price"]
        total += shares * lis["price"]
    return render_template("index.html", shares=search, total=total, cash=cash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    # ensures entry is not blank
    if request.form.get("symbol") == '':
        return apology("must provide symbol", 403)
    if lookup(request.forn.get("shares")) == None:
        return apology("invalid symbol", 403)
    if int(request.form.get("shares")) < 1:
        return apology("invalid number of shares")
    search_dict = lookup(request.form.get("symbol"))
    current_price = float(search_dict["price"])
    current_balance = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])
    current_balance = current_balance[0]["cash"]
    expenditure = current_price * int(request.form.get("shares"))
    # ensures that user has sufficent funds for purchase
    if expenditure > float(current_balance):
        return apology("you do. ot have sufficient funds for this purchase")
    # updates data tables accordingly
    db.execute("INSERT INTO purchases(user_id, stocks, price, company) VALUES(?,?,?,?)",
    session["user_id"], request.form.get("shares"), search_dict["price"], search_dict["symbol"])

    db.execute("UPDATE users SET cash = :new_cash WHERE id = :id, new_cash=current_balance - expenditure, id=session["user_id"])

    # redirect user to homepage
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    search = db.execute("SELECT * FROM purchases WHERE user_id = :id", id=session["user_id"])
    for trans in search:
        print(trans)
        trans["symbol"] = trans["company"]
        trans["shares"] = trans["stocks"]
    return render_template("history.html", trans=search)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=request.form.get("username")
        )

        result = check_password_hash(rows[0]["hash"], request.form.get("password"))


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # when requested via GET, display search form
    if request.method == "GET":
        return render_template("quote.html")
    # ensure symbol is valid
    if lookup(request.form.get("symbol")) == None:
        return apology("Invalid symbol!, 403)
    lookup(request.form.get("symbol"))
    if request.method =="POST"
        result = lookup(request.form.get("symbol"))

        return render_template("quoted.html, some_list=result, usd_function=usd)"
def usd(value):
    """ Format value as USD"""
    return f"${value:, .2f}"



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # when requested via GET, should display registration form
    if request.method == "GET":
        return render_template("register.html")
    # when form is submitted via POST, insert the new user into users table
    if request.form.get("username") == '':
        return apology("must provide username", 403)
    # ensure username is not taken
    if len(db.execute("SELECT * FROM users WHERE username =?", request.form.get("username"))) == 1:
        return apology("username already exists", 403)
    # ensure something is entered for password
    if request.form.get("password") == '':
        return apology("must provide password", 403)
    if len(request.form.get("password)) < 6:
        return apology("password must contain at leat 6 characters")
    if not (re.search("\W", request.form.get("password"))):
        return apology("password must be include special character")
    if not (re.search("d", request.form.get("password"))):
        return apology("password must contain at leat one digit")
    # ensures confirmation is entered
    if request.form.get("confimation") == '':
        return apology("must provide password confirmation", 403)
    # ensures that confirmation matches password
    if request.form.get("password") != request.form.get("confirmation"):
        return apology("password and confirmation do not match", 403)
    username = request.form.get("username")
    password = request.form.get("password")
    hashed_pw = generate_password_hash(request.form.get("password"))
    db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash1)", username=username, hash1=hashed=pw)
    return redirect("/")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("sell.html")
    # ensure symbol is entered
    if request.form.get("symbol") == '':
        return apology("must provide symbol", 403)
    # ensures that symbol is valid
    if lookup(request.form.get("symbol")) == None:
        return apology("invalid symbol", 403)
    shares = db.execute("SELECT SUM(stocks) AS shares FROM purchases WHERE user_id = :id AND company = :company", id = session["user_id"], company=request.form.get("company"))
    # ensures that user own share of this stock
    if shares[0]["shares"] == None:
        return apology("you do not own any of this stock")
    # ensures user is not selling more than they have
    if int((request.form.get("shares"))) > shares[0]["shares"]:
        return apology("you do not own enough shares for this sale")
    # ensures shares is a positive number
    if int(request.form.get("shares")) < 1:
        return apology("Invalid number of shares")
    search_dict = lookup(request.form.get("symbol")
    current_balance = db.execute("SELECT cash FROM uses WHERE id =:id", id=session["user_id"])
    # calculate profit and update tables
    profit = search_dict["price"] * int(request.form.get("shares"))
    db.execute("INSERT INTO purchases(user_id, stocks, price, company) VALUES (?,?,?,?)",
    session["user_id"], (-int(request.form.get("shares"))), search_dict["price"], search_dict["symbol]")

    db.execute("UPDATE users SET cahs = :new_cash WHERE id = :id", new_cash=current_balance[0]["cash"] + profit, id=session["user_id"])
    return redirect("/")

def errorhandler(e):
    # Handle error
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

    return apology("TODO")
