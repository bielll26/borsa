# Cruces de medias 7 · 50 · 200 — Bolsa española

Detecta, entre los 35 valores del IBEX 35 y el resto del Mercado Continuo, **en cuáles se ha
producido un cruce de las medias móviles de 7, 50 y 200 periodos durante la sesión**.

Se vigilan los tres pares posibles: **7 × 50**, **7 × 200** y **50 × 200**, en tres marcos
temporales (15 minutos, 1 hora y diario), distinguiendo cruce **alcista** (la media rápida
atraviesa hacia arriba a la lenta) y **bajista**.

## Cómo usarla

### 1. Web publicada (sin instalar nada)

El panel se publica en GitHub Pages y un robot lo actualiza cada 15 minutos mientras la bolsa
está abierta:

> **https://bielll26.github.io/borsa/**

Para activarlo la primera vez: **Settings → Pages → Build and deployment → Source: _GitHub
Actions_**. A partir de ahí el flujo `.github/workflows/escaneo.yml` escanea y publica solo.

### 2. En local, con datos del momento

```bash
python3 -m scanner.server        # abre http://localhost:8000
```

El servidor local descarga cotizaciones frescas en cada petición (caché de 60 s), así que los
cruces se ven en el momento en lugar de con el retardo del robot.

### 3. Por consola

```bash
python3 -m scanner.scan --universo ibex35 --timeframes 15m --salida docs/data --resumen
```

```
== 15 minutos · sesion 2026-08-07 · 3/35 valores con cruce ==
  SAB.MC    Banco Sabadell     7x50 alcista a las 10:15
  TEF.MC    Telefonica         7x200 bajista a las 12:45
```

Opciones: `--universo ibex35|continuo|todos`, `--timeframes 15m,60m,1d`, `--workers N`.

No hace falta instalar dependencias: todo es biblioteca estándar de Python 3.9+.

## Qué muestra el panel

- **Cruces de la sesión** — una tarjeta por valor, con el par cruzado, la dirección y la hora
  exacta de la vela en la que se confirmó.
- **A punto de cruzar** — valores con las medias a menos de un 0,5 %, candidatos a cruzar en
  las próximas velas.
- **Todos los valores** — tabla ordenable con último precio, variación, las tres medias y la
  alineación de la tendencia (alcista si 7 > 50 > 200).
- **Sin datos** — tickers que el proveedor no devuelve, normalmente por exclusión de cotización
  o por un cambio de composición del índice.

Filtros por mercado, marco temporal, par de medias, dirección y búsqueda por nombre o ticker.

## Estructura

```
scanner/universe.py     Tickers del IBEX 35 y del Mercado Continuo (editable)
scanner/providers.py    Descarga de velas (Yahoo Finance, con respaldo en Stooq para diario)
scanner/indicators.py   Medias móviles simples y detección de cruces
scanner/scan.py         Orquestación y generación del JSON
scanner/server.py       Servidor local con escaneo en vivo
docs/                   Panel web estático que consume docs/data/*.json
tests/                  Pruebas de las medias, los cruces y el análisis por valor
```

```bash
python3 -m unittest discover -s tests -t .
```

## Detalles que conviene saber

- **Definición de cruce.** Se compara el signo de (media rápida − media lenta) vela a vela. Un
  cruce se confirma cuando ese signo se invierte respecto al último signo distinto de cero: un
  simple toque entre medias no cuenta si el precio vuelve por donde vino.
- **"Durante el día".** En 15 minutos y 1 hora se buscan los cruces en cualquier vela de la
  última sesión abierta (hora de Madrid). En diario, donde cada vela es una sesión completa, el
  cruce se busca en la vela de hoy.
- **Composición del IBEX 35.** Se revisa cada seis meses. La lista vive en `scanner/universe.py`
  y cualquier ticker que deje de dar datos aparece en el apartado «Sin datos» del panel.
- **Datos.** Yahoo Finance, con retardo respecto al mercado. Herramienta de análisis técnico:
  **no es asesoramiento de inversión**.
