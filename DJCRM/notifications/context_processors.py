def notifications(request):
    read_messages = None
    unread_messages = None
    all_messages = None
    read_team_invitations = None
    unread_team_invitations = None
    all_team_invitations = None

    if request.user.is_authenticated:
        read_messages = request.user.messages.filter(is_read=True).all()
        unread_messages = request.user.messages.filter(is_read=False).all()
        all_messages = request.user.messages.all()
        read_team_invitations = request.user.team_invitations.filter(status="READ").all()
        unread_team_invitations = request.user.team_invitations.filter(status="NOT_READ").all()
        all_team_invitations = request.user.team_invitations.all()
    return {
        "read_messages": read_messages,
        "unread_messages": unread_messages,
        "all_messages": all_messages,
        "read_team_invitations": read_team_invitations,
        "unread_team_invitations": unread_team_invitations,
        "all_team_invitations": all_team_invitations,
    }