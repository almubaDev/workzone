# workmanager/utils.py
from django.utils import timezone
from .models import Notification, Event

def generate_notifications(user):
    # Limpiar notificaciones antiguas leídas
    Notification.objects.filter(user=user, read=True, created_at__lt=timezone.now() - timezone.timedelta(days=7)).delete()

    # Eventos atrasados
    for event in Event.objects.get_overdue_events(user):
        Notification.objects.get_or_create(
            user=user,
            event=event,
            notification_type='OVERDUE',
            defaults={
                'message': f'El evento "{event.title}" está atrasado. Fecha límite: {event.deadline.strftime("%d/%m/%Y")}'
            }
        )

    # Eventos próximos a vencer
    for event in Event.objects.get_due_soon_events(user):
        Notification.objects.get_or_create(
            user=user,
            event=event,
            notification_type='DUE_SOON',
            defaults={
                'message': f'El evento "{event.title}" vence pronto. Fecha límite: {event.deadline.strftime("%d/%m/%Y")}'
            }
        )

    # Eventos sin actualización
    for event in Event.objects.get_no_updates_events(user):
        Notification.objects.get_or_create(
            user=user,
            event=event,
            notification_type='NO_UPDATES',
            defaults={
                'message': f'El evento "{event.title}" no ha sido actualizado en {event.alert_frequency} días'
            }
        )