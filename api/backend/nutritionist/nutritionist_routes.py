from flask import jsonify, request
from ..db import get_db
from . import nutritionist_bp

@nutritionist_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    """Get nutritionist dashboard data"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get total number of clients
        cursor.execute("SELECT COUNT(*) as total_clients FROM clients")
        total_clients = cursor.fetchone()['total_clients']
        
        # Get recent client activities
        cursor.execute("""
            SELECT c.client_id, c.name, c.email, 
                   COUNT(m.meal_id) as total_meals,
                   MAX(m.date) as last_meal_date
            FROM clients c
            LEFT JOIN meals m ON c.client_id = m.client_id
            GROUP BY c.client_id
            ORDER BY last_meal_date DESC
            LIMIT 5
        """)
        recent_activities = cursor.fetchall()
        
        return jsonify({
            'total_clients': total_clients,
            'recent_activities': recent_activities
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutritionist_bp.route('/clients', methods=['GET'])
def get_clients():
    """Get all clients assigned to the nutritionist"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT c.*, 
                   COUNT(m.meal_id) as total_meals,
                   AVG(m.calories) as avg_calories
            FROM clients c
            LEFT JOIN meals m ON c.client_id = m.client_id
            GROUP BY c.client_id
        """)
        clients = cursor.fetchall()
        
        return jsonify(clients), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutritionist_bp.route('/client/<int:client_id>', methods=['GET'])
def get_client_details(client_id):
    """Get detailed information about a specific client"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get client basic info
        cursor.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
        client = cursor.fetchone()
        
        if not client:
            return jsonify({'error': 'Client not found'}), 404
            
        # Get client's recent meals
        cursor.execute("""
            SELECT * FROM meals 
            WHERE client_id = %s 
            ORDER BY date DESC 
            LIMIT 7
        """, (client_id,))
        recent_meals = cursor.fetchall()
        
        # Get client's nutritional trends
        cursor.execute("""
            SELECT 
                DATE(date) as meal_date,
                AVG(calories) as avg_calories,
                AVG(protein) as avg_protein,
                AVG(carbs) as avg_carbs,
                AVG(fats) as avg_fats
            FROM meals
            WHERE client_id = %s
            GROUP BY DATE(date)
            ORDER BY meal_date DESC
            LIMIT 30
        """, (client_id,))
        nutritional_trends = cursor.fetchall()
        
        return jsonify({
            'client': client,
            'recent_meals': recent_meals,
            'nutritional_trends': nutritional_trends
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutritionist_bp.route('/client/<int:client_id>/progress', methods=['GET'])
def get_client_progress(client_id):
    """Get client's progress and nutritional analysis"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # Get client's weight history
        cursor.execute("""
            SELECT date, weight, body_fat_percentage
            FROM client_measurements
            WHERE client_id = %s
            ORDER BY date DESC
        """, (client_id,))
        measurements = cursor.fetchall()
        
        # Get client's nutritional deficiencies
        cursor.execute("""
            SELECT 
                nutrient_name,
                recommended_amount,
                AVG(amount) as average_intake,
                (recommended_amount - AVG(amount)) as deficiency
            FROM meal_nutrients mn
            JOIN nutrients n ON mn.nutrient_id = n.nutrient_id
            JOIN meals m ON mn.meal_id = m.meal_id
            WHERE m.client_id = %s
            GROUP BY nutrient_name, recommended_amount
            HAVING deficiency > 0
        """, (client_id,))
        deficiencies = cursor.fetchall()
        
        return jsonify({
            'measurements': measurements,
            'deficiencies': deficiencies
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 