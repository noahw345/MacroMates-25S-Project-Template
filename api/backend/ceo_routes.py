from flask import Blueprint, jsonify
from backend.db import get_db_connection
import datetime

ceo_bp = Blueprint('ceo', __name__)

@ceo_bp.route('/ceo/key_metrics', methods=['GET'])
def get_ceo_key_metrics():
    """
    API route to get key metrics for the CEO dashboard.
    Returns:
        A JSON response containing key metrics data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEODashboardKeyMetrics")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/growth_trend', methods=['GET'])
def get_ceo_growth_trend():
    """
    API route to get growth trend data for the CEO dashboard.
    Returns:
        A JSON response containing growth trend data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEODashboardGrowthTrend ORDER BY Date")
        data = cursor.fetchall()
        
        for row in data:
            row['Date'] = row['Date'].strftime('%Y-%m-%d')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/engagement_indicators', methods=['GET'])
def get_ceo_engagement_indicators():
    """
    API route to get key engagement indicators for the CEO dashboard.
    Returns:
        A JSON response containing engagement indicators data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOEngagementIndicators")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/daily_active_users', methods=['GET'])
def get_ceo_daily_active_users():
    """
    API route to get daily active users data.
    Returns:
        A JSON response containing daily active users data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEODailyActiveUsers ORDER BY Date")
        data = cursor.fetchall()
        
        for row in data:
            row['Date'] = row['Date'].strftime('%Y-%m-%d')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/client_activity', methods=['GET'])
def get_ceo_client_activity():
    """
    API route to get client activity data.
    Returns:
        A JSON response containing client activity data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOClientActivity")
        data = cursor.fetchall()
        
        for row in data:
            row['LastLogin'] = row['LastLogin'].strftime('%Y-%m-%d')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/financial_indicators', methods=['GET'])
def get_ceo_financial_indicators():
    """
    API route to get financial indicators.
    Returns:
        A JSON response containing financial indicators data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOFinancialIndicators")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/revenue_trend', methods=['GET'])
def get_ceo_revenue_trend():
    """
    API route to get revenue trend data.
    Returns:
        A JSON response containing revenue trend data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEORevenueTrend ORDER BY Month")
        data = cursor.fetchall()
        
        for row in data:
            row['Month'] = row['Month'].strftime('%Y-%m-%d')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/expense_breakdown', methods=['GET'])
def get_ceo_expense_breakdown():
    """
    API route to get expense breakdown data.
    Returns:
        A JSON response containing expense breakdown data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOExpenseBreakdown")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/performance_indicators', methods=['GET'])
def get_ceo_performance_indicators():
    """
    API route to get system performance indicators.
    Returns:
        A JSON response containing system performance indicators data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOSystemPerformanceIndicators")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/api_response_time', methods=['GET'])
def get_ceo_api_response_time():
    """
    API route to get API response time data.
    Returns:
        A JSON response containing API response time data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOAPIResponseTime ORDER BY Time")
        data = cursor.fetchall()
        
        for row in data:
            row['Time'] = row['Time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@ceo_bp.route('/ceo/user_traffic', methods=['GET'])
def get_ceo_user_traffic():
    """
    API route to get user traffic data.
    Returns:
        A JSON response containing user traffic data.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CEOUserTraffic ORDER BY Hour")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()