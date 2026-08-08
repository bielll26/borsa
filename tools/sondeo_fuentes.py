"""Sondeo temporal: explora la estructura de las fuentes que si responden."""

from __future__ import annotations

import html.parser
import re
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def traer(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/json,*/*",
        "Accept-Language": "es-ES,es;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


class Tablas(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tablas = []
        self._pila = []
        self._fila = None
        self._celda = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._pila.append({"id": a.get("id", ""), "class": a.get("class", ""), "filas": []})
        elif tag == "tr" and self._pila:
            self._fila = []
        elif tag in ("td", "th") and self._fila is not None:
            self._celda = []

    def handle_data(self, data):
        if self._celda is not None:
            self._celda.append(data.strip())

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._celda is not None:
            self._fila.append(" ".join(x for x in self._celda if x))
            self._celda = None
        elif tag == "tr" and self._fila is not None and self._pila:
            self._pila[-1]["filas"].append(self._fila)
            self._fila = None
        elif tag == "table" and self._pila:
            self.tablas.append(self._pila.pop())


def describir_tablas(nombre, url):
    print(f"\n===== {nombre} :: {url}")
    try:
        estado, cuerpo = traer(url)
    except urllib.error.HTTPError as exc:
        print(f"  HTTP {exc.code}")
        return None
    except Exception as exc:
        print(f"  FALLO {type(exc).__name__}: {exc}")
        return None

    print(f"  HTTP {estado} · {len(cuerpo)} bytes")
    p = Tablas()
    p.feed(cuerpo)
    for i, t in enumerate(p.tablas):
        filas = [f for f in t["filas"] if f]
        if len(filas) < 3:
            continue
        print(f"  tabla[{i}] id={t['id']!r} class={t['class']!r} filas={len(filas)}")
        for fila in filas[:3]:
            print(f"      {fila[:9]}")
    return cuerpo


def enlaces(cuerpo, patron, limite=6):
    if not cuerpo:
        return
    vistos = re.findall(r'href="([^"]*)"', cuerpo)
    coinciden = [h for h in vistos if re.search(patron, h, re.I)]
    print(f"  enlaces {patron}: {coinciden[:limite]}")


if __name__ == "__main__":
    cuerpo = describir_tablas(
        "BME IBEX 35 precios",
        "https://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESI100000000")
    enlaces(cuerpo, r"ISIN=")
    enlaces(cuerpo, r"hist|Hist")

    describir_tablas(
        "BME mercado continuo",
        "https://www.bolsamadrid.es/esp/aspx/Mercados/Precios.aspx?indice=ESIB00000000")

    cuerpo = describir_tablas(
        "BME info historica Santander",
        "https://www.bolsamadrid.es/esp/aspx/Empresas/InfHistorica.aspx?ISIN=ES0113900J37&ClvEmis=113900")
    enlaces(cuerpo, r"csv|excel|xls|Descarga")

    for nombre, url in [
        ("google finance SAN", "https://www.google.com/finance/quote/SAN:BME"),
        ("yahoo html es", "https://es.finance.yahoo.com/quote/SAN.MC/history"),
        ("stockanalysis v2", "https://stockanalysis.com/quote/bme/SAN/history/"),
        ("investing api", "https://api.investing.com/api/financialdata/historical/1150?start-date=2026-01-01&end-date=2026-08-08&time-frame=Daily"),
    ]:
        print(f"\n===== {nombre} :: {url}")
        try:
            estado, cuerpo = traer(url)
            print(f"  HTTP {estado} · {len(cuerpo)} bytes · {cuerpo[:200]!r}")
        except urllib.error.HTTPError as exc:
            print(f"  HTTP {exc.code}")
        except Exception as exc:
            print(f"  FALLO {type(exc).__name__}: {exc}")
