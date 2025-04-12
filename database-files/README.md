# `database-files` Folder

# NutritionBuddy Database Sample Data

This folder contains the SQL files for creating and populating the NutritionBuddy database system.

## Files Overview

1. `nutrition_buddy_schema.sql` - Contains the database schema definition with all table structures
2. `01_nutrition_buddy_system_data.sql` - May be renoved. Sample data for system-related tables (SystemPerformance, Dataset, ActivityLog, SecurityStatus)
3. `02_nutrition_buddy_people_data.sql` - Sample data for user-related tables (Client, Nutritionist)
4. `03_nutrition_buddy_plans_reports.sql` - Sample data for nutrition plans and progress reports
4. `04_nutrition_buddy_meal_nutrients.sql` - Sample data for meal logs and nutrients

## Data Volumes

This sample data follows the requirements:
- Strong entities (Client, Nutritionist, SystemPerformance, Dataset): 35 rows each
- Weak entities (NutritionPlan, ProgressReport, MealLog, ActivityLog, SecurityStatus): 60-75 rows each
- Detail data (Nutrient): 150 rows

## Usage

The files should be executed in order (they're prefixed with numbers to ensure proper execution order). When creating a new database container, these files will be automatically executed.

Note: If you make changes to these files, you'll need to recreate the database container in Docker for the changes to take effect. 