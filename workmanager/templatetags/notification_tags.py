from django import template
from ..models import Notification
from ..utils import generate_notifications

register = template.Library()

@register.simple_tag(takes_context=True)
def get_notifications(context):
    user = context['request'].user
    if user.is_authenticated:
        generate_notifications(user)
        return Notification.objects.filter(user=user).order_by('-created_at')
    return []