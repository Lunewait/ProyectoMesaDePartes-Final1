# En tramites/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import CategoriaTramite, TipoTramite, Solicitante, Tramite, Documento, HistorialTramite

@admin.register(Tramite)
class TramiteAdmin(admin.ModelAdmin):
    """ Personalización del panel para el modelo Tramite. """
    list_display = ('codigo_seguimiento', 'solicitante', 'tipo_tramite', 'estado_actual', 'fecha_creacion', 'ver_documentos')
    list_filter = ('estado_actual', 'tipo_tramite__categoria')
    search_fields = ('codigo_seguimiento', 'solicitante__nombre_completo', 'solicitante__dni')
    ordering = ('-fecha_creacion',)

    def ver_documentos(self, obj):
        # Crea enlaces para cada documento adjunto
        links = [f'<a href="{doc.archivo.url}" target="_blank">Documento {i+1}</a>' for i, doc in enumerate(obj.documentos.all())]
        return format_html('<br>'.join(links))
    ver_documentos.short_description = "Archivos Adjuntos"

    def save_model(self, request, obj, form, change):
        # Guarda automáticamente un registro en el historial cada vez que se cambia un trámite
        if change: # Solo si es una modificación, no una creación
            estado_anterior = Tramite.objects.get(pk=obj.pk).estado_actual
            if estado_anterior != obj.estado_actual:
                HistorialTramite.objects.create(
                    tramite=obj,
                    administrador=request.user,
                    estado_anterior=estado_anterior,
                    estado_nuevo=obj.estado_actual,
                    observacion="Cambio de estado desde el panel de administración."
                )
        super().save_model(request, obj, form, change)

# Registra los otros modelos de forma simple
admin.site.register(CategoriaTramite)
admin.site.register(TipoTramite)
admin.site.register(Solicitante)
admin.site.register(Documento)
admin.site.register(HistorialTramite)