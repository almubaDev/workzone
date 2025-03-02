
from django.urls import path
from . import views

app_name = 'meece_teacher'

urlpatterns = [
    path('', views.TeacherManagerView.as_view(), name='teacher_manager'),
    path('<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    path('<int:pk>/detail/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    
    # URLs para el perfil
    path('<int:teacher_id>/profile/create/', views.TeacherProfileCreateView.as_view(), name='teacher_profile_create'),
    path('<int:teacher_id>/profile/update/', views.TeacherProfileUpdateView.as_view(), name='teacher_profile_update'),
    
    # URLs para categorías
    path('categories/', views.TeacherCategoryManagerView.as_view(), name='category_manager'),
    path('categories/<int:pk>/update/', views.TeacherCategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.TeacherCategoryDeleteView.as_view(), name='category_delete'),
    
  # URLs para horarios

    # URL que faltaba para horarios
    path('<int:teacher_id>/schedule/', views.TeacherScheduleManagerView.as_view(), name='teacher_schedule'),
    path('schedule/<int:pk>/clone/', views.TeacherScheduleCloneView.as_view(), name='schedule_clone'),
    path('schedule/<int:pk>/update/', views.TeacherScheduleUpdateView.as_view(), name='schedule_update'),
    path('schedule/<int:pk>/delete/', views.TeacherScheduleDeleteView.as_view(), name='schedule_delete'),
    #path('<int:teacher_id>/schedule/import/', views.ImportScheduleView.as_view(), name='schedule_import'),
    
   
    # URLs para Links Globales
    path('global-links/', views.GlobalTeacherLinkManagerView.as_view(), name='global_link_manager'),
    path('global-links/<int:pk>/update/', views.GlobalTeacherLinkUpdateView.as_view(), name='global_link_update'),
    path('global-links/<int:pk>/delete/', views.GlobalTeacherLinkDeleteView.as_view(), name='global_link_delete'),    

    # URLs para URLs de Links Globales por profesor
    path('<int:teacher_id>/global-links/', views.TeacherGlobalLinkURLManagerView.as_view(), name='teacher_global_links'),
    path('global-link-url/<int:pk>/update/', views.TeacherGlobalLinkURLUpdateView.as_view(), name='global_link_url_update'),

    # URLs para Links Personales
    path('<int:teacher_id>/personal-links/create/', views.TeacherPersonalLinkCreateView.as_view(), name='personal_link_create'),
    path('personal-links/<int:pk>/update/', views.TeacherPersonalLinkUpdateView.as_view(), name='personal_link_update'),
    path('personal-links/<int:pk>/delete/', views.TeacherPersonalLinkDeleteView.as_view(), name='personal_link_delete'),
    
    # Flujo de cumplimiento
    path('compliance/', views.ComplianceManagerView.as_view(), name='compliance_manager'),
    path('compliance/<int:pk>/delete/', views.ComplianceTaskDeleteView.as_view(), name='compliance_task_delete'),
    path('compliance/status/update/', views.ComplianceStatusUpdateView.as_view(), name='compliance_status_update'),

    #Control de asignaturas
    path('courses/', views.CourseManagerView.as_view(), name='course_manager'),  # Nueva URL sin teacher_id
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),  # Sin teacher_id
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),  # Sin teacher_id
    path('courses/overview/', views.CourseOverviewView.as_view(), name='course_overview'),
    
    #URL MPA
    path('mpa/', views.MPAListView.as_view(), name='mpa_list'),
    path('mpa/<int:pk>/detail/', views.MPADetailView.as_view(), name='mpa_detail'),
    path('mpa/<int:pk>/delete/', views.MPADeleteView.as_view(), name='mpa_delete'),
    path('mpa/<int:pk>/edit/', views.MPAEditView.as_view(), name='mpa_edit'),
    path('mpa/upload/', views.MPAUploadView.as_view(), name='mpa_upload'),
    path('mpa/intake-status/', views.MPAIntakeStatusView.as_view(), name='mpa_intake_status'),
    path('mpa/validation/', views.MPAValidationView.as_view(), name='mpa_validation'),
    
    #URL para exportar ad pdf
    path('<int:pk>/profile/pdf/', views.TeacherProfilePDFView.as_view(), name='teacher_profile_pdf'),
    path('<int:teacher_id>/schedule/pdf/', views.TeacherSchedulePDFView.as_view(), name='teacher_schedule_pdf'),
    path('compliance/report/', views.ComplianceReportView.as_view(), name='compliance_report'),
    path('courses/overview/pdf/', views.CourseOverviewPDFView.as_view(), name='course_overview_pdf'),
    path('mpa/validation/pdf/', views.MPAValidationPDFView.as_view(), name='mpa_validation_pdf'),
    path('mpa/intake-status/pdf/', views.MPAIntakeStatusPDFView.as_view(), name='mpa_intake_status_pdf'),
    
    # urls.py
    path('mpa/<int:mpa_id>/timeline/', views.MPATimelineView.as_view(), name='mpa_timeline'),
    path('mpa/<int:mpa_id>/timeline/event/create/', views.TimelineEventCreateView.as_view(), name='timeline_event_create'),
    path('mpa/<int:mpa_id>/timeline/event/<int:event_id>/update/', views.TimelineEventUpdateView.as_view(), name='timeline_event_update'),
path('mpa/<int:mpa_id>/timeline/event/<int:event_id>/delete/', views.TimelineEventDeleteView.as_view(), name='timeline_event_delete'),
]

