from sqlalchemy import Column, Integer, String, Date
from database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100), nullable=False)
    job_role = Column(String(100), nullable=False)
    job_type = Column(String(30), default="Internship")
    application_status = Column(
        String(30),
        default="Applied",
        nullable=False
    )
    applied_date = Column(Date, nullable=True)
    notes = Column(String(500), nullable=True)
