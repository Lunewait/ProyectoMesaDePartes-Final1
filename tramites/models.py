# Create your models here.
# En tramites/models.py
from django.db import models
from django.contrib.auth.models import User


class CategoriaTramite(models.Model):
    nombre_categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_categoria


class TipoTramite(models.Model):
    categoria = models.ForeignKey(CategoriaTramite, on_delete=models.CASCADE)
    nombre_tramite = models.CharField(max_length=255)
    requiere_pago = models.BooleanField(default=False)
    requisitos = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_tramite


class Solicitante(models.Model):
    nombre_completo = models.CharField(max_length=200)
    dni = models.CharField(max_length=8, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.nombre_completo


class Tramite(models.Model):
    ESTADO_OPCIONES = [
        ('Recibido', 'Recibido'),
        ('En Proceso', 'En Proceso'),
        ('Observado', 'Observado'),
        ('Finalizado', 'Finalizado'),
        ('Rechazado', 'Rechazado'),
    ]

    codigo_seguimiento = models.CharField(max_length=15, unique=True, blank=True)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.PROTECT)
    tipo_tramite = models.ForeignKey(TipoTramite, on_delete=models.PROTECT)
    mensaje = models.TextField()
    estado_actual = models.CharField(max_length=50, choices=ESTADO_OPCIONES, default='Recibido')
    pago_confirmado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            last_tramite = Tramite.objects.all().order_by('id').last()
            next_id = (last_tramite.id + 1) if last_tramite else 1
            self.codigo_seguimiento = f'TRAMITE-{next_id:05d}'
        super(Tramite, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo_seguimiento} - {self.solicitante.nombre_completo}'


class Documento(models.Model):
    tramite = models.ForeignKey(Tramite, related_name='documentos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Documento para {self.tramite.codigo_seguimiento}'


class HistorialTramite(models.Model):
    tramite = models.ForeignKey(Tramite, related_name='historial', on_delete=models.CASCADE)
    administrador = models.ForeignKey(User, on_delete=models.PROTECT)
    estado_anterior = models.CharField(max_length=50, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=50)
    observacion = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cambio en {self.tramite.codigo_seguimiento} por {self.administrador.username}'