import cv2
import numpy as np

def classify_platform(image_path):
    """
    Esta función intenta determinar visualmente a qué plataforma pertenece
    una captura de pantalla (ATAS, NinjaTrader, SierraChart, etc.)
    usando características simples como colores dominantes o logos.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"❌ No se puede abrir la imagen: {image_path}")

    # Reduce la imagen para acelerar el análisis
    img_small = cv2.resize(img, (100, 100))
    img_lab = cv2.cvtColor(img_small, cv2.COLOR_BGR2LAB)
    avg_color = cv2.mean(img_lab)

    l, a, b, _ = avg_color

    # Heurística simple basada en colores (esto debe mejorarse con ML)
    if a > 150:
        platform = "NinjaTrader"
    elif b > 150:
        platform = "SierraChart"
    else:
        platform = "ATAS"

    print(f"🔍 Plataforma detectada visualmente: {platform}")
    return platform

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python visual_platform_classifier.py ruta/a/imagen.png")
    else:
        classify_platform(sys.argv[1])




# import cv2
# import numpy as np
# import os

# # Dummy model - for real case, replace with trained classifier
# def predict_platform(image):
#     # Placeholder logic based on mean brightness
#     mean_brightness = np.mean(image)
#     if mean_brightness > 120:
#         return "ATAS"
#     else:
#         return "NinjaTrader"

# def classify_capture(image_path):
#     image = cv2.imread(image_path)
#     prediction = predict_platform(image)
#     print(f"Predicted platform: {prediction}")

# if __name__ == "__main__":
#     classify_capture("screenshots/sample_capture.png")  # replace with your own path
