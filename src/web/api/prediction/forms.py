from django import forms
from django.forms import widgets

#Crear el formulario para la prediccion
class RLForm(forms.Form):
    CRIM = forms.FloatField(
        required=True,
        label="CRIM (Tasa de criminalidad per cápita)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo:  0.00632'}))
    ZN = forms.FloatField(
        required=True,
        label="ZN (Proporción de terrenos residenciales zonificados para lotes de más de 25,000 pies cuadrados)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' Ejemplo: 0.00'}))
    INDUS = forms.FloatField(
        required=True,
        label="INDUS (Proporción de acres comerciales no minoristas por ciudad)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 18.10'}))
    CHAS = forms.FloatField(
        required=True,
        label="CHAS (Variable ficticia que indica si el tramo limita con el río Charles)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 0.00'}))
    NOX  = forms.FloatField(
        required=True,
        label="NOX (Concentración de óxidos nítricos en partes por 10 millones)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 0.538'}))
    RM = forms.FloatField(
        required=True,
        label="RM (Número promedio de habitaciones por vivienda)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 6.575'}))
    AGE  = forms.FloatField(
        required=True,
        label="AGE (Proporción de unidades ocupadas por propietarios construidas antes de 1940)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 100.00'})) 
    DIS = forms.FloatField(
        required=True,
        label="DIS (Distancia ponderada a cinco centros de empleo de Boston)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 4.0980'}))
    RAD = forms.FloatField(
        required=True,
        label="RAD (Índice de accesibilidad a carreteras radiales)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 1.00'}))
    TAX = forms.FloatField(
        required=True,
        label="TAX (Tasa de impuesto a la propiedad de valor total en $10,000)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 330.00'}))
    PTRATIO = forms.FloatField(
        required=True,
        label="PTRATIO (Proporción alumno-profesor por ciudad)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 18.70'}))
    B = forms.FloatField(
        required=True,
        label="B (1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 4.98'}))
    LSTAT = forms.FloatField(
        required=True,
        label="LSTAT (Porcentaje de población de bajo estatus socioeconómico)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: 24.00'}))