"""Universo de valores: IBEX 35 y resto del Mercado Continuo español.

Los tickers usan el sufijo `.MC` (Bolsa de Madrid) que emplea Yahoo Finance.

La composicion del IBEX 35 se revisa cada seis meses, asi que esta lista es un
punto de partida editable: basta con cambiar las tuplas de abajo. El escaner
marca como "sin datos" cualquier ticker que deje de cotizar, de modo que los
cambios de composicion se detectan a simple vista en el panel.
"""

from __future__ import annotations

from typing import Dict, List, NamedTuple


class Valor(NamedTuple):
    symbol: str
    name: str
    index: str  # "ibex35" | "continuo"


# --- IBEX 35 -----------------------------------------------------------------
# Revisar tras cada revision ordinaria del Comite Asesor Tecnico (junio/diciembre).
IBEX35: List[Valor] = [
    Valor("ACS.MC", "ACS", "ibex35"),
    Valor("ACX.MC", "Acerinox", "ibex35"),
    Valor("AENA.MC", "Aena", "ibex35"),
    Valor("AMS.MC", "Amadeus IT Group", "ibex35"),
    Valor("ANA.MC", "Acciona", "ibex35"),
    Valor("ANE.MC", "Acciona Energia", "ibex35"),
    Valor("BBVA.MC", "BBVA", "ibex35"),
    Valor("BKT.MC", "Bankinter", "ibex35"),
    Valor("CABK.MC", "CaixaBank", "ibex35"),
    Valor("CLNX.MC", "Cellnex Telecom", "ibex35"),
    Valor("COL.MC", "Inmobiliaria Colonial", "ibex35"),
    Valor("ELE.MC", "Endesa", "ibex35"),
    Valor("ENG.MC", "Enagas", "ibex35"),
    Valor("FDR.MC", "Fluidra", "ibex35"),
    Valor("FER.MC", "Ferrovial", "ibex35"),
    Valor("GRF.MC", "Grifols", "ibex35"),
    Valor("IAG.MC", "IAG", "ibex35"),
    Valor("IBE.MC", "Iberdrola", "ibex35"),
    Valor("IDR.MC", "Indra Sistemas", "ibex35"),
    Valor("ITX.MC", "Inditex", "ibex35"),
    Valor("LOG.MC", "Logista", "ibex35"),
    Valor("MAP.MC", "Mapfre", "ibex35"),
    Valor("MRL.MC", "Merlin Properties", "ibex35"),
    Valor("MTS.MC", "ArcelorMittal", "ibex35"),
    Valor("NTGY.MC", "Naturgy", "ibex35"),
    Valor("PUIG.MC", "Puig Brands", "ibex35"),
    Valor("RED.MC", "Redeia", "ibex35"),
    Valor("REP.MC", "Repsol", "ibex35"),
    Valor("ROVI.MC", "Laboratorios Rovi", "ibex35"),
    Valor("SAB.MC", "Banco Sabadell", "ibex35"),
    Valor("SAN.MC", "Banco Santander", "ibex35"),
    Valor("SCYR.MC", "Sacyr", "ibex35"),
    Valor("SLR.MC", "Solaria Energia", "ibex35"),
    Valor("TEF.MC", "Telefonica", "ibex35"),
    Valor("UNI.MC", "Unicaja Banco", "ibex35"),
]

# --- Resto del Mercado Continuo ----------------------------------------------
CONTINUO: List[Valor] = [
    Valor("A3M.MC", "Atresmedia", "continuo"),
    Valor("ADX.MC", "Audax Renovables", "continuo"),
    Valor("AEDAS.MC", "AEDAS Homes", "continuo"),
    Valor("ALB.MC", "Corporacion Financiera Alba", "continuo"),
    Valor("ALM.MC", "Almirall", "continuo"),
    Valor("ALNT.MC", "Alantra Partners", "continuo"),
    Valor("AMP.MC", "Amper", "continuo"),
    Valor("ARM.MC", "Airtificial", "continuo"),
    Valor("ATRY.MC", "Atrys Health", "continuo"),
    Valor("AZK.MC", "Azkoyen", "continuo"),
    Valor("BDL.MC", "Baron de Ley", "continuo"),
    Valor("CAF.MC", "CAF", "continuo"),
    Valor("CASH.MC", "Prosegur Cash", "continuo"),
    Valor("CIE.MC", "CIE Automotive", "continuo"),
    Valor("COX.MC", "Cox", "continuo"),
    Valor("DIA.MC", "DIA", "continuo"),
    Valor("DOM.MC", "Global Dominion Access", "continuo"),
    Valor("EBRO.MC", "Ebro Foods", "continuo"),
    Valor("ECR.MC", "Ercros", "continuo"),
    Valor("EDR.MC", "Ence Energia y Celulosa", "continuo"),
    Valor("ENO.MC", "Elecnor", "continuo"),
    Valor("FAE.MC", "Faes Farma", "continuo"),
    Valor("FCC.MC", "FCC", "continuo"),
    Valor("GCO.MC", "Grupo Catalana Occidente", "continuo"),
    Valor("GEST.MC", "Gestamp Automocion", "continuo"),
    Valor("GSJ.MC", "Grupo Empresarial San Jose", "continuo"),
    Valor("HOME.MC", "Neinor Homes", "continuo"),
    Valor("IBG.MC", "Iberpapel Gestion", "continuo"),
    Valor("INSU.MC", "Inmobiliaria del Sur", "continuo"),
    Valor("LDA.MC", "Linea Directa Aseguradora", "continuo"),
    Valor("LGT.MC", "Lingotes Especiales", "continuo"),
    Valor("MCM.MC", "Miquel y Costas", "continuo"),
    Valor("MDF.MC", "Duro Felguera", "continuo"),
    Valor("MEL.MC", "Melia Hotels International", "continuo"),
    Valor("MVC.MC", "Metrovacesa", "continuo"),
    Valor("NEA.MC", "Nueva Expresion Textil", "continuo"),
    Valor("NHH.MC", "NH Hotel Group", "continuo"),
    Valor("NXT.MC", "Nextil", "continuo"),
    Valor("OHLA.MC", "OHLA", "continuo"),
    Valor("PHM.MC", "PharmaMar", "continuo"),
    Valor("PSG.MC", "Prosegur", "continuo"),
    Valor("R4.MC", "Renta 4 Banco", "continuo"),
    Valor("RJF.MC", "Reig Jofre", "continuo"),
    Valor("TLGO.MC", "Talgo", "continuo"),
    Valor("TRE.MC", "Tecnicas Reunidas", "continuo"),
    Valor("TRG.MC", "Tubos Reunidos", "continuo"),
    Valor("TUB.MC", "Tubacex", "continuo"),
    Valor("VID.MC", "Vidrala", "continuo"),
    Valor("VIS.MC", "Viscofan", "continuo"),
    Valor("VOC.MC", "Vocento", "continuo"),
]

TODOS: List[Valor] = IBEX35 + CONTINUO

_POR_NOMBRE: Dict[str, List[Valor]] = {
    "ibex35": IBEX35,
    "continuo": CONTINUO,
    "todos": TODOS,
}


def universo(nombre: str) -> List[Valor]:
    """Devuelve la lista de valores de un universo ('ibex35', 'continuo', 'todos')."""
    try:
        return _POR_NOMBRE[nombre]
    except KeyError:
        opciones = ", ".join(sorted(_POR_NOMBRE))
        raise ValueError(f"Universo desconocido: {nombre!r}. Opciones: {opciones}") from None
