import os
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from django.conf import settings

# Construir la ruta absoluta al modelo
FILE_PATH = os.path.join(settings.BASE_DIR, '..', '..', '..', 'models', 'best_asl_model.keras')

CLASS_INDICES = {
    "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
    "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14,
    "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21,
    "W": 22, "X": 23, "Y": 24, "Z": 25, "del": 26, "nothing": 27, "space": 28,
}

model = None
try:
    if os.path.exists(FILE_PATH):
        model = keras.models.load_model(FILE_PATH)
        print("Modelo ASL cargado exitosamente.")
    else:
        print(f"Error: No se encontró el archivo del modelo en {FILE_PATH}")
except Exception as e:
    print(f"Error al cargar el modelo ASL: {e}")

def predict_image(img_path):
    """Carga una imagen, la preprocesa y predice su clase."""
    if model is None:
        print("El modelo ASL no está cargado, no se puede predecir.")
        return None, 0.0

    try:
        img = image.load_img(img_path, target_size=(200, 200))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        preds = model.predict(img_array)[0]
        pred_idx = np.argmax(preds)
        confidence = preds[pred_idx]

        index_to_class = {v: k for k, v in CLASS_INDICES.items()}
        pred_name = index_to_class.get(pred_idx, "Desconocido")

        print(f"Clase: {pred_name}, Confianza: {confidence:.4f}")
        return pred_name, confidence
    except Exception as e:
        print(f"Ocurrió un error durante la predicción: {e}")
        return None, 0.0