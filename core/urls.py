from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('workmanager.urls')),
    path('meece/', include(('MEECETeacherManager.urls', 'meece_teacher'), namespace='meece_teacher')),
    path('tinymce/', include('tinymce.urls')),
]