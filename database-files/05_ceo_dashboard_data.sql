USE NutritionBuddy;

CREATE TABLE IF NOT EXISTS CEODashboardKeyMetrics (
    Metric VARCHAR(255) PRIMARY KEY,
    Value DECIMAL(10, 2)
);

INSERT INTO CEODashboardKeyMetrics (Metric, Value) VALUES
('Active Users', 1200),
('New Clients', 150),
('Plan Completion Rate', 0.85),
('Avg. Client Retention (Months)', 6.2);

CREATE TABLE IF NOT EXISTS CEODashboardGrowthTrend (
    Date DATE PRIMARY KEY,
    Value INT
);

INSERT INTO CEODashboardGrowthTrend (Date, Value) VALUES
('2024-01-01', 1000),
('2024-02-01', 1100),
('2024-03-01', 1300),
('2024-04-01', 1250),
('2024-05-01', 1400),
('2024-06-01', 1550);

CREATE TABLE IF NOT EXISTS CEOEngagementIndicators (
    Metric VARCHAR(255) PRIMARY KEY,
    Value VARCHAR(255),
    Description TEXT
);

INSERT INTO CEOEngagementIndicators (Metric, Value, Description) VALUES
('Daily Active Users', '850', 'Users active in the last 24 hours'),
('Weekly Active Users', '1200', 'Users active in the last 7 days'),
('Avg. Session Duration', '25 mins', 'Average time spent per session'),
('Feature X Usage', '78%', 'Percentage of users using Feature X'),
('Plan Adherence Rate', '62%', 'Percentage of users adhering to their nutrition plans');

CREATE TABLE IF NOT EXISTS CEODailyActiveUsers (
    Date DATE PRIMARY KEY,
    Users INT
);

INSERT INTO CEODailyActiveUsers (Date, Users)
SELECT CURDATE() - INTERVAL (30 - n) DAY, 500 + FLOOR(RAND() * 500)
FROM (SELECT 1 + units.i + tens.i * 10 AS n FROM        (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS units CROSS JOIN (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3) AS tens) as t
WHERE n <= 30;

CREATE TABLE IF NOT EXISTS CEOClientActivity (
    ClientID INT PRIMARY KEY,
    Name VARCHAR(255),
    LastLogin DATE,
    MealsLogged INT,
    PlansFollowed INT
);

INSERT INTO CEOClientActivity (ClientID, Name, LastLogin, MealsLogged, PlansFollowed) VALUES
(1, 'Alice Smith', '2024-03-01', 15, 4),
(2, 'Bob Johnson', '2024-02-15', 9, 2),
(3, 'Charlie Williams', '2024-02-28', 25, 6),
(4, 'Diana Brown', '2024-03-02', 18, 5),
(5, 'Ethan Davis', '2024-02-25', 12, 3);

CREATE TABLE IF NOT EXISTS CEOFinancialIndicators (
    Metric VARCHAR(255) PRIMARY KEY,
    Value DECIMAL(15, 2),
    Unit VARCHAR(50)
);

INSERT INTO CEOFinancialIndicators (Metric, Value, Unit) VALUES
('Revenue', 1500000.00, '$'),
('Expenses', 500000.00, '$'),
('Profit', 1000000.00, '$'),
('Client Acquisition Cost', 150.00, '$'),
('Average Revenue per User', 1200.00, '$');

CREATE TABLE IF NOT EXISTS CEORevenueTrend (
    Month DATE PRIMARY KEY,
    Revenue DECIMAL(15, 2)
);

INSERT INTO CEORevenueTrend (Month, Revenue) VALUES
('2024-01-01', 110000.00),
('2024-02-01', 125000.00),
('2024-03-01', 145000.00),
('2024-04-01', 135000.00),
('2024-05-01', 170000.00),
('2024-06-01', 190000.00);

CREATE TABLE IF NOT EXISTS CEOExpenseBreakdown (
    Category VARCHAR(255) PRIMARY KEY,
    Percentage DECIMAL(5, 2)
);

INSERT INTO CEOExpenseBreakdown (Category, Percentage) VALUES
('Marketing', 22.00),
('Salaries', 38.00),
('Technology', 28.00),
('Operations', 12.00);

CREATE TABLE IF NOT EXISTS CEOSystemPerformanceIndicators (
    Metric VARCHAR(255) PRIMARY KEY,
    Value VARCHAR(255),
    Description TEXT
);

INSERT INTO CEOSystemPerformanceIndicators (Metric, Value, Description) VALUES
('API Response Time', '110ms', 'Average time to respond to API requests'),
('Database Load', '0.5', 'Current database server load'),
('User Traffic', '1400 req/min', 'Number of requests to the server per minute'),
('Error Rate', '0.02%', 'Percentage of requests resulting in an error');

CREATE TABLE IF NOT EXISTS CEOAPIResponseTime (
    Time DATETIME PRIMARY KEY,
    ResponseTime INT
);

INSERT INTO CEOAPIResponseTime (Time, ResponseTime)
SELECT NOW() - INTERVAL (24 - n) HOUR, 80 + FLOOR(RAND() * 80)
FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23) as t;

CREATE TABLE IF NOT EXISTS CEOUserTraffic (
    Hour INT PRIMARY KEY,
    Traffic INT
);

INSERT INTO CEOUserTraffic (Hour, Traffic)
SELECT n, 50 + FLOOR(RAND() * 50)
FROM (SELECT 0 AS n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23) as t;