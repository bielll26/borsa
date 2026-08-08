"""Sondeo temporal: localiza el endpoint de históricos completos."""

from __future__ import annotations

import re
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def traer(url, timeout=25, cabeceras=None):
    cab = {"User-Agent": UA, "Accept": "text/html,application/json,*/*"}
    cab.update(cabeceras or {})
    req = urllib.request.Request(url, headers=cab)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def pistas(nombre, url):
    print(f"\n===== {nombre}\n      {url}")
    try:
        estado, cuerpo = traer(url)
    except urllib.error.HTTPError as exc:
        print(f"      HTTP {exc.code}")
        return
    except Exception as exc:
        print(f"      FALLO {type(exc).__name__}: {exc}")
        return

    print(f"      HTTP {estado} · {len(cuerpo)} bytes")
    apis = sorted({m for m in re.findall(r'["\'/]((?:api|data)/[A-Za-z0-9_\-/{}$.]+)', cuerpo)})
    print(f"      rutas api ({len(apis)}): {apis[:25]}")
    descargas = sorted({m for m in re.findall(r'[\w/?=&.-]*(?:download|csv|export)[\w/?=&.-]*', cuerpo, re.I)})
    print(f"      descargas: {descargas[:12]}")
    rangos = sorted({m for m in re.findall(r'"(?:range|period|interval)":"?([\w]+)', cuerpo)})
    print(f"      rangos: {rangos[:15]}")


def probar(nombre, url, cabeceras=None):
    print(f"\n----- {nombre}\n      {url}")
    try:
        estado, cuerpo = traer(url, cabeceras=cabeceras)
        print(f"      HTTP {estado} · {len(cuerpo)} bytes · {cuerpo[:260]!r}")
    except urllib.error.HTTPError as exc:
        print(f"      HTTP {exc.code}: {exc.read()[:160].decode('utf-8', 'replace')!r}")
    except Exception as exc:
        print(f"      FALLO {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    pistas("stockanalysis histórico SAN", "https://stockanalysis.com/quote/bme/SAN/history/")

    cab_api = {"Referer": "https://stockanalysis.com/quote/bme/SAN/history/",
               "Accept": "application/json"}
    for ruta in [
        "https://stockanalysis.com/api/symbol/s/bme/SAN/history",
        "https://stockanalysis.com/api/quotes/s/bme/SAN",
        "https://stockanalysis.com/api/charts/s/bme/SAN/1Y",
        "https://stockanalysis.com/api/screener/s/f?m=marketCap&s=desc&c=s,n,price&cn=20&e=bme",
        "https://stockanalysis.com/quote/bme/SAN/history/?period=Daily&range=5Y&x=1",
    ]:
        probar(ruta.split("/")[-1] or ruta, ruta, cab_api)
