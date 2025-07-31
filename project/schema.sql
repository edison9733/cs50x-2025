-- CS50x 2025 Health Tracker Database Schema
-- Simple and complete database setup

-- Drop existing tables to start fresh (optional, for development)
DROP TABLE IF EXISTS food_log;
DROP TABLE IF EXISTS workout_log;
DROP TABLE IF EXISTS body_metrics;
DROP TABLE IF EXISTS foods;
DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS users;
DROP VIEW IF EXISTS daily_summary;

-- Create users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create foods table
CREATE TABLE foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories REAL NOT NULL DEFAULT 0,
    carbs REAL NOT NULL DEFAULT 0,
    protein REAL NOT NULL DEFAULT 0,
    fat REAL NOT NULL DEFAULT 0,
    fiber REAL NOT NULL DEFAULT 0,
    water REAL NOT NULL DEFAULT 0,
    vitamins TEXT,
    minerals TEXT,
    serving_size REAL DEFAULT 100,
    serving_unit TEXT DEFAULT 'g'
);

-- Create workouts table
CREATE TABLE workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    calories_per_minute REAL NOT NULL,
    description TEXT
);

-- Create food log table
CREATE TABLE food_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE DEFAULT (DATE('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (food_id) REFERENCES foods(id)
);

-- Create workout log table
CREATE TABLE workout_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    workout_id INTEGER NOT NULL,
    duration_minutes REAL NOT NULL,
    calories_burnt REAL NOT NULL,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE DEFAULT (DATE('now')),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (workout_id) REFERENCES workouts(id)
);

-- Create body metrics table
CREATE TABLE body_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    bmi REAL GENERATED ALWAYS AS (weight / ((height/100.0) * (height/100.0))) STORED,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date DATE DEFAULT (DATE('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create daily summary view
CREATE VIEW daily_summary AS
SELECT
    u.id as user_id,
    u.username,
    DATE('now') as date,
    COALESCE(SUM(fl.quantity * f.calories / f.serving_size), 0) as total_calories_consumed,
    COALESCE(SUM(wl.calories_burnt), 0) as total_calories_burnt,
    (SELECT bm.weight FROM body_metrics bm WHERE bm.user_id = u.id ORDER BY bm.recorded_at DESC LIMIT 1) as current_weight,
    (SELECT bm.bmi FROM body_metrics bm WHERE bm.user_id = u.id ORDER BY bm.recorded_at DESC LIMIT 1) as current_bmi
FROM users u
LEFT JOIN food_log fl ON u.id = fl.user_id AND fl.date = DATE('now')
LEFT JOIN foods f ON fl.food_id = f.id
LEFT JOIN workout_log wl ON u.id = wl.user_id AND wl.date = DATE('now')
GROUP BY u.id;

-- Insert sample foods (using proper JSON format)
INSERT INTO foods (name, calories, carbs, protein, fat, fiber, water, vitamins, minerals) VALUES
('Apple', 52, 14, 0.3, 0.2, 2.4, 86, '{"C": "8mg", "A": "3mcg"}', '{"Potassium": "107mg"}'),
('Chicken Breast', 165, 0, 31, 3.6, 0, 65, '{"B6": "0.9mg", "B12": "0.3mcg"}', '{"Iron": "1mg", "Zinc": "1mg"}'),
('Brown Rice', 112, 24, 2.6, 0.9, 1.8, 73, '{"B1": "0.2mg"}', '{"Magnesium": "44mg"}'),
('Broccoli', 55, 11, 3.7, 0.6, 2.6, 89, '{"C": "89mg", "K": "102mcg"}', '{"Calcium": "47mg"}'),
('Egg', 155, 1.1, 13, 11, 0, 76, '{"D": "2mcg", "B12": "0.9mcg"}', '{"Selenium": "30mcg"}'),
('Banana', 89, 23, 1.1, 0.3, 2.6, 75, '{"C": "8.7mg", "B6": "0.4mg"}', '{"Potassium": "358mg"}'),
('Salmon', 208, 0, 20, 13, 0, 68, '{"D": "11mcg", "B12": "3.2mcg"}', '{"Selenium": "36mcg"}'),
('Oatmeal', 389, 66, 17, 7, 11, 8, '{"B1": "0.8mg"}', '{"Iron": "4.7mg"}'),
('Greek Yogurt', 59, 3.6, 10, 0.4, 0, 85, '{"B12": "0.5mcg"}', '{"Calcium": "110mg"}'),
('Sweet Potato', 86, 20, 1.6, 0.1, 3, 77, '{"A": "961mcg", "C": "2.4mg"}', '{"Potassium": "337mg"}');

-- Insert sample workouts
INSERT INTO workouts (name, category, calories_per_minute, description) VALUES
('Push-ups', 'chest', 7, 'Classic chest exercise'),
('Sit-ups', 'abs', 8, 'Core strengthening exercise'),
('Squats', 'legs', 5, 'Lower body compound movement'),
('Shoulder Press', 'shoulder', 6, 'Overhead pressing movement'),
('Plank', 'abs', 4, 'Isometric core exercise'),
('Lunges', 'legs', 6, 'Single leg exercise'),
('Dips', 'chest', 8, 'Triceps and chest exercise'),
('Mountain Climbers', 'abs', 10, 'Dynamic core exercise'),
('Jumping Jacks', 'cardio', 8, 'Full body cardio exercise'),
('Burpees', 'cardio', 10, 'High intensity full body exercise'),
('Crunches', 'abs', 5, 'Abdominal exercise'),
('Leg Raises', 'abs', 6, 'Lower abs exercise'),
('Bench Press', 'chest', 8, 'Chest pressing movement'),
('Lateral Raises', 'shoulder', 5, 'Shoulder isolation exercise'),
('Calf Raises', 'legs', 3, 'Lower leg exercise'),
('Running', 'cardio', 10, 'Cardiovascular exercise'),
('Cycling', 'cardio', 8, 'Low impact cardio'),
('Jump Rope', 'cardio', 12, 'High intensity cardio');

-- Create indexes for better performance
CREATE INDEX idx_food_log_user_date ON food_log(user_id, date);
CREATE INDEX idx_workout_log_user_date ON workout_log(user_id, date);
CREATE INDEX idx_body_metrics_user ON body_metrics(user_id);
