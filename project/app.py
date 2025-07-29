import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tools import apology, login_required, lookup, usd
import re

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["myr"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///transactions.db")

@app.after_request
def after_request(response):
    """No caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


