from django.shortcuts import render, redirect
from .logic import ProductoInMemoria

# Create your views here.

# Base de datos en memoria (Datos iniciales para pruebas)
PRODUCTOS_DB = [
    ProductoInMemoria(101, "Papas", "Verduras", 1000, 1200, "Activo", "Kg", 50),
    ProductoInMemoria(102, "Cocacola", "Bebidas", 800, 1200, "Activo", "Unidades", 24),
]

#lista, inicio
def inventario_general(request):
    return render(request, 'productos/inventario.html', {'productos': PRODUCTOS_DB})

#llevar a otra vista
def registrar_producto(request):
    if request.method == 'POST':
        nuevo_id = max([p.id_producto for p in PRODUCTOS_DB]) + 1 if PRODUCTOS_DB else 101
        nuevo_p = ProductoInMemoria(
            id_prod=nuevo_id,
            nombre=request.POST.get('nombre'),
            id_cat=request.POST.get('categoria'),
            p_compra=request.POST.get('precio_compra', 0),
            p_venta=request.POST.get('precio_venta', 0),
            estado=request.POST.get('estado'),
            unidad=request.POST.get('tipo_unidad'),
            stock=request.POST.get('stock', 0)
        )
        PRODUCTOS_DB.append(nuevo_p)
        return redirect('inventario')
    return render(request, 'productos/registro.html')

def editar_producto(request, p_id):
    producto = next((p for p in PRODUCTOS_DB if p.id_producto == int(p_id)), None)
    if request.method == 'POST':
        producto.nom_producto = request.POST.get('nombre')
        producto.id_categoria = request.POST.get('categoria')
        producto.precio_venta = float(request.POST.get('precio_venta'))
        producto.estado = request.POST.get('estado')
        return redirect('inventario')
    return render(request, 'productos/editar.html', {'producto': producto})

def eliminar_producto(request, p_id):
    producto = next((p for p in PRODUCTOS_DB if p.id_producto == int(p_id)), None)
    if request.method == 'POST':
        PRODUCTOS_DB.remove(producto)
        return redirect('inventario')
    return render(request, 'productos/eliminar.html', {'producto': producto})