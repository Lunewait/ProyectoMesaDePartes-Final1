# En tramites/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .forms import TramiteForm
from .models import Solicitante, Tramite, Documento, TipoTramite


# Vista para la página de inicio
class PaginaInicioView(TemplateView):
    template_name = "tramites/inicio.html"


# Vista para el formulario de creación de trámites
class CrearTramiteView(View):
    def get(self, request):
        form = TramiteForm()
        return render(request, 'tramites/crear_tramite.html', {'form': form})

    def post(self, request):
        form = TramiteForm(request.POST, request.FILES)

        # --- INICIO DE LA CORRECCIÓN ---
        # Si hay datos enviados, volvemos a llenar el queryset de tipo_tramite
        # para que no aparezca vacío en caso de error.
        if 'categoria' in request.POST:
            try:
                categoria_id = int(request.POST.get('categoria'))
                form.fields['tipo_tramite'].queryset = TipoTramite.objects.filter(categoria_id=categoria_id)
            except (ValueError, TypeError):
                pass
        # --- FIN DE LA CORRECCIÓN ---

        if form.is_valid():
            solicitante, created = Solicitante.objects.get_or_create(
                dni=form.cleaned_data['dni'],
                defaults={
                    'nombre_completo': form.cleaned_data['nombre_completo'],
                    'email': form.cleaned_data['email'],
                }
            )
            nuevo_tramite = Tramite.objects.create(
                solicitante=solicitante,
                tipo_tramite=form.cleaned_data['tipo_tramite'],
                mensaje=form.cleaned_data['mensaje']
            )
            Documento.objects.create(
                tramite=nuevo_tramite,
                archivo=request.FILES['archivo_adjunto']
            )
            return redirect('tramite_exito', codigo_seguimiento=nuevo_tramite.codigo_seguimiento)

        # Si el formulario no es válido, lo volvemos a renderizar
        # pero ahora con el queryset de tipo_tramite ya cargado.
        return render(request, 'tramites/crear_tramite.html', {'form': form})
# Vista para la página de consulta de trámites
# En tramites/views.py
class ConsultarTramiteView(View):
    def get(self, request):
        # Muestra la página con el formulario de búsqueda
        return render(request, 'tramites/consultar_tramite.html')

    def post(self, request):
        codigo = request.POST.get('codigo_seguimiento')
        contexto = {} # Usaremos un diccionario para enviar los datos

        try:
            # Busca el trámite en la base de datos
            tramite = Tramite.objects.get(codigo_seguimiento__iexact=codigo)
            contexto['tramite'] = tramite
            # Busca el historial asociado a ese trámite y lo ordena por fecha
            historial = tramite.historial.all().order_by('fecha_cambio')
            contexto['historial'] = historial
        except Tramite.DoesNotExist:
            # Si no lo encuentra, envía un mensaje de error
            contexto['error'] = "No se encontró ningún trámite con ese código. Por favor, verifíquelo e intente de nuevo."

        return render(request, 'tramites/consultar_tramite.html', contexto)

# Vista para la página de éxito tras crear un trámite
class TramiteExitoView(TemplateView):
    template_name = 'tramites/tramite_exito.html'
# Al final de tramites/views.py
class TiposTramitePorCategoriaView(View):
    def get(self, request, categoria_id):
        tipos_tramite = TipoTramite.objects.filter(categoria_id=categoria_id).values('id', 'nombre_tramite')
        return JsonResponse(list(tipos_tramite), safe=False)