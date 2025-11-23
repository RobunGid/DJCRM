from teams.models import Team

def team(request):
    team = Team.objects.filter(created_by=request.user).first()
    return {"team": team}