# ✍️ Bitácora de Desarrollo - Proyecto Tsis.ai

> Documento de referencia para entender, retomar y continuar el proyecto sin perder contexto.

---

## 🔖 Objetivo del Proyecto

Crear una aplicación científica que:

1. Capture en tiempo real zonas de pantalla donde se ejecuta trading en la plataforma **ATAS**.
2. Detecte patrones visuales definidos por estrategias basadas en **Order Flow, Delta, Volumen Profile, TPO**, etc.
3. Permita etiquetar manualmente las capturas según criterios del sistema de puntuación **Kayzen**.
4. Prepare un dataset para entrenar un modelo que reconozca patrones automáticamente.
5. Visualice un **score en pantalla en tiempo real**, basado en la evaluación heurística o aprendizaje automático.

---

## 📂 Estructura general del proyecto

```
DS_end_to_end-main/
├── capture_engine/               # Scripts para captura, selección y clasificación visual
├── data/
│   ├── images/                   # Imágenes etiquetadas por fecha
│   ├── labels/                   # Archivos JSON con las etiquetas Kayzen
│   └── detected_events/         # Carpetas con capturas, audios y transcripciones
├── docs/                        # Documentación extendida
├── notebooks/                   # Formularios interactivos para etiquetado (Jupyter)
├── label_entry.py               # Etiquetado por terminal
├── label_entry_widgets.py       # Etiquetado visual en Jupyter
├── kayzen_scoring.py            # Reglas para puntuar trades según estrategia
├── image_labeling.py            # Guarda imagen + etiquetas automáticamente
├── live_scoring.py              # Análisis en tiempo real y score visual
├── video_recorder.py            # Grabación de pantalla al detectar patrón
├── audio_transcriber.py         # Grabación + transcripción con Whisper
└── config/region.json           # Región seleccionada por el usuario
```

---

## 🚦 Nuevo Módulo: Scoring en Tiempo Real

### 🎯 Objetivo

Mostrar un widget en pantalla con la puntuación en vivo (**Kayzen Score**), actualizada cada segundo mientras se analiza visualmente la zona de trading del usuario.

### 🧠 Lógica

* El sistema analiza la zona definida (capturada en `region.json`).
* Aplica una heurística o red entrenada (más adelante).
* Calcula un **score acumulado**.
* Muestra en tiempo real ese score.
* Si supera cierto umbral, se lanza la grabación y transcripción.

### 📌 Widgets flotantes

* Se mostrarán siempre (aunque el score esté en cero).
* Transparente, discreto, pero informativo.

---

## 📆 Flujo de trabajo cuando el sistema detecta patrón

1. El score sube progresivamente (hasta +10 por ejemplo).
2. Si supera el umbral (ej. +6.5):

   * Se guarda imagen
   * Se graba 1 minuto de audio y pantalla
   * Se transcribe el audio
   * Se guarda todo como evidencia de la entrada

```
data/detected_events/20250605_12-21-30/
├── image.png
├── audio.wav
├── transcript.txt
├── score.json
└── metadata.json
```

---

## ✅ Siguientes pasos inmediatos

1. Crear `live_scoring.py`:

   * Leer `config/region.json`
   * Mostrar score flotante siempre
   * Actualizar cada segundo

2. Crear widget flotante (`tkinter` o `PyQt`):

   * Score visible en pantalla
   * Ligero, sin foco de teclado o ratón

3. Definir lógica heurística temporal:

   * Ej: detección de color, número de barras, etc.
   * Evaluar reglas con `kayzen_scoring.py`

4. Activar grabación + transcripción si el score supera umbral:

   * Ejecutar `video_recorder.py`
   * Ejecutar `audio_transcriber.py`

---

## 🧰 A tener en cuenta

* El sistema debe poder ejecutarse en segundo plano sin interrumpir al trader.
* Todo debe guardarse automáticamente por fecha/hora.
* No se graba toda la sesión completa, solo fragmentos útiles.
* El score debe ser interpretable y modificable a posteriori.

---

## 🧪 Validación y checklist

* [ ] `live_scoring.py` muestra score visible (aunque sea 0)
* [ ] Se analiza la región seleccionada sin error
* [ ] El score se actualiza automáticamente
* [ ] Se lanza la grabación si hay patrón
* [ ] Se transcribe y guarda correctamente

---

## 🧠 Relevancia emocional

* El sistema permite incluir emociones y pensamientos del trader grabando su voz y transcribiendo lo que dice.
* Se usará para análisis cognitivo-conductual y mejora operativa futura.

---


