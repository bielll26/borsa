"""Medias moviles simples y deteccion de cruces."""

from __future__ import annotations

from typing import List, NamedTuple, Optional, Sequence

Serie = List[Optional[float]]

ALCISTA = "alcista"  # la media rapida cruza por encima de la lenta (golden cross)
BAJISTA = "bajista"  # la media rapida cruza por debajo de la lenta (death cross)


class Cruce(NamedTuple):
    index: int  # posicion de la vela en la que se confirma el cruce
    fast: int  # periodo de la media rapida
    slow: int  # periodo de la media lenta
    direction: str  # ALCISTA | BAJISTA


def sma(values: Sequence[float], period: int) -> Serie:
    """Media movil simple. Devuelve None en las posiciones sin historico suficiente."""
    if period <= 0:
        raise ValueError("El periodo debe ser mayor que cero")

    out: Serie = [None] * len(values)
    acumulado = 0.0
    for i, v in enumerate(values):
        acumulado += v
        if i >= period:
            acumulado -= values[i - period]
        if i >= period - 1:
            out[i] = acumulado / period
    return out


def cruces(fast: Serie, slow: Serie, periodo_rapido: int, periodo_lento: int,
           desde: int = 0) -> List[Cruce]:
    """Detecta los cruces entre dos medias, devolviendo los de la vela `desde` en adelante.

    Un cruce se confirma cuando el signo de (rapida - lenta) se invierte respecto
    al ultimo signo distinto de cero. Las velas en las que ambas medias coinciden
    exactamente no rompen la racha: un toque solo cuenta como cruce si despues la
    media rapida sale por el lado contrario.

    La serie se recorre entera aunque `desde` sea alto, porque el signo previo es
    lo que define si hay cruce.
    """
    encontrados: List[Cruce] = []
    ultimo_signo: Optional[int] = None

    for i in range(min(len(fast), len(slow))):
        f, s = fast[i], slow[i]
        if f is None or s is None:
            continue

        diferencia = f - s
        if diferencia == 0:
            continue
        signo = 1 if diferencia > 0 else -1

        if ultimo_signo is not None and signo != ultimo_signo and i >= desde:
            encontrados.append(
                Cruce(i, periodo_rapido, periodo_lento, ALCISTA if signo > 0 else BAJISTA)
            )
        ultimo_signo = signo

    return encontrados


def separacion_pct(fast: Optional[float], slow: Optional[float]) -> Optional[float]:
    """Distancia entre dos medias en % sobre la media lenta (signo = posicion relativa)."""
    if fast is None or slow is None or slow == 0:
        return None
    return (fast - slow) / slow * 100.0


def alineacion(sma_rapida: Optional[float], sma_media: Optional[float],
               sma_lenta: Optional[float]) -> str:
    """Clasifica el orden de las tres medias: alcista, bajista o mixta."""
    if None in (sma_rapida, sma_media, sma_lenta):
        return "desconocida"
    if sma_rapida > sma_media > sma_lenta:
        return "alcista"
    if sma_rapida < sma_media < sma_lenta:
        return "bajista"
    return "mixta"
