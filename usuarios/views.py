from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

from .models import Usuario, Rol


# =========================
# LOGIN
# =========================
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import Usuario


def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # validación básica
        if not email or not password:
            return render(request, 'usuarios/login.html', {
                'error': 'Completa todos los campos'
            })

        try:
            user = Usuario.objects.select_related('rol').get(email__iexact=email)
        except Usuario.DoesNotExist:
            return render(request, 'usuarios/login.html', {
                'error': 'Usuario no existe'
            })

        # validar contraseña
        if not check_password(password, user.password):
            return render(request, 'usuarios/login.html', {
                'error': 'Contraseña incorrecta'
            })

        # normalizar rol
        rol = user.rol.nom_rol.strip().lower()

        # guardar sesión
        request.session['usuario_id'] = user.id
        request.session['rol'] = rol
        request.session['nombre'] = user.nom_usuario

        # redirección por rol (CORREGIDO Y ROBUSTO)
        if rol == "administrador":
            return redirect('dashboard_admin')
        elif rol == "cajero":
            return redirect('dashboard_cajero')
        else:
            return render(request, 'usuarios/login.html', {
                'error': 'Rol no válido'
            })

    return render(request, 'usuarios/login.html')

# =========================
# REGISTER
# =========================
def register(request):

    roles = Rol.objects.all()

    if request.method == "POST":

        nom_usuario = request.POST.get('nom_usuario', '').strip()
        ap1 = request.POST.get('ap1', '').strip()
        ap2 = request.POST.get('ap2', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        rol_id = request.POST.get('rol')
        estado = request.POST.get('estado') == 'on'

        if not nom_usuario or not email or not password or not rol_id:
            return render(request, 'usuarios/register.html', {
                'roles': roles,
                'error': 'Completa todos los campos obligatorios'
            })

        try:
            rol_obj = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return render(request, 'usuarios/register.html', {
                'roles': roles,
                'error': 'Rol inválido'
            })

        try:
            Usuario.objects.create(
                nom_usuario=nom_usuario,
                ap1=ap1,
                ap2=ap2,
                email=email,
                password=make_password(password),
                rol=rol_obj,
                estado=estado
            )

        except IntegrityError:
            return render(request, 'usuarios/register.html', {
                'roles': roles,
                'error': 'Ese email ya está registrado'
            })

        return redirect('login')

    return render(request, 'usuarios/register.html', {
        'roles': roles
    })


# =========================
# DASHBOARD CAJERO
# =========================
def dashboard_cajero(request):

    if request.session.get('usuario_id') is None:
        return redirect('login')

    return render(request, 'usuarios/dashboard_cajero.html')


# =========================
# DASHBOARD ADMIN
# =========================
def dashboard_admin(request):

    if request.session.get('rol') != "administrador":
        return redirect('login')

    usuarios = Usuario.objects.select_related('rol').all()

    return render(request, 'usuarios/dashboard_admin.html', {
        'usuarios': usuarios
    })


# =========================
# MODIFICAR USUARIO
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Rol


def modificar_usuario(request, id):

    # 🔐 obtener sesión segura
    usuario_sesion = request.session.get('usuario_id')
    rol = (request.session.get('rol') or '').strip().lower()

    print("ROL EN SESION:", rol)  # debug

    # 🔒 validar login
    if not usuario_sesion:
        return redirect('login')

    # 🔒 validar rol admin
    if rol != "administrador":
        return redirect('login')

    # 🔎 usuario seguro
    usuario = get_object_or_404(Usuario, id=id)
    roles = Rol.objects.all()

    if request.method == "POST":

        usuario.nom_usuario = request.POST.get('nom_usuario', '').strip()
        usuario.ap1 = request.POST.get('ap1', '').strip()
        usuario.ap2 = request.POST.get('ap2', '').strip()
        usuario.email = request.POST.get('email', '').strip()

        rol_id = request.POST.get('rol')

        # 🔒 evitar crash
        if rol_id:
            try:
                usuario.rol = Rol.objects.get(id=rol_id)
            except Rol.DoesNotExist:
                pass

        usuario.estado = request.POST.get('estado') == 'on'

        usuario.save()

        return redirect('dashboard_admin')

    return render(request, 'usuarios/modify.html', {
        'usuario': usuario,
        'roles': roles
    })

# =========================
# LOGOUT
# =========================
def logout_view(request):

    request.session.flush()
    return redirect('login')
#==========================
#eliminar
#==========================
def eliminar_usuario(request, id):

    if request.session.get('rol') != "administrador":
        return redirect('login')

    usuario = Usuario.objects.get(id=id)
    usuario.delete()

    return redirect('dashboard_admin')