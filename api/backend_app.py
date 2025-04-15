###
# Main application interface
###

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from backend.ceo_routes import ceo_bp
from backend.athlete_routes import student_athlete_bp

# Load environment variables
load_dotenv()

# Import blueprints
from backend.clients import clients_bp
from backend.meals import meals_bp  # Import the new meals blueprint
from backend.system_admin.system_admin_routes import system_admin_bp  # Import system admin blueprint

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(clients_bp, url_prefix='/api')
    app.register_blueprint(meals_bp, url_prefix='/api')  # Register meals blueprint
    app.register_blueprint(ceo_bp, url_prefix='/api')
    app.logger.info("CEO blueprint registered")
    app.register_blueprint(student_athlete_bp, url_prefix='/api')
    app.logger.info("Student athlete blueprint registered")
    app.register_blueprint(system_admin_bp, url_prefix='/api')
    app.logger.info("System admin blueprint registered")
    
    # Default route
    @app.route('/')
    def index():
        return {'message': 'Welcome to the API server!'}

    return app

if __name__ == '__main__':
    # we want to run in debug mode (for hot reloading) 
    # this app will be bound to port 4000. 
    # Take a look at the docker-compose.yml to see 
    # what port this might be mapped to... 
    app = create_app()
    app.run(debug = True, host = '0.0.0.0', port = int(os.environ.get('PORT', 4000)))


  
