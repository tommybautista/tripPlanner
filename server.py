from flask_app.TripPlanner import app
from flask_app.TripPlanner.controllers import mainDashboards, users, events, tripBudgets

if __name__ == "__main__":
    app.run(debug=True)