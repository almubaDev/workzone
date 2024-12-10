# workmanager/forms.py
from django import forms
from .models import WorkZone, Tag, Event, LogEntry, TodoItem
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
        self.fields['work_zone'].queryset = WorkZone.objects.filter(created_by=user)

        # Si es una edición y hay una fecha límite
        if self.instance.pk and self.instance.deadline:
            # Formatear la fecha al formato requerido por datetime-local
            self.initial['deadline'] = self.instance.deadline.strftime('%Y-%m-%dT%H:%M')

        # Manejar las etiquetas según la workzone
        if self.instance.pk and self.instance.work_zone:
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
            valid_tags = Tag.objects.filter(
                work_zone=work_zone,
                id__in=[tag.id for tag in tags]
            )
            if valid_tags.count() != tags.count():
                self.add_error('tags', 'Por favor, seleccione etiquetas válidas.')

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