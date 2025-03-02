from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # Auth URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # WorkZone URLs
    path('workzones/', views.WorkZoneListView.as_view(), name='workzone_list'),
    path('workzones/create/', views.WorkZoneCreateView.as_view(), name='workzone_create'),
    path('workzones/<int:pk>/', views.WorkZoneDetailView.as_view(), name='workzone_detail'),
    path('workzones/<int:pk>/update/', views.WorkZoneUpdateView.as_view(), name='workzone_update'),
    path('workzones/<int:pk>/delete/', views.WorkZoneDeleteView.as_view(), name='workzone_delete'),

    #Tag URLs
    path('tags/', views.TagListView.as_view(), name='tag_list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<int:pk>/update/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tags/<int:pk>/delete/', views.TagDeleteView.as_view(), name='tag_delete'),
    
    
    #Events URLs
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    #LogEntry
    path('events/<int:event_pk>/log/create/', views.LogEntryCreateView.as_view(), name='logentry_create'),
    path('events/log/<int:pk>/delete/', views.LogEntryDeleteView.as_view(), name='logentry_delete'),

    
    #TaskList
    path('events/<int:event_pk>/todo/create/', views.TodoItemCreateView.as_view(), name='todo_create'),
    path('events/todo/<int:pk>/toggle/', views.TodoItemToggleView.as_view(), name='todo_toggle'),
    path('events/todo/<int:pk>/delete/', views.TodoItemDeleteView.as_view(), name='todo_delete'),
    
    
    #Notifications
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
    path('notifications/<int:pk>/mark-read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('notifications/mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark_all_notifications_read'),

    #Calendar
    path('calendar/', views.CalendarView.as_view(), name='calendar'),

    
    #API
       #Tag
    path('get-tags-by-workzone/', views.GetTagsByWorkzone.as_view(), name='get_tags_by_workzone'),
       #Calendar
    path('api/calendar-events/', views.CalendarEventsAPI.as_view(), name='calendar_events_api'),
    
    

    path('workzone/apps/', views.WorkZoneAppManagerView.as_view(), name='workzone_app_manager'),
    path('workzone/apps/<int:pk>/update/', views.WorkZoneAppUpdateView.as_view(), name='workzone_app_update'),
    path('workzone/apps/<int:pk>/delete/', views.WorkZoneAppDeleteView.as_view(), name='workzone_app_delete'),
]