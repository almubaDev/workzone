from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce.models import HTMLField

class WorkZone(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workzones')

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