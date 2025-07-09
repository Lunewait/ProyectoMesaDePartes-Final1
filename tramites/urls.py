# En tramites/urls.py (archivo nuevo)
from django.urls import path
from .views import PaginaInicioView, CrearTramiteView, TramiteExitoView, ConsultarTramiteView, \
    TiposTramitePorCategoriaView

urlpatterns = [
    path('', PaginaInicioView.as_view(), name='inicio'),
    path('tramite/nuevo/', CrearTramiteView.as_view(), name='crear_tramite'),
    path('tramite/exito/<str:codigo_seguimiento>/', TramiteExitoView.as_view(), name='tramite_exito'),
    path('consultar/', ConsultarTramiteView.as_view(), name='consultar_tramite'),
path('api/tipos-tramite/<int:categoria_id>/', TiposTramitePorCategoriaView.as_view(), name='api_tipos_tramite'),
]