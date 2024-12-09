# workmanager/admin.py
from django.contrib import admin
from .models import WorkZone, Event, LogEntry, TodoItem, Tag

@admin.register(WorkZone)
class WorkZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    list_filter = ('created_by', 'created_at')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'created_by')
    list_filter = ('created_by',)
    search_fields = ('name',)

class LogEntryInline(admin.TabularInline):
    model = LogEntry
    extra = 1
    readonly_fields = ('created_at',)

class TodoItemInline(admin.TabularInline):
    model = TodoItem
    extra = 1
    readonly_fields = ('created_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'work_zone', 'priority', 'status', 'deadline', 'is_overdue', 'created_by')
    list_filter = ('work_zone', 'priority', 'status', 'created_by', 'tags')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    filter_horizontal = ('tags',)
    inlines = [LogEntryInline, TodoItemInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'description', 'work_zone')
        }),
        ('Estado y Prioridad', {
            'fields': ('status', 'priority', 'tags')
        }),
        ('Fechas', {
            'fields': ('deadline', 'alert_frequency')
        }),
        ('Asignación', {
            'fields': ('created_by',)
        }),
    )

    def is_overdue(self, obj):
        return obj.is_overdue()
    is_overdue.boolean = True
    is_overdue.short_description = 'Atrasado'

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('event', 'content_preview', 'created_by', 'created_at')
    list_filter = ('event', 'created_by', 'created_at')
    search_fields = ('content', 'event__title')
    date_hierarchy = 'created_at'

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'event', 'is_completed', 'created_at', 'completed_at')
    list_filter = ('is_completed', 'event', 'created_at')
    search_fields = ('description', 'event__title')
    date_hierarchy = 'created_at'