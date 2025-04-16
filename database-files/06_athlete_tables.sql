-- Create tables for Athletes, Workout Plans, and Reminders
USE NutritionBuddy;

-- Table: Athlete
CREATE TABLE IF NOT EXISTS Athlete (
  athlete_id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  weight_kg DECIMAL(5,2),
  height_cm DECIMAL(5,2),
  age INT,
  activity_level ENUM('low', 'moderate', 'high') DEFAULT 'moderate'
);

-- Table: Workout_Plan
CREATE TABLE IF NOT EXISTS Workout_Plan (
  plan_id INT PRIMARY KEY AUTO_INCREMENT,
  athlete_id INT,
  goal VARCHAR(255),
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (athlete_id) REFERENCES Athlete(athlete_id)
);

-- Table: Reminders
CREATE TABLE IF NOT EXISTS Reminders (
  reminder_id INT PRIMARY KEY AUTO_INCREMENT,
  athlete_id INT,
  reminder_type VARCHAR(50),
  time TIME,
  message TEXT,
  FOREIGN KEY (athlete_id) REFERENCES Athlete(athlete_id)
);

-- Table: Meal_Log (for athlete if different from the existing MealLog)
CREATE TABLE IF NOT EXISTS Meal_Log (
  log_id INT PRIMARY KEY AUTO_INCREMENT,
  athlete_id INT,
  log_date DATE,
  day_of_week VARCHAR(10),
  meal_type VARCHAR(50),
  meal_time TIME,
  calories INT,
  protein_g DECIMAL(6,2),
  carbs_g DECIMAL(6,2),
  fats_g DECIMAL(6,2),
  daily_caloric_total INT,
  FOREIGN KEY (athlete_id) REFERENCES Athlete(athlete_id)
);

-- Insert some sample data
INSERT INTO Athlete (athlete_id, name, weight_kg, height_cm, age, activity_level)
VALUES 
  (1, 'John Doe', 75.5, 180.0, 25, 'moderate'),
  (2, 'Jane Smith', 62.0, 165.0, 22, 'high'),
  (3, 'Bob Johnson', 85.0, 190.0, 30, 'low');

-- Insert workout plans
INSERT INTO Workout_Plan (athlete_id, goal, start_date, end_date)
VALUES 
  (1, 'Weight loss', '2025-04-01', '2025-04-30'),
  (2, 'Muscle gain', '2025-04-01', '2025-05-15'),
  (3, 'Maintenance', '2025-04-10', '2025-05-10');

-- Insert reminders
INSERT INTO Reminders (athlete_id, reminder_type, time, message)
VALUES 
  (1, 'Meal', '08:00:00', 'Time for breakfast!'),
  (1, 'Workout', '17:00:00', 'Time for your workout!'),
  (1, 'Hydration', '12:00:00', 'Drink water!'),
  (2, 'Meal', '07:30:00', 'Protein breakfast time');

-- Insert meal logs
INSERT INTO Meal_Log (athlete_id, log_date, day_of_week, meal_type, meal_time, calories, protein_g, carbs_g, fats_g, daily_caloric_total)
VALUES 
  (1, '2025-04-15', 'Monday', 'Breakfast', '08:00:00', 450, 25.5, 50.0, 15.2, 2200),
  (1, '2025-04-15', 'Monday', 'Lunch', '12:30:00', 650, 35.0, 70.0, 20.0, 2200),
  (1, '2025-04-15', 'Monday', 'Dinner', '19:00:00', 750, 40.0, 80.0, 25.0, 2200),
  (1, '2025-04-16', 'Tuesday', 'Breakfast', '08:00:00', 400, 20.0, 45.0, 15.0, 2100),
  (1, '2025-04-16', 'Tuesday', 'Lunch', '12:30:00', 600, 30.0, 65.0, 20.0, 2100),
  (2, '2025-04-15', 'Monday', 'Breakfast', '07:30:00', 550, 40.0, 50.0, 15.0, 2600),
  (2, '2025-04-15', 'Monday', 'Lunch', '12:00:00', 700, 45.0, 65.0, 22.0, 2600); 