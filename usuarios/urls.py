from django.urls import path
from . import views

urlpatterns = [
    #  LOGIN
    path('login/', views.login_view, name='login'),

    #  LOGOUT
    path('logout/', views.logout_view, name='logout'),

    # REGISTER
    path('register/', views.register, name='register'),

    # DASHBOARDS
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/cajero/', views.dashboard_cajero, name='dashboard_cajero'),

    #MODIFICAR USUARIO
    path('modificar/<int:id>/', views.modificar_usuario, name='modificar_usuario'),
    #eliminar
    path('eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
]