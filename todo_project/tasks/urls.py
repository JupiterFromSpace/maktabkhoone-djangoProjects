from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/<int:pk>/toggle/', views.TaskToggleView.as_view(), name='task-toggle'),
]