import time
import cv2
import mss
from pathlib import Path
from datetime import datetime

def capture_screen(region):
    with mss.mss() as sct:
        screenshot = sct.grab(region)
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)
        return img

def save_image(img, name=None):
    images_dir = Path("data/images")
    images_dir.mkdir(parents=True, exist_ok=True)
    if not name:
        name = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = images_dir / f"{name}.png"
    cv2.imwrite(str(path), img)
    return path

if __name__ == "__main__":
    import json

    config_path = Path("config/region.json")
    if not config_path.exists():
        print("❌ Región no definida. Ejecuta define_trading_region.py primero.")
        exit()

    with open(config_path) as f:
        region = json.load(f)

    print("✅ Iniciando captura continua...")
    while True:
        img = capture_screen(region)
        cv2.imshow("Live Capture", img)

        if cv2.waitKey(1) == ord("q"):
            break

    cv2.destroyAllWindows()
