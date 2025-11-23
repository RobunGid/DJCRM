from teams.models import Team

def team(request):
    if request.user.is_authenticated:
	    team = Team.objects.filter(created_by=request.user).first()
    else:
        team = None
    return {"team": team}