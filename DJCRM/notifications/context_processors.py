def notifications(request):
    notifications = None
    if request.user.is_authenticated:
        notifications = request.user.notifications.all()
    return {"notifications": notifications}