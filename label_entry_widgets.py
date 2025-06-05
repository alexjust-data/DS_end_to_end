
# label_entry_widgets.py

import json
from pathlib import Path
import ipywidgets as widgets
from IPython.display import display, clear_output
from datetime import datetime

# Carpetas
IMAGE_DIR = Path("data/images")
LABEL_DIR = Path("data/labels")
LABEL_DIR.mkdir(parents=True, exist_ok=True)

def dropdown_dict(preguntas_dict):
    return {
        k: widgets.HBox([
            widgets.Label(value=k, layout=widgets.Layout(width="400px")),
            widgets.Dropdown(options=v, layout=widgets.Layout(width="60px"))
        ])
        for k, v in preguntas_dict.items()
    }

# Rangos según Excel
PREGUNTAS_ESTRATEGIA_0 = {
    "¿Tenemos una banda de OFERTA y DEMANDA?": [-2, 0],
    "¿Camino LIBRE de OBSTÁCULOS (al menos en un 2:1)?": [-3, 0],
    "¿Tenemos stacked imbalance?": [0, 1],
    "¿Hay doble absorción?": [0, 2],
    "¿El precio ha tocado VWAP en el momento de la entrada?": [0, 1],
    "¿Hay absorción?": [0, 1],
    "¿Hay DIVERGENCIA en DELTA?": [0, 1],
    "¿Tenemos VELA REVERSAL (Blanca o Negra)?": [0, 1],
    "¿Hay imbalances de rechazo?": [0, 1],
    "¿Has hecho cierre parcial?": [-1, 1],
    "¿El CLÚSTER de la vela indica impulso?": [0, 1],
    "¿Tenemos zona en M1?": [0, 2],
    "¿Has respetado la hora de la estrategia?": [-2, 0],
    "BONUS: Banda generada con ABSORCIÓN + REVERSA + CVM impulso": [0, 3]
}

PREGUNTAS_ESTRATEGIA_2 = {
    "¿Más de 3 imbalances agrupados/Bigtrades/VWAP?": [-2, 1],
    "¿Están en zona de flip o extremo del hueco?": [-2, 1],
    "¿Tengo stacked en M1?": [0, 1],
    "¿Hueco coincide con perfil volumen?": [-2, 2],
    "¿Renko está OK?": [-2, 1],
    "¿M1 despejado de velas contrarias?": [-2, 0],
    "¿He comprobado los colores?": [0, 1],
    "¿Reacción de imbalances o absorción?": [-2, 0],
    "¿Hora/volatilidad/news?": [-1, 2],
    "¿He hecho cierre parcial?": [-1, 1],
    "¿Respetado mi cifra?": [-2, 2],
    "¿He entrado antes de la cuenta?": [-2, 0]
}

PREGUNTAS_INTRADIA = {
    "¿Toca zona de VAH / VAL?": [-3, 0],
    "¿Hay VOLUMEN VERTICAL relevante?": [-3, 0],
    "¿Hay ABSORCIÓN delta?": [-1, 2],
    "¿Vela AGOTAMIENTO, ESR?": [-1, 2],
    "¿Distancia a VWAP ≥ 2-3x SL?": [-1, 2],
    "¿TPO contrario, Single prints o Imbalances?": [0, 2],
    "¿Stop comprometido (>20 ticks)?": [-3, 1],
    "¿Máx órdenes diarias superado?": [-2, 1]
}

def lanzar_formulario():
    dropdowns_0 = dropdown_dict(PREGUNTAS_ESTRATEGIA_0)
    dropdowns_2 = dropdown_dict(PREGUNTAS_ESTRATEGIA_2)
    dropdowns_intra = dropdown_dict(PREGUNTAS_INTRADIA)

    guardar_btn = widgets.Button(description="Guardar etiquetas", button_style='success')
    salida = widgets.Output()

    def guardar_datos(b):
        etiquetas = {
            "estrategia_0": {k: int(w.children[1].value) for k, w in dropdowns_0.items()},
            "estrategia_2": {k: int(w.children[1].value) for k, w in dropdowns_2.items()},
            "intradia": {k: int(w.children[1].value) for k, w in dropdowns_intra.items()}
        }

        nombre = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(LABEL_DIR / f"{nombre}.json", "w") as f:
            json.dump(etiquetas, f, indent=2)

        with salida:
            clear_output()
            print(f"✔️ Etiquetas guardadas en {nombre}.json")

    guardar_btn.on_click(guardar_datos)

    display(widgets.HTML("<h3>🧠 Etiquetado Kayzen</h3>"))
    display(widgets.HTML("<b>Estrategia 0</b>"))
    display(*dropdowns_0.values())
    display(widgets.HTML("<b>Estrategia 2</b>"))
    display(*dropdowns_2.values())
    display(widgets.HTML("<b>Intradía</b>"))
    display(*dropdowns_intra.values())
    display(guardar_btn, salida)
