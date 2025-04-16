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
    conn = None
    cursor = None
    try:
        # Get query parameters
        name = request.args.get('name', '')
        email = request.args.get('email', '')
        
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
                'email': client['Email']
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
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
            'email': client['Email']
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
        query = "INSERT INTO Client (Name, DOB, Email) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['name'], dob, data['email']))
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
        if not any(key in data for key in ['name', 'dob', 'email']):
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
                (SELECT COUNT(*) FROM NutritionPlan WHERE ClientID = %s) +
                (SELECT COUNT(*) FROM ProgressReport WHERE ClientID = %s) as total
        """, (client_id, client_id, client_id))
        
        result = cursor.fetchone()
        if result and result['total'] > 0:
            # There are associated records, so we should not delete but archive instead
            # Note: In a real system, you might add an 'is_active' field to Client table
            # For this example, we'll just return a message
            return jsonify({
                "message": "Client has associated data and cannot be deleted. Consider archiving instead.",
                "has_associated_data": True
            }), 400
        
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
                'age': client['age']
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
        cursor.execute("SELECT COUNT(*) as total FROM Client")
        total_clients = cursor.fetchone()['total']
        
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
            'new_clients': new_clients,
            'existing_clients': total_clients - new_clients,
            'trend_data': trend_data
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        cursor.close()
        conn.close() 