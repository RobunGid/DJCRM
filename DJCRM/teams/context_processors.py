from teams.models import Team

def team(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "userprofile") and request.user.userprofile.active_team:
            team = request.user.userprofile.active_team
        else:
            team = Team.objects.filter(created_by=request.user).first()
    else:
        team = None
    return {"team": team}