from django.db import models
from decimal import Decimal

# Create your models here.

class Producto(models.Model):

    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    # Basado en la tabla 'productos' del diagrama
    
    codProducto = models.CharField(max_length=45, unique=True, verbose_name="Código de Producto",null=True)
    nomProducto = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    precioCompra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Compra")
    precioVenta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stockActual = models.IntegerField(default=0, verbose_name="Stock disponible") #esta con esto porque es una cagada hacerlo de otra manera
    tipoUnidad = models.CharField(max_length=100, verbose_name="Unidad De Medición del Producto") #lo mismo que stockActual
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    categoria = models.CharField(max_length=100, default="General", verbose_name="Categoría")


    def __str__(self):
        return self.nomProducto

    class Meta:
        db_table = 'productos'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nomProducto']