from flask import Blueprint, request, jsonify
from datetime import datetime
import pymysql
from backend.db import get_db_connection  # Adjust if your db connection module is elsewhere

system_admin_bp = Blueprint('system_admin', __name__, url_prefix='/api')


# 1) GET /api/system-performance
@system_admin_bp.route('/system-performance', methods=['GET'])
def get_system_performance():
    """
    Retrieve system performance metrics (e.g., CPU usage, memory usage, client counts)
    from the SystemPerformance table.
    
    Example table schema:
        SystemPerformance(
          PerformanceID INT (PK),
          Performance_Metric VARCHAR(255),
          System_Status VARCHAR(255),
          Existing_Clients INT,
          New_Clients INT,
          Timestamp DATETIME
        )
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
          SELECT 
            PerformanceID as id,
            Performance_Metric,
            System_Status,
            Existing_Clients,
            New_Clients,
            Timestamp
          FROM SystemPerformance
          ORDER BY Timestamp
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Convert rows to a list of dictionaries
        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "Performance_Metric": row["Performance_Metric"],
                "System_Status": row["System_Status"],
                "Existing_Clients": row["Existing_Clients"],
                "New_Clients": row["New_Clients"],
                "Timestamp": row["Timestamp"].strftime("%Y-%m-%d %H:%M:%S") if row["Timestamp"] else None
            })

        return jsonify(results), 200

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# 2) GET /api/datasets
@system_admin_bp.route('/datasets', methods=['GET'])
def get_datasets():
    """
    Retrieve all dataset records. 
    Example table schema:
        Dataset(
          DatasetID INT (PK),
          Dataset_Name VARCHAR(255),
          Data_Description TEXT,
          Status VARCHAR(50)
        )
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
          SELECT
            DatasetID as id,
            Dataset_Name,
            Data_Description,
            Status
          FROM Dataset
          ORDER BY DatasetID
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                "id": row["id"],
                "dataset_name": row["Dataset_Name"],
                "data_description": row["Data_Description"],
                "status": row["Status"]
            })

        return jsonify(results), 200

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# 3) POST /api/datasets
@system_admin_bp.route('/datasets', methods=['POST'])
def create_dataset():
    """
    Create a new dataset entry.
    Expected JSON body:
      {
        "dataset_name": "My Dataset",
        "data_description": "Some description",
        "status": "Active"
      }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Validate required fields
        required_fields = ["dataset_name", "data_description", "status"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields in JSON body"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
          INSERT INTO Dataset (Dataset_Name, Data_Description, Status)
          VALUES (%s, %s, %s)
        """
        cursor.execute(query, (
            data["dataset_name"],
            data["data_description"],
            data["status"]
        ))
        conn.commit()

        new_id = cursor.lastrowid
        return jsonify({"message": "Dataset created successfully", "id": new_id}), 201

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()



# 4) PUT /api/datasets/<int:dataset_id>
@system_admin_bp.route('/datasets/<int:dataset_id>', methods=['PUT'])
def update_dataset(dataset_id):
    """
    Update an existing dataset record.
    Expected JSON body:
      {
        "data_description": "New description",
        "status": "Active" (optional)
      }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No update data provided"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the dataset exists
        check_query = "SELECT DatasetID FROM Dataset WHERE DatasetID = %s"
        cursor.execute(check_query, (dataset_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Dataset not found"}), 404

        update_fields = []
        params = []

        # Check updatable fields
        if "data_description" in data and data["data_description"]:
            update_fields.append("Data_Description = %s")
            params.append(data["data_description"])

        if "status" in data and data["status"]:
            update_fields.append("Status = %s")
            params.append(data["status"])

        if not update_fields:
            return jsonify({"message": "No fields to update"}), 200

        params.append(dataset_id)

        query = f"""
          UPDATE Dataset
          SET {', '.join(update_fields)}
          WHERE DatasetID = %s
        """
        cursor.execute(query, params)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "No changes made"}), 200

        return jsonify({"message": "Dataset updated successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# 5) DELETE /api/datasets/<int:dataset_id>
@system_admin_bp.route('/datasets/<int:dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    """
    Delete an existing dataset entry.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the dataset exists
        check_query = "SELECT DatasetID FROM Dataset WHERE DatasetID = %s"
        cursor.execute(check_query, (dataset_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Dataset not found"}), 404

        delete_query = "DELETE FROM Dataset WHERE DatasetID = %s"
        cursor.execute(delete_query, (dataset_id,))
        conn.commit()

        return jsonify({"message": f"Dataset {dataset_id} deleted successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
