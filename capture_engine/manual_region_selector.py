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
from datetime import datetime


region = {}
drawing = False
ix, iy = -1, -1
recording = False
audio_q = queue.Queue()

fullscreen_title = "Select Region"


def choose_monitor(monitors):
    print("\n🖥️ Monitores detectados:")
    for i, m in enumerate(monitors[1:], start=1):
        print(f"Monitor {i}: {m['width']}x{m['height']} @ ({m['left']}, {m['top']})")
    choice = input("\nSelecciona el número del monitor a capturar (0 = Todos): ")
    try:
        idx = int(choice)
        return monitors[idx] if 0 <= idx < len(monitors) else monitors[1]
    except ValueError:
        return monitors[1]


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

        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = Path(f"training_data/{session_id}")
        session_dir.mkdir(parents=True, exist_ok=True)

        with open(session_dir / "region.json", "w") as f:
            json.dump(region, f)
        print(f"\n✅ Región guardada en {session_dir / 'region.json'}: {region}")

        selected = original_screen[y0:y1, x0:x1]
        cv2.imwrite(str(session_dir / "screenshot.png"), selected)

        recording = True
        start_audio_recording(session_dir / "audio.mp3")
        record_video(region, monitor, session_dir / "video.mov")

        with open(session_dir / "metadata.json", "w") as f:
            json.dump({"timestamp": session_id, "region": region}, f, indent=4)

        recording = False
        cv2.destroyAllWindows()


def audio_callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    audio_q.put(indata.copy())


def start_audio_recording(filename_mp3, samplerate=44100, channels=1):
    import tempfile
    import subprocess
    import os

    wav_temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name

    def record():
        global recording
        with sf.SoundFile(wav_temp, mode='w', samplerate=samplerate, channels=channels) as file:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=audio_callback):
                print("🎙️ Grabando audio...")
                while recording:
                    file.write(audio_q.get())
        print(f"💾 Audio temporal guardado en {wav_temp}")

        # Convertir a MP3
        result = subprocess.run(["ffmpeg", "-y", "-i", wav_temp, filename_mp3], capture_output=True)
        if result.returncode == 0:
            print(f"✅ Audio convertido a MP3 en {filename_mp3}")
            os.remove(wav_temp)
        else:
            print("❌ Error al convertir audio a MP3:", result.stderr.decode())

    threading.Thread(target=record, daemon=True).start()




def record_video(region, monitor, video_path, duration=5):
    # está correctamente ordenada, pero si algún día decides grabar 
    # audio/vídeo más largos o separados, 
    # considera sincronizar la duración, o añadir un thread.join() 
    # también en el audio si necesitas esperarlo.
    # recording = True
    # start_audio_recording(session_dir / "audio.mp3")
    # record_video(region, monitor, session_dir / "video.mov")

    global recording  # Asegúrate de acceder a la variable global


    left = region["left"] + monitor["left"]
    top = region["top"] + monitor["top"]
    width = region["width"]
    height = region["height"]

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(str(video_path), fourcc, 10.0, (width, height))

    print(f"🎥 Grabando video en coordenadas absolutas: {left},{top},{width},{height} ...")

    def capture_loop():
        with mss.mss() as sct:
            start_time = time.time()
            while time.time() - start_time < duration:
                bbox = {"top": int(top), "left": int(left), "width": int(width), "height": int(height)}
                img = sct.grab(bbox)
                frame = np.array(img)
                if frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
        out.release()
        print(f"💾 Video guardado en {video_path}")

    # Inicia en hilo independiente para evitar bloqueo
    thread = threading.Thread(target=capture_loop, daemon=True)
    thread.start()
    thread.join()  # Espera a que acabe antes de seguir



if __name__ == "__main__":
    original_screen, monitor = capture_full_screen()
    dim_overlay = np.full_like(original_screen, (30, 30, 30))
    alpha = 0.7
    dimmed_screen = cv2.addWeighted(original_screen, 1 - alpha, dim_overlay, alpha, 0)

    cv2.namedWindow(fullscreen_title, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(fullscreen_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback(fullscreen_title, draw_rectangle)

    print("🖱️ Dibuja una región con el ratón...")
    cv2.imshow(fullscreen_title, dimmed_screen)
    cv2.waitKey(0)



















