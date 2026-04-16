from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Producto
from decimal import Decimal

# Listar productos (Inventario)
def inventario(request):
    # Mostrar solo productos activos
    productos = Producto.objects.filter(estado='activo')
    return render(request, 'productos/inventario.html', {'productos': productos})

# Registrar nuevo producto
def registrar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria = request.POST.get('categoria')
        precio_compra = request.POST.get('precio_compra')
        precio_venta = request.POST.get('precio_venta')
        stock = request.POST.get('stock')
        
        if not nombre:
            messages.error(request, 'El nombre es obligatorio')
            return redirect('productos:registrar')
        
        producto = Producto.objects.create(
            nombre=nombre,
            categoria=categoria,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            estado='activo'  # ← minúscula
        )
        
        messages.success(request, f'Producto "{nombre}" creado exitosamente')
        return redirect('productos:inventario')
    
    categorias = ["Lacteos", "Pan", "Frutas", "Bebidas", "Snacks", "General"]
    return render(request, 'productos/registrar.html', {'categorias': categorias})

# Editar producto
def editar(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    categorias = ["Lacteos", "Pan", "Frutas", "Bebidas", "Snacks", "General"]
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.categoria = request.POST.get('categoria')
        
        # Convertir precios correctamente
        precio_compra_str = request.POST.get('precio_compra', '0')
        precio_venta_str = request.POST.get('precio_venta', '0')
        
        # Reemplazar coma por punto si existe
        precio_compra_str = precio_compra_str.replace(',', '.')
        precio_venta_str = precio_venta_str.replace(',', '.')
        
        # Convertir a Decimal
        try:
            producto.precio_compra = Decimal(precio_compra_str) if precio_compra_str else 0.0
            producto.precio_venta = Decimal(precio_venta_str) if precio_venta_str else 0.0
        except ValueError:
            producto.precio_compra = 0.0
            producto.precio_venta = 0.0

            
        
        # Convertir stock a entero
        stock_str = request.POST.get('stock', '0')
        try:
            producto.stock = int(stock_str) if stock_str else 0
        except ValueError:
            producto.stock = 0
        
        producto.estado = request.POST.get('estado')
        
        if not producto.nombre:
            messages.error(request, 'El nombre es obligatorio')
            return redirect('productos:editar', id_producto=id_producto)
        
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" actualizado')
        return redirect('productos:inventario')
    
    return render(request, 'productos/editar.html', {
        'producto': producto,
        'categorias': categorias
    })

# Cambiar estado a inactivo (en lugar de eliminar)
def eliminar(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    
    if request.method == 'POST':
        nombre = producto.nombre
        # Cambiar estado a 'inactivo' en lugar de eliminar
        producto.estado = 'inactivo'  
        producto.save()
        messages.success(request, f'Producto "{nombre}" marcado como inactivo')
        return redirect('productos:inventario')
    
    return render(request, 'productos/eliminar.html', {'producto': producto})

# Para la recuperación - Vista para ver la lista de inactivos
def lista_recuperar(request):
    # Filtramos los que están en la "papelera" (Inactivos)
    productos_inactivos = Producto.objects.filter(estado='inactivo')  # ← minúscula
    return render(request, 'productos/recuperar.html', {'productos': productos_inactivos})

# Función lógica para activar el producto
def ejecutar_recuperacion(request, id_producto):
    producto = get_object_or_404(Producto, id=id_producto)
    producto.estado = 'activo'  # ← minúscula
    producto.save()
    messages.success(request, f"¡{producto.nombre} ha vuelto al inventario!")  # ← nombre, no nom_producto
    return redirect('productos:lista_recuperar')  # ← nombre correcto de la URL