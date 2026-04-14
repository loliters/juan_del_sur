#rutas
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventario_general, name='inventario'),
    path('nuevo/', views.registrar_producto, name='registrar'),
    path('editar/<int:p_id>/', views.editar_producto, name='editar'),
    path('eliminar/<int:p_id>/', views.eliminar_producto, name='eliminar'),
]