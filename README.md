# AI Job & Internship Application Tracker using MCP

## Project Overview

The AI Job & Internship Application Tracker is a Python-based MCP server that helps users manage and track their job and internship applications using PostgreSQL.

It supports adding applications, searching applications, verifying application details, updating application status, and preparing for interviews.

The project also integrates Filesystem MCP and GitHub MCP for file operations and GitHub repository and issue searches.

## Features

- Add job and internship applications.
- Search applications by company name or job role.
- Verify application details.
- Update application status.
- Retrieve all applications through an MCP resource.
- Generate interview preparation prompts for saved applications.
- Use PostgreSQL to store application data.
- Use Filesystem MCP to read, write, and list files securely.
- Use GitHub MCP to search repositories, issues, and pull requests.

## Technologies Used

- Python 3.10
- MCP SDK 2.3.0
- PostgreSQL
- SQLAlchemy
- python-dotenv
- pytest
- Filesystem MCP
- GitHub MCP
- MCP Inspector

## Project Structure

```text
MCP-INTERN-SANTHOSHKUMAR N/
│
├── .env
├── .gitignore
├── requirements.txt
├── database.py
├── models.py
├── create_tables.py
├── server.py
├── test_server.py
└── workspace/
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd <your-project-folder>
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/job_tracker
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
```

Replace the database username, password, and database name with your actual PostgreSQL details.

Add your GitHub personal access token if you use GitHub MCP.

**Security:** Never upload `.env` or expose your GitHub token publicly.

### 5. Create Database Tables

Make sure PostgreSQL is running and the database exists.

```bash
python create_tables.py
```

### 6. Run the Job Application MCP Server

```bash
python server.py
```

The server communicates through standard input/output (stdio).

## MCP Tools

| Tool | Description |
|---|---|
| `get_project_info` | Returns server information. |
| `add_application` | Adds a job or internship application. |
| `search_applications` | Searches applications by company or role. |
| `verify_application` | Verifies saved application details. |
| `update_application_status` | Updates an application's status. |

### Supported Application Statuses

- Applied
- Interview
- Selected
- Rejected

## MCP Resource

`applications://all`

Retrieves all saved job and internship applications.

## MCP Prompt

`prepare-for-interview`

Generates interview preparation guidance for a company and role when a matching application exists in the database.

## Filesystem MCP

Run the Filesystem MCP server using:

```bash
npx -y @modelcontextprotocol/server-filesystem "D:\path\to\your\workspace"
```

This provides file reading, writing, and directory listing within the configured workspace.

## GitHub MCP

Run the GitHub MCP server using:

```bash
npx -y @modelcontextprotocol/server-github
```

Configure `GITHUB_PERSONAL_ACCESS_TOKEN` in the MCP Inspector server environment.

The GitHub token should have only the permissions needed for your tasks.

## Testing

Run the automated Python tests:

```bash
python -m pytest test_server.py -v
```

The test suite previously completed with **19 passed tests**.

Additional manual tests were completed using MCP Inspector:

- Filesystem file writing
- Filesystem file reading
- Directory listing
- Filesystem access restriction
- GitHub repository search
- GitHub issue search
- GitHub pull request search

PostgreSQL integration was also tested for creating, updating, and reading application records.

## Future Improvements

- Add a web dashboard.
- Add application deadline reminders.
- Add application statistics and reports.
- Integrate more AI-powered interview preparation features.
