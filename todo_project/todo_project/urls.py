from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda req: redirect('task-list')),
    path('', include('tasks.urls')),
    path('tasks/api/v1/', include('tasks.api.v1.urls')),
]