from django import forms
from usuario.models import *

class CambiarRolForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['id_rol']
        labels = {'id_rol': 'Rol'}


class EditarReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["observacion", "estado"]
        labels = {
            "observacion": "Observación",
            "estado": "Estado"
        }


class NoticiasForm(forms.ModelForm):
    class Meta:
        model = Noticias
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la descripción'
            }),
        }