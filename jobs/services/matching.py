from candidates.models import CandidateProfile, CandidateSkill
from jobs.models import JobSkill, Job


def calculate_match_score(candidate, job):
    candidate_skills = CandidateSkill.objects.filter(candidate=candidate)
    job_skills = JobSkill.objects.filter(job=job)

    candidate_skill_map = {
        cs.skill_id: cs for cs in candidate_skills
    }
    level_scores = {
        'beginner': 1,
        'intermediate': 2,
        'expert': 3
    }

    IMPORTANCE_WEIGHT = {
        "nice_to_have": 1,
        "preferred": 2,
        "very_important": 3
    }

    total_score = 0
    for skill in job_skills:
        candidate_skill = candidate_skill_map.get(skill.skill_id)
        if not candidate_skill:
            continue

        candidate_level = level_scores.get(candidate_skill.proficiency_level, 1)
        required_level = level_scores.get(skill.required_level, 1)

        level_ratio = candidate_level / required_level

        if level_ratio > 1:
            level_ratio = 1

        importance = IMPORTANCE_WEIGHT.get(skill.importance, 1)

        score = level_ratio * importance * 10

        total_score += score

    return round(total_score, 2)


def get_top_jobs_for_candidate(candidate):
    jobs = Job.objects.select_related("company", "created_by").all()
    result = []

    for job in jobs:
        score = calculate_match_score(candidate, job)
        if score > 0:
            result.append((job, score))

    result.sort(key=lambda x: x[1], reverse=True)

    return result[:10]


def get_top_candidates_for_job(job):
    candidates = CandidateProfile.objects.all()
    results = []

    for candidate in candidates:
        score = calculate_match_score(candidate, job)

        if score > 0:
            results.append({
                "candidate": candidate,
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]

