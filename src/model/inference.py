from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing import image

FILE_PATH = "../../models/best_asl_model.keras"

train_generator_predict = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "del": 26,
    "nothing": 27,
    "space": 28,
}

try:
    model = keras.models.load_model(FILE_PATH)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


def predict_image(model, img_path, class_indices):
    """Carga una imagen, la preprocesa y predice su clase."""
    img = image.load_img(img_path, target_size=(200, 200))
    img_array = image.img_to_array(img)[None, ...]
    img_array = img_array / 255.0

    preds = model.predict(img_array)[0] 
    pred_idx = np.argmax(preds)


    confidence = preds[pred_idx]

    index_to_class = {v: k for k, v in class_indices.items()}
    pred_name = index_to_class[pred_idx]

    print(f"Clase: {pred_name}, Índice: {pred_idx}, Confianza: {confidence:.4f}")
    return pred_name

# example usage
# try:
#     image_path = "../../data/test_images/j.jpg"
#     predicted_class = predict_image(model, image_path, train_generator_predict)
#     print(f"\nResultado final para {image_path}: {predicted_class}")
# except Exception as e:
#     print(f"Ocurrió un error durante la predicción: {e}")