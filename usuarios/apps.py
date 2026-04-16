from django.apps import AppConfig
#roles default
from django.db.models.signals import post_migrate

class UsuariosConfig(AppConfig):
    name = 'usuarios'

#roles defautl
def crear_roles_por_defecto(sender, **kwargs):
    """Función que crea los roles por defecto después de cada migración"""
    from .models import Rol
    roles_default = ['administrador', 'cajero']
    for rol_nombre in roles_default:
        Rol.objects.get_or_create(nom_rol=rol_nombre)
        print(f'✅ Rol "{rol_nombre}" verificado/creado')


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        """Se ejecuta cuando la app está lista"""
        # Conectar la señal post_migrate para crear roles automáticamente
        post_migrate.connect(crear_roles_por_defecto, sender=self)
