# ✍️ Bitácora de Desarrollo - Proyecto Tsis.ai

> Documento de referencia para entender, retomar y continuar el proyecto sin perder contexto.

---

## 🔖 Objetivo del Proyecto

Crear una aplicación científica que:

1. Capture en tiempo real zonas de pantalla donde se ejecuta trading en la plataforma **ATAS**.
2. Detecte patrones visuales definidos por estrategias basadas en **Order Flow, Delta, Volumen Profile, TPO**, etc.
3. Permita etiquetar manualmente las capturas según criterios del sistema de puntuación **Kayzen**.
4. Prepare un dataset para entrenar un modelo que reconozca patrones automáticamente.

---

## 📂 Estructura general del proyecto

```
DS_end_to_end-main/
├── capture_engine/               # Scripts para captura, selección y clasificación visual
├── data/
│   ├── images/                   # Imágenes etiquetadas por fecha
│   └── labels/                   # Archivos JSON con las etiquetas Kayzen
├── docs/                        # Documentación extendida
├── notebooks/                   # Formularios interactivos para etiquetado (Jupyter)
├── label_entry.py               # Etiquetado por terminal
├── label_entry_widgets.py       # Etiquetado visual en Jupyter
├── kayzen_scoring.py            # Reglas para puntuar trades según estrategia
└── image_labeling.py            # Guarda imagen + etiquetas automáticamente
```

---

## 🎨 Captura y selección de zona de trading

### Paso 1. Definir zona de captura:

```bash
python capture_engine/define_trading_region.py
```

* Se abre pantalla completa.
* Se dibuja una región con el ratón.
* Se confirma con `c`, resetea con `r`, sale con `ESC`.
* Se guarda:

  * Zona en `config/region.json`
  * Imagen en `data/images/selected_region.png`

### Paso 2. Capturar en vivo esa región:

```bash
python capture_engine/main_from_selection.py
```

* Muestra en tiempo real solo la zona marcada.
* Usado para debug y futuro reconocimiento visual.

---

## 📅 Sistema de puntuación Kayzen (manual)

### Archivos clave:

* `kayzen_scoring.py`: contiene las funciones `evaluar_estrategia_0`, `evaluar_estrategia_2` e `intradia`.
* Entrada: diccionarios con respuestas booleanas
* Salida: puntuación entera total

### Ejemplo de uso:

```python
from kayzen_scoring import puntuar_trade_total

res_estr0 = {...}
res_estr2 = {...}
res_intradia = {...}

puntos = puntuar_trade_total(res_estr0, res_estr2, res_intradia)
```

---

## 📁 Etiquetado de capturas

### 1. Desde terminal:

```bash
python label_entry.py
```

* Pide nombre de imagen (sin `.png`)
* Pregunta uno a uno los criterios
* Guarda JSON en `data/labels/`

### 2. Desde Jupyter:

```python
from label_entry_widgets import lanzar_formulario
lanzar_formulario()
```

* Formulario visual con casillas de verificación
* Guarda archivo de etiquetas en `data/labels/`

---

## 📚 Dataset para entrenamiento

### Imagen y etiqueta deben tener el mismo nombre base:

```
data/images/20250604_204532.png
           └────────────────────────────────────────────────────

             data/labels/20250604_204532.json
```

Estos pares están listos para ser cargados por cualquier modelo de clasificación visual.

---

## 🧰 Pendiente para el futuro

* Entrenamiento de modelo CNN o clasificador visual con etiquetas Kayzen.
* Sistema automático que reconozca en vivo la puntuación y envíe alerta.
* Dashboard para visualizar capturas, etiquetas, puntuaciones y logs.

---

## 🚫 Problemas comunes y soluciones

| Problema                                   | Solución                                                             |
| ------------------------------------------ | -------------------------------------------------------------------- |
| La ventana de selección se ve gris y vacía | Ejecutar desde terminal del sistema, no desde VSCode                 |
| No se abre imagen al seleccionar región    | Asegurarse de tener permisos en `Privacidad > Grabación de pantalla` |
| `ModuleNotFoundError: ipywidgets`          | Ejecutar `pip install ipywidgets` dentro del entorno virtual         |
| Imagen y etiqueta no se corresponden       | Verificar que tengan el mismo nombre base (sin extensión)            |


