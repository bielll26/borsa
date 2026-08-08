"""Historico diario acumulado en el repositorio.

La fuente de respaldo (la que funciona desde los runners de GitHub) solo devuelve
unas 50 sesiones, y para un cruce de la media de 50 hacen falta 51, mientras que
la de 200 necesita 201. Guardando cada escaneo en un CSV por valor, la serie
crece sola y el panel publicado va detectando cada vez mas cruces.

Un escaneo hecho desde una conexion domestica (donde Yahoo si responde) rellena
estos ficheros con dos anos de golpe: basta ejecutarlo una vez.
"""

from __future__ import annotations

import calendar
import csv
import datetime as dt
import os
from typing import Dict, Optional, Tuple

from .providers import Velas

CABECERA = ("fecha", "cierre")


def ruta(directorio: str, symbol: str) -> str:
    return os.path.join(directorio, f"{symbol.replace('/', '_')}.csv")


def _fecha_de(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).date().isoformat()


def _ts_de(fecha: str) -> int:
    y, m, d = (int(p) for p in fecha.split("-"))
    return calendar.timegm((y, m, d, 12, 0, 0, 0, 0, 0))


def cargar(directorio: str, symbol: str) -> Optional[Velas]:
    """Lee el historico guardado de un valor, o None si aun no existe."""
    camino = ruta(directorio, symbol)
    if not os.path.exists(camino):
        return None

    timestamps, cierres = [], []
    with open(camino, newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            try:
                cierre = float(fila["cierre"])
                ts = _ts_de(fila["fecha"])
            except (KeyError, ValueError, TypeError):
                continue
            timestamps.append(ts)
            cierres.append(cierre)

    if not cierres:
        return None
    return Velas(timestamps, cierres, "historico")


def combinar(previas: Optional[Velas], nuevas: Optional[Velas]) -> Optional[Velas]:
    """Une dos series diarias por fecha de sesion; ante empate manda la nueva.

    Las fuentes fechan la vela diaria a horas distintas (Yahoo en la apertura,
    el respaldo a mediodia), asi que la clave es el dia, no la marca de tiempo.
    """
    por_fecha: Dict[str, Tuple[int, float]] = {}
    for serie in (previas, nuevas):
        if not serie:
            continue
        for ts, cierre in zip(serie.timestamps, serie.closes):
            por_fecha[_fecha_de(ts)] = (ts, cierre)

    if not por_fecha:
        return None

    ordenadas = [por_fecha[f] for f in sorted(por_fecha)]
    fuente = (nuevas or previas).source
    return Velas([ts for ts, _ in ordenadas], [c for _, c in ordenadas], fuente)


def guardar(directorio: str, symbol: str, velas: Velas) -> int:
    """Escribe la serie completa y devuelve cuantas sesiones han quedado."""
    os.makedirs(directorio, exist_ok=True)
    with open(ruta(directorio, symbol), "w", newline="", encoding="utf-8") as fh:
        escritor = csv.writer(fh)
        escritor.writerow(CABECERA)
        for ts, cierre in zip(velas.timestamps, velas.closes):
            escritor.writerow([_fecha_de(ts), f"{cierre:.4f}"])
    return len(velas.closes)
