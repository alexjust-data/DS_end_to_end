# label_entry.py
import json
from datetime import datetime
from pathlib import Path

# Configuración de carpetas
IMAGE_DIR = Path("data/images")
LABEL_DIR = Path("data/labels")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)
LABEL_DIR.mkdir(parents=True, exist_ok=True)

# Lista de criterios de la Estrategia 0 (puedes añadir más luego)
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

def pedir_etiquetas_manual() -> dict:
    etiquetas = {}
    for criterio in CRITERIOS:
        while True:
            respuesta = input(f"¿{criterio.replace('_', ' ').capitalize()}? [s/n]: ").strip().lower()
            if respuesta in ('s', 'n'):
                etiquetas[criterio] = True if respuesta == 's' else False
                break
            else:
                print("Por favor responde 's' o 'n'.")
    return etiquetas

def guardar_etiqueta_para(imagen: str, etiquetas: dict):
    nombre_base = Path(imagen).stem
    etiqueta_path = LABEL_DIR / f"{nombre_base}.json"
    with open(etiqueta_path, "w") as f:
        json.dump(etiquetas, f, indent=2)
    print(f"✅ Etiquetas guardadas en {etiqueta_path}")

if __name__ == "__main__":
    print("Etiquetado manual de imagen capturada")
    imagen = input("Nombre del archivo de imagen en 'data/images/' (sin extensión): ").strip()
    ruta_imagen = IMAGE_DIR / f"{imagen}.png"
    if not ruta_imagen.exists():
        print("❌ Imagen no encontrada.")
    else:
        etiquetas = pedir_etiquetas_manual()
        guardar_etiqueta_para(ruta_imagen.name, etiquetas)
