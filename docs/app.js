/* Panel de cruces de medias 7/50/200 — sin dependencias externas. */
(() => {
  "use strict";

  const TIMEFRAMES_POR_DEFECTO = [
    { id: "15m", label: "15 minutos", file: "15m.json" },
    { id: "60m", label: "1 hora", file: "60m.json" },
    { id: "1d", label: "Diario", file: "1d.json" },
  ];

  const UMBRAL_CERCANO = 0.5; // % de separación entre medias para considerarlo inminente
  const EN_LOCAL = ["localhost", "127.0.0.1", "[::1]"].includes(location.hostname);

  const estado = {
    timeframes: TIMEFRAMES_POR_DEFECTO,
    tf: localStorage.getItem("tf") || "15m",
    universo: localStorage.getItem("universo") || "todos",
    pares: new Set(["7x50", "7x200", "50x200"]),
    direcciones: new Set(["alcista", "bajista"]),
    busqueda: "",
    orden: { campo: "crosses", dir: "desc" },
    datos: null,
    cache: new Map(),
    apiViva: null, // null = sin comprobar, true/false = hay servidor local de escaneo
  };

  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // Los precios de la bolsa española van de céntimos a cientos de euros:
  // se ajustan los decimales para no arrastrar ceros ni perder precisión.
  const decimales = (v) => (Math.abs(v) >= 100 ? 2 : Math.abs(v) >= 1 ? 3 : 4);
  const num = (v) =>
    v === null || v === undefined ? "—" : v.toLocaleString("es-ES", {
      minimumFractionDigits: decimales(v), maximumFractionDigits: decimales(v),
    });
  const hora = (iso) => (iso ? iso.slice(11, 16) : "—");

  /* ---------- Carga de datos ---------- */

  async function cargarIndice() {
    try {
      const resp = await fetch("data/index.json", { cache: "no-store" });
      if (!resp.ok) throw new Error(resp.status);
      const indice = await resp.json();
      if (Array.isArray(indice.timeframes) && indice.timeframes.length) {
        estado.timeframes = indice.timeframes;
      }
    } catch {
      /* sin índice se usan los marcos temporales por defecto */
    }
    if (!estado.timeframes.some((t) => t.id === estado.tf)) {
      estado.tf = estado.timeframes[0].id;
    }
  }

  async function cargarDatos(tf, { forzar = false } = {}) {
    if (!forzar && estado.cache.has(tf)) return estado.cache.get(tf);

    // En local puede estar corriendo `python -m scanner.server`, que escanea en vivo.
    // Se prueba una sola vez: si no responde, se usan los ficheros estáticos.
    if (EN_LOCAL && estado.apiViva !== false) {
      try {
        const resp = await fetch(`/api/scan?tf=${encodeURIComponent(tf)}&universo=todos`,
          { cache: "no-store" });
        estado.apiViva = resp.ok;
        if (resp.ok) {
          const datos = await resp.json();
          datos.envivo = true;
          estado.cache.set(tf, datos);
          return datos;
        }
      } catch {
        estado.apiViva = false;
      }
    }

    const meta = estado.timeframes.find((t) => t.id === tf);
    const resp = await fetch(`data/${meta?.file || tf + ".json"}`, { cache: "no-store" });
    if (!resp.ok) throw new Error(`No hay datos para ${tf} (HTTP ${resp.status})`);
    const datos = await resp.json();
    estado.cache.set(tf, datos);
    return datos;
  }

  /* ---------- Filtrado ---------- */

  const crucesVisibles = (valor) =>
    (valor.crosses || []).filter(
      (c) => estado.pares.has(c.pair) && estado.direcciones.has(c.dir));

  function valoresFiltrados() {
    const texto = estado.busqueda.trim().toLowerCase();
    return (estado.datos?.results || []).filter((v) => {
      if (estado.universo !== "todos" && v.index !== estado.universo) return false;
      if (!texto) return true;
      return v.name.toLowerCase().includes(texto) || v.symbol.toLowerCase().includes(texto);
    });
  }

  /* ---------- Render ---------- */

  function pintarSenales(valores) {
    const conCruce = valores
      .map((v) => ({ valor: v, cruces: crucesVisibles(v) }))
      .filter((x) => x.cruces.length)
      .sort((a, b) => (b.cruces.at(-1).time > a.cruces.at(-1).time ? 1 : -1));

    $("#contador-cruces").textContent = conCruce.length;
    $("#sin-senales").hidden = conCruce.length > 0;

    $("#senales").innerHTML = conCruce.map(({ valor, cruces }) => {
      const ultima = cruces.at(-1).dir;
      const variacion = valor.changePct;
      const claseVar = variacion > 0 ? "sube" : variacion < 0 ? "baja" : "";
      const signo = variacion > 0 ? "+" : "";
      return `
        <article class="tarjeta tarjeta--${ultima}">
          <div class="tarjeta__cabecera">
            <div>
              <div class="tarjeta__nombre">${esc(valor.name)}</div>
              <div class="tarjeta__ticker">${esc(valor.symbol)}</div>
            </div>
            <div class="tarjeta__precio">
              <b>${num(valor.price)}</b>
              <span class="${claseVar}">${variacion === null ? "—" : signo + variacion.toFixed(2) + " %"}</span>
            </div>
          </div>
          <ul class="tarjeta__cruces">
            ${cruces.map((c) => `
              <li class="cruce cruce--${c.dir}">
                <span>${c.dir === "alcista" ? "▲" : "▼"}</span>
                <span class="cruce__par">MM ${c.fast} × MM ${c.slow}</span>
                <span class="cruce__hora">${hora(c.time)}</span>
              </li>`).join("")}
          </ul>
        </article>`;
    }).join("");
  }

  function pintarCercanos(valores) {
    const cercanos = [];
    for (const valor of valores) {
      if (crucesVisibles(valor).length) continue;
      let mejor = null;
      for (const par of estado.pares) {
        const hueco = valor.gaps?.[par];
        if (hueco === null || hueco === undefined) continue;
        if (Math.abs(hueco) <= UMBRAL_CERCANO &&
            (mejor === null || Math.abs(hueco) < Math.abs(mejor.hueco))) {
          mejor = { par, hueco };
        }
      }
      if (mejor) cercanos.push({ valor, ...mejor });
    }
    cercanos.sort((a, b) => Math.abs(a.hueco) - Math.abs(b.hueco));

    $("#contador-cerca").textContent = cercanos.length;
    $("#cercanos").innerHTML = cercanos.length
      ? cercanos.map(({ valor, par, hueco }) => {
          const [rapida, lenta] = par.split("x");
          return `
            <div class="cercano">
              <div>
                <div class="cercano__nombre">${esc(valor.name)}</div>
                <div class="tarjeta__ticker">MM ${rapida} × MM ${lenta}</div>
              </div>
              <div class="cercano__dato">
                <b class="${hueco > 0 ? "sube" : "baja"}">${hueco > 0 ? "+" : ""}${hueco.toFixed(2)} %</b>
                ${hueco > 0 ? "por encima" : "por debajo"}
              </div>
            </div>`;
        }).join("")
      : `<p class="vacio">Ningún valor tiene sus medias a menos de un ${UMBRAL_CERCANO} %.</p>`;
  }

  const CAMPOS = {
    name: (v) => v.name.toLowerCase(),
    price: (v) => v.price ?? -Infinity,
    changePct: (v) => v.changePct ?? -Infinity,
    sma7: (v) => v.sma?.["7"] ?? -Infinity,
    sma50: (v) => v.sma?.["50"] ?? -Infinity,
    sma200: (v) => v.sma?.["200"] ?? -Infinity,
    align: (v) => v.align,
    crosses: (v) => crucesVisibles(v).length,
  };

  function pintarTabla(valores) {
    const { campo, dir } = estado.orden;
    const clave = CAMPOS[campo] || CAMPOS.name;
    const ordenados = [...valores].sort((a, b) => {
      const va = clave(a), vb = clave(b);
      if (va === vb) return a.name.localeCompare(b.name, "es");
      return (va > vb ? 1 : -1) * (dir === "asc" ? 1 : -1);
    });

    $("#contador-tabla").textContent = ordenados.length;
    $("#tabla tbody").innerHTML = ordenados.map((v) => {
      const cruces = crucesVisibles(v);
      const variacion = v.changePct;
      const claseVar = variacion > 0 ? "sube" : variacion < 0 ? "baja" : "";
      const signo = variacion > 0 ? "+" : "";
      return `
        <tr class="${cruces.length ? "destacada" : ""}">
          <td><strong>${esc(v.name)}</strong><br><span class="tarjeta__ticker">${esc(v.symbol)}</span></td>
          <td class="num">${num(v.price)}</td>
          <td class="num ${claseVar}">${variacion === null ? "—" : signo + variacion.toFixed(2)}</td>
          <td class="num">${num(v.sma?.["7"])}</td>
          <td class="num">${num(v.sma?.["50"])}</td>
          <td class="num">${num(v.sma?.["200"])}</td>
          <td><span class="etiqueta etiqueta--${v.align}">${v.align}</span></td>
          <td>${cruces.length
            ? cruces.map((c) => `<span class="mini-cruce mini-cruce--${c.dir}">${c.fast}×${c.slow} ${hora(c.time)}</span>`).join("")
            : "—"}</td>
        </tr>`;
    }).join("");

    document.querySelectorAll("#tabla th").forEach((th) => {
      th.classList.toggle("orden-asc", th.dataset.orden === campo && dir === "asc");
      th.classList.toggle("orden-desc", th.dataset.orden === campo && dir === "desc");
    });
  }

  function pintarErrores() {
    const errores = (estado.datos?.errors || []).filter(
      (e) => estado.universo === "todos" || e.index === estado.universo);
    $("#bloque-errores").hidden = errores.length === 0;
    $("#contador-errores").textContent = errores.length;
    $("#errores").innerHTML = errores
      .map((e) => `<span class="error-chip" title="${esc(e.error)}">${esc(e.symbol)} · ${esc(e.name)}</span>`)
      .join("");
  }

  function pintarSello() {
    const d = estado.datos;
    if (!d) return;
    const generado = d.generatedAt ? `${d.generatedAt.slice(11, 16)}` : "—";
    $("#sello").textContent = `Actualizado ${generado}${d.envivo ? " · en vivo" : ""}`;
    $("#sello").title = `Escaneo del ${d.generatedAt || "?"} · ${d.count} valores`;
    $("#sesion").textContent = d.session
      ? `Sesión del ${new Date(d.session + "T12:00:00").toLocaleDateString("es-ES", {
          weekday: "long", day: "numeric", month: "long", year: "numeric" })} · velas de ${d.label?.toLowerCase() || d.timeframe}.`
      : "";
  }

  function pintar() {
    const valores = valoresFiltrados();
    pintarSello();
    pintarSenales(valores);
    pintarCercanos(valores);
    pintarTabla(valores);
    pintarErrores();
  }

  /* ---------- Interacción ---------- */

  function pintarBotonesTf() {
    $("#tf").innerHTML = estado.timeframes
      .map((t) => `<button type="button" data-valor="${esc(t.id)}" class="${t.id === estado.tf ? "activo" : ""}">${esc(t.label)}</button>`)
      .join("");
  }

  function grupoExclusivo(contenedor, alCambiar) {
    contenedor.addEventListener("click", (ev) => {
      const boton = ev.target.closest("button[data-valor]");
      if (!boton) return;
      contenedor.querySelectorAll("button").forEach((b) => b.classList.remove("activo"));
      boton.classList.add("activo");
      alCambiar(boton.dataset.valor);
    });
  }

  function grupoMultiple(contenedor, conjunto) {
    contenedor.addEventListener("click", (ev) => {
      const boton = ev.target.closest("button[data-valor]");
      if (!boton) return;
      const valor = boton.dataset.valor;
      if (conjunto.has(valor) && conjunto.size > 0) {
        conjunto.delete(valor);
        boton.classList.remove("activo");
      } else {
        conjunto.add(valor);
        boton.classList.add("activo");
      }
      pintar();
    });
  }

  async function cambiarTimeframe(tf) {
    estado.tf = tf;
    localStorage.setItem("tf", tf);
    await refrescar();
  }

  async function refrescar({ forzar = false } = {}) {
    document.body.classList.add("cargando");
    try {
      estado.datos = await cargarDatos(estado.tf, { forzar });
      document.querySelector(".aviso")?.remove();
      pintar();
    } catch (err) {
      mostrarAviso(`No se han podido cargar los datos: ${err.message}. ` +
        `Si acabas de publicar la web, espera a que el robot haga el primer escaneo.`);
    } finally {
      document.body.classList.remove("cargando");
    }
  }

  function mostrarAviso(mensaje) {
    document.querySelector(".aviso")?.remove();
    const div = document.createElement("div");
    div.className = "aviso";
    div.textContent = mensaje;
    document.querySelector("main").prepend(div);
  }

  function aplicarTema(tema) {
    if (tema) document.documentElement.dataset.tema = tema;
    else delete document.documentElement.dataset.tema;
  }

  function iniciarEventos() {
    grupoExclusivo($("#tf"), cambiarTimeframe);
    grupoExclusivo($("#universo"), (v) => {
      estado.universo = v;
      localStorage.setItem("universo", v);
      pintar();
    });
    grupoMultiple($("#pares"), estado.pares);
    grupoMultiple($("#direcciones"), estado.direcciones);

    $("#busqueda").addEventListener("input", (ev) => {
      estado.busqueda = ev.target.value;
      pintar();
    });

    $("#recargar").addEventListener("click", () => refrescar({ forzar: true }));

    $("#tema").addEventListener("click", () => {
      const actual = document.documentElement.dataset.tema;
      const siguiente = actual === "oscuro" ? "claro" : actual === "claro" ? "" : "oscuro";
      aplicarTema(siguiente);
      siguiente ? localStorage.setItem("tema", siguiente) : localStorage.removeItem("tema");
    });

    document.querySelectorAll("#tabla th[data-orden]").forEach((th) => {
      th.addEventListener("click", () => {
        const campo = th.dataset.orden;
        estado.orden = estado.orden.campo === campo
          ? { campo, dir: estado.orden.dir === "asc" ? "desc" : "asc" }
          : { campo, dir: campo === "name" ? "asc" : "desc" };
        pintar();
      });
    });

    // Refresco automático cada 5 minutos: el robot publica cada 15.
    setInterval(() => refrescar({ forzar: true }), 5 * 60 * 1000);
  }

  async function iniciar() {
    aplicarTema(localStorage.getItem("tema"));
    document.querySelector(`#universo button[data-valor="${estado.universo}"]`)?.classList.add("activo");
    document.querySelectorAll("#universo button").forEach((b) => {
      if (b.dataset.valor !== estado.universo) b.classList.remove("activo");
    });

    await cargarIndice();
    pintarBotonesTf();
    iniciarEventos();
    await refrescar();
  }

  iniciar();
})();
