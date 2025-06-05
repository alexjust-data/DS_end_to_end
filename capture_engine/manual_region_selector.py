import cv2
import numpy as np
import mss
import json
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import threading
import queue
import time

CONFIG_DIR = Path("config")
CONFIG_DIR.mkdir(exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "region.json"
AUDIO_FILE = CONFIG_DIR / "audio_temp.wav"
VIDEO_FILE = CONFIG_DIR / "video_temp.mov"  # Cambiado a .mov para compatibilidad Mac

region = {}
drawing = False
ix, iy = -1, -1
recording = False
audio_q = queue.Queue()

def choose_monitor(monitors):
    print("\n🖥️ Monitores detectados:")
    for i, m in enumerate(monitors[1:], start=1):
        print(f"Monitor {i}: {m['width']}x{m['height']} @ ({m['left']}, {m['top']})")
    choice = input("\nSelecciona el número del monitor a capturar (0 = Todos): ")
    try:
        idx = int(choice)
        return monitors[idx] if 0 <= idx < len(monitors) else monitors[1]
    except ValueError:
        return monitors[1]  # por defecto

def capture_full_screen():
    with mss.mss() as sct:
        monitor = choose_monitor(sct.monitors)
        screenshot = np.array(sct.grab(monitor))[:, :, :3]
        return screenshot, monitor

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, region, dimmed_screen, original_screen, recording

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        mask = np.zeros(dimmed_screen.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (ix, iy), (x, y), 255, -1)
        mask_3ch = np.stack([mask] * 3, axis=-1)
        result = (original_screen * (mask_3ch / 255) + dimmed_screen * (1 - mask_3ch / 255)).astype(np.uint8)
        cv2.rectangle(result, (ix, iy), (x, y), (0, 255, 0), 2)
        cv2.imshow(fullscreen_title, result)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x0, y0 = min(ix, x), min(iy, y)
        x1, y1 = max(ix, x), max(iy, y)
        region = {
            "left": x0,
            "top": y0,
            "width": x1 - x0,
            "height": y1 - y0
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(region, f)
        print(f"\n✅ Región guardada en {CONFIG_FILE}: {region}")

        # Guardar imagen del área seleccionada
        selected = original_screen[y0:y1, x0:x1]
        cv2.imwrite(str(CONFIG_DIR / "selected_region.png"), selected)

        # Iniciar grabación
        start_audio_recording()
        record_video(region, monitor)

        global recording
        recording = False
        cv2.destroyAllWindows()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_q.put(indata.copy())

def start_audio_recording(filename=AUDIO_FILE, samplerate=44100, channels=1):
    def record():
        with sf.SoundFile(filename, mode='w', samplerate=samplerate, channels=channels) as file:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback):
                print("🎙️ Grabando audio...")
                while recording:
                    file.write(audio_q.get())
        print(f"💾 Audio guardado en {filename}")

    thread = threading.Thread(target=record, daemon=True)
    thread.start()

def record_video(region, monitor, duration=5):
    with mss.mss() as sct:
        left = region["left"] + monitor["left"]
        top = region["top"] + monitor["top"]
        width = region["width"]
        height = region["height"]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(VIDEO_FILE), fourcc, 10.0, (width, height))

        print("🎥 Grabando video...")
        start_time = time.time()
        while time.time() - start_time < duration:
            bbox = {"top": int(top), "left": int(left), "width": int(width), "height": int(height)}
            img = sct.grab(bbox)
            frame = np.array(img)
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)
        out.release()
        print(f"💾 Video guardado en {VIDEO_FILE}")

if __name__ == "__main__":
    original_screen, monitor = capture_full_screen()
    dim_overlay = np.full_like(original_screen, (30, 30, 30))
    alpha = 0.7
    dimmed_screen = cv2.addWeighted(original_screen, 1 - alpha, dim_overlay, alpha, 0)

    fullscreen_title = "Select Region"
    cv2.namedWindow(fullscreen_title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(fullscreen_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(fullscreen_title, draw_rectangle)

    print("🖱️ Dibuja una región con el ratón...")
    cv2.imshow(fullscreen_title, dimmed_screen)
    cv2.waitKey(0)


















