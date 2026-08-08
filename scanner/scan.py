"""Escaner de cruces de medias (7 / 50 / 200) para la bolsa espanola.

Uso:
    python -m scanner.scan --universo todos --salida docs/data
    python -m scanner.scan --universo ibex35 --timeframes 15m --resumen
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import sys
from typing import Dict, List, Optional, Tuple

from . import historico as hist
from . import indicators as ind
from . import providers
from .universe import Valor, universo

try:  # tzdata esta disponible en los runners de GitHub y en la mayoria de distros
    from zoneinfo import ZoneInfo

    MADRID = ZoneInfo("Europe/Madrid")
except Exception:  # pragma: no cover - respaldo minimo si falta la base de husos
    MADRID = dt.timezone(dt.timedelta(hours=2), "CEST")

PERIODOS = (7, 50, 200)
PARES: Tuple[Tuple[int, int], ...] = ((7, 50), (7, 200), (50, 200))

# interval/range de Yahoo por marco temporal. El rango debe dar de sobra para
# calcular una media de 200 periodos.
TIMEFRAMES: Dict[str, Dict[str, str]] = {
    "15m": {"interval": "15m", "range": "1mo", "label": "15 minutos"},
    "60m": {"interval": "60m", "range": "6mo", "label": "1 hora"},
    "1d": {"interval": "1d", "range": "2y", "label": "Diario"},
}


def _fecha_sesion(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, MADRID).date().isoformat()


def _iso(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, MADRID).isoformat()


def analizar(valor: Valor, velas: providers.Velas, timeframe: str) -> dict:
    """Calcula medias, cruces de la sesion y estado actual de un valor."""
    cierres = velas.closes
    medias = {p: ind.sma(cierres, p) for p in PERIODOS}

    fechas = [_fecha_sesion(ts) for ts in velas.timestamps]
    sesion = fechas[-1]
    # Primera vela de la ultima sesion: define la ventana "durante el dia".
    inicio_sesion = len(fechas) - 1
    while inicio_sesion > 0 and fechas[inicio_sesion - 1] == sesion:
        inicio_sesion -= 1

    # En diario cada vela es una sesion: el cruce "de hoy" es el de la ultima vela.
    desde = inicio_sesion if timeframe != "1d" else len(cierres) - 1

    detectados = []
    for rapido, lento in PARES:
        for cruce in ind.cruces(medias[rapido], medias[lento], rapido, lento, desde=desde):
            detectados.append(
                {
                    "pair": f"{rapido}x{lento}",
                    "fast": rapido,
                    "slow": lento,
                    "dir": cruce.direction,
                    "time": _iso(velas.timestamps[cruce.index]),
                    "price": round(cierres[cruce.index], 4),
                }
            )
    detectados.sort(key=lambda c: c["time"])

    # Variacion frente al cierre de la sesion anterior.
    previo: Optional[float] = cierres[inicio_sesion - 1] if inicio_sesion > 0 else None
    if timeframe == "1d":
        previo = cierres[-2] if len(cierres) >= 2 else None

    ultimo = cierres[-1]
    variacion = round((ultimo / previo - 1) * 100, 2) if previo else None

    actuales = {p: medias[p][-1] for p in PERIODOS}
    return {
        "symbol": valor.symbol,
        "name": valor.name,
        "index": valor.index,
        "price": round(ultimo, 4),
        "changePct": variacion,
        "sma": {str(p): (round(v, 4) if v is not None else None) for p, v in actuales.items()},
        "align": ind.alineacion(actuales[7], actuales[50], actuales[200]),
        "crosses": detectados,
        "gaps": {
            f"{r}x{l}": (
                round(g, 3) if (g := ind.separacion_pct(actuales[r], actuales[l])) is not None else None
            )
            for r, l in PARES
        },
        "session": sesion,
        "lastBar": _iso(velas.timestamps[-1]),
        "bars": len(cierres),
        "source": velas.source,
    }


def _descargar(valor: Valor, timeframe: str,
               historico_dir: Optional[str] = None) -> providers.Velas:
    """Yahoo primero; si rechaza la peticion, se recurre a los respaldos diarios.

    Yahoo responde 429 a las IP de centros de datos (por ejemplo los runners de
    GitHub), asi que en ese entorno solo funcionan los respaldos, que unicamente
    ofrecen velas diarias y de las ultimas semanas. Con `historico_dir` esas
    sesiones se acumulan en el repositorio y la serie deja de depender de lo que
    alcance a dar el proveedor en una sola peticion.
    """
    cfg = TIMEFRAMES[timeframe]
    descargadas: Optional[providers.Velas] = None
    fallo: Optional[providers.DataError] = None
    try:
        descargadas = providers.yahoo_chart(valor.symbol, cfg["interval"], cfg["range"])
    except providers.DataError as exc:
        fallo = exc
        if timeframe == "1d":
            for respaldo in (providers.stockanalysis_diario, providers.stooq_diario):
                try:
                    descargadas = respaldo(valor.symbol)
                    break
                except providers.DataError:
                    continue

    if timeframe != "1d" or not historico_dir:
        if descargadas is None:
            raise fallo or providers.DataError(f"{valor.symbol}: sin datos")
        return descargadas

    serie = hist.combinar(hist.cargar(historico_dir, valor.symbol), descargadas)
    if serie is None:
        raise fallo or providers.DataError(f"{valor.symbol}: sin datos")
    if descargadas is not None:
        hist.guardar(historico_dir, valor.symbol, serie)
    return serie


def escanear(valores: List[Valor], timeframe: str, *, workers: int = 6,
             historico_dir: Optional[str] = None) -> dict:
    """Escanea un universo completo en un marco temporal."""
    resultados: List[dict] = []
    errores: List[dict] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futuros = {pool.submit(_descargar, v, timeframe, historico_dir): v for v in valores}
        for futuro in concurrent.futures.as_completed(futuros):
            valor = futuros[futuro]
            try:
                velas = futuro.result()
                # Con menos velas que el periodo mayor todavia se pueden calcular
                # las medias cortas; las que no llegan quedan a null.
                if len(velas.closes) < min(PERIODOS) + 1:
                    raise providers.DataError(
                        f"solo {len(velas.closes)} velas, se necesitan {min(PERIODOS) + 1}"
                    )
                resultados.append(analizar(valor, velas, timeframe))
            except Exception as exc:  # un valor caido no debe tumbar el escaneo
                errores.append(
                    {"symbol": valor.symbol, "name": valor.name, "index": valor.index,
                     "error": str(exc)}
                )

    resultados.sort(key=lambda r: (-len(r["crosses"]), r["name"]))
    errores.sort(key=lambda e: e["name"])

    sesiones = [r["session"] for r in resultados]
    sesion = max(set(sesiones), key=sesiones.count) if sesiones else None

    fuentes = sorted({r["source"] for r in resultados})
    return {
        "timeframe": timeframe,
        "label": TIMEFRAMES[timeframe]["label"],
        "generatedAt": dt.datetime.now(MADRID).isoformat(timespec="seconds"),
        "session": sesion,
        "periods": list(PERIODOS),
        "count": len(resultados),
        "withCrosses": sum(1 for r in resultados if r["crosses"]),
        # Los respaldos solo dan unas 50 sesiones: sin historico para la media de 200.
        "missing200": sum(1 for r in resultados if r["sma"]["200"] is None),
        "sources": fuentes,
        "results": resultados,
        "errors": errores,
    }


def resumen_texto(datos: dict) -> str:
    lineas = [
        f"== {datos['label']} · sesion {datos['session']} · "
        f"{datos['withCrosses']}/{datos['count']} valores con cruce =="
    ]
    for r in datos["results"]:
        if not r["crosses"]:
            continue
        detalle = ", ".join(
            f"{c['pair']} {c['dir']} a las {c['time'][11:16]}" for c in r["crosses"]
        )
        lineas.append(f"  {r['symbol']:<9} {r['name']:<28} {detalle}")
    if datos["errors"]:
        lineas.append(f"  ({len(datos['errors'])} valores sin datos)")
    return "\n".join(lineas)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Cruces de medias 7/50/200 en la bolsa espanola")
    parser.add_argument("--universo", default="todos", choices=["ibex35", "continuo", "todos"])
    parser.add_argument("--timeframes", default="15m,60m,1d",
                        help="lista separada por comas: 15m,60m,1d")
    parser.add_argument("--salida", default="docs/data", help="directorio donde escribir el JSON")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--historico", default=None,
                        help="directorio donde acumular los cierres diarios (CSV por valor)")
    parser.add_argument("--resumen", action="store_true", help="imprime el resultado por consola")
    args = parser.parse_args(argv)

    valores = universo(args.universo)
    timeframes = [t.strip() for t in args.timeframes.split(",") if t.strip()]
    desconocidos = [t for t in timeframes if t not in TIMEFRAMES]
    if desconocidos:
        parser.error(f"timeframes desconocidos: {', '.join(desconocidos)}")

    os.makedirs(args.salida, exist_ok=True)
    indice = {
        "generatedAt": dt.datetime.now(MADRID).isoformat(timespec="seconds"),
        "universe": args.universo,
        "periods": list(PERIODOS),
        "timeframes": [],
    }

    for timeframe in timeframes:
        print(f"[scan] {timeframe}: {len(valores)} valores...", file=sys.stderr)
        datos = escanear(valores, timeframe, workers=args.workers,
                         historico_dir=args.historico)
        ruta = os.path.join(args.salida, f"{timeframe}.json")
        with open(ruta, "w", encoding="utf-8") as fh:
            json.dump(datos, fh, ensure_ascii=False, separators=(",", ":"))
        indice["timeframes"].append(
            {
                "id": timeframe,
                "label": datos["label"],
                "file": f"{timeframe}.json",
                "session": datos["session"],
                "generatedAt": datos["generatedAt"],
                "count": datos["count"],
                "withCrosses": datos["withCrosses"],
                "errors": len(datos["errors"]),
            }
        )
        if args.resumen:
            print(resumen_texto(datos))

    with open(os.path.join(args.salida, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(indice, fh, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
