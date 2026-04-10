from candidates.models import CandidateProfile
from companies.models import RecruiterProfile


def current_user_role(request):
    role = None
    if request.user.is_authenticated:
        if RecruiterProfile.objects.filter(user=request.user).exists():
            role = "recruiter"
        elif CandidateProfile.objects.filter(user=request.user).exists():
            role = "candidate"
    return {"current_user_role": role}
