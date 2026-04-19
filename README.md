<div align="center">

# Job Matching Backend (Django)

A backend-focused Django project for matching candidates and jobs using skill-based logic.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge" />
  <img src="https://img.shields.io/badge/Django-Backend-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Badge" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite Badge" />
  <img src="https://img.shields.io/badge/Status-Student%20Project-6A5ACD?style=for-the-badge" alt="Status Badge" />
</p>

</div>

---

## Overview

This project is a Django-based backend system for a job matching platform. It supports candidate and recruiter workflows, including profile handling, skill management, job posting, applications, and skill-based candidate-job matching. The focus is on backend architecture, relational data modeling, and practical business logic implementation.

## Core Features

- Role-based authentication for `Candidate` and `Recruiter` users
- Candidate skill management (add/remove skills, level, experience)
- Recruiter job creation with required skills
- Skill-based matching engine to:
  - rank jobs for a candidate
  - rank candidates for a job
- Job application flow with status tracking:
  - `Applied`
  - `Shortlisted`
  - `Rejected`
- Access control using decorators and role checks

## Tech Stack

- Python
- Django
- SQLite (default development database)
- Django Templates (server-rendered UI)

## Project Structure

```text
job_matching/
├─ accounts/        # Authentication, registration, role-based access
├─ candidates/      # Candidate profile and skills management
├─ companies/       # Company and recruiter profile models
├─ jobs/            # Job posting, listing, recruiter dashboard, matching views
│  └─ services/
│     └─ matching.py
├─ applications/    # Job application and status tracking
├─ core/            # Shared models (e.g., Skill) + seed/reset migrations
├─ templates/       # Shared templates (base, home, about)
├─ job_matching/    # Project settings, root urls, ASGI/WSGI
└─ manage.py
```

## Matching Logic (Simple)

The matching system compares candidate skills against required job skills and computes a score using:

- skill overlap
- candidate proficiency level
- required skill level
- importance weight per required skill

Top results are sorted by score and shown in candidate and recruiter match pages.

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd job_matching
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install django
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start development server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Main App Flows

### Candidate Flow

1. Register as candidate
2. Add skills in profile
3. View matched jobs
4. Apply to jobs
5. Track application statuses

### Recruiter Flow

1. Register as recruiter
2. Create job posts with required skills
3. View applicants per job
4. View top matched candidates

## Why This Project

This project demonstrates backend internship-ready fundamentals:

- real-world relational modeling
- role-based authorization
- clean modular Django app design
- practical scoring logic in a service layer
- maintainable and extendable project structure

## Future Improvements

- Convert to Django REST API + JWT auth
- Add filtering (location, salary, job type, score)
- Add recruiter actions to update application status from dashboard
- Improve matching with weighted normalization or ML ranking
- Add automated tests for services and views

---

## Author

Built as a backend-focused student project for internship preparation.
