# En tramites/forms.py
from django import forms
from .models import TipoTramite, CategoriaTramite


class TramiteForm(forms.Form):
    # Campos para el Solicitante
    nombre_completo = forms.CharField(
        label="Nombre Completo",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    dni = forms.CharField(
        label="DNI",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    # Campo 1: El usuario primero selecciona si es estudiante, egresado, etc.
    categoria = forms.ModelChoiceField(
        queryset=CategoriaTramite.objects.all(),
        label="Soy",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Campo 2: Este menú empieza vacío y se llenará con JavaScript.
    tipo_tramite = forms.ModelChoiceField(
        queryset=TipoTramite.objects.none(),  # <-- Empieza vacío
        label="Tipo de Trámite que deseo realizar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Resto de los campos
    mensaje = forms.CharField(
        label="Mensaje o Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    archivo_adjunto = forms.FileField(
        label="Adjuntar Documento",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )