# workmanager/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import WorkZone, Tag, Event, LogEntry, TodoItem
from .forms import WorkZoneForm, TagForm, EventForm, LogEntryForm, TodoItemForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.utils import timezone
from django.utils.formats import date_format
from datetime import datetime as dt
from django.http import JsonResponse
from django.urls import reverse
import logging

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
        
        # Filtros
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')
        work_zone = self.request.GET.get('work_zone')
        tag = self.request.GET.get('tag')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)
        if work_zone:
            queryset = queryset.filter(work_zone_id=work_zone)
        if tag:
            queryset = queryset.filter(tags__id=tag)
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

        return queryset.order_by('deadline')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Opciones para los filtros
        context['work_zones'] = WorkZone.objects.filter(created_by=user)
        context['all_tags'] = Tag.objects.filter(created_by=user)
        context['status_choices'] = Event.STATUS_CHOICES
        context['priority_choices'] = Event.PRIORITY_CHOICES
        
        # Valores actuales de los filtros
        context.update({
            'selected_status': self.request.GET.get('status', ''),
            'selected_priority': self.request.GET.get('priority', ''),
            'selected_work_zone': self.request.GET.get('work_zone', ''),
            'selected_tag': self.request.GET.get('tag', ''),
            'selected_date_from': self.request.GET.get('date_from', ''),
            'selected_date_to': self.request.GET.get('date_to', '')
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
        
        # Work Zones
        context['workzones'] = WorkZone.objects.filter(created_by=user)
        
        # Events
        events = Event.objects.filter(created_by=user)
        context['events'] = events
        context['events_not_started'] = events.filter(status='NOT_STARTED').count()
        context['events_in_progress'] = events.filter(status='IN_PROGRESS').count()
        context['events_completed'] = events.filter(status='COMPLETED').count()
        context['events_overdue'] = events.filter(deadline__lt=timezone.now()).exclude(status='COMPLETED').count()
        
        # Upcoming events (próximos 7 días)
        context['upcoming_events'] = events.filter(
            deadline__gte=timezone.now(),
            deadline__lte=timezone.now() + timezone.timedelta(days=7)
        ).order_by('deadline')[:5]
        
        # Tags
        context['tags'] = Tag.objects.filter(created_by=user)
        
        return context
    
    
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