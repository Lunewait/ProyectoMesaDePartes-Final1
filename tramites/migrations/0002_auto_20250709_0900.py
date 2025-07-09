# En el archivo de migración nuevo (ej. 0002_auto_...)
from django.db import migrations

def crear_datos_iniciales(apps, schema_editor):
    CategoriaTramite = apps.get_model('tramites', 'CategoriaTramite')
    TipoTramite = apps.get_model('tramites', 'TipoTramite')

    # Crear Categorías (Pregrado y Egresados)
    cat_estudiantes = CategoriaTramite.objects.create(nombre_categoria='Trámites para Estudiantes')
    cat_egresados = CategoriaTramite.objects.create(nombre_categoria='Trámites para Egresados')

    # Crear Tipos de Trámite para Estudiantes
    TipoTramite.objects.create(categoria=cat_estudiantes, nombre_tramite='Constancia de Estudios')
    TipoTramite.objects.create(categoria=cat_estudiantes, nombre_tramite='Reporte de Notas')
    TipoTramite.objects.create(categoria=cat_estudiantes, nombre_tramite='Reserva de Matrícula')

    # Crear Tipos de Trámite para Egresados
    TipoTramite.objects.create(categoria=cat_egresados, nombre_tramite='Trámite para Obtener Título Profesional')
    TipoTramite.objects.create(categoria=cat_egresados, nombre_tramite='Constancia de Egresado')

class Migration(migrations.Migration):
    dependencies = [
        ('tramites', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(crear_datos_iniciales),
    ]
