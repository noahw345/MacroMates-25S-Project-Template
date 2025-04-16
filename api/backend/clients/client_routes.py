########################################################
# Client Routes Blueprint
########################################################

from flask import Blueprint, request, jsonify
from datetime import datetime 
import pymysql
from backend.db import get_db_connection

# Create the blueprint
clients_bp = Blueprint('clients', __name__)

# Route to get all clients
@clients_bp.route('/clients', methods=['GET'])
def get_all_clients():
    """Retrieve all clients or filter by query parameters"""
    try:
        # Get query parameters
        name = request.args.get('name', '')
        email = request.args.get('email', '')
        include_archived = request.args.get('include_archived', 'false').lower() == 'true'
        only_archived = request.args.get('only_archived', 'false').lower() == 'true'
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query
        query = "SELECT * FROM Client WHERE 1=1"
        params = []
        
        # Add filters if provided
        if name:
            query += " AND Name LIKE %s"
            params.append(f"%{name}%")
        
        if email:
            query += " AND Email LIKE %s"
            params.append(f"%{email}%")
        
        # Handle archived status filtering
        if only_archived:
            query += " AND is_archived = TRUE"
        elif not include_archived:
            query += " AND is_archived = FALSE"
        
        # Execute the query
        cursor.execute(query, params)
        clients = cursor.fetchall()
        
        # Format the result
        result = []
        for client in clients:
            result.append({
                'id': client['ID'],
                'name': client['Name'],
                'dob': client['DOB'].strftime('%Y-%m-%d') if client['DOB'] else None,
                'email': client['Email'],
                'is_archived': bool(client['is_archived'])
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to get a specific client by ID
@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    """Retrieve a single client by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Client WHERE ID = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            return jsonify({"error": "Client not found"}), 404
        
        result = {
            'id': client['ID'],
            'name': client['Name'],
            'dob': client['DOB'].strftime('%Y-%m-%d') if client['DOB'] else None,
            'email': client['Email'],
            'is_archived': bool(client['is_archived'])
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to add a new client
@clients_bp.route('/clients', methods=['POST'])
def add_client():
    """Add a new client during onboarding"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['name', 'email']):
            return jsonify({"error": "Name and email are required fields"}), 400
        
        # Parse date of birth if provided
        dob = None
        if 'dob' in data and data['dob']:
            try:
                dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT ID FROM Client WHERE Email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 409
        
        # Insert new client
        query = "INSERT INTO Client (Name, DOB, Email, is_archived) VALUES (%s, %s, %s, %s)"
        is_archived = data.get('is_archived', False)
        cursor.execute(query, (data['name'], dob, data['email'], is_archived))
        conn.commit()
        
        # Get the ID of the newly created client
        new_id = cursor.lastrowid
        
        return jsonify({
            "message": "Client created successfully",
            "id": new_id
        }), 201
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to update a client
@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    """Update client details (contact info, status, etc.)"""
    try:
        data = request.get_json()
        
        # Ensure at least one field to update
        if not any(key in data for key in ['name', 'dob', 'email', 'is_archived']):
            return jsonify({"error": "No fields to update provided"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT ID FROM Client WHERE ID = %s", (client_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Client not found"}), 404
        
        # Check email uniqueness if updating email
        if 'email' in data:
            cursor.execute("SELECT ID FROM Client WHERE Email = %s AND ID != %s", 
                          (data['email'], client_id))
            if cursor.fetchone():
                return jsonify({"error": "Email already in use by another client"}), 409
        
        # Build update query
        update_fields = []
        params = []
        
        if 'name' in data:
            update_fields.append("Name = %s")
            params.append(data['name'])
        
        if 'dob' in data:
            if data['dob']:
                try:
                    dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
                    update_fields.append("DOB = %s")
                    params.append(dob)
                except ValueError:
                    return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
            else:
                update_fields.append("DOB = NULL")
        
        if 'email' in data:
            update_fields.append("Email = %s")
            params.append(data['email'])
            
        if 'is_archived' in data:
            update_fields.append("is_archived = %s")
            params.append(data['is_archived'])
        
        # Add client_id to params
        params.append(client_id)
        
        # Execute update
        query = f"UPDATE Client SET {', '.join(update_fields)} WHERE ID = %s"
        cursor.execute(query, params)
        conn.commit()
        
        # Check if anything was updated
        if cursor.rowcount == 0:
            return jsonify({"message": "No changes made"}), 200
        
        return jsonify({"message": "Client updated successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to delete a client
@clients_bp.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    """Remove or archive inactive clients"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT ID FROM Client WHERE ID = %s", (client_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Client not found"}), 404
        
        # Check if client has associated data (meal logs, nutrition plans, reports)
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM MealLog WHERE ClientID = %s) +
                (SELECT COUNT(*) FROM NutritionPlan WHERE ClientID = %s) as total
        """, (client_id, client_id))
        
        result = cursor.fetchone()
        if result and result['total'] > 0:
            # There are associated records, so we should not delete but archive instead
            cursor.execute("UPDATE Client SET is_archived = TRUE WHERE ID = %s", (client_id,))
            conn.commit()
            return jsonify({
                "message": "Client has associated data and was archived instead of deleted",
                "has_associated_data": True,
                "was_archived": True
            }), 200
        
        # Delete the client
        cursor.execute("DELETE FROM Client WHERE ID = %s", (client_id,))
        conn.commit()
        
        return jsonify({"message": "Client deleted successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to archive a client
@clients_bp.route('/clients/<int:client_id>/archive', methods=['PUT'])
def archive_client(client_id):
    """Archive a client to keep workspace organized"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT ID, is_archived FROM Client WHERE ID = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            return jsonify({"error": "Client not found"}), 404
        
        if client['is_archived']:
            return jsonify({"message": "Client is already archived"}), 200
        
        # Archive the client
        cursor.execute("UPDATE Client SET is_archived = TRUE WHERE ID = %s", (client_id,))
        conn.commit()
        
        return jsonify({"message": "Client archived successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to restore an archived client
@clients_bp.route('/clients/<int:client_id>/restore', methods=['PUT'])
def restore_client(client_id):
    """Restore an archived client"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if client exists
        cursor.execute("SELECT ID, is_archived FROM Client WHERE ID = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            return jsonify({"error": "Client not found"}), 404
        
        if not client['is_archived']:
            return jsonify({"message": "Client is not archived"}), 200
        
        # Restore the client
        cursor.execute("UPDATE Client SET is_archived = FALSE WHERE ID = %s", (client_id,))
        conn.commit()
        
        return jsonify({"message": "Client restored successfully"}), 200
    
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to search clients
@clients_bp.route('/clients/search', methods=['GET'])
def search_clients():
    """Search clients with more advanced filters"""
    try:
        # Get query parameters
        name = request.args.get('name', '')
        email = request.args.get('email', '')
        min_age = request.args.get('min_age')
        max_age = request.args.get('max_age')
        include_archived = request.args.get('include_archived', 'false').lower() == 'true'
        only_archived = request.args.get('only_archived', 'false').lower() == 'true'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Base query using year calculation for age filtering
        query = """
            SELECT *, 
            TIMESTAMPDIFF(YEAR, DOB, CURDATE()) as age 
            FROM Client 
            WHERE 1=1
        """
        params = []
        
        # Add filters
        if name:
            query += " AND Name LIKE %s"
            params.append(f"%{name}%")
        
        if email:
            query += " AND Email LIKE %s"
            params.append(f"%{email}%")
        
        if min_age:
            query += " AND TIMESTAMPDIFF(YEAR, DOB, CURDATE()) >= %s"
            params.append(int(min_age))
        
        if max_age:
            query += " AND TIMESTAMPDIFF(YEAR, DOB, CURDATE()) <= %s"
            params.append(int(max_age))
            
        # Handle archived status filtering
        if only_archived:
            query += " AND is_archived = TRUE"
        elif not include_archived:
            query += " AND is_archived = FALSE"
        
        # Execute the query
        cursor.execute(query, params)
        clients = cursor.fetchall()
        
        # Format the result
        result = []
        for client in clients:
            result.append({
                'id': client['ID'],
                'name': client['Name'],
                'dob': client['DOB'].strftime('%Y-%m-%d') if client['DOB'] else None,
                'email': client['Email'],
                'age': client['age'],
                'is_archived': bool(client['is_archived'])
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to get system stats (for admin dashboard)
@clients_bp.route('/clients/stats', methods=['GET'])
def get_client_stats():
    """Get client statistics for System Admin dashboard"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get time range parameters
        from_date = request.args.get('from_date', datetime.now().replace(day=1).strftime('%Y-%m-%d'))
        to_date = request.args.get('to_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Get total clients count
        cursor.execute("SELECT COUNT(*) as total FROM Client WHERE is_archived = FALSE")
        total_clients = cursor.fetchone()['total']
        
        # Get archived clients count
        cursor.execute("SELECT COUNT(*) as total FROM Client WHERE is_archived = TRUE")
        total_archived = cursor.fetchone()['total']
        
        # Get new clients count (assuming SystemPerformance table tracks this)
        cursor.execute("""
            SELECT SUM(New_Clients) as new_clients
            FROM SystemPerformance
            WHERE DATE(Timestamp) BETWEEN %s AND %s
        """, (from_date, to_date))
        
        new_clients_result = cursor.fetchone()
        new_clients = new_clients_result['new_clients'] if new_clients_result and new_clients_result['new_clients'] else 0
        
        # Get existing clients data
        cursor.execute("""
            SELECT 
                DATE(Timestamp) as date,
                Existing_Clients as existing_clients,
                New_Clients as new_clients
            FROM SystemPerformance
            WHERE DATE(Timestamp) BETWEEN %s AND %s
            ORDER BY Timestamp
        """, (from_date, to_date))
        
        trend_data = []
        for row in cursor.fetchall():
            trend_data.append({
                'date': row['date'].strftime('%Y-%m-%d'),
                'existing_clients': row['existing_clients'],
                'new_clients': row['new_clients']
            })
        
        return jsonify({
            'total_clients': total_clients,
            'total_archived': total_archived,
            'new_clients': new_clients,
            'existing_clients': total_clients - new_clients,
            'trend_data': trend_data
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close()

# Route to get nutrition metrics dashboard
@clients_bp.route('/clients/nutrition-dashboard', methods=['GET'])
def get_nutrition_dashboard():
    """Get consolidated view of all clients with nutrition metrics averages and alerts"""
    try:
        # Get query parameters
        days = int(request.args.get('days', '30'))  # Default to last 30 days
        include_archived = request.args.get('include_archived', 'false').lower() == 'true'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all active clients
        query = "SELECT ID, Name, Email, DOB FROM Client WHERE 1=1"
        if not include_archived:
            query += " AND is_archived = FALSE"
        cursor.execute(query)
        clients = cursor.fetchall()
        
        result = []
        
        # For each client, get nutrition metrics
        for client in clients:
            client_id = client['ID']
            
            # Get latest nutrition plan
            cursor.execute("""
                SELECT ID, StartDate, EndDate, CaloriesGoal
                FROM NutritionPlan
                WHERE ClientID = %s
                ORDER BY StartDate DESC
                LIMIT 1
            """, (client_id,))
            latest_plan = cursor.fetchone()
            
            # Calculate the average macronutrients
            cursor.execute("""
                SELECT 
                    AVG(CASE WHEN n.Name = 'Protein' THEN n.Quantity ELSE NULL END) as avg_protein,
                    AVG(CASE WHEN n.Name = 'Carbohydrates' THEN n.Quantity ELSE NULL END) as avg_carbs,
                    AVG(CASE WHEN n.Name = 'Fat' THEN n.Quantity ELSE NULL END) as avg_fat,
                    AVG(CASE WHEN n.Name = 'Fiber' THEN n.Quantity ELSE NULL END) as avg_fiber,
                    COUNT(DISTINCT ml.ID) as total_meals
                FROM MealLog ml
                JOIN Nutrient n ON ml.ID = n.MealLogID
                WHERE ml.ClientID = %s AND ml.Datetime >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """, (client_id, days))
            
            metrics = cursor.fetchone()
            
            # Get latest deficiency alerts from progress reports - REMOVED due to removal of progress reports functionality
            # cursor.execute("""
            #     SELECT ID, CreatedDate, DeficiencyAlerts
            #     FROM ProgressReport
            #     WHERE ClientID = %s AND DeficiencyAlerts IS NOT NULL
            #     ORDER BY CreatedDate DESC
            #     LIMIT 1
            # """, (client_id,))
            # latest_report = cursor.fetchone()
            latest_report = None
            
            # Get meal log activity
            cursor.execute("""
                SELECT COUNT(*) as log_count, MAX(Datetime) as last_logged
                FROM MealLog
                WHERE ClientID = %s AND Datetime >= DATE_SUB(NOW(), INTERVAL %s DAY)
            """, (client_id, days))
            
            activity = cursor.fetchone()
            
            # Calculate age
            age = None
            if client['DOB']:
                today = datetime.now().date()
                dob = client['DOB']
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            # Format client data with nutrition metrics
            client_data = {
                'id': client['ID'],
                'name': client['Name'],
                'email': client['Email'],
                'age': age,
                'nutrition_plan': {
                    'id': latest_plan['ID'] if latest_plan else None,
                    'start_date': latest_plan['StartDate'].strftime('%Y-%m-%d') if latest_plan and latest_plan['StartDate'] else None,
                    'end_date': latest_plan['EndDate'].strftime('%Y-%m-%d') if latest_plan and latest_plan['EndDate'] else None,
                    'calories_goal': latest_plan['CaloriesGoal'] if latest_plan else None
                } if latest_plan else None,
                'metrics': {
                    'avg_protein': float(metrics['avg_protein']) if metrics['avg_protein'] else 0,
                    'avg_carbs': float(metrics['avg_carbs']) if metrics['avg_carbs'] else 0,
                    'avg_fat': float(metrics['avg_fat']) if metrics['avg_fat'] else 0,
                    'avg_fiber': float(metrics['avg_fiber']) if metrics['avg_fiber'] else 0,
                    'total_meals': metrics['total_meals'] or 0
                },
                'activity': {
                    'log_count': activity['log_count'] or 0,
                    'last_logged': activity['last_logged'].strftime('%Y-%m-%d %H:%M:%S') if activity['last_logged'] else None,
                    'days_since_last_log': (datetime.now() - activity['last_logged']).days if activity['last_logged'] else None
                },
                'alerts': {
                    'deficiencies': latest_report['DeficiencyAlerts'] if latest_report else None,
                    'report_date': latest_report['CreatedDate'].strftime('%Y-%m-%d') if latest_report and latest_report['CreatedDate'] else None
                } if latest_report else None,
                'tracking_period': f"Last {days} days"
            }
            
            # Add adherence flags/alerts
            adherence_issues = []
            
            # No meal logs in last 7 days
            if not activity['last_logged'] or (datetime.now() - activity['last_logged']).days > 7:
                adherence_issues.append("No meal logs in last 7 days")
            
            # Low meal log count
            if activity['log_count'] < (days / 7):  # Less than 1 log per week on average
                adherence_issues.append("Low meal logging activity")
            
            # Add issues to client data
            client_data['alerts'] = client_data.get('alerts', {}) or {}
            client_data['alerts']['adherence_issues'] = adherence_issues if adherence_issues else None
            
            result.append(client_data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close() 