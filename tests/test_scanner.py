"""Pruebas del calculo de medias y de la deteccion de cruces.

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import calendar
import datetime as dt
import pathlib
import shutil
import sys
import tempfile
import unittest

from scanner import historico as hist
from scanner import indicators as ind
from scanner import providers
from scanner.scan import MADRID, analizar
from scanner.universe import IBEX35, TODOS
from scanner.universe import Valor


class TestSMA(unittest.TestCase):
    def test_periodos_iniciales_sin_valor(self):
        self.assertEqual(ind.sma([1, 2, 3], 3), [None, None, 2.0])

    def test_ventana_movil(self):
        self.assertEqual(ind.sma([2, 4, 6, 8], 2), [None, 3.0, 5.0, 7.0])

    def test_serie_mas_corta_que_el_periodo(self):
        self.assertEqual(ind.sma([1, 2], 5), [None, None])

    def test_periodo_invalido(self):
        with self.assertRaises(ValueError):
            ind.sma([1, 2, 3], 0)


class TestCruces(unittest.TestCase):
    def test_cruce_alcista(self):
        rapida = [1.0, 2.0, 3.0]
        lenta = [2.0, 2.0, 2.0]
        detectados = ind.cruces(rapida, lenta, 7, 50)
        self.assertEqual([(c.index, c.direction) for c in detectados], [(2, ind.ALCISTA)])

    def test_cruce_bajista(self):
        rapida = [3.0, 2.5, 1.0]
        lenta = [2.0, 2.0, 2.0]
        detectados = ind.cruces(rapida, lenta, 7, 50)
        self.assertEqual([(c.index, c.direction) for c in detectados], [(2, ind.BAJISTA)])

    def test_contacto_sin_ruptura_no_es_cruce(self):
        rapida = [1.0, 2.0, 1.5]
        lenta = [2.0, 2.0, 2.0]
        self.assertEqual(ind.cruces(rapida, lenta, 7, 50), [])

    def test_contacto_y_ruptura_cuenta_una_vez(self):
        rapida = [1.0, 2.0, 2.5]
        lenta = [2.0, 2.0, 2.0]
        detectados = ind.cruces(rapida, lenta, 7, 50)
        self.assertEqual([(c.index, c.direction) for c in detectados], [(2, ind.ALCISTA)])

    def test_ignora_huecos_sin_media(self):
        rapida = [None, None, 3.0]
        lenta = [None, 2.0, 2.0]
        self.assertEqual(ind.cruces(rapida, lenta, 7, 50), [])

    def test_filtro_desde(self):
        rapida = [1.0, 3.0, 1.0, 3.0]
        lenta = [2.0, 2.0, 2.0, 2.0]
        self.assertEqual(len(ind.cruces(rapida, lenta, 7, 50)), 3)
        self.assertEqual(len(ind.cruces(rapida, lenta, 7, 50, desde=3)), 1)


class TestAuxiliares(unittest.TestCase):
    def test_separacion_pct(self):
        self.assertAlmostEqual(ind.separacion_pct(11.0, 10.0), 10.0)
        self.assertAlmostEqual(ind.separacion_pct(9.0, 10.0), -10.0)
        self.assertIsNone(ind.separacion_pct(None, 10.0))
        self.assertIsNone(ind.separacion_pct(10.0, 0))

    def test_alineacion(self):
        self.assertEqual(ind.alineacion(3, 2, 1), "alcista")
        self.assertEqual(ind.alineacion(1, 2, 3), "bajista")
        self.assertEqual(ind.alineacion(2, 1, 3), "mixta")
        self.assertEqual(ind.alineacion(2, 1, None), "desconocida")


def _ts(fecha: str) -> int:
    """Epoch a las 12:00 UTC de una fecha ISO, como guarda el historico."""
    y, m, d = (int(p) for p in fecha.split("-"))
    return calendar.timegm((y, m, d, 12, 0, 0, 0, 0, 0))


def _velas_sinteticas(n_previas: int, n_hoy: int, precios) -> providers.Velas:
    """Genera velas de 15 minutos: `n_previas` en dias anteriores y `n_hoy` en la ultima sesion."""
    total = n_previas + n_hoy
    assert len(precios) == total
    fin = dt.datetime.now(MADRID).replace(hour=17, minute=30, second=0, microsecond=0)
    inicio_hoy = fin - dt.timedelta(minutes=15 * (n_hoy - 1))
    ayer_fin = inicio_hoy - dt.timedelta(days=1)

    timestamps = [
        int((ayer_fin - dt.timedelta(minutes=15 * (n_previas - 1 - i))).timestamp())
        for i in range(n_previas)
    ]
    timestamps += [int((inicio_hoy + dt.timedelta(minutes=15 * i)).timestamp()) for i in range(n_hoy)]
    return providers.Velas(timestamps, list(precios), "test")


class TestAnalizar(unittest.TestCase):
    def setUp(self):
        self.valor = Valor("TEST.MC", "Valor de prueba", "ibex35")

    def test_detecta_cruce_alcista_en_la_sesion(self):
        # 260 velas bajando y 40 subiendo con fuerza: la media de 7 supera a la de 50 hoy.
        bajada = [100.0 - i * 0.1 for i in range(260)]
        subida = [bajada[-1] + (i + 1) * 1.5 for i in range(40)]
        velas = _velas_sinteticas(260, 40, bajada + subida)

        resultado = analizar(self.valor, velas, "15m")

        pares = {(c["pair"], c["dir"]) for c in resultado["crosses"]}
        self.assertIn(("7x50", "alcista"), pares)
        self.assertEqual(resultado["align"], "alcista")
        self.assertEqual(resultado["session"], dt.datetime.now(MADRID).date().isoformat())
        self.assertEqual(resultado["symbol"], "TEST.MC")
        self.assertEqual(resultado["bars"], 300)

    def test_serie_plana_no_genera_cruces(self):
        velas = _velas_sinteticas(260, 40, [10.0] * 300)
        resultado = analizar(self.valor, velas, "15m")
        self.assertEqual(resultado["crosses"], [])
        self.assertEqual(resultado["changePct"], 0.0)

    def test_cruce_de_ayer_no_cuenta_como_de_hoy(self):
        # Todo el movimiento ocurre en la sesion previa; hoy la serie es plana.
        bajada = [100.0 - i * 0.1 for i in range(220)]
        subida = [bajada[-1] + (i + 1) * 1.5 for i in range(40)]
        hoy = [subida[-1]] * 40
        velas = _velas_sinteticas(260, 40, bajada + subida + hoy)

        resultado = analizar(self.valor, velas, "15m")
        self.assertEqual(resultado["crosses"], [])

    def test_diario_solo_mira_la_ultima_vela(self):
        bajada = [100.0 - i * 0.1 for i in range(260)]
        subida = [bajada[-1] + (i + 1) * 1.5 for i in range(40)]
        velas = _velas_sinteticas(260, 40, bajada + subida)

        resultado = analizar(self.valor, velas, "1d")
        for cruce in resultado["crosses"]:
            self.assertEqual(cruce["time"], resultado["lastBar"])


class TestHistorico(unittest.TestCase):
    """El historico acumulado es lo que permite que el panel publicado mejore solo."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)

    def test_guardar_y_cargar(self):
        velas = providers.Velas([_ts("2026-08-05"), _ts("2026-08-06")], [10.5, 11.25], "test")
        self.assertEqual(hist.guardar(self.dir, "SAN.MC", velas), 2)

        recuperadas = hist.cargar(self.dir, "SAN.MC")
        self.assertEqual(recuperadas.closes, [10.5, 11.25])
        self.assertEqual(recuperadas.timestamps, velas.timestamps)

    def test_cargar_sin_fichero(self):
        self.assertIsNone(hist.cargar(self.dir, "NOEXISTE.MC"))

    def test_combinar_une_por_fecha_y_ordena(self):
        previas = providers.Velas([_ts("2026-08-03"), _ts("2026-08-04")], [1.0, 2.0], "historico")
        nuevas = providers.Velas([_ts("2026-08-05"), _ts("2026-08-04")], [4.0, 3.0], "yahoo")

        unidas = hist.combinar(previas, nuevas)
        self.assertEqual(unidas.closes, [1.0, 3.0, 4.0])  # el 4 de agosto lo pisa la nueva

    def test_combinar_tolera_ausencias(self):
        velas = providers.Velas([_ts("2026-08-05")], [9.0], "yahoo")
        self.assertEqual(hist.combinar(None, velas).closes, [9.0])
        self.assertEqual(hist.combinar(velas, None).closes, [9.0])
        self.assertIsNone(hist.combinar(None, None))

    def test_la_serie_acumulada_desbloquea_el_cruce_de_50(self):
        # Con 50 sesiones la media de 50 solo existe en la ultima vela, asi que
        # no hay cruce posible: hacen falta dos velas seguidas con ambas medias.
        # Al acumular una sesion mas, el mismo movimiento ya se detecta.
        precios = [50.0 - i * 0.2 for i in range(50)] + [200.0]
        fechas = [_ts(f"2026-0{5 + (d // 28)}-{d % 28 + 1:02d}") for d in range(51)]
        valor = Valor("TEST.MC", "Prueba", "ibex35")

        corta = providers.Velas(fechas[:50], precios[:50], "respaldo")
        self.assertEqual(analizar(valor, corta, "1d")["crosses"], [])

        larga = providers.Velas(fechas, precios, "respaldo")
        cruces_larga = analizar(valor, larga, "1d")["crosses"]
        self.assertEqual([(c["pair"], c["dir"]) for c in cruces_larga], [("7x50", "alcista")])


class TestUniversoGenerado(unittest.TestCase):
    """docs/universo.js es la copia que usa el navegador: no debe quedarse atrás."""

    def test_universo_js_al_dia(self):
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
        from generar_universo import DESTINO, render

        self.assertTrue(DESTINO.exists(), "falta docs/universo.js")
        self.assertEqual(
            DESTINO.read_text(encoding="utf-8"), render(),
            "docs/universo.js está desincronizado: ejecuta python3 tools/generar_universo.py")


class TestUniverso(unittest.TestCase):
    def test_ibex_tiene_35_valores(self):
        self.assertEqual(len(IBEX35), 35)

    def test_sin_tickers_duplicados(self):
        simbolos = [v.symbol for v in TODOS]
        self.assertEqual(len(simbolos), len(set(simbolos)))

    def test_todos_los_tickers_son_del_mercado_continuo(self):
        for valor in TODOS:
            self.assertTrue(valor.symbol.endswith(".MC"), valor.symbol)


if __name__ == "__main__":
    unittest.main()
