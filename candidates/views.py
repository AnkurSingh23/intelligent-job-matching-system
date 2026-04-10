from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.decorators import candidate_required
from core.models import Skill
from .models import CandidateSkill


@login_required
@candidate_required
def manage_candidate_skills(request):
	candidate = request.candidate_profile

	if request.method == "POST":
		action = request.POST.get("action")

		if action == "add":
			skill_id = request.POST.get("skill_id")
			proficiency_level = request.POST.get("proficiency_level") or "beginner"
			experience = request.POST.get("experience") or 0

			if not skill_id:
				messages.error(request, "Please select a skill.")
				return redirect("candidate_skills")

			skill = get_object_or_404(Skill, id=skill_id)
			exists = CandidateSkill.objects.filter(candidate=candidate, skill=skill).exists()
			if exists:
				messages.info(request, "You already added this skill.")
				return redirect("candidate_skills")

			CandidateSkill.objects.create(
				candidate=candidate,
				skill=skill,
				proficiency_level=proficiency_level,
				experience=experience,
			)
			messages.success(request, "Skill added successfully.")
			return redirect("candidate_skills")

		if action == "remove":
			candidate_skill_id = request.POST.get("candidate_skill_id")
			candidate_skill = get_object_or_404(CandidateSkill, id=candidate_skill_id, candidate=candidate)
			candidate_skill.delete()
			messages.success(request, "Skill removed successfully.")
			return redirect("candidate_skills")

	existing_skills = CandidateSkill.objects.filter(candidate=candidate).select_related("skill")
	added_skill_ids = existing_skills.values_list("skill_id", flat=True)
	available_skills = Skill.objects.exclude(id__in=added_skill_ids).order_by("name")

	return render(request, "candidates/manage_skills.html", {
		"existing_skills": existing_skills,
		"available_skills": available_skills,
	})
