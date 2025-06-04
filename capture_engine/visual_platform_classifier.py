import cv2
import numpy as np
import os

# Dummy model - for real case, replace with trained classifier
def predict_platform(image):
    # Placeholder logic based on mean brightness
    mean_brightness = np.mean(image)
    if mean_brightness > 120:
        return "ATAS"
    else:
        return "NinjaTrader"

def classify_capture(image_path):
    image = cv2.imread(image_path)
    prediction = predict_platform(image)
    print(f"Predicted platform: {prediction}")

if __name__ == "__main__":
    classify_capture("screenshots/sample_capture.png")  # replace with your own path
