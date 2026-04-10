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
