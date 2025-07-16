from django import forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImageUploadForm(forms.Form):
    images = MultipleFileField(
        label='Selecciona las imágenes',
        widget=MultipleFileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        })
    )

class SingleImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'accept': 'image/*',
            'class': 'form-control'
        }),
        label='Selecciona una imagen'
    )
class TextToSignsForm(forms.Form):
    text = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe una palabra o frase...',
            'autocomplete': 'off'
        }),
        label='Texto a convertir'
    )