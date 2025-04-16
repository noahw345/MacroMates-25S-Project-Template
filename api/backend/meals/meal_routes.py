########################################################
# MealLog Routes Blueprint
########################################################

from flask import Blueprint, request, jsonify
from datetime import datetime 
import pymysql
from backend.db import get_db_connection

# Create the blueprint
meals_bp = Blueprint('meals', __name__)

# Route to get all meal logs for a client
@meals_bp.route('/meal-logs', methods=['GET'])
def get_meal_logs():
    """Retrieve all meal logs for a client with optional date filtering"""
    try:
        # Get query parameters
        client_id = request.args.get('client_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Client ID is required
        if not client_id:
            return jsonify({"error": "client_id parameter is required"}), 400
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM MealLog WHERE ClientID = %s"
        params = [client_id]
        
        # Add date filters if provided
        if date_from:
            try:
                # Validate date format
                datetime.strptime(date_from, '%Y-%m-%d')
                query += " AND DATE(Datetime) >= %s"
                params.append(date_from)
            except ValueError:
                return jsonify({"error": "Invalid date_from format. Use YYYY-MM-DD"}), 400
        
        if date_to:
            try:
                # Validate date format
                datetime.strptime(date_to, '%Y-%m-%d')
                query += " AND DATE(Datetime) <= %s"
                params.append(date_to)
            except ValueError:
                return jsonify({"error": "Invalid date_to format. Use YYYY-MM-DD"}), 400
        
        # Order by date, newest first
        query += " ORDER BY Datetime DESC"
        
        # Execute the query
        cursor.execute(query, params)
        meals = cursor.fetchall()
        
        # Format the result
        result = []
        for meal in meals:
            # Get nutrients for this meal
            cursor.execute("SELECT * FROM Nutrient WHERE MealLogID = %s", (meal['ID'],))
            nutrients = cursor.fetchall()
            
            # Format nutrients
            nutrients_list = []
            for nutrient in nutrients:
                nutrients_list.append({
                    'id': nutrient['ID'],
                    'name': nutrient['Name'],
                    'category': nutrient['Category'],
                    'quantity': float(nutrient['Quantity']),
                    'unit': nutrient['Unit']
                })
            
            # Add meal with nutrients to result
            result.append({
                'id': meal['ID'],
                'datetime': meal['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
                'notes': meal['Notes'],
                'client_id': meal['ClientID'],
                'nutrients': nutrients_list
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to get a specific meal log by ID
@meals_bp.route('/meal-logs/<int:meal_id>', methods=['GET'])
def get_meal_log(meal_id):
    """Retrieve a single meal log by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get the meal log
        cursor.execute("SELECT * FROM MealLog WHERE ID = %s", (meal_id,))
        meal = cursor.fetchone()
        
        if not meal:
            return jsonify({"error": "Meal log not found"}), 404
        
        # Get nutrients for this meal
        cursor.execute("SELECT * FROM Nutrient WHERE MealLogID = %s", (meal_id,))
        nutrients = cursor.fetchall()
        
        # Format nutrients
        nutrients_list = []
        for nutrient in nutrients:
            nutrients_list.append({
                'id': nutrient['ID'],
                'name': nutrient['Name'],
                'category': nutrient['Category'],
                'quantity': float(nutrient['Quantity']),
                'unit': nutrient['Unit']
            })
        
        # Format the result
        result = {
            'id': meal['ID'],
            'datetime': meal['Datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'notes': meal['Notes'],
            'client_id': meal['ClientID'],
            'nutrients': nutrients_list
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to add a new meal log
@meals_bp.route('/meal-logs', methods=['POST'])
def add_meal_log():
    """Add a new meal log entry for a client"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['client_id', 'notes']):
            return jsonify({"error": "client_id and notes are required fields"}), 400
        
        # Parse datetime if provided, otherwise use current time
        meal_datetime = datetime.now()
        if 'datetime' in data and data['datetime']:
            try:
                meal_datetime = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT ID FROM Client WHERE ID = %s", (data['client_id'],))
        if not cursor.fetchone():
            return jsonify({"error": "Client not found"}), 404
        
        # Insert new meal log
        query = "INSERT INTO MealLog (Datetime, Notes, ClientID) VALUES (%s, %s, %s)"
        cursor.execute(query, (meal_datetime, data['notes'], data['client_id']))
        conn.commit()
        
        # Get the ID of the newly created meal log
        meal_log_id = cursor.lastrowid
        
        # Add nutrients if provided
        if 'nutrients' in data and isinstance(data['nutrients'], list):
            for nutrient in data['nutrients']:
                # Validate required nutrient fields
                if not all(key in nutrient for key in ['name', 'category', 'quantity', 'unit']):
                    continue  # Skip invalid nutrients
                
                # Insert nutrient
                nutrient_query = """
                    INSERT INTO Nutrient (Name, Category, Quantity, Unit, MealLogID) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(nutrient_query, (
                    nutrient['name'],
                    nutrient['category'],
                    nutrient['quantity'],
                    nutrient['unit'],
                    meal_log_id
                ))
        
        conn.commit()
        
        return jsonify({
            "message": "Meal log created successfully",
            "id": meal_log_id
        }), 201
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to update a meal log
@meals_bp.route('/meal-logs/<int:meal_id>', methods=['PUT'])
def update_meal_log(meal_id):
    """Update a meal log entry"""
    try:
        data = request.get_json()
        
        # Ensure at least one field to update
        if not any(key in data for key in ['datetime', 'notes', 'client_id']):
            return jsonify({"error": "No fields to update provided"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if meal log exists
        cursor.execute("SELECT * FROM MealLog WHERE ID = %s", (meal_id,))
        meal = cursor.fetchone()
        if not meal:
            return jsonify({"error": "Meal log not found"}), 404
        
        # Check if client exists if client_id is being updated
        if 'client_id' in data:
            cursor.execute("SELECT ID FROM Client WHERE ID = %s", (data['client_id'],))
            if not cursor.fetchone():
                return jsonify({"error": "Client not found"}), 404
        
        # Build update query
        update_fields = []
        params = []
        
        if 'datetime' in data:
            try:
                meal_datetime = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
                update_fields.append("Datetime = %s")
                params.append(meal_datetime)
            except ValueError:
                return jsonify({"error": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400
        
        if 'notes' in data:
            update_fields.append("Notes = %s")
            params.append(data['notes'])
        
        if 'client_id' in data:
            update_fields.append("ClientID = %s")
            params.append(data['client_id'])
        
        # Add meal_id to params
        params.append(meal_id)
        
        # Execute update
        query = f"UPDATE MealLog SET {', '.join(update_fields)} WHERE ID = %s"
        cursor.execute(query, params)
        
        # Update nutrients if provided
        if 'nutrients' in data and isinstance(data['nutrients'], list):
            # Option 1: Delete all existing nutrients and add new ones
            cursor.execute("DELETE FROM Nutrient WHERE MealLogID = %s", (meal_id,))
            
            # Insert new nutrients
            for nutrient in data['nutrients']:
                # Validate required nutrient fields
                if not all(key in nutrient for key in ['name', 'category', 'quantity', 'unit']):
                    continue  # Skip invalid nutrients
                
                # Insert nutrient
                nutrient_query = """
                    INSERT INTO Nutrient (Name, Category, Quantity, Unit, MealLogID) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(nutrient_query, (
                    nutrient['name'],
                    nutrient['category'],
                    nutrient['quantity'],
                    nutrient['unit'],
                    meal_id
                ))
        
        conn.commit()
        
        return jsonify({"message": "Meal log updated successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to delete a meal log
@meals_bp.route('/meal-logs/<int:meal_id>', methods=['DELETE'])
def delete_meal_log(meal_id):
    """Delete a meal log entry"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if meal log exists
        cursor.execute("SELECT ID FROM MealLog WHERE ID = %s", (meal_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Meal log not found"}), 404
        
        # Delete associated nutrients first (due to foreign key constraint)
        cursor.execute("DELETE FROM Nutrient WHERE MealLogID = %s", (meal_id,))
        
        # Delete the meal log
        cursor.execute("DELETE FROM MealLog WHERE ID = %s", (meal_id,))
        conn.commit()
        
        return jsonify({"message": "Meal log deleted successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to get summary of nutrients for a specific day
@meals_bp.route('/meal-logs/daily-summary', methods=['GET'])
def get_daily_summary():
    """Get a summary of nutrients for a specific day"""
    try:
        # Get query parameters
        client_id = request.args.get('client_id')
        date = request.args.get('date')
        
        # Both parameters are required
        if not client_id or not date:
            return jsonify({"error": "client_id and date parameters are required"}), 400
        
        try:
            # Validate date format
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all meals for the specific day
        cursor.execute("""
            SELECT MealLog.ID
            FROM MealLog
            WHERE ClientID = %s AND DATE(Datetime) = %s
            ORDER BY Datetime
        """, (client_id, date))
        
        meal_ids = [meal['ID'] for meal in cursor.fetchall()]
        
        if not meal_ids:
            return jsonify({
                "client_id": int(client_id),
                "date": date,
                "meals_count": 0,
                "nutrients_summary": {},
                "message": "No meals recorded for this day"
            }), 200
        
        # Get nutrients summary
        placeholders = ', '.join(['%s'] * len(meal_ids))
        query = f"""
            SELECT 
                Category,
                Name,
                SUM(Quantity) as total,
                Unit
            FROM Nutrient
            WHERE MealLogID IN ({placeholders})
            GROUP BY Category, Name, Unit
            ORDER BY Category, Name
        """
        
        cursor.execute(query, meal_ids)
        nutrients = cursor.fetchall()
        
        # Format the result
        nutrients_by_category = {}
        for nutrient in nutrients:
            category = nutrient['Category']
            if category not in nutrients_by_category:
                nutrients_by_category[category] = []
                
            nutrients_by_category[category].append({
                'name': nutrient['Name'],
                'total': float(nutrient['total']),
                'unit': nutrient['Unit']
            })
        
        return jsonify({
            "client_id": int(client_id),
            "date": date,
            "meals_count": len(meal_ids),
            "nutrients_summary": nutrients_by_category
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close() 