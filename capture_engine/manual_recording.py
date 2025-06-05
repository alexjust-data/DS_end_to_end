import cv2
import numpy as np
import mss
import json
import time
import threading
import queue
from datetime import datetime
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import subprocess

# Load region
config_path = Path("config/region.json")
if not config_path.exists():
    print("❌ No se encontró config/region.json. Ejecuta primero manual_region_selector.py")
    exit()

with open(config_path) as f:
    region = json.load(f)

# Globals
recording = False
video_writer = None
audio_q = queue.Queue()

# Setup session directory
session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
session_dir = Path(f"training_data/{session_id}")
session_dir.mkdir(parents=True, exist_ok=True)
video_path = session_dir / "video.mov"
audio_path = session_dir / "audio.wav"
transcript_path = session_dir / "transcription.txt"

# Save metadata
with open(session_dir / "metadata.json", "w") as f:
    json.dump({"timestamp": session_id, "region": region}, f, indent=4)

# Audio recording

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_q.put(indata.copy())

def record_audio():
    tmp_wav = session_dir / "temp_audio.wav"
    print("🎙️ Grabando audio...")
    try:
        with sf.SoundFile(tmp_wav, mode='w', samplerate=44100, channels=1) as file:
            with sd.InputStream(samplerate=44100, channels=1, callback=lambda indata, frames, time, status: file.write(indata.copy())):
                while recording:
                    sd.sleep(100)
        print(f"💾 Audio temporal guardado en {tmp_wav}")
    except Exception as e:
        print(f"❌ Error durante la grabación: {e}")
        return

    # Convertir a MP3 usando ffmpeg
    try:
        audio_mp3_path = session_dir / "audio.mp3"
        subprocess.run(["ffmpeg", "-y", "-i", str(tmp_wav), str(audio_mp3_path)], check=True)
        print(f"✅ Audio convertido a MP3 en {audio_mp3_path}")
        tmp_wav.unlink()  # Borra el archivo temporal WAV
    except Exception as e:
        print(f"❌ Error al convertir a MP3: {e}")


# Video capture

def start_video_recording():
    global video_writer
    print("🎥 Iniciando grabación de video...")
    left, top = region['left'], region['top']
    width, height = region['width'], region['height']
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video_writer = cv2.VideoWriter(str(video_path), fourcc, 10.0, (width, height))

    def capture_loop():
        with mss.mss() as sct:
            while recording:
                bbox = {"top": top, "left": left, "width": width, "height": height}
                img = sct.grab(bbox)
                frame = np.array(img)
                if frame.shape[2] == 4:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                video_writer.write(frame)
        video_writer.release()
        print(f"💾 Video guardado en {video_path}")

    threading.Thread(target=capture_loop, daemon=True).start()

# Create empty kaizen and emotion JSON files

def create_empty_jsons():
    kaizen_template = {
        "puntuaciones_kaizen": {
            "precision_entrada": None,
            "estructura_clara": None,
            "riesgo_controlado": None,
            "contexto_macro_apoyaba": None
        },
        "etiquetas_binarias": {
            "vela_delta": None,
            "absorcion_detectada": None,
            "fallo_de_maximos": None,
            "entrada_con_flujo": None
        },
        "emocion_detectada": None,
        "comentario_trader": "",
        "probabilidad_modelo_IA": None
    }

    emotion_template = {
        "antes": None,
        "durante": None,
        "despues": None
    }

    with open(session_dir / "kaizen.json", "w") as f:
        json.dump(kaizen_template, f, indent=4)

    with open(session_dir / "emotion.json", "w") as f:
        json.dump(emotion_template, f, indent=4)

    print("📄 JSONs kaizen.json y emotion.json creados.")

# Transcription with Whisper

def transcribe_audio():
    try:
        print("🧠 Transcribiendo audio con Whisper...")
        subprocess.run(["whisper", str(audio_path), "--language", "Spanish", "--output_dir", str(session_dir)], check=True)
        print("✅ Transcripción completada.")
        create_empty_jsons()
        subprocess.run(["env", f"TSIS_SESSION_PATH={session_dir}", "jupyter", "notebook", "notebooks/formulary.ipynb"])
    except Exception as e:
        print(f"⚠️ Error en transcripción: {e}")

# Main control loop

def main():
    global recording
    print("🖥️ Mostrando región en directo. Pulsa 'g' para grabar, 's' para parar, 'q' para salir.")
    left, top = region['left'], region['top']
    width, height = region['width'], region['height']

    with mss.mss() as sct:
        while True:
            bbox = {"top": top, "left": left, "width": width, "height": height}
            img = sct.grab(bbox)
            frame = np.array(img)
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            cv2.imshow("Live Trading Region", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('g') and not recording:
                recording = True
                threading.Thread(target=record_audio, daemon=True).start()
                start_video_recording()

            elif key == ord('s') and recording:
                recording = False
                time.sleep(1)
                transcribe_audio()

            elif key == ord('q'):
                if recording:
                    recording = False
                    time.sleep(1)
                    transcribe_audio()
                break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
