from django import forms
from .models import (Teacher, TeacherCategory, TeacherProfile, Course, TeacherSchedule, 
                     TeacherPersonalLink, TeacherGlobalLinkURL, GlobalTeacherLink, ComplianceTask, 
                     ComplianceStatus, MPA, MPASchedule,MPASheet, TimelineEvent)

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'rut']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre completo'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 12345678-9'
            })
        }


class TeacherCategoryForm(forms.ModelForm):
    class Meta:
        model = TeacherCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['category', 'institutional_email', 'personal_email', 
                 'phone', 'profession', 'academic_degree']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'institutional_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_degree': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
# forms.py
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
        

class TeacherScheduleForm(forms.ModelForm):
    is_accepted = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = TeacherSchedule
        fields = ['course', 'day', 'start_time', 'end_time', 'start_date', 'end_date', 
                 'modality', 'vacancies', 'intake', 'is_accepted']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'modality': forms.Select(attrs={'class': 'form-select'}),
            'vacancies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'intake': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2024-1'
            }),
        }
        
#links

class GlobalTeacherLinkForm(forms.ModelForm):
    class Meta:
        model = GlobalTeacherLink
        fields = ['name', 'description', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.Select(attrs={'class': 'form-select icon-select'}, choices=[
                ('fa-link', 'Link (Default)'),
                ('fa-folder', 'Carpeta'),
                ('fa-file', 'Documento'),
                ('fa-book', 'Libro/Publicación'),
                ('fa-globe', 'Sitio Web'),
                ('fa-drive', 'Google Drive'),
                ('fa-dropbox', 'Dropbox'),
                ('fa-github', 'GitHub'),
                ('fa-linkedin', 'LinkedIn'),
            ])
        }

class TeacherGlobalLinkURLForm(forms.ModelForm):
    class Meta:
        model = TeacherGlobalLinkURL
        fields = ['url', 'is_active']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
class TeacherPersonalLinkForm(forms.ModelForm):
    class Meta:
        model = TeacherPersonalLink
        fields = ['name', 'description', 'url', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'icon': forms.Select(attrs={'class': 'form-select icon-select'}, choices=[
                ('fa-link', 'Link (Default)'),
                ('fa-folder', 'Carpeta'),
                ('fa-file', 'Documento'),
                ('fa-book', 'Libro/Publicación'),
                ('fa-globe', 'Sitio Web'),
                ('fa-drive', 'Google Drive'),
                ('fa-dropbox', 'Dropbox'),
                ('fa-github', 'GitHub'),
                ('fa-linkedin', 'LinkedIn'),
            ])
        }
        
class ComplianceTaskForm(forms.ModelForm):
    class Meta:
        model = ComplianceTask
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la tarea'
            })
        }
        
        
#MPAs
class MPAUploadForm(forms.ModelForm):
    file = forms.FileField(
        label='Archivo MPA',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        })
    )

    class Meta:
        model = MPA
        fields = []  # No incluimos campos del modelo directamente

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError('El archivo debe ser un Excel (.xlsx o .xls)')
        return file


# forms.py
class MPAEditForm(forms.ModelForm):
    class Meta:
        model = MPA
        fields = ['program_name', 'program_code', 'faculty', 'school', 'campus', 'period']
        widgets = {
            'program_name': forms.TextInput(attrs={'class': 'form-control'}),
            'program_code': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'campus': forms.TextInput(attrs={'class': 'form-control'}),
            'period': forms.TextInput(attrs={'class': 'form-control'})
        }
        


# forms.py
class TimelineEventForm(forms.ModelForm):
    class Meta:
        model = TimelineEvent
        fields = ['title', 'event_type', 'event_date', 'color', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'value': '#3498db'
            }),
            'icon': forms.Select(attrs={
                'class': 'form-select'
            }, choices=TimelineEvent.ICON_CHOICES)
        }