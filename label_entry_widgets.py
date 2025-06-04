# label_entry_widgets.py
import json
from pathlib import Path
import ipywidgets as widgets
from IPython.display import display, clear_output

# Carpetas
IMAGE_DIR = Path("data/images")
LABEL_DIR = Path("data/labels")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LABEL_DIR.mkdir(parents=True, exist_ok=True)

# Criterios Kayzen
CRITERIOS = [
    "banda_oferta_demanda",
    "stacked_imbalance",
    "doble_absorcion",
    "absorcion_en_cima",
    "rotura_hacia_nivel",
    "en_zona_de_rechazo",
    "divergencia_en_delta",
    "delta_reversal",
    "cambio_de_color",
    "velas_dentro",
    "recupera_nivel",
    "microtrampolin",
    "respeta_hora_estrategia",
    "bonus_absorcion_reversal",
]

# Crear widgets
nombre_input = widgets.Text(description="Nombre", placeholder="20250604_204532")
checkboxes = {c: widgets.Checkbox(description=c.replace('_', ' ').capitalize()) for c in CRITERIOS}
boton = widgets.Button(description="Guardar etiqueta", button_style="success")
salida = widgets.Output()

def guardar_etiqueta_widgets(_):
    etiquetas = {criterio: cb.value for criterio, cb in checkboxes.items()}
    nombre_base = nombre_input.value.strip()
    if not nombre_base:
        with salida:
            clear_output()
            print("⚠️ Debes ingresar un nombre de imagen.")
        return
    etiqueta_path = LABEL_DIR / f"{nombre_base}.json"
    with open(etiqueta_path, "w") as f:
        json.dump(etiquetas, f, indent=2)
    with salida:
        clear_output()
        print(f"✅ Etiquetas guardadas en: {etiqueta_path}")

boton.on_click(guardar_etiqueta_widgets)

def lanzar_formulario():
    display(nombre_input)
    for cb in checkboxes.values():
        display(cb)
    display(boton)
    display(salida)
