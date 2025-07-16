from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm, SingleImageUploadForm, TextToSignsForm
from .model_handler import predict_image
from django.conf import settings
import os
import json

def prediction_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener todas las imágenes del formulario
            images = request.FILES.getlist('images')
            results = []
            successful_predictions = 0
            
            # Configurar FileSystemStorage para usar MEDIA_ROOT
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            
            for image in images:
                try:
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
                    
                    results.append({
                        'image_name': image.name,
                        'image_url': img_url,
                        'prediction': predicted_class,
                        'confidence': f"{confidence:.2%}",
                        'success': True
                    })
                    successful_predictions += 1
                    
                except Exception as e:
                    print(f"Error procesando {image.name}: {str(e)}")
                    results.append({
                        'image_name': image.name,
                        'image_url': None,
                        'prediction': None,
                        'confidence': None,
                        'success': False,
                        'error': str(e)
                    })
                
                # Opcional: Eliminar el archivo después de la predicción
                # try:
                #     os.remove(img_path)
                # except:
                #     pass

            # Formar palabra con las predicciones exitosas
            word_formed = ''.join([result['prediction'] for result in results if result['success']])
            
            return render(request, 'prediction/image_to_text.html', {
                'form': form,
                'results': results,
                'multiple_images': True,
                'successful_predictions': successful_predictions,
                'total_images': len(images),
                'word_formed': word_formed
            })
    else:
        form = ImageUploadForm()
    
    return render(request, 'prediction/image_to_text.html', {'form': form})

def single_prediction_view(request):
    if request.method == 'POST':
        form = SingleImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            
            # Configurar FileSystemStorage para usar MEDIA_ROOT
            fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
            
            try:
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

                return render(request, 'prediction/single_image.html', {
                    'form': form,
                    'prediction': predicted_class,
                    'confidence': f"{confidence:.2%}",
                    'image_url': img_url,
                    'success': True
                })
                
            except Exception as e:
                print(f"Error procesando la imagen: {str(e)}")
                return render(request, 'prediction/single_image.html', {
                    'form': form,
                    'error': str(e),
                    'success': False
                })
    else:
        form = SingleImageUploadForm()
    return render(request, 'prediction/single_image.html', {'form': form})


def text_to_signs_view(request):
    if request.method == 'POST':
        form = TextToSignsForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text'].upper().strip()
            results = []
            
            # Directorio donde están las imágenes de referencia
            input_dir = os.path.join(settings.MEDIA_ROOT, 'input')
            
            # Cargar el índice de imágenes
            index_file = os.path.join(input_dir, 'index.json')
            image_index = load_image_index(input_dir, index_file)
            
            for char in text:
                if char.isalpha():  # Solo procesar letras
                    if char in image_index:
                        # Construir la URL de la imagen
                        image_path = image_index[char]
                        image_url = os.path.join(settings.MEDIA_URL, 'input', image_path)
                        
                        results.append({
                            'letter': char,
                            'image_url': image_url,
                            'image_name': image_path,
                            'found': True
                        })
                    else:
                        results.append({
                            'letter': char,
                            'image_url': None,
                            'image_name': None,
                            'found': False
                        })
                elif char == ' ':
                    results.append({
                        'letter': ' ',
                        'image_url': None,
                        'image_name': 'espacio',
                        'found': True,
                        'is_space': True
                    })
            
            return render(request, 'prediction/text_to_signs.html', {
                'form': form,
                'results': results,
                'original_text': text,
                'total_letters': len([r for r in results if r['letter'] != ' ']),
                'found_letters': len([r for r in results if r['found'] and r['letter'] != ' '])
            })
    else:
        form = TextToSignsForm()
    
    return render(request, 'prediction/text_to_signs.html', {'form': form})

def load_image_index(input_dir, index_file):
    """
    Carga o crea un índice de imágenes para cada letra
    """
    # Si existe el archivo de índice, cargarlo
    if os.path.exists(index_file):
        try:
            with open(index_file, 'r') as f:
                return json.load(f)
        except:
            pass
    
    # Si no existe o hay error, crear uno nuevo
    image_index = {}
    
    if os.path.exists(input_dir):
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Extraer la letra del nombre del archivo
                # Asumiendo nombres como "A.jpg", "B.png", "letter_A.jpg", etc.
                name_without_ext = os.path.splitext(filename)[0]
                
                # Buscar la letra en el nombre del archivo
                letter = None
                if len(name_without_ext) == 1 and name_without_ext.isalpha():
                    letter = name_without_ext.upper()
                elif '_' in name_without_ext:
                    parts = name_without_ext.split('_')
                    for part in parts:
                        if len(part) == 1 and part.isalpha():
                            letter = part.upper()
                            break
                elif name_without_ext.upper().startswith('LETTER_'):
                    letter = name_without_ext.replace('LETTER_', '').replace('letter_', '').upper()
                    if len(letter) == 1:
                        letter = letter
                    else:
                        letter = None
                
                if letter and letter.isalpha():
                    image_index[letter] = filename
    
    # Guardar el índice para futuras consultas
    try:
        with open(index_file, 'w') as f:
            json.dump(image_index, f, indent=2)
    except:
        pass
    
    return image_index