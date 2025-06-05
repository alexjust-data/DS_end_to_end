# 📃 Bitácora del Sistema TSIS (Tracking System for Intelligent Scalping)

## 🔐 Objetivo General

Desarrollar una herramienta para traders profesionales que permita:

* Detectar patrones de operativa en pantalla (ATAS u otra)
* Registrar en tiempo real evidencias de entrada (pantalla, audio, video, anotaciones)
* Etiquetar cada operación con un sistema de puntuación Kaizen
* Crear datasets etiquetados para entrenamiento de modelos futuros

---

## 📅 Estado del desarrollo hasta el 5 de junio de 2025

### 1. ✅ Captura de región de pantalla seleccionada por el usuario

* Se activa un modo de pantalla completa oscurecida.
* El usuario dibuja un rectángulo para seleccionar la región de trading.
* La región se guarda en `config/region.json`
* La imagen recortada se guarda como `selected_region.png`

**Archivo clave:** `manual_region_selector.py`

### 2. 🎤 Grabación de audio al soltar el click del ratón

* Se inicia grabación con `sounddevice`
* Se guarda como `config/audio_temp.wav`

**Integrado dentro de:** `manual_region_selector.py`

### 3. 🎥 Grabación de video al soltar el click

* Se graba sólo la región seleccionada
* Usa `mss` y `cv2.VideoWriter`
* Duración: 5 segundos
* Se guarda como `config/video_temp.mov`

**Problemas solucionados:**

* Compatibilidad macOS: cambiamos a formato `.mov`
* Visualización en pantalla gris traslúcida implementada correctamente
* Soporte multimonitor con selección inicial por consola

### 4. 📐 Etiquetado Kaizen de las operaciones

* Formulario visual en Jupyter Notebook (`formulari.ipynb`)
* Dos formatos:

  * **Binario:** etiquetas booleanas (ej. "vela delta?")
  * **Puntuación Kaizen:** selectores -2, 0, +1, +2 según estrategia

**Archivos relacionados:**

* `label_entry_widgets.py`: interfaz interactiva
* `label_entry.py`: etiquetado plano
* `kayzen_scoring.py`: reglas de puntuación

---

## 🏦 Estructura de carpetas actual

```
DS_end_to_end-main/
├── capture_engine/
│   ├── manual_region_selector.py
│   ├── define_trading_region.py
│   ├── visual_platform_classifier.py
│   ├── main.py
│   └── main_from_selection.py
├── config/
│   ├── region.json
│   ├── audio_temp.wav
│   └── video_temp.mov
├── notebooks/
│   └── formulari.ipynb
├── data/
├── docs/
├── label_entry_widgets.py
├── label_entry.py
├── kayzen_scoring.py
├── requirements.txt
└── README.md
```

---

## ⏰ Flujo de uso actual (prototipo funcional)

1. Ejecutar `manual_region_selector.py`
2. Seleccionar región con el ratón
3. Al soltar el ratón:

   * Se guarda imagen
   * Se inicia grabación de audio y video
4. Ir a `notebooks/formulari.ipynb` para etiquetar la imagen

---

## 🚀 Siguientes pasos sugeridos (prioridad alta)

1. Asociar ID único a cada grabación y carpeta propia
2. Agregar transcripción de audio con `Whisper`
3. Mostrar score de probabilidad en pantalla (modelo a futuro)
4. Guardar todo en `training_data/{id}/`
5. Integrar backend API y dashboard

---

## 📷 Evidencias

* Captura pantalla completa gris OK
* Selección visual con rectángulo verde OK
* Grabación de video (solo región seleccionada) OK
* Grabación de audio OK
* Notebook de puntuación funcional OK

---

## 🧱 Recomendaciones para continuar mañana

* Ejecutar `manual_region_selector.py` para probar comportamiento
* Verificar que se guarden los archivos correctamente
* Revisar formulari.ipynb y su visualización
* Hacer un test de grabación completa (imagen + audio + video)
* Confirmar permisos de pantalla (macOS)

---

*Actualizado el 5 de junio de 2025 a las 19:00h por ChatGPT*


