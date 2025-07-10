# En tramites/migrations/0003_crear_superuser.py
from django.db import migrations
from django.contrib.auth.models import User


def crear_superuser(apps, schema_editor):
    """
    Crea un superusuario predeterminado para el sistema.
    """
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@mesadepartes.com',
            password='admin_password_123'  # <-- ¡CAMBIA ESTA CONTRASEÑA!
        )


class Migration(migrations.Migration):
    dependencies = [
        ('tramites', '0002_auto_...'),  # <-- Reemplaza '0002_auto_...' con el nombre de tu migración anterior
    ]

    operations = [
        migrations.RunPython(crear_superuser),
    ]

