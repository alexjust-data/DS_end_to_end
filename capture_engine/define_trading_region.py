import cv2
import mss
import numpy as np
import os
import json

from pathlib import Path

CONFIG_PATH = "config/region.json"

def select_screen_region():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    clone = screenshot.copy()
    selecting = False
    ix, iy = -1, -1
    region = {}

    def draw_rectangle(event, x, y, flags, param):
        nonlocal ix, iy, selecting, region, clone

        if event == cv2.EVENT_LBUTTONDOWN:
            selecting = True
            ix, iy = x, y
            region = {}

        elif event == cv2.EVENT_MOUSEMOVE and selecting:
            temp = clone.copy()
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Select Region", temp)

        elif event == cv2.EVENT_LBUTTONUP:
            selecting = False
            region = {
                "top": min(iy, y),
                "left": min(ix, x),
                "width": abs(x - ix),
                "height": abs(y - iy)
            }
            temp = clone.copy()
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Select Region", temp)

    cv2.namedWindow("Select Region", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Select Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("Select Region", draw_rectangle)
    cv2.imshow("Select Region", screenshot)

    print("🖱️ Selecciona la región deseada y presiona 'c' para confirmar o 'q' para cancelar.")
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c") and region:
            os.makedirs("config", exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                json.dump(region, f, indent=4)
            print(f"✅ Región guardada en {CONFIG_PATH}")
            break
        elif key == ord("q"):
            print("❌ Selección cancelada.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    select_screen_region()



# import cv2
# import mss
# import numpy as np
# import json
# import os

# def select_region():
#     with mss.mss() as sct:
#         monitor = sct.monitors[2]
#         screenshot = sct.grab(monitor)
#         img = np.array(screenshot)
#         img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

#     clone = img.copy()
#     selecting = False
#     region = [0, 0, 0, 0]

#     def draw_rectangle(event, x, y, flags, param):
#         nonlocal selecting, region
#         if event == cv2.EVENT_LBUTTONDOWN:
#             selecting = True
#             region[0], region[1] = x, y
#             region[2], region[3] = x, y
#         elif event == cv2.EVENT_MOUSEMOVE and selecting:
#             region[2], region[3] = x, y
#         elif event == cv2.EVENT_LBUTTONUP:
#             selecting = False
#             region[2], region[3] = x, y

#     cv2.namedWindow("Select Trading Region", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Select Trading Region", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.setMouseCallback("Select Trading Region", draw_rectangle)

#     while True:
#         overlay = clone.copy()
#         display = clone.copy()
#         alpha = 0.5
#         dark = np.full_like(display, (50, 50, 50), dtype=np.uint8)
#         cv2.addWeighted(dark, alpha, display, 1 - alpha, 0, display)

#         if region[0] != region[2] and region[1] != region[3]:
#             x1, y1, x2, y2 = region
#             left, top = min(x1, x2), min(y1, y2)
#             right, bottom = max(x1, x2), max(y1, y2)

#             display[top:bottom, left:right] = clone[top:bottom, left:right]
#             cv2.rectangle(display, (left, top), (right, bottom), (0, 255, 0), 2)

#         cv2.imshow("Select Trading Region", display)
#         key = cv2.waitKey(1) & 0xFF

#         if key == ord("c"):
#             x1, y1, x2, y2 = region
#             left = min(x1, x2)
#             top = min(y1, y2)
#             width = abs(x2 - x1)
#             height = abs(y2 - y1)
#             os.makedirs("config", exist_ok=True)
#             with open("config/region.json", "w") as f:
#                 json.dump({"top": top, "left": left, "width": width, "height": height}, f)

#             # ✅ Guarda la imagen seleccionada
#             selected_region = clone[top:top+height, left:left+width]
#             os.makedirs("data/images", exist_ok=True)
#             cv2.imwrite("data/images/selected_region.png", selected_region)


#             print("✅ Región guardada en config/region.json")
#             print("🖼️ Imagen guardada en data/images/selected_region.png")
#             break
#         elif key == ord("r"):
#             region = [0, 0, 0, 0]
#         elif key == 27:
#             print("❌ Cancelado")
#             break

#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     select_region()
