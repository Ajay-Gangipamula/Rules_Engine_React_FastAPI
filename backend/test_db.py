from database import SessionLocal

# Try to connect to the database
try:
    db = SessionLocal()
    print("Database connection successful! 🎉💖")
    db.close()
except Exception as e:
    print("Database connection failed:", e)
