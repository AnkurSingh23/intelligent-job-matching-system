<div align="center">

# Job Matching Backend

A Django-based job portal for candidates and recruiters, with skill-based matching, application tracking, and recruiter dashboards.

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge" />
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django Badge" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite Badge" />
  <img src="https://img.shields.io/badge/UI-Django%20Templates-2D2D2D?style=for-the-badge" alt="Django Templates Badge" />
</p>

</div>

## Overview

This project is a server-rendered Django application built around a real job matching workflow. Candidates can create profiles, manage skills, upload resumes, and apply to jobs. Recruiters can create jobs, inspect applicants, and rank candidates using a rule-based matching engine.

The codebase is split into focused Django apps so the project stays modular and easy to extend.

## Highlights

- Email-based authentication with custom user model
- Separate candidate and recruiter registration flows
- Candidate profile management with resume upload and salary expectations
- Candidate skill tracking with proficiency and experience
- Company and recruiter profiles
- Job creation with skill requirements and importance levels
- Candidate-to-job and job-to-candidate ranking
- Application status tracking with applied, shortlisted, and rejected states
- Django admin support for managing the main models

## Project Structure

```text
job_matching/
├── accounts/       # Custom user model, login, logout, registration, role checks
├── applications/   # Job applications and application status workflow
├── candidates/     # Candidate profile and skill management
├── companies/      # Company and recruiter profile models
├── core/           # Shared Skill model and seed/reset migrations
├── jobs/           # Job listing, creation, applicants, and matching views
├── matching/       # Reserved app placeholder
├── templates/      # Shared pages such as home and about
├── media/          # Uploaded resume files
├── job_matching/   # Project settings and URL configuration
└── manage.py
```

## Main Apps

### accounts

Handles email-based user creation, login, logout, candidate registration, and recruiter registration.

### candidates

Stores candidate profile data and the many-to-one relationship between candidates and skills.

### companies

Stores company records and recruiter profiles linked to a company.

### jobs

Contains job listing, job creation, recruiter job dashboard, applicant views, and the matching service.

### applications

Stores job applications and application statuses.

### core

Provides the shared `Skill` model used by both candidates and jobs.

## Matching Logic

The matching engine lives in [jobs/services/matching.py](jobs/services/matching.py). It scores candidate and job pairs using:

- skill overlap
- candidate proficiency level: beginner, intermediate, expert
- required skill level: beginner, intermediate, expert
- importance weight: nice_to_have, preferred, very_important

The result is a ranked list of the top 10 matches for candidates or jobs.

## Data Model

### User

The project uses a custom user model based on email instead of username.

### CandidateProfile

Stores:

- full name
- bio
- total experience
- resume file
- preferred location
- expected salary

### CandidateSkill

Links a candidate to a skill and stores:

- proficiency level
- experience

### Company

Stores organization details for recruiters.

### RecruiterProfile

Links a recruiter user to a company.

### Job

Stores:

- title
- description
- job type
- location
- salary range
- company
- creator

### JobSkill

Connects a job to required skills with:

- required level
- importance level

### JobApplication

Tracks applications with:

- candidate
- job
- status
- applied timestamp

## Routes

### Public

- `/` - Home page
- `/about/` - About page
- `/jobs/` - Job list with match ranking for logged-in candidates

### Accounts

- `/accounts/register/` - Choose registration type
- `/accounts/register/candidate/` - Candidate registration
- `/accounts/register/recruiter/` - Recruiter registration
- `/accounts/login/` - Login
- `/accounts/logout/` - Logout

### Candidate actions

- `/candidates/skills/` - Manage candidate skills
- `/applications/apply/<job_id>/` - Apply to a job
- `/applications/applied/` - View applied jobs
- `/candidate/<candidate_id>/matches/` - View matched jobs for a candidate

### Recruiter actions

- `/jobs/create/` - Create a job
- `/jobs/my/` - View recruiter-created jobs
- `/jobs/<job_id>/applicants/` - View applicants for a job
- `/job/<job_id>/matches/` - View top candidates for a job

## Tech Stack

- Python
- Django 5.x
- SQLite
- Django templates
- django-money for salary fields

## Setup

1. Install the project dependencies.

```bash
pip install Django django-money
```

2. Apply database migrations.

```bash
python manage.py migrate
```

3. Create an admin user if needed.

```bash
python manage.py createsuperuser
```

4. Start the development server.

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Notes

- The project uses SQLite through `db.sqlite3`.
- Resume uploads are stored in `media/resumes/`.
- Application statuses currently are `applied`, `shortlisted`, and `rejected`.
- The repository includes seed and reset migrations under `core/migrations/`.
- There is no `requirements.txt` in the current workspace, so dependencies are listed manually here.

## Future Improvements

- Add a `requirements.txt` file for dependency pinning
- Add filtering for location, salary, and job type
- Expose the matching logic through an API
- Add recruiter actions for updating application status from the dashboard
- Add automated tests for views and matching logic

## License

No license file is currently included in the repository.
