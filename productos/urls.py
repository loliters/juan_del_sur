#rutas
from django.urls import path, include
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.inventario, name='inventario'),  # Redirige a inventario por defecto
    path('registrar/', views.registrar, name='registrar'),
    path('editar/<int:id_producto>/', views.editar, name='editar'),
    path('eliminar/<int:id_producto>/', views.eliminar, name='eliminar'),
    path('recuperar/', views.lista_recuperar, name='lista_recuperar'),  # ← nombre consistente
    path('confirmar-recuperacion/<int:id_producto>/', views.ejecutar_recuperacion, name='confirmar_recuperacion'),
]