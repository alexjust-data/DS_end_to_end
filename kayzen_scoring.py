
# kayzen_scoring.py

def evaluar_estrategia_0(respuestas: dict) -> int:
    """Suma directamente los valores asignados a cada criterio de Estrategia 0."""
    total = sum(respuestas.values())
    return total

def evaluar_estrategia_2(respuestas: dict) -> int:
    """Suma directamente los valores asignados a cada criterio de Estrategia 2."""
    total = sum(respuestas.values())
    return total

def evaluar_intradia(respuestas: dict) -> int:
    """Suma directamente los valores asignados a cada criterio Intradía."""
    total = sum(respuestas.values())
    return total

def puntuar_trade_total(estrategia_0: dict, estrategia_2: dict, intradia: dict) -> int:
    """Devuelve la suma total de los tres bloques."""
    return (
        evaluar_estrategia_0(estrategia_0) +
        evaluar_estrategia_2(estrategia_2) +
        evaluar_intradia(intradia)
    )
