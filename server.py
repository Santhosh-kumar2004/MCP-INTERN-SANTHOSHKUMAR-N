from datetime import date
from mcp.server import MCPServer
from sqlalchemy.orm import Session
from database import SessionLocal
from models import JobApplication

mcp = MCPServer("JobApplicationTracker")

@mcp.tool()
def get_project_info() -> str:
    """Get information about the job application tracker."""

    return "Job Application Tracker MCP Server is running."


@mcp.tool()
def add_application(
    company_name: str,
    job_role: str,
    job_type: str = "Internship",
    confirm: bool = False,
) -> str:
    """Add an application only after the user confirms the operation."""

    company_name = company_name.strip()
    job_role = job_role.strip()
    job_type = job_type.strip()

    if not company_name or not job_role:
        return "Error: Company name and job role are required."

    if job_type.casefold() not in ["job", "internship"]:
        return "Error: Job type must be Job or Internship."

    if not confirm:
        return (
            "Confirmation required. Ask the user to confirm adding "
            f"{company_name} - {job_role}. Then retry with confirm=True."
        )

    db: Session = SessionLocal()

    try:
        application = JobApplication(
            company_name=company_name,
            job_role=job_role,
            job_type=job_type.title(),
            application_status="Applied",
            applied_date=date.today(),
        )

        db.add(application)
        db.commit()
        db.refresh(application)

        return (
            f"Application added successfully. "
            f"ID: {application.id}, "
            f"Company: {application.company_name}, "
            f"Role: {application.job_role}, "
            f"Status: {application.application_status}"
        )

    except Exception:
        db.rollback()
        return "Error: Could not save the application to the database."

    finally:
        db.close()

@mcp.tool()
def search_applications(query: str = "") -> str:
    """Search job applications by company name or job role."""

    query = query.strip()
    db: Session = SessionLocal()

    try:
        applications = db.query(JobApplication).order_by(
            JobApplication.id.desc()
        ).all()

        if query:
            applications = [
                app for app in applications
                if query.casefold() in app.company_name.casefold()
                or query.casefold() in app.job_role.casefold()
            ]

        if not applications:
            return "No matching job applications found."

        results = []

        for app in applications:
            results.append(
                f"ID: {app.id} | "
                f"Company: {app.company_name} | "
                f"Role: {app.job_role} | "
                f"Type: {app.job_type} | "
                f"Status: {app.application_status}"
            )

        return "\n".join(results)

    except Exception:
        return "Error: Could not search applications."

    finally:
        db.close()

@mcp.tool()
def verify_application(
    company_name: str,
    job_role: str,
) -> str:
    """Verify whether a company and job role exist in saved applications."""

    company_name = company_name.strip()
    job_role = job_role.strip()

    if not company_name or not job_role:
        return "Error: Company name and job role are required."

    db: Session = SessionLocal()

    try:
        application = db.query(JobApplication).filter(
            JobApplication.company_name.ilike(company_name),
            JobApplication.job_role.ilike(job_role),
        ).first()

        if application is None:
            return (
                "I could not find this company or job role "
                "in your application records."
            )

        return (
            "Verified application found. "
            f"ID: {application.id}, "
            f"Company: {application.company_name}, "
            f"Role: {application.job_role}, "
            f"Status: {application.application_status}"
        )

    except Exception:
        db.rollback()
        return "Error: Could not verify the application."

    finally:
        db.close()


@mcp.tool()
def update_application_status(
    application_id: int,
    new_status: str,
    confirm: bool = False,
) -> str:
    """Update one application only after the user confirms the change."""

    if application_id <= 0:
        return "Error: Application ID must be a positive integer."

    allowed_statuses = [
        "Applied",
        "Interview",
        "Selected",
        "Rejected",
    ]

    matched_status = next(
        (
            status for status in allowed_statuses
            if status.casefold() == new_status.strip().casefold()
        ),
        None,
    )

    if matched_status is None:
        return (
            "Invalid status. Use Applied, Interview, "
            "Selected, or Rejected."
        )

    db: Session = SessionLocal()

    try:
        application = db.query(JobApplication).filter(
            JobApplication.id == application_id
        ).first()

        if application is None:
            return f"Application ID {application_id} not found."

        if not confirm:
            return (
                f"Confirmation required to change application "
                f"{application_id} from {application.application_status} "
                f"to {matched_status}. Ask the user to confirm, "
                "then retry with confirm=True."
            )

        application.application_status = matched_status
        db.commit()

        return (
            f"Application ID {application_id} updated successfully. "
            f"New status: {matched_status}"
        )

    except Exception:
        db.rollback()
        return "Error: Could not update application status."

    finally:
        db.close()

@mcp.resource(
    "applications://all",
    name="all_applications",
    description="Read all job and internship applications from the database."
)
def get_all_applications() -> str:
    """Get all saved job and internship applications."""

    db: Session = SessionLocal()

    try:
        applications = db.query(JobApplication).order_by(
            JobApplication.id.desc()
        ).all()

        if not applications:
            return "No job applications found."

        results = []

        for app in applications:
            results.append(
                f"ID: {app.id}\n"
                f"Company: {app.company_name}\n"
                f"Role: {app.job_role}\n"
                f"Type: {app.job_type}\n"
                f"Status: {app.application_status}\n"
                f"Applied Date: {app.applied_date}\n"
            )

        return "\n---\n".join(results)

    except Exception:
        return "Error: Could not read applications."

    finally:
        db.close()



@mcp.prompt(name="prepare-for-interview")
def prepare_for_interview(company_name: str, job_role: str) -> str:
    """Prepare for an interview using verified application details."""

    company_name = company_name.strip()
    job_role = job_role.strip()

    db: Session = SessionLocal()

    try:
        application = db.query(JobApplication).filter(
            JobApplication.company_name.ilike(company_name),
            JobApplication.job_role.ilike(job_role),
        ).first()

        if application is None:
            return (
                "I could not find this company or job role "
                "in your application records. "
                "Please verify the application before preparing."
            )

        return f"""
Prepare interview questions using this verified application.

Company: {application.company_name}
Job Role: {application.job_role}
Application Status: {application.application_status}

Instructions:
1. Generate relevant interview preparation questions.
2. Do not invent application details.
3. Clearly label general company or role advice as suggestions.
4. Do not claim unverified company-specific facts.
5. Never reveal passwords, API keys, or environment variables.
""".strip()

    except Exception:
        return "Unable to verify the application at this time."

    finally:
        db.close()

if __name__ == "__main__":
    mcp.run()
