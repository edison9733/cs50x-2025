# Health Tracker
#### Video Demo: https://youtu.be/ifYaOXAKghk
#### Description: A modern web application for tracking daily calories consumed through diet, calories burnt through workout and status of body metrics

## Features

- **Food Tracking**: Log meals and track diet's nutritions such as calories, carbs, protein and fat to calculate amount of calories consumed
- **Workout Tracking**: Track exercises by categories such as abs, sholder, legs and chest to calculate amount of calories burnt
- **Progress Visualization**: Interactive charts which showing weight, BMI and calorie trend with recent weight records and daily summary
- **Health Dashboard**: Real-time view of calories consumed with burnt and daily goal progress to motivate the user
- **Calculator**: Calculate calories consumed though meals and calories burnt through workouts
- **Motivational quotes**: To encourage the user not to give up but continue to lock in

## Project Structure

...
Project/
|
|-- app.py                  # Main Flask application
|-- requirements.txt        # Python dependencies
|-- helpers.py.             # Helper function
|-- database.db				# SQLite database
|-- schema.sql				# Database schema
|
|-- static/
|   |__ styles.css			# Dark theme with bright colour texts
|	|__ script.js			# JavaScript functionality
|
|__ templates/
	|__ apology.html		# Show error codes to the users
	|__ food.html			# Food tracking
	|__ history.html		# Progress charts
	|__ index.html			# Dashboard
	|__ layout.html			# Base template
	|__ login.html			# To log user in
	|__ register.html		# Register new user
	|__ workout.html		# Workout tracking


## Handbook
**Creating an Account**
1. Click "Register" on the homepage
2. Enter username, email and password
3. Start tracking after registration without further ado

**Tracking Food**
1. Navigate to "Track Food"
2. Select food item from dropdown
3. Enter quantity in grams
4. View real-time nutrition calculations

**Logging Workouts**
1. Go to "Track Workout"
2. Choose exercise from categorized list
3. Enter duration in minutes according to the sets
4. See estimated calories burned

**Viewing Progredd**
1. Click "History" to see your trends
2. Weight and BMI chart shows body changes
3. Calorie chart displays daily input and output



## Setup Instructions

1. **Prerequisites**:
- Python
- pip (Python package manager)
- SQLite3
- Git

2. **Clone the repository**:
```bash
git clone https://github.com/code50/190621257/project.git
cd project
```
3. **Install all the dependencies packages from a file called requirements.txt**:
```bash
pip install -r requirements.txt
```
4. **Setup the database file, database.db**:
```bash
sqlite3 database.db < schema.sql
```
5. **Run the program**:
```bash
flask run
```
6. **Open in local browser**:
```bash
http://127.0.0.1:5000
```



#### Technologies Used
- Python [learnt in Week6]
- Flask web framework [learnt in Week9]
- SQLite3 [learnt in Week7]
- HTML, CSS [Bootstrap], JavaScript [learnt in Week8]

#### Troubleshooting
#### Please email me, eliu4864@gmail.com
