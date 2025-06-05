## 🎯 Tu intención: grabación controlada, zona fija, IA emocional

- El trader selecciona **una vez** la región (p. ej. la zona de ATAS con Order Flow).
- A partir de ahí, el sistema **vigila siempre esa zona**.
- El trader decide **cuándo grabar** (con botón o tecla).

### Se graba:
- 📹 Vídeo de lo que pasa en pantalla
- 🎤 Audio de lo que piensa/dice el trader

### El sistema:
- 📝 Transcribe lo que el trader dice (`transcription.txt`)
- 🧠 Clasifica su estado emocional (duda, euforia, confianza) → `emotion.json`
- 🗂️ Guarda todo en `training_data/ID/` con sus `json` listos para entrenar un modelo.

---

## ❌ Problemas actuales del sistema

- Siempre obliga a **reseleccionar la región** → esto **no es realista**.
- Graba automáticamente **5 segundos** y luego se detiene sola.
- El trader **no puede controlar** cuándo parar.
- No se transcribe ni se analiza emocionalmente el audio (aún).

---

## ✅ Qué hay que cambiar (resumen técnico)

### 1. Selección de región una vez
- Guardar la región seleccionada en `config/region.json`.
- En futuras sesiones, **no volver a seleccionar**.

### 2. Script de grabación manual
- Script que muestra la zona seleccionada en directo.
- El trader pulsa una tecla (`g` para grabar / `s` para parar).
- Mientras graba: **vídeo y audio en paralelo**.
- Al parar: se guarda todo.

### 3. Crear JSONs
- `metadata.json`: tiempo, región, ID
- `kaizen.json`: emociones, nota, resumen
- `transcription.txt`: texto del audio grabado
- `emotion.json`: etiquetas como “confianza”, “duda”, “ansiedad”

---

## 🧠 ¿Y la IA?

### Más adelante:
- Transcribes con **Whisper**
- Detectas emociones con un **clasificador NLP** (emociones del trader)
- El modelo entrenado usa **imágenes + texto** para predecir:
    - Si es un **buen momento de entrada**
    - El **estado mental del trader** antes/durante/después

---

### ✅ ¿Quieres que te cree ahora un nuevo script llamado `manual_recording.py` que:
- Usa la región guardada
- Muestra la pantalla en directo
- Permite iniciar/parar grabación con teclas
- Guarda vídeo/audio/transcripción automáticamente?