"""Sondeo temporal: busca una fuente de históricos diarios usable desde los runners."""

from __future__ import annotations

import html.parser
import json
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
        if tag == "table":
            self._pila.append({"filas": []})
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


def mirar(nombre, url, mostrar_tablas=True, buscar=None):
    print(f"\n===== {nombre}\n      {url}")
    try:
        estado, cuerpo = traer(url)
    except urllib.error.HTTPError as exc:
        print(f"      HTTP {exc.code}: {exc.read()[:150].decode('utf-8', 'replace')}")
        return None
    except Exception as exc:
        print(f"      FALLO {type(exc).__name__}: {exc}")
        return None

    print(f"      HTTP {estado} · {len(cuerpo)} bytes")
    if mostrar_tablas:
        p = Tablas()
        p.feed(cuerpo)
        for i, t in enumerate(p.tablas):
            filas = [f for f in t["filas"] if f]
            if len(filas) < 5:
                continue
            print(f"      tabla[{i}] filas={len(filas)}")
            for fila in filas[:3]:
                print(f"          {fila[:8]}")
    if buscar:
        for patron in buscar:
            m = re.search(patron, cuerpo)
            print(f"      {patron!r} -> {cuerpo[m.start():m.start() + 220]!r}" if m else f"      {patron!r} -> no aparece")
    return cuerpo


if __name__ == "__main__":
    mirar("stockanalysis histórico SAN (BME)",
          "https://stockanalysis.com/quote/bme/SAN/history/")

    mirar("stockanalysis histórico SAN 5 años",
          "https://stockanalysis.com/quote/bme/SAN/history/?range=5Y&period=Daily")

    mirar("stockanalysis __data.json",
          "https://stockanalysis.com/quote/bme/SAN/history/__data.json?x-sveltekit-invalidated=001",
          mostrar_tablas=False, buscar=[r'"close"', r'"data"'])

    for ruta in ["api/charts/s/bme/SAN/max",
                 "api/charts/s/bme/SAN/1Y",
                 "api/symbol/b/bme/SAN/history"]:
        mirar(f"stockanalysis {ruta}", f"https://stockanalysis.com/{ruta}",
              mostrar_tablas=False, buscar=[r'\['])

    mirar("stockanalysis valor pequeño (LGT)",
          "https://stockanalysis.com/quote/bme/LGT/history/")

    mirar("stockanalysis listado BME",
          "https://stockanalysis.com/quote/bme/", mostrar_tablas=True)
