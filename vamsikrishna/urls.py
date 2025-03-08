from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('admin/', views.admin_login, name='admin'),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
    path('delete-message/<int:msg_id>/', views.delete_message, name='delete_message'),
    path("logout/", views.admin_logout, name="logout"),
]
