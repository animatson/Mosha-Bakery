from Bakery import app, db

# Create the database tables if they do not exist
with app.app_context():
    db.create_all()
    # This ensures that the database is created when the application starts