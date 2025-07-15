from django import forms
from django.forms import widgets

#Crear el formulario para la prediccion
class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Selecciona una imagen", widget=widgets.ClearableFileInput(attrs={'class': 'form-control'}))