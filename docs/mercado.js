/* Escaneo desde el navegador.
 *
 * Yahoo rechaza con 429 las peticiones que salen de centros de datos, así que el
 * robot de GitHub solo consigue cierres diarios de una fuente de respaldo. Desde
 * el navegador del usuario, en cambio, la petición sale de una conexión normal y
 * Yahoo responde con el histórico completo, también intradía. Este módulo hace
 * ese escaneo y devuelve exactamente la misma estructura que genera el escáner
 * de Python, para que el panel no note la diferencia.
 */
(() => {
  "use strict";

  const PERIODOS = [7, 50, 200];
  const PARES = [[7, 50], [7, 200], [50, 200]];

  const TIMEFRAMES = {
    "15m": { interval: "15m", range: "1mo", label: "15 minutos" },
    "60m": { interval: "60m", range: "6mo", label: "1 hora" },
    "1d": { interval: "1d", range: "2y", label: "Diario" },
  };

  const CONCURRENCIA = 8;
  const HOSTS = ["https://query1.finance.yahoo.com", "https://query2.finance.yahoo.com"];

  /* ---------- Indicadores (mismo criterio que scanner/indicators.py) ---------- */

  function sma(valores, periodo) {
    const salida = new Array(valores.length).fill(null);
    let acumulado = 0;
    for (let i = 0; i < valores.length; i++) {
      acumulado += valores[i];
      if (i >= periodo) acumulado -= valores[i - periodo];
      if (i >= periodo - 1) salida[i] = acumulado / periodo;
    }
    return salida;
  }

  // Un cruce ocurre cuando el signo de (rápida - lenta) se invierte respecto al
  // último signo distinto de cero; un toque exacto no rompe la racha.
  function cruces(rapida, lenta, periodoRapido, periodoLento, desde = 0) {
    const encontrados = [];
    let ultimoSigno = null;
    const n = Math.min(rapida.length, lenta.length);
    for (let i = 0; i < n; i++) {
      const f = rapida[i], l = lenta[i];
      if (f === null || l === null) continue;
      const diferencia = f - l;
      if (diferencia === 0) continue;
      const signo = diferencia > 0 ? 1 : -1;
      if (ultimoSigno !== null && signo !== ultimoSigno && i >= desde) {
        encontrados.push({
          index: i, fast: periodoRapido, slow: periodoLento,
          dir: signo > 0 ? "alcista" : "bajista",
        });
      }
      ultimoSigno = signo;
    }
    return encontrados;
  }

  function separacionPct(rapida, lenta) {
    if (rapida === null || lenta === null || lenta === 0) return null;
    return (rapida - lenta) / lenta * 100;
  }

  function alineacion(a, b, c) {
    if (a === null || b === null || c === null) return "desconocida";
    if (a > b && b > c) return "alcista";
    if (a < b && b < c) return "bajista";
    return "mixta";
  }

  /* ---------- Fechas en hora de Madrid ---------- */

  const FMT_FECHA = new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Europe/Madrid", year: "numeric", month: "2-digit", day: "2-digit",
  });
  const FMT_HORA = new Intl.DateTimeFormat("es-ES", {
    timeZone: "Europe/Madrid", hour: "2-digit", minute: "2-digit", hour12: false,
  });

  // El desfase horario va en la marca de tiempo para que coincida al carácter con
  // lo que genera el escáner de Python (CET en invierno, CEST en verano).
  const FMT_DESFASE = new Intl.DateTimeFormat("en-US", {
    timeZone: "Europe/Madrid", timeZoneName: "longOffset",
  });

  const fechaMadrid = (ts) => FMT_FECHA.format(new Date(ts * 1000));
  const horaMadrid = (ts) => FMT_HORA.format(new Date(ts * 1000)).replace(".", ":");

  function desfaseMadrid(ts) {
    const parte = FMT_DESFASE.formatToParts(new Date(ts * 1000))
      .find((p) => p.type === "timeZoneName");
    const desfase = (parte?.value || "").replace("GMT", "");
    return desfase || "+00:00";
  }

  const isoMadrid = (ts) => `${fechaMadrid(ts)}T${horaMadrid(ts)}:00${desfaseMadrid(ts)}`;

  const redondear = (v, dec) => (v === null || v === undefined ? null
    : Math.round(v * 10 ** dec) / 10 ** dec);

  /* ---------- Análisis de un valor ---------- */

  function analizar(valor, velas, timeframe) {
    const cierres = velas.closes;
    const medias = {};
    for (const p of PERIODOS) medias[p] = sma(cierres, p);

    const fechas = velas.timestamps.map(fechaMadrid);
    const sesion = fechas[fechas.length - 1];
    let inicioSesion = fechas.length - 1;
    while (inicioSesion > 0 && fechas[inicioSesion - 1] === sesion) inicioSesion--;

    // En diario cada vela es una sesión: el cruce de hoy es el de la última vela.
    const desde = timeframe === "1d" ? cierres.length - 1 : inicioSesion;

    const detectados = [];
    for (const [rapido, lento] of PARES) {
      for (const c of cruces(medias[rapido], medias[lento], rapido, lento, desde)) {
        detectados.push({
          pair: `${rapido}x${lento}`, fast: rapido, slow: lento, dir: c.dir,
          time: isoMadrid(velas.timestamps[c.index]),
          price: redondear(cierres[c.index], 4),
        });
      }
    }
    detectados.sort((a, b) => (a.time < b.time ? -1 : 1));

    let previo = inicioSesion > 0 ? cierres[inicioSesion - 1] : null;
    if (timeframe === "1d") previo = cierres.length >= 2 ? cierres[cierres.length - 2] : null;

    const ultimo = cierres[cierres.length - 1];
    const actuales = {};
    for (const p of PERIODOS) actuales[p] = medias[p][medias[p].length - 1];

    const gaps = {};
    for (const [r, l] of PARES) gaps[`${r}x${l}`] = redondear(separacionPct(actuales[r], actuales[l]), 3);

    return {
      symbol: valor.s, name: valor.n, index: valor.i,
      price: redondear(ultimo, 4),
      changePct: previo ? redondear((ultimo / previo - 1) * 100, 2) : null,
      sma: { 7: redondear(actuales[7], 4), 50: redondear(actuales[50], 4), 200: redondear(actuales[200], 4) },
      align: alineacion(actuales[7], actuales[50], actuales[200]),
      crosses: detectados,
      gaps,
      session: sesion,
      lastBar: isoMadrid(velas.timestamps[velas.timestamps.length - 1]),
      bars: cierres.length,
      source: velas.source,
    };
  }

  /* ---------- Descarga ---------- */

  async function traerVelas(symbol, timeframe, señal) {
    const cfg = TIMEFRAMES[timeframe];
    let ultimoError;
    for (let intento = 0; intento < HOSTS.length; intento++) {
      const url = `${HOSTS[intento]}/v8/finance/chart/${encodeURIComponent(symbol)}` +
        `?interval=${cfg.interval}&range=${cfg.range}&includePrePost=false`;
      try {
        const resp = await fetch(url, { signal: señal });
        if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
        const payload = await resp.json();
        const resultado = payload?.chart?.result?.[0];
        if (!resultado) throw new Error(payload?.chart?.error?.description || "sin resultados");

        const ts = resultado.timestamp || [];
        const cierres = resultado.indicators?.quote?.[0]?.close || [];
        const tsLimpio = [], cierreLimpio = [];
        for (let i = 0; i < ts.length; i++) {
          if (cierres[i] === null || cierres[i] === undefined) continue;
          tsLimpio.push(ts[i]);
          cierreLimpio.push(cierres[i]);
        }
        if (!cierreLimpio.length) throw new Error("sin cierres válidos");
        return { timestamps: tsLimpio, closes: cierreLimpio, source: "yahoo" };
      } catch (err) {
        ultimoError = err;
        if (err.name === "AbortError") throw err;
      }
    }
    throw ultimoError;
  }

  /* ---------- Escaneo completo ---------- */

  async function escanear(timeframe, { alProgresar, señal } = {}) {
    const valores = window.UNIVERSO || [];
    const resultados = [];
    const errores = [];
    let hechos = 0;

    const cola = valores.slice();
    async function trabajador() {
      while (cola.length) {
        const valor = cola.shift();
        try {
          const velas = await traerVelas(valor.s, timeframe, señal);
          if (velas.closes.length < 8) throw new Error(`solo ${velas.closes.length} velas`);
          resultados.push(analizar(valor, velas, timeframe));
        } catch (err) {
          if (err.name === "AbortError") return;
          errores.push({ symbol: valor.s, name: valor.n, index: valor.i, error: String(err.message || err) });
        }
        alProgresar?.(++hechos, valores.length);
      }
    }

    await Promise.all(Array.from({ length: CONCURRENCIA }, trabajador));

    if (!resultados.length) {
      throw new Error(errores[0]?.error || "ningún valor ha devuelto datos");
    }

    resultados.sort((a, b) => (b.crosses.length - a.crosses.length) || a.name.localeCompare(b.name, "es"));
    errores.sort((a, b) => a.name.localeCompare(b.name, "es"));

    const sesiones = resultados.map((r) => r.session);
    const frecuencia = new Map();
    for (const s of sesiones) frecuencia.set(s, (frecuencia.get(s) || 0) + 1);
    const sesion = [...frecuencia.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || null;

    const ahora = new Date();
    return {
      timeframe,
      label: TIMEFRAMES[timeframe].label,
      generatedAt: isoMadrid(ahora / 1000),
      session: sesion,
      periods: PERIODOS,
      count: resultados.length,
      withCrosses: resultados.filter((r) => r.crosses.length).length,
      missing200: resultados.filter((r) => r.sma["200"] === null).length,
      sources: ["yahoo"],
      results: resultados,
      errors: errores,
      envivo: true,
    };
  }

  // Comprobación rápida: ¿deja Yahoo que el navegador le pida datos?
  async function disponible(señal) {
    try {
      await traerVelas("SAN.MC", "1d", señal);
      return true;
    } catch {
      return false;
    }
  }

  window.Mercado = { TIMEFRAMES, sma, cruces, separacionPct, alineacion, analizar, escanear, disponible };
})();
