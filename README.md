<<<<<<< HEAD
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
=======
Intelligent Job Matching Backend System

A backend-driven job matching platform built using Django that intelligently matches candidates and jobs using a rule-based scoring engine.

🔥 Project Overview

This system simulates a mini job portal where:

Candidates can register, add skills, and apply for jobs
Recruiters can create jobs under companies
The system computes a matching score to recommend:
Jobs to candidates
Candidates to recruiters

The core highlight is a custom matching engine that ranks results instead of simple filtering.

🧠 System Architecture

The project follows a multi-app Django architecture:

App	Responsibility
accounts	Custom user model, authentication (email-based login)
candidates	Candidate profile and skill management
companies	Company and recruiter management
jobs	Job creation, listing, and matching views
core	Shared entities like Skill
applications	Job application workflow
🗂️ Data Model Overview
🔐 User
Custom authentication using email
Base model for both candidates and recruiters
👤 CandidateProfile
Linked to User (OneToOne)
Stores:
Name, bio, experience
Resume
Preferred location
Expected salary
🧠 Skill
Central skill table
Shared across candidates and jobs
🔗 CandidateSkill
Links Candidate ↔ Skill
Stores:
Proficiency level (beginner, intermediate, expert)
Experience
🏢 Company
Represents an organization
Managed via admin panel
👨‍💼 RecruiterProfile
Linked to User and Company
Represents recruiter identity
💼 Job
Created by recruiter under a company
Stores:
Title, description
Job type, location
Salary range
🎯 JobSkill
Links Job ↔ Skill
Stores:
Required level
Importance (nice_to_have, preferred, very_important)
📄 JobApplication
Links Candidate ↔ Job
Stores:
Status (applied, shortlisted, rejected)
Timestamp
🔗 Database Relationships
OneToOne
User ↔ CandidateProfile / RecruiterProfile
ForeignKey
Job → Company
Job → RecruiterProfile
Through Models
CandidateSkill
JobSkill

👉 Used to store extra attributes like proficiency and importance.

⚙️ Core Features
🔥 1. Matching Engine
Compares candidate skills with job requirements
Generates a score for ranking
📊 2. Candidate → Job Recommendation
Returns top jobs based on matching score
🧑‍💼 3. Recruiter → Candidate Ranking
Returns top candidates for a job
📄 4. Job Application System
Candidates can apply to jobs
Tracks application status
🔐 5. Authentication System
Email-based login
Protected routes using login_required
🧮 Matching Algorithm

The scoring system is based on:

🔢 Level Mapping
Level	Value
Beginner	1
Intermediate	2
Expert	3
⚖️ Importance Weights
Importance	Weight
Nice to have	1
Preferred	2
Very important	3
🧠 Formula
score = (candidate_level / required_level) * importance_weight
Ratio capped at 1
Aggregated across all job skills
Used for ranking
🌐 URL Routes
Route	Description
/accounts/register/	User registration
/accounts/login/	Login page
/accounts/logout/	Logout
/candidate/<id>/matches/	Recommended jobs
/job/<id>/matches/	Top candidates
/applications/apply/<id>/	Apply to job
/applications/applied/	View applied jobs
/about/	Live system documentation
🛠️ Admin Panel

Registered models:

User
CandidateProfile
CandidateSkill
Company
RecruiterProfile
Skill
Job
JobSkill
JobApplication

👉 Used for:

Managing companies
Creating test data
Monitoring applications
🖥️ UI Pages
Home page
Login/Register
Job listing
Candidate matches
Applied jobs
Recruiter candidate view
About (documentation page)
🚀 How to Run
git clone https://github.com/ankursingh23/intelligent-job-matching-system.git
cd intelligent-job-matching-system

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
📈 Future Improvements
Add filters (location, salary, experience)
Pagination and search
Convert to DRF APIs
ML-based ranking system
Better UI/UX
💡 Key Highlights
Clean multi-app architecture
Service-layer based matching logic
Use of intermediate models for rich relationships
Real-world backend system design
Extensible and scalable structure
>>>>>>> 9d427d13144bb20cb1cda112db5857b5e469d71b
