"""Descarga de velas historicas. Solo biblioteca estandar."""

from __future__ import annotations

import calendar
import csv
import html.parser
import io
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import List, NamedTuple, Optional

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

_YAHOO_HOSTS = ("query1.finance.yahoo.com", "query2.finance.yahoo.com")


class Velas(NamedTuple):
    timestamps: List[int]  # epoch en segundos (UTC)
    closes: List[float]
    source: str


class DataError(RuntimeError):
    """No se han podido obtener datos para un ticker."""


def _get(url: str, timeout: float) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json,text/csv,*/*",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def yahoo_chart(symbol: str, interval: str, range_: str, *, timeout: float = 20.0,
                intentos: int = 3) -> Velas:
    """Descarga velas de la API publica de graficos de Yahoo Finance."""
    ultimo_error: Optional[Exception] = None

    for intento in range(intentos):
        host = _YAHOO_HOSTS[intento % len(_YAHOO_HOSTS)]
        url = (
            f"https://{host}/v8/finance/chart/{urllib.parse.quote(symbol)}"
            f"?interval={interval}&range={range_}&includePrePost=false"
        )
        try:
            payload = json.loads(_get(url, timeout))
            return _parse_yahoo(payload, symbol)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, DataError) as exc:
            ultimo_error = exc
            if intento < intentos - 1:
                time.sleep((2 ** intento) + random.random())

    raise DataError(f"{symbol}: {ultimo_error}")


def _parse_yahoo(payload: dict, symbol: str) -> Velas:
    chart = payload.get("chart") or {}
    if chart.get("error"):
        raise DataError(f"{symbol}: {chart['error'].get('description', chart['error'])}")

    resultados = chart.get("result") or []
    if not resultados:
        raise DataError(f"{symbol}: respuesta sin resultados")

    result = resultados[0]
    timestamps = result.get("timestamp") or []
    quotes = (result.get("indicators") or {}).get("quote") or [{}]
    closes = quotes[0].get("close") or []

    ts_limpios: List[int] = []
    cierres: List[float] = []
    for ts, close in zip(timestamps, closes):
        if close is None:
            continue  # vela sin negociacion (subasta, festivo parcial)
        ts_limpios.append(int(ts))
        cierres.append(float(close))

    if not cierres:
        raise DataError(f"{symbol}: sin cierres validos")
    return Velas(ts_limpios, cierres, "yahoo")


_MESES = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), start=1)}


class _TablaHistorico(html.parser.HTMLParser):
    """Extrae la primera tabla con cabecera Date/Open/High/Low/Close."""

    def __init__(self) -> None:
        super().__init__()
        self.filas: List[List[str]] = []
        self._fila: Optional[List[str]] = None
        self._celda: Optional[List[str]] = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._fila = []
        elif tag in ("td", "th") and self._fila is not None:
            self._celda = []

    def handle_data(self, data):
        if self._celda is not None:
            self._celda.append(data.strip())

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._celda is not None:
            self._fila.append(" ".join(t for t in self._celda if t))
            self._celda = None
        elif tag == "tr" and self._fila:
            self.filas.append(self._fila)
            self._fila = None


def stockanalysis_diario(symbol: str, *, timeout: float = 25.0) -> Velas:
    """Cierres diarios de stockanalysis.com.

    Es la fuente de respaldo cuando Yahoo rechaza la peticion (los centros de
    datos reciben 429). Devuelve alrededor de 50 sesiones, suficientes para las
    medias de 7 y 50 pero no para la de 200.
    """
    base = symbol.split(".")[0].upper()
    url = f"https://stockanalysis.com/quote/bme/{urllib.parse.quote(base)}/history/"
    try:
        html_crudo = _get(url, timeout).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise DataError(f"{symbol}: stockanalysis {exc}") from exc

    parser = _TablaHistorico()
    parser.feed(html_crudo)

    cabecera_vista = False
    filas: List[tuple] = []
    for fila in parser.filas:
        if not cabecera_vista:
            cabecera_vista = fila[:2] == ["Date", "Open"]
            continue
        if len(fila) < 5:
            continue
        fecha, cierre = _fecha_en(fila[0]), _decimal(fila[4])
        if fecha is None or cierre is None:
            continue
        filas.append((fecha, cierre))

    if not filas:
        raise DataError(f"{symbol}: stockanalysis sin filas de cotizacion")

    filas.sort()  # la web las lista de mas reciente a mas antigua
    return Velas([f for f, _ in filas], [c for _, c in filas], "stockanalysis")


def _fecha_en(texto: str) -> Optional[int]:
    """Convierte 'Aug 7, 2026' en epoch a las 12:00 UTC de esa sesion."""
    partes = texto.replace(",", " ").split()
    if len(partes) != 3 or partes[0] not in _MESES:
        return None
    try:
        return calendar.timegm((int(partes[2]), _MESES[partes[0]], int(partes[1]), 12, 0, 0, 0, 0, 0))
    except ValueError:
        return None


def _decimal(texto: str) -> Optional[float]:
    try:
        return float(texto.replace(",", ""))
    except ValueError:
        return None


def stooq_diario(symbol: str, *, timeout: float = 20.0) -> Velas:
    """Respaldo para velas diarias: CSV publico de Stooq (solo timeframe diario)."""
    base = symbol.split(".")[0].lower()
    url = f"https://stooq.com/q/d/l/?s={base}.es&i=d"
    try:
        texto = _get(url, timeout).decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise DataError(f"{symbol}: stooq {exc}") from exc

    filas = list(csv.DictReader(io.StringIO(texto)))
    ts: List[int] = []
    cierres: List[float] = []
    for fila in filas:
        fecha, close = fila.get("Date"), fila.get("Close")
        if not fecha or not close or close == "N/A":
            continue
        try:
            y, m, d = (int(p) for p in fecha.split("-"))
            cierres.append(float(close))
        except ValueError:
            continue
        # 12:00 UTC: cae dentro de la sesion en cualquier huso europeo.
        ts.append(calendar.timegm((y, m, d, 12, 0, 0, 0, 0, 0)))

    if not cierres:
        raise DataError(f"{symbol}: stooq sin datos")
    return Velas(ts, cierres, "stooq")
