"""Sondeo temporal: prueba fuentes de datos candidatas desde donde se ejecute."""

from __future__ import annotations

import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CANDIDATAS = [
    ("stooq csv diario .com", "https://stooq.com/q/d/l/?s=san.es&i=d"),
    ("stooq csv diario .pl", "https://stooq.pl/q/d/l/?s=san.es&i=d"),
    ("stooq csv diario mayus", "https://stooq.com/q/d/l/?s=SAN.ES&i=d"),
    ("stooq cotizacion", "https://stooq.com/q/l/?s=san.es&f=sd2t2ohlcv&h&e=csv"),
    ("stooq bulk diario es", "https://stooq.com/db/d/?b=d_es_txt"),
    ("stooq bulk 5min es", "https://stooq.com/db/d/?b=5_es_txt"),
    ("stockanalysis bme", "https://stockanalysis.com/api/symbol/bme/SAN/history?range=1Y&period=Daily"),
    ("stockanalysis quote", "https://stockanalysis.com/api/quotes/bme/SAN"),
    ("wsj csv", "https://www.wsj.com/market-data/quotes/ES/XMAD/SAN/historical-prices/download?MOD=mw_quote&startDate=01/01/2026&endDate=08/08/2026"),
    ("yahoo via jina", "https://r.jina.ai/https://query1.finance.yahoo.com/v8/finance/chart/SAN.MC?interval=1d&range=1mo"),
    ("twelvedata demo", "https://api.twelvedata.com/time_series?symbol=SAN&exchange=BME&interval=1day&outputsize=5&apikey=demo"),
    ("alphavantage demo", "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=SAN.MAD&apikey=demo"),
    ("investing scrape", "https://es.investing.com/equities/banco-santander-historical-data"),
    ("bolsamadrid", "https://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000"),
]


def sondear(nombre, url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            cuerpo = resp.read(1400)
            tipo = resp.headers.get("Content-Type", "?")
            largo = resp.headers.get("Content-Length", "?")
            muestra = cuerpo[:260].decode("utf-8", "replace").replace("\n", " | ")
            print(f"[{resp.status}] {nombre}\n      tipo={tipo} largo={largo}\n      {muestra}\n")
    except urllib.error.HTTPError as exc:
        muestra = exc.read()[:200].decode("utf-8", "replace").replace("\n", " ")
        print(f"[HTTP {exc.code}] {nombre}: {muestra}\n")
    except Exception as exc:
        print(f"[FALLO] {nombre}: {type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    for nombre, url in CANDIDATAS:
        sondear(nombre, url)
