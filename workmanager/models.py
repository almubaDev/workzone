from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField

class WorkZone(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workzones')
    updated_at = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, blank=True, null=True)  # Nuevo campo
    
    def save(self, *args, **kwargs):
        if not self.color:  # Si no tiene color asignado
            from .utils import generate_unique_color
            existing_colors = WorkZone.objects.exclude(id=self.id)\
                                            .values_list('color', flat=True)
            self.color = generate_unique_color(list(existing_colors))
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#000000")
    work_zone = models.ForeignKey(
        WorkZone, 
        on_delete=models.CASCADE, 
        related_name='tags'
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')

    def __str__(self):
        return f"{self.name} ({self.work_zone.name})"

    class Meta:
        unique_together = ['name', 'work_zone']
        
 
class EventManager(models.Manager):
    def get_overdue_events(self, user):
        return self.filter(
            created_by=user,
            status__in=['NOT_STARTED', 'IN_PROGRESS'],
            deadline__lt=timezone.now()
        )

    def get_due_soon_events(self, user):
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        return self.filter(
            created_by=user,
            status__in=['NOT_STARTED', 'IN_PROGRESS'],
            deadline__range=[timezone.now(), tomorrow]
        )

    def get_no_updates_events(self, user):
        events = []
        for event in self.filter(created_by=user, status__in=['NOT_STARTED', 'IN_PROGRESS']):
            time_since_update = timezone.now() - event.last_updated
            if time_since_update.days >= event.alert_frequency:
                events.append(event)
        return events       

class Event(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('URGENT', 'Urgente'),
    ]

    STATUS_CHOICES = [
        ('NOT_STARTED', 'No iniciado'),
        ('IN_PROGRESS', 'En proceso'),
        ('COMPLETED', 'Completado'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    work_zone = models.ForeignKey(WorkZone, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    tags = models.ManyToManyField(Tag, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    last_updated = models.DateTimeField(auto_now=True)
    alert_frequency = models.IntegerField(default=7)  # días entre alertas
    objects = EventManager()

    def __str__(self):
        return self.title

    def is_overdue(self):
        return self.deadline < timezone.now()

class LogEntry(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='log_entries')
    content = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_logs')  # Cambiado aquí

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Log para {self.event.title} - {self.created_at}"

class TodoItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='todo_items')
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.description
    
    
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('OVERDUE', 'Evento Atrasado'),
        ('DUE_SOON', 'Próximo a Vencer'),
        ('NO_UPDATES', 'Sin Actualizaciones'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.event.title}"
    
    
    
class WorkZoneApp(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Nombre del ícono de FontAwesome", default="fa-tool")
    url_name = models.CharField(max_length=100, help_text="Nombre de la URL de la aplicación")
    work_zone = models.ForeignKey(
        WorkZone, 
        on_delete=models.CASCADE, 
        related_name='applications'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.work_zone.name}"