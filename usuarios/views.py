from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError

from .models import Usuario, Rol


# =========================
# LOGIN
# =========================
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import Usuario
import re


def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        #  Validación básica
        if not email or not password:
            messages.error(request, 'Completa todos los campos')
            return redirect('login')

        #  Validar formato de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'Correo inválido')
            return redirect('login')

        try:
            user = Usuario.objects.select_related('rol').get(email__iexact=email)
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no existe')
            return redirect('login')

        #  Validar usuario activo
        if not user.estado:
            messages.error(request, 'Usuario deshabilitado')
            return redirect('login')

        #  Validar contraseña
        if not check_password(password, user.password):
            messages.error(request, 'Contraseña incorrecta')
            return redirect('login')

        #  Validar rol
        if not user.rol or not user.rol.nom_rol:
            messages.error(request, 'Usuario sin rol asignado')
            return redirect('login')

        rol = user.rol.nom_rol.strip().lower()

        #  Guardar sesión
        request.session['usuario_id'] = user.id
        request.session['rol'] = rol
        request.session['nombre'] = user.nom_usuario

        # Redirección por rol
        if rol == "administrador":
            return redirect('dashboard_admin')

        elif rol == "cajero":
            return redirect('dashboard_cajero')

        else:
            messages.error(request, 'Rol no válido')
            return redirect('login')

    return render(request, 'usuarios/login.html')

# =========================
# REGISTER
# =========================
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.contrib import messages
from .models import Usuario, Rol
import re


def register(request):

    roles = Rol.objects.all()

    if request.method == "POST":

        nom_usuario = request.POST.get('nom_usuario', '').strip()
        ap1 = request.POST.get('ap1', '').strip()
        ap2 = request.POST.get('ap2', '').strip()
        password = request.POST.get('password', '')
        rol_id = request.POST.get('rol')
        estado = request.POST.get('estado') == 'on'

        # 🔹 Validar nombre o apellido (CORREGIDO)
        if not nom_usuario and not ap1 and not ap2:
            messages.error(request, 'Debes ingresar al menos un nombre o un apellido')
            return redirect('register')

        # 🔹 Validar campos obligatorios
        if not password or not rol_id:
            messages.error(request, 'Completa todos los campos obligatorios')
            return redirect('register')

        # 🔐 Validar contraseña fuerte
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&._-])[A-Za-z\d@$!%*#?&._-]{8,}$', password):
            messages.error(request, 'La contraseña debe tener mínimo 8 caracteres, incluir letras, números y un carácter especial')
            return redirect('register')

        # 🔹 Obtener rol
        try:
            rol_obj = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            messages.error(request, 'Rol inválido')
            return redirect('register')

        # 🔹 Generar correo empresarial
        base = ""

        if nom_usuario:
            base += nom_usuario.split()[0].lower()

        # elegir apellido disponible
        apellido = ""
        if ap1:
            apellido = ap1
        elif ap2:
            apellido = ap2

        if apellido:
            if base:
                base += "."
            base += apellido.split()[0].lower()

        dominio = "juandedios.com"
        email_generado = f"{base}@{dominio}"

        # 🔁 Evitar duplicados
        contador = 1
        email_final = email_generado

        while Usuario.objects.filter(email=email_final).exists():
            email_final = f"{base}{contador}@{dominio}"
            contador += 1

        # 💾 Guardar usuario
        try:
            Usuario.objects.create(
                nom_usuario=nom_usuario,
                ap1=ap1,
                ap2=ap2,
                email=email_final,
                password=make_password(password),
                rol=rol_obj,
                estado=estado
            )

        except IntegrityError:
            messages.error(request, 'Error al registrar usuario')
            return redirect('register')

        # 🔥 Mensaje + redirección
        messages.success(request, f'Usuario creado correctamente. Tu correo es: {email_final}')
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