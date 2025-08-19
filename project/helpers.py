import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''")
        ]:
            s = s.replace(old, new)
        return s

    # create apology message for meme
    top_text = escape("Sorry")
    bottom_text = escape(message)

    # render the apology template with a fun meme
    # using different meme templates for variety
    meme_templates = [
        "bad-luck-brian",
        "y-u-no",
        "first-world-problems",
        "philosoraptor",
        "grumpy-cat",
        "conspiracy-keanu",
        "hide-the-pain-harold"
    ]

    # Select a meme based on the error code
    meme_index = code % len(meme_templates)
    meme = meme_templates[meme_index]

    return render_template("apology.html", top=top_text, bottom=bottom_text, meme=meme, code=code), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI (Body Mass Index)

    Formula: BMI = weight (kg) / (height (m))^2
    """
    if (height_cm <= 0 or weight_kg <= 0):
        return None

    height_m = (height_cm / 100.0)
    bmi =( weight_kg / (height_m * height_m))
    return round(bmi, 2)


def get_bmi_category(bmi):
    """
    Get BMI category based on WHO standards
    """
    if (bmi is None):
        return "Unknown"
    elif (bmi < 18.5):
        return "Underweight"
    elif (bmi < 25):
        return "Normal weight"
    elif (bmi < 30):
        return "Overweight"
    else:
        return "Obese"


def format_nutrients(food_data):
    """
    Format nutrient data for display
    """
    nutrients = {
        "Calories": f"{food_data.get('calories', 0):.1f} kcal",
        "Carbohydrates": f"{food_data.get('carbs', 0):.1f} g",
        "Protein": f"{food_data.get('protein', 0):.1f} g",
        "Fat": f"{food_data.get('fat', 0):.1f} g",
        "Fiber": f"{food_data.get('fiber', 0):.1f} g",
        "Water": f"{food_data.get('water', 0):.1f} g"
    }
    return nutrients


def get_daily_calorie_recommendation(age, gender, activity_level, weight_kg, height_cm):
    """
    Calculate daily calorie recommendation based on Mifflin-St Jeor equation

    activity_level: sedentary, lightly_active, moderately_active, very_active, extra_active
    """
    # Calculate BMR (Basal Metabolic Rate)
    if gender.lower() == "male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)
    daily_calories = bmr * multiplier

    return round(daily_calories)


def validate_email(email):
    """
    Validate email format
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def sanitize_input(text):
    """
    Sanitize user input to prevent XSS attacks
    """
    if text is None:
        return None

    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '"', "'", '&', '%', '=', '(', ')', '{', '}']
    for char in dangerous_chars:
        text = text.replace(char, '')

    return text.strip()
