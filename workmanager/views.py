# workmanager/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import WorkZone, Tag, Event, LogEntry, TodoItem, Notification, WorkZoneApp
from .forms import WorkZoneForm, TagForm, EventForm, LogEntryForm, TodoItemForm, WorkZoneAppForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.formats import date_format
from datetime import datetime as dt
from django.http import JsonResponse
from django.urls import reverse
from .utils import generate_notifications
from django.db.models import Count, Q, F
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta
import logging
import json

logger = logging.getLogger(__name__)

#TaskList
class TodoItemCreateView(LoginRequiredMixin, View):
    def post(self, request, event_pk):
        event = get_object_or_404(Event, pk=event_pk, created_by=request.user)
        description = request.POST.get('description')
        
        if description:
            todo = TodoItem.objects.create(
                event=event,
                description=description
            )
            
            return JsonResponse({
                'status': 'success',
                'id': todo.id,
                'description': todo.description,
                'created_at': todo.created_at.strftime("%d/%m/%Y %H:%M")
            })
        return JsonResponse({'status': 'error', 'message': 'Descripción requerida'})

class TodoItemToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(TodoItem, pk=pk, event__created_by=request.user)
        todo.is_completed = not todo.is_completed
        todo.completed_at = timezone.localtime() if todo.is_completed else None
        todo.save()
        
        return JsonResponse({
            'status': 'success',
            'is_completed': todo.is_completed,
            'completed_at': date_format(timezone.localtime(todo.completed_at), format="d/m/Y H:i") if todo.completed_at else None
        })

class TodoItemDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(TodoItem, pk=pk, event__created_by=request.user)
        todo.delete()
        return JsonResponse({'status': 'success'})


#LogEntry
class LogEntryCreateView(LoginRequiredMixin, View):
    def post(self, request, event_pk):
        event = get_object_or_404(Event, pk=event_pk, created_by=request.user)
        content = request.POST.get('content')
        
        if content:
            log_entry = LogEntry.objects.create(
                event=event,
                content=content,
                created_by=request.user
            )
            
            return JsonResponse({
                'status': 'success',
                'id': log_entry.id,
                'content': log_entry.content,
                'created_at': date_format(timezone.localtime(log_entry.created_at), format="d/m/Y H:i"),
                'created_by': log_entry.created_by.username
            })
            
        return JsonResponse({
            'status': 'error',
            'message': 'El contenido es requerido'
        })
    
    
class LogEntryDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        log_entry = get_object_or_404(LogEntry, 
            pk=pk,
            created_by=request.user  # Aseguramos que solo el creador pueda eliminar
        )
        
        try:
            log_entry.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


#EVENT
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'workmanager/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.filter(created_by=self.request.user)
        
        # Búsqueda por texto
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filtros
        statuses = self.request.GET.getlist('status')
        priorities = self.request.GET.getlist('priority')
        work_zone = self.request.GET.get('work_zone')
        tags = self.request.GET.getlist('tag')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if statuses:
            queryset = queryset.filter(status__in=statuses)
        if priorities:
            queryset = queryset.filter(priority__in=priorities)
        if work_zone:
            queryset = queryset.filter(work_zone_id=work_zone)
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        if date_from:
            try:
                date_from = dt.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(deadline__date__gte=date_from)
            except ValueError:
                pass
        if date_to:
            try:
                date_to = dt.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(deadline__date__lte=date_to)
            except ValueError:
                pass

        return queryset.distinct().order_by('deadline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener la zona de trabajo seleccionada
        selected_workzone = self.request.GET.get('work_zone')
        
        # Opciones para los filtros
        context['work_zones'] = WorkZone.objects.filter(created_by=user)
        
        # Filtrar etiquetas según la zona seleccionada
        if selected_workzone:
            context['all_tags'] = Tag.objects.filter(
                created_by=user,
                work_zone_id=selected_workzone
            )
        else:
            context['all_tags'] = Tag.objects.filter(created_by=user)
            
        context['status_choices'] = Event.STATUS_CHOICES
        context['priority_choices'] = Event.PRIORITY_CHOICES
        
        # Valores actuales de los filtros
        context.update({
            'selected_status': self.request.GET.getlist('status'),
            'selected_priority': self.request.GET.getlist('priority'),
            'selected_work_zone': selected_workzone,
            'selected_tag': self.request.GET.getlist('tag'),
            'selected_date_from': self.request.GET.get('date_from', ''),
            'selected_date_to': self.request.GET.get('date_to', ''),
            'search_query': self.request.GET.get('search', '')
        })
        
        return context
    
    
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'workmanager/event_form.html'
    success_url = reverse_lazy('event_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Evento creado exitosamente.')
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'workmanager/event_form.html'
    success_url = reverse_lazy('event_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir URL para la vista que devolverá las etiquetas
        context['get_tags_url'] = reverse_lazy('get_tags_by_workzone')
        return context

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'workmanager/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'workmanager/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = LogEntryForm()  # Añadir el formulario al contexto
        return context

#AUTH
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'workmanager/auth/login.html'
    redirect_authenticated_user = True
    
    
#DASHBOARD    


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'workmanager/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()
        
        # Obtener todas las zonas de trabajo del usuario
        workzones = WorkZone.objects.filter(created_by=user)
        
        # Eventos por estado
        events_by_status = list(Event.objects.filter(
            created_by=user
        ).values('status').annotate(
            count=Count('id')
        ).order_by('status'))
        
        # Asegurarse de que todos los estados estén representados
        status_dict = {status[0]: 0 for status in Event.STATUS_CHOICES}
        for event_status in events_by_status:
            status_dict[event_status['status']] = event_status['count']
        
        events_by_status = [
            {'status': status, 'count': count}
            for status, count in status_dict.items()
        ]
        
        # Eventos por zona de trabajo con colores
        events_by_workzone = []
        for workzone in workzones:
            count = Event.objects.filter(
                created_by=user,
                work_zone=workzone
            ).count()
            
            events_by_workzone.append({
                'name': workzone.name,
                'count': count,
                'color': workzone.color or 'rgb(200, 200, 200)'  # Color por defecto si es None
            })
        
        # Eventos del calendario (mes actual)
        calendar_events = Event.objects.filter(
            created_by=user,
            deadline__range=[
                today.replace(day=1),
                (today + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            ]
        ).values('id', 'title', 'deadline', 'priority')
        
        # Formatear eventos del calendario
        calendar_events_formatted = []
        for event in calendar_events:
            calendar_events_formatted.append({
                'id': event['id'],
                'title': event['title'],
                'deadline': event['deadline'].isoformat(),
                'priority': event['priority']
            })
        
        # Actualizar el contexto con todos los datos necesarios
        context.update({
            # Estadísticas generales
            'total_events': Event.objects.filter(created_by=user).count(),
            'events_completed': Event.objects.filter(created_by=user, status='COMPLETED').count(),
            'events_in_progress': Event.objects.filter(created_by=user, status='IN_PROGRESS').count(),
            'events_not_started': Event.objects.filter(created_by=user, status='NOT_STARTED').count(),
            
            # Eventos urgentes y próximos
            'urgent_events': Event.objects.filter(
                created_by=user,
                priority='URGENT',
                status__in=['NOT_STARTED', 'IN_PROGRESS']
            ).order_by('deadline')[:5],
            
            'upcoming_events': Event.objects.filter(
                created_by=user,
                deadline__range=[today, today + timedelta(days=3)],
                status__in=['NOT_STARTED', 'IN_PROGRESS']
            ).order_by('deadline')[:5],
            
            'overdue_events': Event.objects.filter(
                created_by=user,
                deadline__lt=today,
                status__in=['NOT_STARTED', 'IN_PROGRESS']
            ).order_by('deadline')[:5],
            
            # Datos para los gráficos (serializados para JavaScript)
            'events_by_status': json.dumps(events_by_status, cls=DjangoJSONEncoder),
            'events_by_workzone': json.dumps(events_by_workzone, cls=DjangoJSONEncoder),
            'calendar_events': json.dumps(calendar_events_formatted, cls=DjangoJSONEncoder),
            
            # Actividad reciente
            'recent_logs': LogEntry.objects.filter(
                created_by=user
            ).select_related('event').order_by('-created_at')[:5],
            
            # Tareas completadas recientemente
            'completed_todos': TodoItem.objects.filter(
                event__created_by=user,
                is_completed=True
            ).select_related('event').order_by('-completed_at')[:5],
            
            # Porcentaje de cumplimiento
            'completion_rate': self.calculate_completion_rate(user),
        })
        
        return context
    
    def calculate_completion_rate(self, user):
        """
        Calcula el porcentaje de eventos completados.
        """
        total_events = Event.objects.filter(created_by=user).count()
        
        if total_events == 0:
            return 0
        
        completed_events = Event.objects.filter(
            created_by=user,
            status='COMPLETED'
        ).count()
        
        return int((completed_events / total_events) * 100)
    
    
#WORKZONE
class WorkZoneListView(LoginRequiredMixin, ListView):
    model = WorkZone
    template_name = 'workmanager/workzone_list.html'
    context_object_name = 'workzones'

    def get_queryset(self):
        return WorkZone.objects.filter(created_by=self.request.user)

class WorkZoneCreateView(LoginRequiredMixin, CreateView):
    model = WorkZone
    form_class = WorkZoneForm
    template_name = 'workmanager/workzone_form.html'
    success_url = reverse_lazy('workzone_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Zona de trabajo creada exitosamente.')
        return super().form_valid(form)

class WorkZoneUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkZone
    form_class = WorkZoneForm
    template_name = 'workmanager/workzone_form.html'
    success_url = reverse_lazy('workzone_list')

    def get_queryset(self):
        return WorkZone.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Zona de trabajo actualizada exitosamente.')
        return super().form_valid(form)

class WorkZoneDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkZone
    template_name = 'workmanager/workzone_confirm_delete.html'
    success_url = reverse_lazy('workzone_list')
    
    def get_queryset(self):
        return WorkZone.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Zona de trabajo eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

class WorkZoneDetailView(LoginRequiredMixin, DetailView):
    model = WorkZone
    template_name = 'workmanager/workzone_detail.html'
    context_object_name = 'workzone'

    def get_queryset(self):
        return WorkZone.objects.filter(created_by=self.request.user)
    
    
#TAGS
class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = 'workmanager/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user)

class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'workmanager/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Etiqueta creada exitosamente.')
        return super().form_valid(form)

class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'workmanager/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Etiqueta actualizada exitosamente.')
        return super().form_valid(form)

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    template_name = 'workmanager/tag_confirm_delete.html'
    success_url = reverse_lazy('tag_list')
    
    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Etiqueta eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)
    

class GetTagsByWorkzone(LoginRequiredMixin, View):
    def get(self, request):
        workzone_id = request.GET.get('workzone_id')
        tags = Tag.objects.filter(
            work_zone_id=workzone_id,
            created_by=request.user
        ).values('id', 'name')
        
        # Añadir logs para depuración
        print("Workzone ID:", workzone_id)
        print("Tags encontradas:", list(tags))
        
        return JsonResponse({
            'status': 'success',
            'tags': list(tags)
        })
        
#NOTIFICATIONS
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'workmanager/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Generar notificaciones antes de mostrar la lista
        generate_notifications(self.request.user)
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})

class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(user=request.user).update(read=True)
        return JsonResponse({'status': 'success'})
    

#CALENDAR
class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'workmanager/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['work_zones'] = WorkZone.objects.filter(created_by=self.request.user)
        return context

class CalendarEventsAPI(LoginRequiredMixin, View):
    def get(self, request):
        events = Event.objects.filter(created_by=request.user)
        
        if work_zone := request.GET.get('work_zone'):
            events = events.filter(work_zone_id=work_zone)

        calendar_events = []
        for event in events:
            calendar_events.append({
                'id': event.id,
                'title': event.title,
                'start': event.deadline.isoformat(),
                'end': event.deadline.isoformat(),
                'url': reverse('event_detail', args=[event.id]),
                'className': [
                    f'priority-{event.priority.lower()}',
                    f'status-{event.status.lower()}'
                ],
                'extendedProps': {
                    'description': event.description,
                    'workZone': event.work_zone.name,
                    'status': event.get_status_display(),
                    'priority': event.priority
                }
            })
        
        return JsonResponse(calendar_events, safe=False)
    
    
class WorkZoneAppCreateView(LoginRequiredMixin, CreateView):
    model = WorkZoneApp
    form_class = WorkZoneAppForm
    template_name = 'workmanager/workzone_app_form.html'
    
    def form_valid(self, form):
        form.instance.work_zone_id = self.kwargs['workzone_pk']
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('workzone_detail', kwargs={'pk': self.kwargs['workzone_pk']})
    
    
class WorkZoneAppManagerView(LoginRequiredMixin, View):
    template_name = 'workmanager/workzone_app_manager.html'
    
    def get(self, request):
        form = WorkZoneAppForm()
        apps = WorkZoneApp.objects.filter(
            work_zone__created_by=request.user
        ).select_related('work_zone').order_by('work_zone__name', 'order', 'name')
        
        # Obtener todas las zonas de trabajo del usuario para el filtro
        work_zones = WorkZone.objects.filter(created_by=request.user)
        
        # Filtrar por zona de trabajo si se especifica
        selected_zone = request.GET.get('work_zone')
        if selected_zone:
            apps = apps.filter(work_zone_id=selected_zone)
        
        return render(request, self.template_name, {
            'form': form,
            'apps': apps,
            'work_zones': work_zones,
            'selected_zone': selected_zone
        })
    
    def post(self, request):
        form = WorkZoneAppForm(request.POST)
        
        if form.is_valid():
            app = form.save(commit=False)
            # Verificar que la zona de trabajo pertenece al usuario
            if app.work_zone.created_by != request.user:
                messages.error(request, 'Zona de trabajo no válida.')
                return redirect('workzone_app_manager')
            
            app.save()
            messages.success(request, 'Aplicación creada exitosamente.')
            return redirect('workzone_app_manager')
        
        apps = WorkZoneApp.objects.filter(
            work_zone__created_by=request.user
        ).select_related('work_zone').order_by('work_zone__name', 'order', 'name')
        work_zones = WorkZone.objects.filter(created_by=request.user)
        
        return render(request, self.template_name, {
            'form': form,
            'apps': apps,
            'work_zones': work_zones
        })


class WorkZoneAppUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        app = get_object_or_404(WorkZoneApp, pk=pk, work_zone__created_by=request.user)
        form = WorkZoneAppForm(request.POST, instance=app)
        
        if form.is_valid():
            # Verificar que la zona de trabajo pertenece al usuario
            if form.cleaned_data['work_zone'].created_by != request.user:
                messages.error(request, 'Zona de trabajo no válida.')
                return redirect('workzone_app_manager')
                
            form.save()
            messages.success(request, 'Aplicación actualizada exitosamente.')
        else:
            messages.error(request, 'Error al actualizar la aplicación.')
            
        return redirect('workzone_app_manager')


class WorkZoneAppDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        app = get_object_or_404(WorkZoneApp, pk=pk, work_zone__created_by=request.user)
        app.delete()
        messages.success(request, 'Aplicación eliminada exitosamente.')
        return redirect('workzone_app_manager')