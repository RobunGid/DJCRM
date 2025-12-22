def notifications(request):
    read_notifications = None
    unread_notifications = None
    all_notifications = None
    
    if request.user.is_authenticated:
        read_notifications = request.user.notifications.filter(is_read=True).all()
        unread_notifications = request.user.notifications.filter(is_read=False).all()
        all_notifications = request.user.notifications.all()
        read_team_invitations = request.user.team_invitations.filter(status="READ").all()
        unread_team_invitations = request.user.team_invitations.filter(status="NOT_READ").all()
        all_team_invitations = request.user.team_invitations.all()
    return {
        "read_notifications": read_notifications,
        "unread_notifications": unread_notifications,
        "all_notifications": all_notifications,
        "read_team_invitations": read_team_invitations,
        "unread_team_invitations": unread_team_invitations,
        "all_team_invitations": all_team_invitations,
	}