from database import Base, engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("Tables created successfully! 🎉💖")

