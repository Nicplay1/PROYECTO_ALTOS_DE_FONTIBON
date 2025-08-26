from django import forms
from usuario.models import *


class DetalleResidenteForm(forms.ModelForm):
    class Meta:
        model = DetalleResidente
        fields = ['propietario', 'apartamento', 'torre']
        widgets = {
            'propietario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apartamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'torre': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['hora_inicio', 'hora_fin', 'fecha_uso']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'fecha_uso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }