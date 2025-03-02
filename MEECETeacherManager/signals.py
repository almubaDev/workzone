# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Teacher, GlobalTeacherLink, TeacherGlobalLinkURL, ComplianceTask, ComplianceStatus

@receiver(post_save, sender=GlobalTeacherLink)
def create_global_link_urls(sender, instance, created, **kwargs):
    """Crear TeacherGlobalLinkURL para todos los profesores cuando se crea un nuevo link global"""
    if created:  # Solo cuando se crea un nuevo link global
        teachers = Teacher.objects.all()
        link_urls = [
            TeacherGlobalLinkURL(
                teacher=teacher,
                global_link=instance
            ) for teacher in teachers
        ]
        TeacherGlobalLinkURL.objects.bulk_create(link_urls)

# También podemos agregar un log para debug
        print(f"Created {len(link_urls)} TeacherGlobalLinkURL instances for GlobalTeacherLink {instance.name}")

@receiver(post_save, sender=Teacher)
def create_teacher_global_links(sender, instance, created, **kwargs):
    """Crear TeacherGlobalLinkURL para todos los links globales cuando se crea un nuevo profesor"""
    if created:  # Solo cuando se crea un nuevo profesor
        global_links = GlobalTeacherLink.objects.all()
        link_urls = [
            TeacherGlobalLinkURL(
                teacher=instance,
                global_link=link
            ) for link in global_links
        ]
        TeacherGlobalLinkURL.objects.bulk_create(link_urls)
        
        
@receiver(post_save, sender=Teacher)
def create_compliance_statuses(sender, instance, created, **kwargs):
    """Crear estados de cumplimiento para todas las tareas cuando se crea un nuevo profesor"""
    if created:
        tasks = ComplianceTask.objects.all()
        ComplianceStatus.objects.bulk_create([
            ComplianceStatus(teacher=instance, task=task)
            for task in tasks
        ])

@receiver(post_save, sender=ComplianceTask)
def create_task_statuses(sender, instance, created, **kwargs):
    """Crear estados de cumplimiento para todos los profesores cuando se crea una nueva tarea"""
    if created:
        teachers = Teacher.objects.all()
        ComplianceStatus.objects.bulk_create([
            ComplianceStatus(teacher=teacher, task=instance)
            for teacher in teachers
        ])