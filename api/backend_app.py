###
# Main application interface
###

from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import blueprints
from api.backend.customers import customers_bp
from api.backend.products import products_bp
from api.backend.clients import clients_bp
from api.backend.meals import meals_bp  # Import the new meals blueprint

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/api')
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(clients_bp, url_prefix='/api')
    app.register_blueprint(meals_bp, url_prefix='/api')  # Register meals blueprint
    
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
