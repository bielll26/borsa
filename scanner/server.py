"""Servidor local: sirve el panel y permite escanear en vivo.

    python -m scanner.server              # http://localhost:8000
    python -m scanner.server --puerto 9000

A diferencia de la version publicada en GitHub Pages (que lee los JSON generados
por el robot cada 15 minutos), aqui cada peticion a /api/scan descarga cotizaciones
frescas, asi que los cruces se ven en el momento.
"""

from __future__ import annotations

import argparse
import http.server
import json
import os
import threading
import time
import urllib.parse
from typing import Dict, Tuple

from .scan import TIMEFRAMES, escanear
from .universe import universo

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
CACHE_SEGUNDOS = 60

_cache: Dict[Tuple[str, str], Tuple[float, dict]] = {}
_lock = threading.Lock()


def _escaneo_cacheado(universo_id: str, timeframe: str) -> dict:
    clave = (universo_id, timeframe)
    ahora = time.time()
    with _lock:
        entrada = _cache.get(clave)
        if entrada and ahora - entrada[0] < CACHE_SEGUNDOS:
            return entrada[1]

    datos = escanear(universo(universo_id), timeframe)
    with _lock:
        _cache[clave] = (time.time(), datos)
    return datos


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=RAIZ, **kwargs)

    def do_GET(self):  # noqa: N802 (nombre impuesto por la clase base)
        partes = urllib.parse.urlparse(self.path)
        if partes.path == "/api/scan":
            self._api_scan(urllib.parse.parse_qs(partes.query))
            return
        super().do_GET()

    def _api_scan(self, query: Dict[str, list]) -> None:
        timeframe = (query.get("tf") or ["15m"])[0]
        universo_id = (query.get("universo") or ["todos"])[0]

        if timeframe not in TIMEFRAMES:
            self._json({"error": f"timeframe desconocido: {timeframe}"}, 400)
            return
        try:
            datos = _escaneo_cacheado(universo_id, timeframe)
        except ValueError as exc:
            self._json({"error": str(exc)}, 400)
            return
        except Exception as exc:  # fallo de red hacia el proveedor
            self._json({"error": f"no se pudieron descargar datos: {exc}"}, 502)
            return
        self._json(datos, 200)

    def _json(self, payload: dict, status: int) -> None:
        cuerpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, formato: str, *args) -> None:
        if self.path.startswith("/api/"):
            super().log_message(formato, *args)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Panel local de cruces de medias")
    parser.add_argument("--puerto", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args(argv)

    servidor = http.server.ThreadingHTTPServer((args.host, args.puerto), Handler)
    print(f"Panel disponible en http://{args.host}:{args.puerto}  (Ctrl+C para salir)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nAdios.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
