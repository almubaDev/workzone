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
        

def generate_unique_color(existing_colors=None):
    """
    Genera un color hexadecimal aleatorio que no esté en la lista de colores existentes.
    
    Args:
        existing_colors (list): Lista de colores hexadecimales ya utilizados
        
    Returns:
        str: Color hexadecimal único
    """
    if existing_colors is None:
        existing_colors = []
        
    # Lista de colores base para asegurar contraste y visibilidad
    base_hues = [
        (54, 162, 235),   # Azul
        (255, 99, 132),   # Rojo claro
        (255, 206, 86),   # Amarillo
        (75, 192, 192),   # Verde azulado
        (153, 102, 255),  # Púrpura
        (255, 159, 64),   # Naranja
        (231, 233, 237),  # Gris claro
        (102, 204, 0),    # Verde lima
        (204, 0, 204),    # Magenta
        (0, 204, 204),    # Cian
    ]
    
    def adjust_color(base_color):
        """Ajusta ligeramente un color base para crear variaciones"""
        r, g, b = base_color
        variation = 30  # Rango de variación
        
        new_r = max(0, min(255, r + random.randint(-variation, variation)))
        new_g = max(0, min(255, g + random.randint(-variation, variation)))
        new_b = max(0, min(255, b + random.randint(-variation, variation)))
        
        return f'rgb({new_r}, {new_g}, {new_b})'
    
    max_attempts = 50  # Límite de intentos para evitar bucles infinitos
    attempts = 0
    
    while attempts < max_attempts:
        # Si hay más zonas que colores base, crear variaciones
        if len(existing_colors) < len(base_hues):
            base_color = base_hues[len(existing_colors)]
            new_color = f'rgb({base_color[0]}, {base_color[1]}, {base_color[2]})'
        else:
            # Seleccionar un color base aleatorio y ajustarlo
            base_color = random.choice(base_hues)
            new_color = adjust_color(base_color)
            
        if new_color not in existing_colors:
            return new_color
            
        attempts += 1
    
    # Si no se encuentra un color único, generar uno completamente aleatorio
    return f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'


def get_workzone_colors(workzones):
    """
    Asigna colores únicos a cada zona de trabajo.
    
    Args:
        workzones (QuerySet): QuerySet de zonas de trabajo
        
    Returns:
        dict: Diccionario con los nombres de las zonas como claves y los colores como valores
    """
    colors = {}
    existing_colors = []
    
    for workzone in workzones:
        if not workzone.color:  # Si la zona no tiene color asignado
            new_color = generate_unique_color(existing_colors)
            colors[workzone.name] = new_color
            existing_colors.append(new_color)
        else:
            colors[workzone.name] = workzone.color
            existing_colors.append(workzone.color)
    
    return colors