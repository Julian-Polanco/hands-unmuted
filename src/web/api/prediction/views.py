from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from .model_handler import predict_image
from django.conf import settings
import os

def prediction_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Configurar FileSystemStorage para usar MEDIA_ROOT
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            
            # Guardar la imagen
            filename = fs.save(image.name, image)
            print(f"Imagen guardada con el nombre: {filename}")
            
            # Obtener la ruta completa del archivo guardado
            img_path = fs.path(filename)
            print(f"Imagen guardada en: {img_path}")
            
            # Realizar la predicción
            predicted_class, confidence = predict_image(img_path)
            
            # Obtener la URL para mostrar la imagen en la plantilla
            img_url = fs.url(filename)
            print(f"URL de la imagen: {img_url}")

            # Opcional: Eliminar el archivo después de la predicción
            # os.remove(img_path)

            return render(request, 'prediction/image_to_text.html', {
                'form': form,
                'prediction': predicted_class,
                'confidence': f"{confidence:.2%}",
                'image_url': img_url
            })
    else:
        form = ImageUploadForm()
    return render(request, 'prediction/image_to_text.html', {'form': form})