from flask import Blueprint, jsonify
from backend.db import get_db_connection
import datetime

student_athlete_bp = Blueprint('student_athlete', __name__)

@student_athlete_bp.route('/athlete/bmi', methods=['GET'])
def get_athlete_bmi():
    """
    API route to calculate BMI from body data (dynamic version).
    Returns:
        A JSON response containing athlete_id, name, and calculated_bmi.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              athlete_id,
              name,
              ROUND(weight_kg / POWER(height_cm / 100, 2), 2) AS calculated_bmi
            FROM Athlete
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@student_athlete_bp.route('/athlete/maintenance_calories', methods=['GET'])
def get_athlete_maintenance_calories():
    """
    API route to estimate daily maintenance calories.
    Returns:
        A JSON response containing athlete_id, name, and maintenance_calories.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              athlete_id,
              name,
              ROUND(
                CASE
                  WHEN activity_level = 'low' THEN 1.2
                  WHEN activity_level = 'moderate' THEN 1.55
                  WHEN activity_level = 'high' THEN 1.9
                  ELSE 1.4
                END * (10 * weight_kg + 6.25 * height_cm - 5 * age + 5), 0
              ) AS maintenance_calories
            FROM Athlete
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@student_athlete_bp.route('/athlete/weight_change', methods=['GET'])
def get_athlete_weight_change():
    """
    API route to estimate weight change over time based on caloric surplus/deficit.
    Returns:
        A JSON response with athlete_id, name, goal, duration_days, and estimated_kg_change.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              a.athlete_id,
              a.name,
              wp.goal,
              DATEDIFF(wp.end_date, wp.start_date) AS duration_days,
              ROUND(SUM(COALESCE(ml.daily_caloric_total, 0) - 3000)/7700, 2) AS estimated_kg_change
            FROM Athlete a
            JOIN Workout_Plan wp ON a.athlete_id = wp.athlete_id
            JOIN Meal_Log ml ON a.athlete_id = ml.athlete_id
            WHERE ml.log_date BETWEEN wp.start_date AND wp.end_date
              AND ml.daily_caloric_total IS NOT NULL
            GROUP BY a.athlete_id, wp.goal, wp.start_date, wp.end_date
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@student_athlete_bp.route('/athlete/daily_macro_breakdown', methods=['GET'])
def get_athlete_daily_macro_breakdown():
    """
    API route to show daily macro breakdown for a given athlete (currently hardcoded WHERE athlete_id=1).
    Returns:
        A JSON response with daily total calories, protein, carbs, and fats.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              athlete_id,
              log_date,
              day_of_week,
              SUM(calories) AS total_calories,
              SUM(protein_g) AS total_protein,
              SUM(carbs_g) AS total_carbs,
              SUM(fats_g) AS total_fats
            FROM Meal_Log
            WHERE athlete_id = 1
            GROUP BY athlete_id, log_date, day_of_week
            ORDER BY log_date DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # If log_date is returned as a datetime object, convert to string
        for row in data:
            if 'log_date' in row and isinstance(row['log_date'], (datetime.date, datetime.datetime)):
                row['log_date'] = row['log_date'].strftime('%Y-%m-%d')

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@student_athlete_bp.route('/athlete/workout_plan_intake', methods=['GET'])
def get_athlete_workout_plan_intake():
    """
    API route to view workout plans alongside calorie intake during that period.
    Returns:
        A JSON response of name, goal, plan dates, meal logs, etc.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              a.name,
              wp.goal,
              wp.start_date,
              wp.end_date,
              ml.log_date,
              ml.meal_type,
              ml.calories
            FROM Workout_Plan wp
            JOIN Athlete a ON wp.athlete_id = a.athlete_id
            JOIN Meal_Log ml ON wp.athlete_id = ml.athlete_id
            WHERE ml.log_date BETWEEN wp.start_date AND wp.end_date
            ORDER BY a.name, ml.log_date, ml.meal_time
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # Convert date fields to string if necessary
        for row in data:
            if 'start_date' in row and isinstance(row['start_date'], (datetime.date, datetime.datetime)):
                row['start_date'] = row['start_date'].strftime('%Y-%m-%d')
            if 'end_date' in row and isinstance(row['end_date'], (datetime.date, datetime.datetime)):
                row['end_date'] = row['end_date'].strftime('%Y-%m-%d')
            if 'log_date' in row and isinstance(row['log_date'], (datetime.date, datetime.datetime)):
                row['log_date'] = row['log_date'].strftime('%Y-%m-%d')

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()


@student_athlete_bp.route('/athlete/reminders', methods=['GET'])
def get_athlete_reminders():
    """
    API route to list all reminders for a given athlete (currently hardcoded WHERE athlete_id=1).
    Returns:
        A JSON response with reminder_type, reminder_time, and message.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT
              athlete_id,
              reminder_type,
              TIME_FORMAT(time, '%h:%i %p') AS reminder_time,
              message
            FROM Reminders
            WHERE athlete_id = 1
            ORDER BY time
        """
        cursor.execute(query)
        data = cursor.fetchall()

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            conn.close()
