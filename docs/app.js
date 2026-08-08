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
    publicados: null, // marcos temporales que el robot llegó a publicar
    apiViva: null, // null = sin comprobar, true/false = hay servidor local de escaneo
    directoDisponible: null, // null = sin comprobar, true/false = Yahoo acepta al navegador
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

  // El índice solo dice qué marcos temporales alcanzó a publicar el robot; los
  // botones son siempre los tres, porque el escaneo desde el navegador los cubre.
  async function cargarIndice() {
    try {
      const resp = await fetch("data/index.json", { cache: "no-store" });
      if (!resp.ok) throw new Error(resp.status);
      const indice = await resp.json();
      estado.publicados = new Set((indice.timeframes || []).map((t) => t.id));
    } catch {
      estado.publicados = null;
    }
  }

  async function cargarDatos(tf, { forzar = false } = {}) {
    if (!forzar && estado.cache.has(tf)) return estado.cache.get(tf);

    // Tres orígenes, de mejor a peor: el servidor local si está en marcha, el
    // escaneo desde el propio navegador y, como último recurso, lo que publicó
    // el robot (que solo alcanza cierres diarios).
    const datos = (await servidorLocal(tf)) || (await escaneoDirecto(tf)) || (await publicado(tf));
    estado.cache.set(tf, datos);
    return datos;
  }

  // `python -m scanner.server` sirve el panel y escanea en vivo en cada petición.
  async function servidorLocal(tf) {
    if (!EN_LOCAL || estado.apiViva === false) return null;
    try {
      const resp = await fetch(`/api/scan?tf=${encodeURIComponent(tf)}&universo=todos`,
        { cache: "no-store" });
      estado.apiViva = resp.ok;
      if (!resp.ok) return null;
      const datos = await resp.json();
      datos.envivo = true;
      datos.origen = "local";
      return datos;
    } catch {
      estado.apiViva = false;
      return null;
    }
  }

  async function escaneoDirecto(tf) {
    if (!window.Mercado || estado.directoDisponible === false) return null;
    if (estado.directoDisponible === null) {
      estado.directoDisponible = await window.Mercado.disponible();
      if (!estado.directoDisponible) return null;
    }
    try {
      mostrarProgreso(0, (window.UNIVERSO || []).length);
      const datos = await window.Mercado.escanear(tf, { alProgresar: mostrarProgreso });
      datos.origen = "directo";
      return datos;
    } catch (err) {
      estado.directoDisponible = false;
      console.warn("Escaneo directo no disponible:", err);
      return null;
    } finally {
      ocultarProgreso();
    }
  }

  async function publicado(tf) {
    const meta = estado.timeframes.find((t) => t.id === tf);
    if (estado.publicados && !estado.publicados.has(tf)) {
      throw new Error(`el robot solo publica el marco diario, y este navegador no ha podido `
        + `consultar las cotizaciones de ${meta?.label || tf} directamente`);
    }
    const resp = await fetch(`data/${meta?.file || tf + ".json"}`, { cache: "no-store" });
    if (!resp.ok) throw new Error(`no hay datos publicados para ${tf} (HTTP ${resp.status})`);
    const datos = await resp.json();
    datos.origen = "publicado";
    return datos;
  }

  /* ---------- Progreso ---------- */

  function mostrarProgreso(hechos, total) {
    const barra = $("#progreso");
    barra.hidden = false;
    // El escaneo directo tarda; en cuanto empieza a avanzar se devuelve la página al usuario.
    document.body.classList.remove("cargando");
    $("#progreso-barra").style.width = total ? `${(hechos / total) * 100}%` : "0%";
    $("#progreso-texto").textContent = `Consultando cotizaciones… ${hechos}/${total}`;
  }

  function ocultarProgreso() {
    $("#progreso").hidden = true;
    $("#progreso-barra").style.width = "0%";
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

  const ORIGENES = {
    local: { texto: "En vivo · servidor local", detalle: "Escaneo hecho por python -m scanner.server" },
    directo: { texto: "En vivo · tu navegador", detalle: "Cotizaciones pedidas a Yahoo Finance desde este navegador" },
    publicado: { texto: "Publicado por el robot", detalle: "Último escaneo hecho en GitHub Actions" },
  };

  function pintarSello() {
    const d = estado.datos;
    if (!d) return;
    const generado = d.generatedAt ? `${d.generatedAt.slice(11, 16)}` : "—";
    $("#sello").textContent = `Actualizado ${generado}`;
    $("#sello").title = `Escaneo del ${d.generatedAt || "?"} · ${d.count} valores`;

    const origen = ORIGENES[d.origen] || ORIGENES.publicado;
    $("#fuente").textContent = origen.texto;
    $("#fuente").title = origen.detalle;
    $("#fuente").classList.toggle("sello--vivo", d.origen !== "publicado");

    if (d.origen === "publicado" && d.missing200) {
      mostrarAviso(`Datos de respaldo: el robot solo consigue las últimas ${
        Math.max(...(d.results || []).map((r) => r.bars || 0), 0)} sesiones diarias, ` +
        `así que en ${d.missing200} valores no hay historia suficiente para la media de 200. ` +
        `Abre el panel desde una conexión doméstica o usa el servidor local para ver los datos completos.`);
    }
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

  async function refrescar({ forzar = false, reintentar = true } = {}) {
    document.body.classList.add("cargando");
    try {
      estado.datos = await cargarDatos(estado.tf, { forzar });
      document.querySelector(".aviso")?.remove();
      pintar();
    } catch (err) {
      // Sin escaneo directo solo hay datos del marco que publica el robot:
      // se cambia a él en vez de dejar la página vacía.
      const alternativa = [...(estado.publicados || [])][0];
      if (reintentar && alternativa && alternativa !== estado.tf) {
        const previo = estado.timeframes.find((t) => t.id === estado.tf)?.label || estado.tf;
        estado.tf = alternativa;
        pintarBotonesTf();
        await refrescar({ forzar, reintentar: false });
        mostrarAviso(`No se ha podido consultar ${previo} desde este navegador, así que se ` +
          `muestra el marco que publica el robot. El servidor local sí cubre el intradía.`,
          { reemplazar: false });
        return;
      }
      mostrarAviso(`No se han podido cargar los datos: ${err.message}.`);
    } finally {
      document.body.classList.remove("cargando");
    }
  }

  function mostrarAviso(mensaje, { reemplazar = true } = {}) {
    if (reemplazar) document.querySelectorAll(".aviso").forEach((n) => n.remove());
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

    $("#recargar").addEventListener("click", () => {
      // Recargar a mano vuelve a intentar el escaneo en vivo aunque antes fallara.
      estado.directoDisponible = null;
      estado.apiViva = null;
      refrescar({ forzar: true });
    });

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
