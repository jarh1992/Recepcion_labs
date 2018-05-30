from django import forms
from .models import Program


input_field = forms.TextInput(attrs={'class': 'form-control'})
select_field = forms.TextInput(attrs={'class': 'custom-select'})

class FormSAS(forms.Form):
    name = forms.CharField(max_length=60, widget=input_field, label='Nombre')
    ced = forms.CharField(required=True, widget=input_field, label='Cédula')
    cod = forms.CharField(required=True, widget=input_field, label='Codigo estudiantil')
    program = forms.ModelChoiceField(label='Programa de Estudio',
                                     queryset=Program.objects.values_list('name', flat=True).distinct(),
                                     widget=select_field)


class FormAddProg(forms.Form):
    name = forms.CharField(max_length=60, widget=input_field, label='Nombre')
    cod = forms.CharField(required=True, widget=input_field, label='Codigo del Programa')