from .models import Notification

def notification_processor(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}