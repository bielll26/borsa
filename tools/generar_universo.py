"""Genera docs/universo.js a partir de scanner/universe.py.

    python3 tools/generar_universo.py

El panel necesita la lista de valores para poder escanear desde el navegador,
y esta es la unica copia: se genera, no se edita a mano.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from scanner.universe import TODOS  # noqa: E402

DESTINO = pathlib.Path(__file__).resolve().parent.parent / "docs" / "universo.js"


def render() -> str:
    filas = ",\n".join(
        f'  {{ s: "{v.symbol}", n: "{v.name}", i: "{v.index}" }}' for v in TODOS)
    return (
        "/* Generado por tools/generar_universo.py a partir de scanner/universe.py.\n"
        "   No editar a mano: se regenera. */\n"
        "window.UNIVERSO = [\n" + filas + "\n];\n"
    )


if __name__ == "__main__":
    DESTINO.write_text(render(), encoding="utf-8")
    print(f"{DESTINO} · {len(TODOS)} valores")
