"""Comprueba desde donde se ejecuta que los proveedores de datos responden.

    python3 tools/diagnostico_proveedores.py

Util cuando el panel aparece con todos los valores en "Sin datos": indica si el
problema es del proveedor, de la red o del ticker.
"""

from __future__ import annotations

import http.cookiejar
import json
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, ".")

from scanner.providers import USER_AGENT  # noqa: E402

TICKER = "SAN.MC"


def prueba(nombre, fn):
    try:
        resultado = fn()
        print(f"[OK]    {nombre}: {resultado}")
        return True
    except urllib.error.HTTPError as exc:
        cuerpo = exc.read()[:220].decode("utf-8", "replace").replace("\n", " ")
        print(f"[HTTP {exc.code}] {nombre}: {cuerpo}")
    except Exception as exc:
        print(f"[FALLO] {nombre}: {type(exc).__name__}: {exc}")
    return False


def _abrir(url, opener=None, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/json,text/csv,*/*",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    })
    abridor = opener.open if opener else urllib.request.urlopen
    with abridor(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def resumen_chart(cuerpo):
    datos = json.loads(cuerpo)
    resultado = (datos.get("chart", {}).get("result") or [{}])[0]
    cierres = ((resultado.get("indicators", {}).get("quote") or [{}])[0]).get("close") or []
    return f"{len(cierres)} velas"


def chart_simple(host, interval="1d", rango="1mo"):
    def fn():
        _, cuerpo = _abrir(
            f"https://{host}/v8/finance/chart/{TICKER}?interval={interval}&range={rango}")
        return resumen_chart(cuerpo)
    return fn


def chart_con_cookie(host, interval="15m", rango="1mo", con_crumb=False):
    def fn():
        tarro = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(tarro))
        try:
            _abrir("https://fc.yahoo.com/", opener)
        except urllib.error.HTTPError:
            pass  # devuelve 404 pero deja las cookies puestas
        sufijo = ""
        if con_crumb:
            _, crumb = _abrir("https://query2.finance.yahoo.com/v1/test/getcrumb", opener)
            sufijo = f"&crumb={urllib.parse.quote(crumb.decode())}"
        _, cuerpo = _abrir(
            f"https://{host}/v8/finance/chart/{TICKER}?interval={interval}&range={rango}{sufijo}",
            opener)
        return resumen_chart(cuerpo) + (f" (cookies: {len(tarro)})")
    return fn


def stooq():
    _, cuerpo = _abrir(f"https://stooq.com/q/d/l/?s={TICKER.split('.')[0].lower()}.es&i=d")
    lineas = cuerpo.decode("utf-8", "replace").strip().splitlines()
    return f"{len(lineas) - 1} filas · ultima: {lineas[-1] if len(lineas) > 1 else 'ninguna'}"


def main():
    print(f"Diagnostico de proveedores para {TICKER}\n")
    pruebas = [
        ("yahoo query1 diario", chart_simple("query1.finance.yahoo.com")),
        ("yahoo query2 diario", chart_simple("query2.finance.yahoo.com")),
        ("yahoo query1 15m", chart_simple("query1.finance.yahoo.com", "15m", "1mo")),
        ("yahoo query1 15m + cookie", chart_con_cookie("query1.finance.yahoo.com")),
        ("yahoo query2 15m + cookie + crumb",
         chart_con_cookie("query2.finance.yahoo.com", con_crumb=True)),
        ("stooq diario", stooq),
    ]
    resultados = [prueba(nombre, fn) for nombre, fn in pruebas]
    print(f"\n{sum(resultados)}/{len(resultados)} proveedores responden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
