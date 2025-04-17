# MacroMates - Your Intelligent Nutrition Companion

MacroMates is a data-driven nutrition tracking application designed to help users make informed dietary choices without the guesswork. Our platform serves different stakeholders including individual clients, student athletes, and company executives.

![MacroMates Logo](app/assets/logo.png)

## Project Overview

MacroMates empowers individuals to achieve their health and fitness goals through personalized nutrition tracking and intelligent recommendations. The application includes:

- **Smart Meal Logging**: Easily track meals and automatically calculate nutritional content
- **Personalized Goal Setting**: Set and track progress towards specific nutrition goals
- **Intelligent Recommendations**: Receive suggestions for meal adjustments to meet goals
- **Progress Tracking**: Monitor nutrition journey with intuitive visualizations
- **Role-Based Access**: Different interfaces for clients, athletes, and executives

## Technical Architecture

The application consists of three main components:

1. **Streamlit Frontend** (`./app` directory): Web interface with role-specific dashboards
2. **Flask REST API** (`./api` directory): Backend services for data processing and business logic
3. **MySQL Database** (`./database-files` directory): Data storage initialized with SQL scripts


### Installation

1. Clone this repository to your local machine
2. Set up the `.env` file in the `api` folder based on the `.env.template` file
3. Start the containers with Docker Compose:
   ```
   docker compose up -d
   ```

### Running the Application

Once the containers are running:

1. Access the Streamlit app at: http://localhost:8501
2. API endpoints are available at: http://localhost:4000/api
3. MySQL database runs on port 3306

To stop the containers:
```
docker compose down
```

## User Roles

MacroMates supports multiple user roles with tailored interfaces:

1. **Clients**: Individual users tracking personal nutrition goals
2. **Student Athletes**: Athletes with specialized nutrition and workout plans
3. **CEO/Executive & System Admin**: Dashboard with business metrics, client engagement, and system performance

## Development

The codebase is organized as follows:

- `app/src/pages/` - Streamlit pages organized by role (30s: CEO, 35-37: Athlete, 40s: Clients)
- `app/src/modules/` - Shared utilities and navigation components
- `api/` - Backend REST API endpoints and business logic
- `database-files/` - SQL initialization scripts
