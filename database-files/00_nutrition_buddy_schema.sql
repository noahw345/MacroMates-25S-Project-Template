-- Create Database
CREATE DATABASE IF NOT EXISTS NutritionBuddy;
USE NutritionBuddy;

-- Drop existing tables in reverse dependency order to avoid foreign key issues
DROP TABLE IF EXISTS Nutrient;
DROP TABLE IF EXISTS ProgressReport;
DROP TABLE IF EXISTS NutritionPlan;
DROP TABLE IF EXISTS Nutritionist;
DROP TABLE IF EXISTS MealLog;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS SecurityStatus;
DROP TABLE IF EXISTS ActivityLog;
DROP TABLE IF EXISTS Dataset;
DROP TABLE IF EXISTS SystemPerformance;
 
-- Table: SystemPerformance
CREATE TABLE SystemPerformance (
 PerformanceID INT PRIMARY KEY AUTO_INCREMENT,
 Performance_Metric VARCHAR(255),
 System_Status VARCHAR(255),
 Existing_Clients INT,
 New_Clients INT,
 Timestamp TIMESTAMP
);
 
-- Table: ActivityLog
CREATE TABLE ActivityLog (
 LogID INT PRIMARY KEY AUTO_INCREMENT,
 Timestamp TIMESTAMP,
 Is_Flagged BOOLEAN,
 Event_Type VARCHAR(255),
 PerformanceID INT,
 FOREIGN KEY (PerformanceID) REFERENCES SystemPerformance(PerformanceID)
);
 
-- Table: Dataset
CREATE TABLE Dataset (
 DatasetID INT PRIMARY KEY AUTO_INCREMENT,
 Dataset_Name VARCHAR(255),
 Data_Description TEXT,
 Status VARCHAR(50),
 PerformanceID INT,
 FOREIGN KEY (PerformanceID) REFERENCES SystemPerformance(PerformanceID)
);
 
-- Table: SecurityStatus
CREATE TABLE SecurityStatus (
 SecurityID INT PRIMARY KEY AUTO_INCREMENT,
 Status VARCHAR(50),
 LogID INT,
 FOREIGN KEY (LogID) REFERENCES ActivityLog(LogID)
);
 
-- Table: Client
CREATE TABLE Client (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 Name VARCHAR(255),
 DOB DATE,
 Email VARCHAR(255) UNIQUE
);
 
-- Table: MealLog
CREATE TABLE MealLog (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 Datetime TIMESTAMP,
 Notes TEXT,
 ClientID INT,
 FOREIGN KEY (ClientID) REFERENCES Client(ID)
);
 
-- Table: Nutritionist
CREATE TABLE Nutritionist (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 Name VARCHAR(255),
 Email VARCHAR(255) UNIQUE
);
 
-- Table: NutritionPlan
CREATE TABLE NutritionPlan (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 StartDate DATE,
 EndDate DATE,
 CaloriesGoal INT,
 NutritionistID INT,
 ClientID INT,
 FOREIGN KEY (NutritionistID) REFERENCES Nutritionist(ID),
 FOREIGN KEY (ClientID) REFERENCES Client(ID)
);
 
-- Table: ProgressReport
CREATE TABLE ProgressReport (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 CreatedDate DATE,
 Summary TEXT,
 DeficiencyAlerts TEXT,
 ClientID INT,
 FOREIGN KEY (ClientID) REFERENCES Client(ID)
);
 
-- Table: Nutrient
CREATE TABLE Nutrient (
 ID INT PRIMARY KEY AUTO_INCREMENT,
 Name VARCHAR(255),
 Category VARCHAR(255),
 Quantity DECIMAL(10,2),
 Unit VARCHAR(50),
 MealLogID INT,
 FOREIGN KEY (MealLogID) REFERENCES MealLog(ID)
); 