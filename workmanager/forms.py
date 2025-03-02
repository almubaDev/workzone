# workmanager/forms.py
from django import forms
from .models import WorkZone, Tag, Event, LogEntry, TodoItem, WorkZoneApp
from datetime import datetime
from tinymce.widgets import TinyMCE


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ['description']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la tarea'
            })
        }


class LogEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = ['content']
        widgets = {
            'content': TinyMCE(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe una actualización o nota sobre este evento...'
            })
        }
        


# workmanager/forms.py
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'work_zone', 'deadline', 
                 'priority', 'status', 'tags', 'alert_frequency']
        labels = {
            'title': 'Título',
            'description': 'Descripción',
            'work_zone': 'Zona de Trabajo',
            'deadline': 'Fecha límite',
            'priority': 'Prioridad',
            'status': 'Estado',
            'tags': 'Etiquetas',
            'alert_frequency': 'Frecuencia de alertas (días)'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del evento'
            }),
            'work_zone': forms.Select(attrs={
                'class': 'form-select'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'alert_frequency': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '30'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['work_zone'].queryset = WorkZone.objects.filter(created_by=user)

        # Si es una edición y hay una fecha límite
        if self.instance.pk and self.instance.deadline:
            self.initial['deadline'] = self.instance.deadline.strftime('%Y-%m-%dT%H:%M')

        # Si hay datos POST y una zona de trabajo seleccionada
        if self.data.get('work_zone'):
            self.fields['tags'].queryset = Tag.objects.filter(
                work_zone_id=self.data.get('work_zone'),
                created_by=user
            )
        # Si es una edición y hay una zona de trabajo
        elif self.instance.pk and self.instance.work_zone:
            self.fields['tags'].queryset = Tag.objects.filter(
                work_zone=self.instance.work_zone,
                created_by=user
            )
        else:
            self.fields['tags'].queryset = Tag.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        work_zone = cleaned_data.get('work_zone')
        tags = cleaned_data.get('tags')

        if work_zone and tags:
            # Obtener las etiquetas válidas para la zona de trabajo
            valid_tags = Tag.objects.filter(
                work_zone=work_zone,
                created_by=self.user
            )
            
            # Verificar que todas las etiquetas seleccionadas son válidas
            selected_tags = set(tag.id for tag in tags)
            valid_tag_ids = set(valid_tags.values_list('id', flat=True))
            
            if not selected_tags.issubset(valid_tag_ids):
                invalid_tags = selected_tags - valid_tag_ids
                self.add_error('tags', 
                    f'Las siguientes etiquetas no son válidas para esta zona de trabajo: {list(invalid_tags)}')

        return cleaned_data
            
        
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color', 'work_zone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la etiqueta'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'work_zone': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_zone'].queryset = WorkZone.objects.filter(created_by=user)



class WorkZoneForm(forms.ModelForm):
    class Meta:
        model = WorkZone
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la zona de trabajo'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la zona de trabajo'}),
        }
        
class WorkZoneAppForm(forms.ModelForm):
    ICON_CHOICES = [
        ('fa-chalkboard-teacher', 'Profesor'),
        ('fa-users', 'Usuarios'),
        ('fa-book', 'Libro'),
        ('fa-graduation-cap', 'Graduación'),
        ('fa-calendar-check', 'Calendario'),
        ('fa-clipboard', 'Portapapeles'),
        ('fa-chart-bar', 'Gráfico'),
        ('fa-cog', 'Configuración'),
        ('fa-tasks', 'Tareas'),
        ('fa-file-alt', 'Documento'),
        ('fa-database', 'Base de datos'),
        ('fa-clock', 'Reloj'),
        ('fa-list-alt', 'Lista'),
        ('fa-folder', 'Carpeta'),
        ('fa-tools', 'Herramientas'),
        ('fa-search', 'Búsqueda'),
        ('fa-bell', 'Notificación'),
        ('fa-envelope', 'Correo'),
        ('fa-chart-line', 'Estadísticas'),
        ('fa-user-graduate', 'Estudiante'),
    ]

    icon = forms.ChoiceField(
        choices=ICON_CHOICES,
        label='Ícono',
        widget=forms.Select(attrs={
            'class': 'form-select icon-select'
        })
    )

    class Meta:
        model = WorkZoneApp
        fields = ['name', 'description', 'icon', 'url_name', 'work_zone', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url_name': forms.TextInput(attrs={'class': 'form-control'}),
            'work_zone': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las zonas de trabajo por usuario si está disponible
        if self.instance and hasattr(self.instance, 'work_zone'):
            user = self.instance.work_zone.created_by
            self.fields['work_zone'].queryset = WorkZone.objects.filter(created_by=user)