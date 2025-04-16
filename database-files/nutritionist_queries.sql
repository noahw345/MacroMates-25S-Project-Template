Use NutritionBuddy;

-- SQL Queries for Persona 1: Nutritionist

-- User Story 1.1: View dashboard summarizing clients' average nutrition metrics
SELECT ClientID, AVG(Quantity) AS Avg_Nutrient_Intake, Nutrient.Name,
       Nutrient.Category
FROM MealLog
JOIN Nutrient ON MealLog.ID = Nutrient.MealLogID
GROUP BY ClientID, Nutrient.Name, Nutrient.Category;

-- User Story 1.2: Generate customizable progress reports for individual clients
SELECT * FROM ProgressReport WHERE ClientID = ?;

-- User Story 1.3: Analyze trends in dietary habits over time
SELECT ClientID, DATE(Datetime) AS LogDate, Nutrient.Name, SUM(Quantity) AS Total_Intake
FROM MealLog
JOIN Nutrient ON MealLog.ID = Nutrient.MealLogID
WHERE Datetime BETWEEN ? AND ?
GROUP BY ClientID, LogDate, Nutrient.Name
ORDER BY LogDate;

-- User Story 1.4: Identify nutrient deficiencies in logged meals
SELECT ClientID, Nutrient.Name, AVG(Quantity) AS Avg_Intake
FROM MealLog
JOIN Nutrient ON MealLog.ID = Nutrient.MealLogID
GROUP BY ClientID, Nutrient.Name
HAVING AVG(Quantity) < ?;

-- User Story 1.5: Add new clients and input baseline nutrition plans
INSERT INTO Client (Name, DOB, Email) VALUES (?, ?, ?);
INSERT INTO NutritionPlan (StartDate, EndDate, CaloriesGoal, NutritionistID, ClientID)
VALUES (?, ?, ?, ?, ?);

-- User Story 1.6: Remove or archive inactive clients
DELETE FROM Client WHERE ID = ?;
