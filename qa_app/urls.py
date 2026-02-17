from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='qa_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]