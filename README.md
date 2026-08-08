# Cruces de medias 7 · 50 · 200 — Bolsa española

Detecta, entre los 35 valores del IBEX 35 y el resto del Mercado Continuo, **en cuáles se ha
producido un cruce de las medias móviles de 7, 50 y 200 periodos durante la sesión**.

Se vigilan los tres pares posibles —**7 × 50**, **7 × 200** y **50 × 200**— en tres marcos
temporales (15 minutos, 1 hora y diario), distinguiendo cruce **alcista** (la media rápida
atraviesa hacia arriba a la lenta) y **bajista**.

## Cómo usarla

### 1. Web publicada

> **https://bielll26.github.io/borsa/**

El panel pide las cotizaciones a Yahoo Finance **desde tu propio navegador**, así que ves el
histórico completo y las velas intradía del momento sin instalar nada. La barra de progreso
muestra el avance mientras consulta los 85 valores.

Si tu navegador o tu red bloquean esa consulta, el panel cae automáticamente en los datos que
publica el robot del repositorio y te lo dice en un aviso.

### 2. En local, con datos del momento

```bash
python3 -m scanner.server        # abre http://localhost:8000
```

El servidor descarga las cotizaciones él mismo (caché de 60 s). Útil si prefieres que el
trabajo lo haga tu máquina y no el navegador.

### 3. Por consola

```bash
python3 -m scanner.scan --universo ibex35 --timeframes 15m --resumen
```

```
== 15 minutos · sesion 2026-08-07 · 3/35 valores con cruce ==
  SAB.MC    Banco Sabadell     7x50 alcista a las 10:15
  TEF.MC    Telefonica         7x200 bajista a las 12:45
```

Opciones: `--universo ibex35|continuo|todos`, `--timeframes 15m,60m,1d`, `--salida DIR`,
`--historico DIR`, `--workers N`.

No hace falta instalar dependencias: todo es biblioteca estándar de Python 3.9+.

## De dónde salen los datos

Yahoo Finance es la única fuente gratuita con histórico intradía de la bolsa española, pero
**responde `429 Too Many Requests` a las peticiones que salen de centros de datos**, incluidos
los runners de GitHub Actions (comprobado con `tools/diagnostico_proveedores.py`). De ahí el
reparto:

| Quién escanea | Fuente | Qué alcanza |
|---|---|---|
| Tu navegador, al abrir el panel | Yahoo Finance | Todo: 15 min, 1 hora y diario, con histórico para la media de 200 |
| `python3 -m scanner.server` en tu equipo | Yahoo Finance | Lo mismo, calculado en tu máquina |
| El robot de GitHub Actions | stockanalysis.com | Solo el cierre diario, unas 50 sesiones por petición |

Como 50 sesiones no bastan ni para un cruce de la media de 50 (hacen falta 51 velas, y 201
para la de 200), cada escaneo del robot **acumula los cierres en `datos/historico/`**. La serie
crece sola con cada sesión, y el panel publicado va detectando cada vez más cruces.

Ese histórico se puede rellenar de golpe desde un equipo donde Yahoo sí responda:

```bash
python3 -m scanner.scan --universo todos --timeframes 1d --historico datos/historico
git add datos/historico && git commit -m "Histórico inicial" && git push
```

Con eso la versión publicada pasa a tener dos años de cierres y las tres medias desde el
primer momento.

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
scanner/providers.py    Descarga de velas: Yahoo Finance y respaldos diarios
scanner/indicators.py   Medias móviles simples y detección de cruces
scanner/historico.py    Acumulación de cierres diarios en CSV por valor
scanner/scan.py         Orquestación y generación del JSON
scanner/server.py       Servidor local con escaneo en vivo
docs/                   Panel web: mercado.js escanea desde el navegador, app.js pinta
docs/universo.js        Copia del universo para el navegador (generada, no editar)
tools/                  Generador del universo y diagnóstico de proveedores
tests/                  Pruebas de medias, cruces, análisis por valor e histórico
```

```bash
python3 -m unittest discover -s tests -t .
python3 tools/generar_universo.py        # tras tocar scanner/universe.py
python3 tools/diagnostico_proveedores.py # si todo aparece como "sin datos"
```

`scanner/scan.py` y `docs/mercado.js` implementan el mismo cálculo por duplicado (uno para el
servidor, otro para el navegador). Sobre las mismas series producen resultados idénticos, hasta
la marca de tiempo de cada cruce.

## Detalles que conviene saber

- **Definición de cruce.** Se compara el signo de (media rápida − media lenta) vela a vela. Un
  cruce se confirma cuando ese signo se invierte respecto al último signo distinto de cero: un
  simple toque entre medias no cuenta si el precio vuelve por donde vino.
- **"Durante el día".** En 15 minutos y 1 hora se buscan los cruces en cualquier vela de la
  última sesión abierta (hora de Madrid). En diario, donde cada vela es una sesión completa, el
  cruce se busca en la vela de hoy.
- **Composición del IBEX 35.** Se revisa cada seis meses. La lista vive en `scanner/universe.py`
  y cualquier ticker que deje de dar datos aparece en el apartado «Sin datos» del panel.
- **Cotizaciones con retardo.** Herramienta de análisis técnico: **no es asesoramiento de
  inversión**.
