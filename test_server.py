
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from server import (
    get_project_info,
    add_application,
    search_applications,
    verify_application,
    update_application_status,
    get_all_applications,
    prepare_for_interview,
)


def sample_application(
    app_id=101,
    company="Test Company",
    role="Python Developer",
    job_type="Internship",
    status="Applied",
):
    return SimpleNamespace(
        id=app_id,
        company_name=company,
        job_role=role,
        job_type=job_type,
        application_status=status,
        applied_date="2026-10-27",
    )


def mock_database():
    db = MagicMock()
    patcher = patch("server.SessionLocal", return_value=db)
    patcher.start()
    return db, patcher


def test_get_project_info():
    result = get_project_info()
    assert "running" in result.lower()


def test_add_valid_application():
    db, patcher = mock_database()
    try:
        db.refresh.side_effect = lambda app: setattr(app, "id", 101)

        result = add_application(
            company_name="Test Company",
            job_role="Python Developer",
            job_type="Internship",
            confirm=True,
        )

        assert "added successfully" in result.lower()
        assert "Test Company" in result
        assert "Python Developer" in result
        db.add.assert_called_once()
        db.commit.assert_called_once()
    finally:
        patcher.stop()


def test_empty_company_name():
    result = add_application("", "Python Developer")
    assert "required" in result.lower()


def test_empty_job_role():
    result = add_application("Test Company", "")
    assert "required" in result.lower()


def test_invalid_job_type():
    result = add_application(
        "Test Company", "Python Developer", "Full-time"
    )
    assert "job type" in result.lower()


def test_add_job_type_case_insensitive():
    db, patcher = mock_database()
    try:
        db.refresh.side_effect = lambda app: setattr(app, "id", 102)

        result = add_application(
            company_name="Test Company",
            job_role="Python Developer",
            job_type="jOb",
            confirm=True,
        )
    
        assert "added successfully" in result.lower()
        assert db.add.call_args[0][0].job_type == "Job"
    finally:
        patcher.stop()


def test_search_existing_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.order_by.return_value.all.return_value = [
            sample_application()
        ]

        result = search_applications("Test Company")

        assert "Test Company" in result
        assert "Python Developer" in result
    finally:
        patcher.stop()


def test_search_missing_company():
    db, patcher = mock_database()
    try:
        db.query.return_value.order_by.return_value.all.return_value = []

        result = search_applications("MissingCompany123")

        assert "no matching" in result.lower()
    finally:
        patcher.stop()


def test_search_case_insensitive():
    db, patcher = mock_database()
    try:
        db.query.return_value.order_by.return_value.all.return_value = [
            sample_application()
        ]

        result = search_applications("test company")

        assert "Test Company" in result
    finally:
        patcher.stop()


def test_verify_existing_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.filter.return_value.first.return_value = (
            sample_application()
        )

        result = verify_application(
            "Test Company", "Python Developer"
        )

        assert "verified application found" in result.lower()
        assert "Test Company" in result
    finally:
        patcher.stop()


def test_verify_missing_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.filter.return_value.first.return_value = None

        result = verify_application(
            "Missing Company", "Unknown Role"
        )

        assert "could not find" in result.lower()
    finally:
        patcher.stop()


def test_verify_empty_company():
    result = verify_application("", "Python Developer")
    assert "required" in result.lower()


def test_update_valid_status():
    db, patcher = mock_database()
    try:
        app = sample_application()
        db.query.return_value.filter.return_value.first.return_value = app

        result = update_application_status(
            application_id=101,
            new_status="Interview",
            confirm=True,
        )

        assert "updated successfully" in result.lower()
        assert app.application_status == "Interview"
        db.commit.assert_called_once()
    finally:
        patcher.stop()


def test_update_missing_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.filter.return_value.first.return_value = None

        result = update_application_status(999999, "Interview")

        assert "not found" in result.lower()
    finally:
        patcher.stop()


def test_invalid_application_status():
    result = update_application_status(101, "Pending")
    assert "invalid status" in result.lower()


def test_resource_returns_applications():
    db, patcher = mock_database()
    try:
        db.query.return_value.order_by.return_value.all.return_value = [
            sample_application()
        ]

        result = get_all_applications()

        assert "Test Company" in result
        assert "Python Developer" in result
        assert "Applied" in result
    finally:
        patcher.stop()


def test_resource_when_empty():
    db, patcher = mock_database()
    try:
        db.query.return_value.order_by.return_value.all.return_value = []

        result = get_all_applications()

        assert "no job applications found" in result.lower()
    finally:
        patcher.stop()


def test_prompt_for_verified_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.filter.return_value.first.return_value = (
            sample_application(status="Interview")
        )

        result = prepare_for_interview(
            "Test Company", "Python Developer"
        )

        assert "Test Company" in result
        assert "Python Developer" in result
        assert "Interview" in result
    finally:
        patcher.stop()


def test_prompt_for_missing_application():
    db, patcher = mock_database()
    try:
        db.query.return_value.filter.return_value.first.return_value = None

        result = prepare_for_interview(
            "Missing Company", "Unknown Role"
        )

        assert "could not find" in result.lower()
    finally:
        patcher.stop()


def test_add_application_requires_confirmation():
    result = add_application(
        company_name="Security Test Company",
        job_role="Python Intern",
    )

    assert "confirmation required" in result.lower()

def test_update_status_requires_confirmation():
    db, patcher = mock_database()

    try:
        app = sample_application(status="Applied")

        db.query.return_value.filter.return_value.first.return_value = app

        result = update_application_status(
            application_id=101,
            new_status="Interview",
        )

        assert "confirmation required" in result.lower()
        assert app.application_status == "Applied"
        db.commit.assert_not_called()

    finally:
        patcher.stop()
