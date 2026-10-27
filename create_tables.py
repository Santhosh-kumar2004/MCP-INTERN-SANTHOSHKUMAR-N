from database import Base, engine
from models import JobApplication

Base.metadata.create_all(bind=engine)

print("Job applications table created successfully!")
