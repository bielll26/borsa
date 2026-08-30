# Prompt maestro — Hero, sistema de color y sistema tipográfico
**Web de marca personal · one-page · dark-first · en español**

Referencias de dirección: **samu-webart.com** (estructura general, escala tipográfica, ritmo de
página) y **southprojects.dev** (paleta, flujo de briefing en 9 pasos, agenda con Cal.com).

> **Alcance de este documento:** especifica al 100% la **barra superior + el hero**, y define
> completos el **sistema de color** y el **sistema tipográfico** de toda la web (no solo del hero),
> porque son la base sobre la que se construirán las secciones siguientes.
> El cuestionario de 9 pasos y la integración de Cal.com se implementan en fases posteriores;
> aquí se dejan definidos su contrato de disparo, sus stubs y su comportamiento esperado.

---

## Índice

0. [Briefing para quien ejecuta el prompt](#0-briefing-para-quien-ejecuta-el-prompt)
1. [Principios de dirección de arte](#1-principios-de-dirección-de-arte)
2. [Sistema de color](#2-sistema-de-color)
3. [Sistema tipográfico](#3-sistema-tipográfico)
4. [Espaciado, rejilla y breakpoints](#4-espaciado-rejilla-y-breakpoints)
5. [Barra superior (header)](#5-barra-superior-header)
6. [El hero](#6-el-hero)
7. [Componentes: botones](#7-componentes-botones)
8. [Copy](#8-copy)
9. [Movimiento y animación](#9-movimiento-y-animación)
10. [Accesibilidad](#10-accesibilidad)
11. [Rendimiento](#11-rendimiento)
12. [Contrato con las fases siguientes](#12-contrato-con-las-fases-siguientes)
13. [Arquitectura de archivos y entregables](#13-arquitectura-de-archivos-y-entregables)
14. [Checklist de QA antes de dar por cerrado el hero](#14-checklist-de-qa-antes-de-dar-por-cerrado-el-hero)
15. [Anti-patrones: qué NO hacer](#15-anti-patrones-qué-no-hacer)
16. [Anexo A — CSS de referencia (tokens listos para pegar)](#anexo-a--css-de-referencia-tokens-listos-para-pegar)
17. [Anexo B — Marcado de referencia](#anexo-b--marcado-de-referencia)
18. [Anexo C — JS de referencia](#anexo-c--js-de-referencia)
19. [Anexo D — Decisiones abiertas](#anexo-d--decisiones-abiertas)

---

## 0. Briefing para quien ejecuta el prompt

Eres un **desarrollador front-end senior con criterio de dirección de arte**. No estás montando una
plantilla: estás construyendo la primera impresión de un profesional que vende trabajo de diseño y
desarrollo. Si el hero parece genérico, el resto de la web ya no importa.

**Stack objetivo (elige uno y sé consistente):**

- **Opción A — Vanilla (recomendada para esta fase):** HTML semántico + CSS moderno (custom
  properties, `clamp()`, CSS Grid, `:has()`, container queries si hacen falta) + un único archivo JS
  ES-module sin dependencias. Es la opción por defecto: el hero no necesita framework y el coste de
  arranque es cero.
- **Opción B — Next.js (App Router) + Tailwind:** solo si el proyecto crecerá a CMS o rutas
  múltiples. En ese caso los tokens del §2 y §3 se declaran en `globals.css` como custom properties
  y se exponen en `tailwind.config` mediante `theme.extend`; **prohibido** usar valores arbitrarios
  de Tailwind (`text-[#E8A33D]`) fuera de los tokens.

**Restricciones duras:**

- Mobile-first real: se diseña a 390px y se escala hacia arriba, no al revés.
- Dark-first: no existe tema claro. `color-scheme: dark` declarado.
- Sin librerías de UI (Bootstrap, MUI, shadcn) ni de animación pesadas. GSAP se admite **solo** si
  la cascada de entrada del H1 lo justifica; si CSS lo resuelve, CSS gana.
- Sin imágenes decorativas en el hero. El impacto lo da la tipografía y el vacío.
- **Una sola lengua: español.** No hay conmutador de idioma ni versión en inglés. El texto puede
  ir directo en el marcado; si prefieres centralizarlo en un objeto de copys, hazlo por comodidad de
  edición, no por i18n.

---

## 1. Principios de dirección de arte

Cinco principios que resuelven cualquier duda que este documento no cubra explícitamente:

1. **El vacío es contenido.** Si dudas entre rellenar o dejar aire, deja aire. El hero debe respirar:
   más del 55% del viewport es negro sin nada encima.
2. **Una sola voz tipográfica fuerte.** Un titular gigantesco manda; todo lo demás es soporte y va
   deliberadamente pequeño y silencioso. Nada compite con el H1.
3. **Un solo acento.** El ámbar es la firma de la marca. Cuanto menos aparece, más vale. Un acento
   que está en todas partes deja de ser acento.
4. **Rectitud, no redondez.** Esquinas casi rectas (2px), bordes de 1px, hairlines. Nada de cápsulas,
   sombras difusas ni tarjetas flotantes. El lenguaje es editorial/estudio, no SaaS.
5. **El movimiento explica, no decora.** Cada animación debe justificar por qué existe: jerarquiza la
   lectura o comunica estado. Si solo "queda bonito", se elimina.

---

## 2. Sistema de color

### 2.1 Tokens primitivos

Estos son los valores crudos. **Nunca se usan directamente en componentes**; se consumen a través de
los tokens semánticos del §2.2.

| Primitivo | Hex | Notas |
|---|---|---|
| `--black-950` | `#000000` | Negro puro, fondo global |
| `--black-900` | `#0A0A0A` | Texto sobre superficies claras |
| `--black-850` | `#0B0B0B` | Superficie elevada nivel 1 |
| `--black-800` | `#121212` | Superficie elevada nivel 2 (dropdown, modal) |
| `--black-700` | `#1C1C1C` | Bordes y hairlines |
| `--black-600` | `#2A2A2A` | Bordes en hover, divisores de más peso |
| `--cream-100` | `#F5F1E8` | Crema principal — sustituye al blanco |
| `--cream-200` | `#E4DFD4` | Crema en estado pressed |
| `--grey-400` | `#9A968E` | Texto secundario |
| `--grey-600` | `#5C5952` | Texto terciario / deshabilitado |
| `--amber-400` | `#F2B457` | Ámbar claro (hover) |
| `--amber-500` | `#E8A33D` | **Ámbar de marca** |
| `--amber-600` | `#C98A2C` | Ámbar oscuro (pressed) |
| `--red-500` | `#E5533D` | Error de validación (solo formularios, fases futuras) |
| `--green-500` | `#5BB98C` | Éxito / disponibilidad |

### 2.2 Tokens semánticos

Esta es la capa que consume el CSS de los componentes.

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `--black-950` | Fondo de página y del hero |
| `--bg-elev-1` | `--black-850` | Header con scroll, tarjetas |
| `--bg-elev-2` | `--black-800` | Overlays, dropdown de país, modal del briefing |
| `--border` | `--black-700` | Hairline por defecto (1px) |
| `--border-strong` | `--black-600` | Borde en hover de elementos interactivos |
| `--fg` | `--cream-100` | Texto principal, H1, wordmark |
| `--fg-muted` | `--grey-400` | Subtítulo del hero, descripciones, texto secundario |
| `--fg-faint` | `--grey-600` | Metadatos, contadores, placeholders |
| `--accent` | `--amber-500` | CTA activo, contador de pasos, barra de progreso, foco |
| `--accent-hover` | `--amber-400` | Hover sobre superficie ámbar |
| `--accent-press` | `--amber-600` | Pressed sobre superficie ámbar |
| `--on-accent` | `--black-900` | Texto sobre ámbar |
| `--on-cream` | `--black-900` | Texto sobre crema |
| `--focus-ring` | `--amber-500` | Anillo de foco (2px sólido + 2px offset) |
| `--selection-bg` | `--amber-500` | `::selection` |
| `--selection-fg` | `--black-900` | `::selection` |

### 2.3 Reglas de uso del color (no negociables)

1. **Blanco puro prohibido.** `#FFFFFF` produce halo sobre negro puro y rompe la calidez de la
   paleta. Todo texto claro usa `--fg`.
2. **Presupuesto de acento: 3 elementos como máximo en el hero.** En la composición por defecto son:
   (a) la barra de progreso inferior, (b) el contador de pasos del cuestionario y (c) el estado
   "listo" del botón primario. Si se quiere teñir una palabra del H1 en ámbar, hay que **retirar** uno de los
   tres anteriores. El CTA primario en reposo es crema, no ámbar.
3. **Sin degradados de marca, sin glassmorphism, sin sombras de color, sin `box-shadow` difusas.**
   La profundidad se consigue con espaciado, contraste tipográfico y hairlines.
4. **Contraste mínimo:** texto normal ≥ 4.5:1 sobre su fondo; texto ≥ 24px o ≥ 19px bold ≥ 3:1.
   `--fg-faint` solo para texto no esencial y nunca por debajo de 14px.
   Ratios verificados sobre `--bg`: `--fg` ≈ 17.5:1 · `--fg-muted` ≈ 8.1:1 · `--fg-faint` ≈ 3.3:1
   (solo texto grande/no esencial) · `--accent` ≈ 9.4:1.
5. **Estados de superficie:**
   - Botón primario en reposo: fondo `--fg`, texto `--on-cream`.
   - Botón primario en hover: fondo `--accent`, texto `--on-accent`.
   - Botón primario cuando el paso está **validado/accionable** (patrón de South Projects, donde el
     "Next" se vuelve ámbar al haber respuesta): fondo `--accent` ya en reposo.
   - Botón secundario: transparente + `1px solid var(--fg)`; en hover, fondo `--fg` y texto
     `--on-cream` (inversión, no relleno translúcido).
6. **`prefers-contrast: more`:** sube `--fg-muted` a `--cream-200` y `--border` a `--border-strong`.
7. **`forced-colors: active` (modo alto contraste de Windows):** no fuerces colores; deja que el
   sistema tome el control y garantiza que los bordes de los botones siguen siendo visibles con
   `border: 1px solid transparent` como base.
8. **Sin tema claro.** No implementes toggle. `color-scheme: dark` en `:root`, y
   `<meta name="theme-color" content="#000000">`.

---

## 3. Sistema tipográfico

Dos familias. Una **display condensada ultra-bold** para titulares; una **grotesque geométrica
neutra** para todo lo demás. Ninguna tercera familia, bajo ningún concepto.

### 3.1 Familias

**Display / titulares**

- Primera opción: **Anton** (Google Fonts, un solo peso). Condensada, negrísima, mayúsculas,
  exactamente el registro de las capturas de referencia.
- Alternativas admitidas: **Archivo Black** (más ancha, más americana) o **Bebas Neue** (más
  estrecha y ligera de color).
- Stack: `"Anton", "Archivo Black", "Haettenschweiler", "Arial Narrow Bold", Impact, sans-serif`.
- Se usa **siempre** con `text-transform: uppercase`, `letter-spacing: -0.015em`,
  `line-height: 0.9`, `font-weight: 400` (la fuente ya es black; nunca apliques `bold` sintético).

**Texto / UI**

- Primera opción: **Poppins** (400 / 500 / 600). Geométrica, redonda, legible, coincide con el
  cuerpo de texto de las capturas.
- Alternativa: **Outfit** (más neutra y ligeramente más estrecha).
- Stack: `"Poppins", "Outfit", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`.
- `line-height: 1.55`, `letter-spacing: 0`, `font-feature-settings: "kern" 1`.

**Carga de fuentes**

- Solo los pesos usados: display 400; texto 400, 500, 600. Nada más.
- `font-display: swap` en todas.
- Subset `latin` + `latin-ext` (hay contenido en ES y CA: acentos, `ñ`, `ç`).
- `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` y
  `<link rel="preload" as="font" type="font/woff2" crossorigin>` **solo** para el `.woff2` de la
  display (es la que causa el LCP).
- Define `size-adjust`/`ascent-override` en una `@font-face` de fallback local para que el swap no
  provoque salto de layout (CLS 0).

### 3.2 Escala tipográfica fluida

| Token | Rol | Familia | Tamaño | Peso | Tracking | Leading |
|---|---|---|---|---|---|---|
| `--fs-display` | H1 del hero | Display | `clamp(3.25rem, 11vw, 9rem)` | 400 | `-0.02em` | `0.9` |
| `--fs-h2` | Titulares de sección | Display | `clamp(2rem, 6vw, 4rem)` | 400 | `-0.015em` | `0.95` |
| `--fs-h3` | Subtitulares | Display | `clamp(1.5rem, 3.5vw, 2.25rem)` | 400 | `-0.01em` | `1` |
| `--fs-lead` | Subtítulo del hero | Texto | `clamp(1.05rem, 2.2vw, 1.375rem)` | 400 | `0` | `1.5` |
| `--fs-body` | Cuerpo | Texto | `1rem` | 400 | `0` | `1.6` |
| `--fs-small` | Notas, ayudas | Texto | `0.875rem` | 400 | `0` | `1.5` |
| `--fs-ui` | Botones, nav | Texto | `0.9375rem` | 500 | `0.01em` | `1` |
| `--fs-eyebrow` | Eyebrow, labels | Texto | `0.75rem` | 600 | `0.18em` | `1` |
| `--fs-counter` | Contador `1 / 9` | Texto | `1rem` | 500 | `0.06em` | `1` |

### 3.3 Reglas de composición

1. **El H1 rompe línea de forma intencionada**, nunca al azar. Usa `<span class="line">` por línea
   (necesario además para la animación de máscara) o `max-width` en `ch` con `text-wrap: balance`.
   Objetivo: **3–4 líneas en móvil, 2–3 en desktop**. Ninguna línea debe quedar huérfana con una
   sola palabra corta.
2. **Medida de lectura:** el subtítulo nunca supera `34ch`; el cuerpo, `68ch`.
3. **`text-wrap: pretty`** en párrafos, `text-wrap: balance` en titulares de 2–3 líneas cortas.
4. **Números tabulares** (`font-variant-numeric: tabular-nums`) en el contador de pasos y en la barra
   de progreso, para que no bailen al cambiar de cifra.
5. **Sin cursivas y sin subrayados decorativos.** El énfasis se hace con color (`--accent`) o
   tamaño, jamás con `<i>`.
6. **Mayúsculas solo en display y eyebrow.** El cuerpo nunca va en mayúsculas.
7. **`hyphens: none`** en titulares (una display partida con guión es un error de composición);
   `hyphens: auto` admitido en cuerpo de texto en móvil estrecho.

---

## 4. Espaciado, rejilla y breakpoints

### 4.1 Escala de espaciado (base 4px)

`--space-1: 4px` · `--space-2: 8px` · `--space-3: 12px` · `--space-4: 16px` · `--space-5: 24px` ·
`--space-6: 32px` · `--space-7: 40px` · `--space-8: 56px` · `--space-9: 72px` ·
`--space-10: 96px` · `--space-11: 128px` · `--space-12: 176px`

Todo margen y padding sale de esta escala. Cero valores sueltos.

### 4.2 Contenedor y rejilla

- `--container-max: 1240px`, `margin-inline: auto`.
- `--gutter: clamp(20px, 5vw, 64px)` como `padding-inline`.
- Rejilla de **12 columnas** a partir de 1024px, `gap: 24px`. En el hero, el bloque de texto ocupa
  **columnas 1–8**; las columnas 9–12 quedan **vacías a propósito** o alojan el detalle discreto
  de disponibilidad (§6.1, punto 8).
- Entre 640 y 1023px: 6 columnas, el texto ocupa 1–5.
- Por debajo de 640px: columna única.

### 4.3 Breakpoints

| Nombre | Min-width | Notas |
|---|---|---|
| `xs` | 0 | 390px es el ancho de diseño de referencia |
| `sm` | 480px | Móviles grandes |
| `md` | 640px | Los CTAs pasan de apilados a fila |
| `lg` | 1024px | El hero pasa de centrado a alineado a la izquierda; rejilla de 12 |
| `xl` | 1280px | Se activa el `--container-max`; crece el ritmo vertical |
| `2xl` | 1536px | Solo aumenta el espaciado, **nunca** el tamaño de fuente por encima del `clamp` |

### 4.4 Ritmo vertical del hero

| Par de bloques | Móvil | Desktop (≥1024px) |
|---|---|---|
| Borde superior → inicio del contenido | `12vh` (mín. `--space-9`) | `18vh` |
| Eyebrow → H1 | `--space-5` (24px) | `--space-6` (32px) |
| H1 → subtítulo | `--space-6` (32px) | `--space-7` (40px) |
| Subtítulo → fila de CTAs | `--space-7` (40px) | `--space-8` (56px) |
| CTAs → borde inferior | `--space-10` mínimo | `--space-11` mínimo |

---

## 5. Barra superior (header)

Réplica estructural de la barra de las capturas de South Projects, adaptada a marca personal.

### 5.1 Anatomía

```
┌──────────────────────────────────────────────────────────────┐
│  ✳ WORDMARK                             [ Contacto → ]       │
└──────────────────────────────────────────────────────────────┘
```

1. **Logotipo + wordmark (izquierda).** Bloque de dos piezas:
   - **Mascota (marca gráfica).** El logo facilitado: una **cara de personaje estilo cómic/manga,
     monocroma en blanco sobre negro**, con contorno grueso, flequillo puntiagudo, cejas marcadas,
     gafas de sol redondeadas y boca pequeña. Es la firma visual de la marca y **sustituye al glifo
     ámbar** que se describía antes (ver §5.3 para su tratamiento completo).
     Tamaño en el header: **28px de alto** en móvil, **32px** en ≥1024px, ancho automático.
   - **Wordmark.** El nombre de marca en tipografía **display**, mayúsculas, `--fs-ui` escalado a
     `clamp(1.125rem, 2.4vw, 1.5rem)`, color `--fg`, `letter-spacing: -0.01em`.
   Orden: **mascota a la izquierda, wordmark a su derecha**, alineados por el eje óptico (no por la
   caja), separación `--space-3` (12px). Todo el bloque es un único enlace a `/` con
   `aria-label` = nombre + " — inicio", y la mascota lleva `aria-hidden="true"` para no duplicar la
   lectura.
2. **Centro: vacío.** No hay navegación ni conmutador de idioma. El header es solo marca a la
   izquierda y acción a la derecha; el espacio intermedio se deja libre a propósito.
3. **Botón de contacto (derecha).** Botón secundario **en variante crema sólida** (fondo `--fg`,
   texto `--on-cream`), `--fs-ui`, `padding: 12px 20px`, `border-radius: 2px`. En las capturas es el
   "Go back" con flecha; aquí lleva una flecha `→` inline a la derecha del texto (SVG, `currentColor`,
   16px). Acción: hace scroll suave a la sección de contacto o abre el popup de Cal.com — ver §12.

### 5.2 Comportamiento

- Posición: `position: fixed; inset-block-start: 0; inline-size: 100%; z-index: 100`.
- Altura: `72px` en móvil, `88px` en ≥1024px. Alineación vertical centrada,
  `padding-inline: var(--gutter)`.
- **En reposo (scroll = 0):** fondo transparente, sin borde.
- **Con scroll > 24px:** fondo `--bg-elev-1`, hairline inferior `1px solid var(--border)`,
  transición de `background-color` y `border-color` en `240ms ease-out`.
  Detectado con `IntersectionObserver` sobre un sentinel de 24px al inicio del `<body>`,
  **no** con listener de `scroll` (evita jank).
- **Sin `backdrop-filter`.** Fondo sólido.
- No se oculta al hacer scroll hacia abajo: siempre visible.
- En viewports < 480px, si los tres elementos no caben, el botón de contacto reduce su texto a solo
  la flecha con `aria-label` intacto — **nunca** se colapsa en un menú hamburguesa (no hay
  navegación que esconder).

---

### 5.3 Tratamiento de la mascota (marca gráfica)

El logo entregado es un **personaje monocromo de trazo grueso**: cara redondeada, flequillo en
punta, cejas gruesas inclinadas, gafas de sol de lentes anchas y boca pequeña, todo en blanco sobre
fondo negro. Encaja de forma natural con la paleta del §2 porque ya es un activo blanco/negro.

**Reglas de uso:**

1. **Formato: SVG.** Vectoriza el archivo entregado (llega como JPG). Nada de PNG ni JPG en el
   header: el trazo debe verse nítido a cualquier densidad y el archivo debe pesar < 4 KB.
2. **Color: `currentColor`.** Los trazos del SVG usan `fill="currentColor"` y heredan `--fg`
   (`#F5F1E8`), **no** blanco puro. Así la mascota queda exactamente en el mismo crema que el
   wordmark y no chirría.
3. **Fondo transparente.** Elimina el fondo negro del JPG original; el logo se recorta sobre el
   `--bg` de la página.
4. **Área de respeto:** un margen libre alrededor igual al **25% de su altura**. Nada invade ese
   espacio.
5. **Tamaño mínimo:** 24px de alto. Por debajo, las gafas y las cejas se empastan y el logo deja de
   leerse: en ese caso, usa solo el wordmark.
6. **Prohibido:** teñir la mascota de ámbar, aplicarle degradados, sombras, contornos adicionales,
   rotarla, deformarla o encerrarla en un círculo o cuadrado de color.
7. **Otros usos previstos:** `favicon` (SVG + fallback ICO 32×32 y PNG 180×180 para
   `apple-touch-icon`), imagen de `og:image` (mascota centrada sobre `--bg` en 1200×630) y marca de
   agua opcional a gran tamaño y muy bajo contraste (`--black-800`) en secciones futuras — **nunca
   en el hero**, que se mantiene limpio.
8. **Animación permitida (opcional, discreta):** un parpadeo de las gafas o un ligero
   `translateY` de 2px al hacer hover sobre el wordmark, `200ms`. Desactivado con
   `prefers-reduced-motion`. Nada más.

El archivo original entregado queda guardado en `marca-personal/assets/logo-mascota.jpg` como
referencia para la vectorización.

---

## 6. El hero

### 6.1 Anatomía, de arriba abajo

1. **Espacio negativo superior.** Mínimo `18vh` en desktop, `12vh` en móvil, por debajo del header.
   Es estructura, no relleno: no lo reduzcas para "que quepa todo".
2. **Eyebrow** (opcional pero recomendado). Una línea, `--fs-eyebrow`, `--fg-muted`, mayúsculas,
   `letter-spacing: 0.18em`. Formato: rol · ubicación.
   Ejemplo: `DISEÑO Y DESARROLLO WEB · BARCELONA`.
3. **H1.** El elemento dominante. Tipografía display, `--fs-display`, `--fg`, mayúsculas.
   4–7 palabras. Alineado al centro por debajo de 1024px; a la izquierda a partir de ahí.
   Cada línea envuelta en `<span class="hero__line"><span>…</span></span>` para la animación de
   máscara. Como máximo **una** palabra en `--accent`, y solo si se retira otro uso del acento (§2.3).
4. **Subtítulo.** `--fs-lead`, `--fg-muted`, `max-width: 34ch`. Una o dos frases que digan **qué
   haces y para quién**, en lenguaje concreto. Prohibidos los adjetivos vacíos.
5. **Fila de CTAs.** Dos botones (§7):
   - **Primario — "Empezar un proyecto"** → abre el cuestionario de 9 pasos.
   - **Secundario — "Agendar una llamada"** → abre el popup de Cal.com.
   Móvil: apilados, ancho completo, `gap: var(--space-3)`, primario arriba.
   ≥640px: en fila, alineados a la izquierda (o centrados si el hero está centrado),
   `gap: var(--space-4)`.
6. **Micro-nota bajo los CTAs** (opcional, `--fs-small`, `--fg-faint`):
   "Respuesta en menos de 24 h" / "Sin compromiso". Una línea como mucho.
7. **Barra de progreso inferior.** Hairline de **3px** anclada al borde inferior del viewport
   (`position: fixed; inset-block-end: 0`), fondo `--border`, con un segmento `--accent` cuyo
   `transform: scaleX()` sigue el progreso de scroll de la página. Es el mismo elemento que en las
   capturas indica el avance `1/9` del cuestionario, reutilizado como progreso de lectura.
   Se oculta con `prefers-reduced-motion: reduce`.
   Actualizada con `requestAnimationFrame` + `transform` (jamás animando `width`).
8. **Detalle de disponibilidad (columnas 9–12, solo ≥1024px).** Un punto `●` de 8px en
   `--green-500` con `--fs-eyebrow` en `--fg-muted`: `DISPONIBLE PARA PROYECTOS · Q4 2026`.
   Alineado al borde superior del bloque de texto. Si no hay disponibilidad real que comunicar,
   **deja las columnas vacías** en lugar de inventar contenido.

### 6.2 Medidas y layout

- `min-block-size: 100svh` (usa `svh`, **no** `vh`: en Safari iOS `vh` provoca salto al ocultarse la
  barra del navegador). Fallback `min-height: 100vh` antes de la declaración `svh`.
- `display: grid; align-content: center;` dentro del contenedor.
- `padding-block-start` igual a la altura del header + el espacio negativo del punto 1.
- El hero **no** debe requerir scroll para ver los CTAs en ningún viewport ≥ 568px de alto.
  Verifícalo a 390×667 (iPhone SE) y a 360×640.

### 6.3 Estados y casos límite

- **Viewport muy bajo (< 600px de alto, p. ej. móvil en horizontal):** reduce el espacio negativo
  superior a `6vh`, baja `--fs-display` un escalón con una media query de `(max-height: 600px)`,
  y permite que el hero use `min-block-size: auto`.
- **Copy largo:** el español es una lengua larga. Comprueba la composición del H1 con el copy
  definitivo, no con el placeholder, y ajusta los saltos de línea a mano (§8).
- **Fallo de carga de fuentes:** con el fallback ajustado por `size-adjust` el layout no debe saltar.
  Comprueba con las fuentes bloqueadas en DevTools.
- **JS deshabilitado:** el hero se ve completo y los CTAs siguen siendo utilizables — el primario
  hace fallback a un enlace `mailto:` o a `/briefing` y el secundario al enlace directo de Cal.com.
  Envuelve la mejora en `<noscript>` o usa `<a>` progresivamente mejorado a `<button>`.

---

## 7. Componentes: botones

### 7.1 Variantes

| Variante | Fondo | Texto | Borde | Uso |
|---|---|---|---|---|
| `.btn--primary` | `--fg` | `--on-cream` | ninguno | CTA principal del hero |
| `.btn--primary.is-ready` | `--accent` | `--on-accent` | ninguno | Paso validado (patrón South Projects) |
| `.btn--secondary` | transparente | `--fg` | `1px solid var(--fg)` | CTA secundario, "Back" |
| `.btn--ghost` | transparente | `--fg-muted` | ninguno | Acciones terciarias |

### 7.2 Medidas

- Alto mínimo: **56px** en desktop, **64px** en móvil (ancho completo).
- Padding desktop: `20px 36px`. `border-radius: 2px`. **Nunca cápsulas.**
- `--fs-ui` (15px / peso 500), `letter-spacing: 0.01em`, sin mayúsculas.
- Área táctil mínima 44×44px en cualquier variante, incluidos iconos sueltos.

### 7.3 Estados (todos obligatorios)

- **Hover:** primario → fondo `--accent`, texto `--on-accent`. Secundario → inversión a fondo `--fg`
  con texto `--on-cream`. Transición `180ms ease-out` sobre `background-color`, `color`,
  `border-color`. **Sin `transform: scale`, sin rebotes, sin elevación.**
- **Focus-visible:** `outline: 2px solid var(--focus-ring); outline-offset: 2px`. Visible en
  **todas** las variantes, incluida la primaria sobre crema.
- **Active/pressed:** primario → `--accent-press`; secundario → fondo `--cream-200`.
- **Disabled:** `opacity: .45; pointer-events: none;` + `aria-disabled="true"`. No uses solo color
  para comunicar el estado.
- **Loading** (para las fases futuras): texto sustituido por un indicador de 3 puntos en
  `currentColor`, ancho del botón **fijado** para que no salte, `aria-busy="true"`.

---

## 8. Copy

### 8.1 Mecánica

- **La web es solo en español.** No hay conmutador de idioma, ni versión en inglés, ni capa de i18n.
  `<html lang="es">` fijo.
- El texto puede escribirse directamente en el marcado. Si aun así prefieres centralizarlo, usa un
  objeto plano en `src/copy.js` con claves por slot (`hero.eyebrow`, `hero.h1.lines`, `hero.lead`,
  `cta.primary`, `cta.secondary`, `hero.note`, `header.contact`) — pero es una comodidad de edición,
  no un requisito.
- El H1 se define como **array de líneas** para controlar los saltos a mano; ese es el único motivo
  para no escribirlo como un string suelto.

### 8.2 Copy de referencia (sustituir por el definitivo, no publicar tal cual)

- Eyebrow: `DISEÑO Y DESARROLLO WEB · BARCELONA`
- H1 (3 líneas): `WEBS QUE` / `NO PARECEN` / `PLANTILLAS`
- Lead: `Diseño y construyo webs a medida para marcas y profesionales que necesitan destacar. De la idea al deploy.`
- CTA primario: `Empezar un proyecto`
- CTA secundario: `Agendar una llamada`
- Nota: `Respuesta en menos de 24 h · Sin compromiso`
- Header contacto: `Contacto`
- Disponibilidad: `DISPONIBLE PARA PROYECTOS · Q4 2026`

> Este copy es **placeholder de estructura**, elegido para validar longitudes y saltos de línea.
> Debe sustituirse por el copy real antes de publicar; no lo tomes como el mensaje definitivo de la
> marca.

---

## 9. Movimiento y animación

### 9.1 Secuencia de entrada (al cargar)

Cascada única, ejecutada una sola vez por sesión (`sessionStorage` para no repetirla al volver):

| Orden | Elemento | Retardo | Transición |
|---|---|---|---|
| 1 | Header (fade) | 0ms | `opacity 400ms ease-out` |
| 2 | Eyebrow | 120ms | `opacity + translateY(16px→0)`, 480ms |
| 3 | H1 línea 1 | 190ms | máscara: `translateY(100%→0)` sobre `overflow:hidden`, 560ms |
| 4 | H1 línea 2 | 260ms | ídem |
| 5 | H1 línea 3 | 330ms | ídem |
| 6 | Subtítulo | 430ms | `opacity + translateY(20px→0)`, 520ms |
| 7 | CTAs (juntos) | 520ms | `opacity + translateY(24px→0)`, 520ms |
| 8 | Nota + disponibilidad | 620ms | `opacity`, 400ms |

- Easing global: `cubic-bezier(.22, 1, .36, 1)`.
- Anima **solo** `opacity` y `transform`. Nada de `top`, `height`, `width` o `filter`.
- Promociona a capa con `will-change: transform, opacity` **solo mientras dura la animación**, y
  retíralo en `transitionend`.
- Estado inicial aplicado con una clase `.js-anim` puesta por JS en `<html>`: si el JS no carga,
  todo se ve en su estado final (nunca contenido invisible por CSS).

### 9.2 Interacciones continuas

- **Hover de CTAs:** `180ms ease-out`, solo color.
- **Barra de progreso:** `transform: scaleX()` con `transform-origin: left`, actualizada en `rAF`
  con el valor `scrollY / (scrollHeight - innerHeight)`, redondeado a 3 decimales.
- **Header con scroll:** `240ms ease-out`.

### 9.3 `prefers-reduced-motion: reduce`

Obligatorio y completo:

- Todos los elementos aparecen directamente en su estado final (sin `translate`, sin máscara).
- La barra de progreso se oculta (`display: none`).
- Las transiciones de hover se reducen a `0.01ms` mediante la regla global de reset.
- El scroll suave del header pasa a `scroll-behavior: auto`.

---

## 10. Accesibilidad

Nivel objetivo: **WCAG 2.2 AA**, verificado, no asumido.

1. **Semántica:** `<header>` para la barra; `<main>` con `<section aria-labelledby="hero-title">`;
   un único `<h1 id="hero-title">` en toda la página.
2. **El H1 debe leerse como una frase continua** pese a estar troceado en `<span>` por línea: los
   spans no llevan `aria-hidden` ni roles, y las líneas terminan con un espacio real o se separa el
   texto con `&#32;` para que el lector de pantalla no pegue palabras.
3. **CTAs que abren overlays son `<button type="button">`**, nunca `<a href="#">`. Si además existe
   una URL real de fallback, usa `<a>` con `role` intacto y previene el default con JS.
4. **Foco:** visible siempre (`:focus-visible`), nunca `outline: none` sin sustituto. Orden de
   tabulación natural: wordmark → contacto → CTA primario → CTA secundario.
5. **Skip link** como primer elemento focusable: "Saltar al contenido", oculto visualmente hasta
   recibir foco, y entonces mostrado sobre el header con fondo `--accent`.
6. **Áreas táctiles ≥ 44×44px** (WCAG 2.2 §2.5.8) en todo elemento interactivo.
7. **Sin trampas de foco**; sin `tabindex` positivos.
8. **Contraste verificado** con herramienta, no a ojo, para las 5 combinaciones del §2.3 punto 4.
9. **Zoom al 200% y `text-spacing`**: el hero no debe cortar contenido ni provocar scroll
    horizontal. Prueba con el bookmarklet de text-spacing de WCAG.
10. **`prefers-reduced-motion`** implementado (§9.3).
11. **`<html lang="es">`** y `<title>` correctos y descriptivos.

---

## 11. Rendimiento

Objetivos medidos en Lighthouse mobile, throttling 4G, y con WebPageTest si es posible:

| Métrica | Objetivo |
|---|---|
| LCP | < 1.8 s |
| CLS | 0 (cero, no "bueno") |
| INP | < 120 ms |
| JS del hero (comprimido) | < 8 KB |
| CSS crítico | < 14 KB inline |
| Peticiones para el primer render | ≤ 4 |

Prácticas obligatorias:

- **Sin imágenes en el hero.** Si por decisión posterior se añade una, debe ser AVIF con fallback
  WebP, `loading="eager"`, `fetchpriority="high"`, `decoding="async"`, con `width`/`height`
  explícitos y `aspect-ratio` en CSS.
- **CSS crítico inline** en `<head>` para el hero; el resto diferido.
- **Fuentes:** preload solo del `.woff2` de la display; el resto con `swap` y métricas de fallback
  ajustadas.
- **Cero librerías de terceros en el primer render.** El script de Cal.com se carga **bajo demanda**,
  al hacer clic en "Agendar una llamada" — nunca en el `<head>` (§12).
- **Sin analítica bloqueante.** Si se añade, que sea diferida y sin cookies.
- El JS del hero es un único módulo con `defer`; no toca el DOM antes del primer paint salvo para
  poner la clase `.js-anim` en `<html>` (script inline mínimo, síncrono, de 1 línea).

---

## 12. Contrato con las fases siguientes

Esta fase **no implementa** el cuestionario ni la agenda, pero deja el contrato cerrado para que la
siguiente no tenga que tocar el hero.

### 12.1 Cuestionario de 9 pasos (fase 2)

- Disparador: `document.querySelector('[data-action="briefing"]')` → llama a `openBriefing()`.
- `openBriefing()` en esta fase es un **stub** que hace `console.info('briefing:open')` y, si no hay
  implementación, navega a `/briefing` como fallback.

#### 12.1.1 Chrome común a todos los pasos

Tomado literalmente de las capturas de South Projects:

- Overlay a pantalla completa sobre `--bg`, con el **mismo header** (logo + wordmark, conmutador
  y, en lugar del CTA de contacto, un botón crema **"← Volver"** con flecha a la izquierda que
  cierra el cuestionario).
- **Contador `n / 9`** centrado sobre el titular: el número actual en `--accent`, la barra `/` y el
  total en `--fg-faint`, `--fs-counter`, con `font-variant-numeric: tabular-nums`.
- **Titular de la pregunta** en tipografía **display**, mayúsculas, centrado,
  `clamp(2rem, 7vw, 3.25rem)`, `line-height: 0.95`. Rompe en 2 líneas como máximo.
- **Texto de ayuda** opcional bajo el titular: `--fs-body`, `--fg-muted`, centrado, `max-width: 42ch`.
- **Campo de entrada minimalista:** sin caja ni fondo, solo **hairline inferior de 1px** en `--fg`,
  texto centrado en `--fs-lead` color `--fg`, placeholder en `--fg-faint`. Al recibir foco, la
  hairline pasa a `--accent` con transición de 180ms. Nunca `outline` por defecto del navegador:
  sustitúyelo por ese cambio de línea **más** un `outline` visible para teclado.
- **Botones de navegación:** `Atrás` (secundario, borde `--fg`) a la izquierda y `Siguiente`
  (primario) a la derecha, en fila, mismo ancho, `gap: var(--space-4)`. En el paso 1 no hay `Atrás`
  y el `Siguiente` ocupa el ancho completo.
- **Regla de color del `Siguiente`** (visible en las capturas): permanece **crema** mientras el paso
  no está respondido/validado y pasa a **ámbar** (`.is-ready`) en cuanto hay una respuesta válida.
  Es el único feedback de validación en pasos no obligatorios.
- **Barra de progreso inferior de 3px** que avanza `n/9` — el mismo componente que el hero,
  reutilizado con la fuente de progreso cambiada.
- **Transición entre pasos:** salida `opacity → 0` + `translateX(-24px)` y entrada desde
  `translateX(24px)`, `320ms var(--ease)`; en sentido inverso al pulsar `Atrás`. Anulada con
  `prefers-reduced-motion`.
- **Teclado:** `Enter` avanza al paso siguiente si es válido (salvo en el textarea del paso 5, donde
  `Enter` hace salto de línea y se avanza con `Cmd/Ctrl+Enter`); `Esc` pide confirmación de cierre.
- **Foco:** al cambiar de paso, el foco va al campo de entrada; el titular se anuncia mediante una
  región `aria-live="polite"`. El overlay es un `role="dialog" aria-modal="true"` con trampa de foco
  y bloqueo de scroll del fondo.
- **Persistencia:** todas las respuestas en `sessionStorage` bajo la clave `briefing`, restauradas al
  recargar, junto con el paso actual.

#### 12.1.2 Los 9 pasos

| # | Pregunta | Tipo de campo | Validación |
|---|---|---|---|
| 1 | ¿CÓMO TE LLAMAS? | Texto de una línea | Obligatorio, ≥ 2 caracteres |
| 2 | ¿DE DÓNDE ERES? | Texto de una línea | Obligatorio |
| 3 | ¿CUÁL ES TU NÚMERO DE WHATSAPP? | Selector de país + campo numérico | Obligatorio, formato válido |
| 4 | NOMBRE DE TU MARCA | Texto de una línea | Obligatorio |
| 5 | CUÉNTANOS MÁS SOBRE TU MARCA | Textarea autoexpansible | Obligatorio, ≥ 20 caracteres |
| 6 | WEB ACTUAL O INSTAGRAM | Texto de una línea (`inputmode="url"`) | **Opcional** |
| 7 | ¿QUÉ SERVICIO TE INTERESA? | Lista de opciones múltiples (checkboxes) | Obligatorio, ≥ 1 opción |
| 8 | TU PRESUPUESTO | Desplegable (`<select>`) | Obligatorio |
| 9 | AGENDA TU VIDEOLLAMADA | **Embed de Cal.com** (§12.2) | — (paso final) |

**Detalle por paso:**

- **Paso 3 — WhatsApp.** Ayuda: "Elige tu país y escribe el número sin el prefijo."
  Dos controles apilados: un `<select>` de país que muestra **bandera + nombre + prefijo**
  (`🇪🇸 España +34`) con hairline inferior propia y chevron `▾` a la derecha en `--fg-muted`; debajo,
  el campo numérico con `inputmode="tel"` y placeholder de ejemplo local (`600 00 00 00`).
  País por defecto: España (+34). Se guarda el número en formato E.164 completo.
- **Paso 5 — Descripción.** Ayuda: "¿En qué sector estás? ¿Cuál es tu producto o servicio? ¿Qué
  quieres conseguir con él?" Textarea que **crece con el contenido** (sin scroll interno hasta un
  máximo de 8 líneas), misma hairline inferior, contador de caracteres discreto en `--fg-faint` solo
  a partir de los 200 caracteres.
- **Paso 6 — Web o Instagram.** Único paso **opcional**: el `Siguiente` ya está en ámbar desde el
  inicio y el usuario puede saltarlo vacío. Acepta URL, dominio suelto o `@usuario`; se normaliza al
  guardar. Nada de validación agresiva que bloquee.
- **Paso 7 — Servicio.** **Selección múltiple.** Cada opción es una fila con caja completa:
  `border: 1px solid var(--border)`, `border-radius: 2px`, alto 72px, `padding-inline: var(--space-5)`,
  con un checkbox cuadrado de 22px a la izquierda (`border: 1px solid var(--fg-faint)`,
  `border-radius: 2px`) y la etiqueta en `--fs-body` color `--fg`.
  Estados: **hover/foco** → `border-color: var(--fg)` (la fila se ilumina, como en la captura);
  **seleccionada** → `border-color: var(--accent)` y checkbox relleno de `--accent` con una marca
  `✓` en `--on-accent`. Toda la fila es clicable (`<label>` envolviendo el `<input type="checkbox">`).
  Opciones: `Diseño + Desarrollo Web` · `Landing Page` · `Rediseño de Web` · `E-commerce` ·
  `Branding` · `Otro`.
  Si se marca **Otro**, aparece debajo un campo de texto libre con la misma hairline.
- **Paso 8 — Presupuesto.** Un `<select>` nativo con la hairline inferior y el chevron `▾`, cuyo
  estado vacío muestra `Elige una opción…` en `--fg-faint`.
  Se usa el `<select>` **nativo** a propósito: en móvil abre la rueda del sistema (como en la
  captura) y es accesible sin código extra. Estilar solo el disparador; el desplegable lo pinta el
  sistema.
  Opciones: `Menos de 750 €` · `750 – 1.500 €` · `1.500 – 3.000 €` · `3.000 – 5.000 €` ·
  `5.000+ €`.
  Moneda: **euros**. La referencia usaba USD, pero siendo una web solo en español EUR es lo
  coherente; si prefieres USD, se cambia solo el copy.
- **Paso 9 — Agendar la videollamada.** Es la **pantalla final** del cuestionario y sustituye a
  cualquier "pantalla de gracias" estática. Ver §12.2.

#### 12.1.3 Envío de las respuestas

- Al llegar al paso 9, las respuestas de los pasos 1–8 se **envían** (endpoint propio, webhook de
  n8n, o el servicio que se decida) **antes** de mostrar el calendario, para no perder el lead si el
  usuario no llega a reservar.
- Estado de envío: el paso 9 muestra el calendario en cuanto el POST responde; si falla, se reintenta
  una vez y, si vuelve a fallar, se muestra el calendario igualmente y las respuestas quedan en
  `sessionStorage` con una marca `pendingSync`.
- Nunca se bloquea la reserva por un fallo de envío.

### 12.2 Cal.com — paso 9 y CTA del hero (fase 2)

Dos puntos de entrada al mismo calendario, con presentación distinta:

**A) Desde el hero y el header** (`data-action="calendar"` → `openCalendar()`):
embed de Cal.com en **modo popup** sobre el hero, sin abandonar la página.

**B) Como paso 9 del cuestionario:** embed **inline**, ocupando el cuerpo del paso, con el mismo
header y contador `9 / 9` encima. Aquí el calendario **no** es un popup: está incrustado en el flujo,
de modo que reservar la videollamada es el cierre natural del briefing.

**Requisitos comunes:**

- Titular del paso: `AGENDA TU VIDEOLLAMADA`, en display, con ayuda debajo: "Elige el día y la
  hora que mejor te vaya. Te llega la invitación al momento."
- **Idioma del embed:** configura Cal.com con `locale: "es"` para que el calendario y sus textos no
  salgan en inglés.
- **Carga perezosa obligatoria:** el script `embed.js` de Cal.com se inyecta **en el primer clic**
  (caso A) o **al entrar en el paso 9** (caso B). Jamás en el `<head>` ni en el primer render (§11).
- **Tema oscuro y tokens de marca:**
  ```js
  cal("ui", {
    theme: "dark",
    cssVarsPerTheme: {
      dark: {
        "cal-brand": "#E8A33D",
        "cal-bg": "#000000",
        "cal-bg-emphasis": "#121212",
        "cal-text": "#F5F1E8",
        "cal-text-emphasis": "#F5F1E8",
        "cal-border": "#1C1C1C",
        "cal-border-emphasis": "#2A2A2A"
      }
    },
    hideEventTypeDetails: false,
    layout: "month_view"
  });
  ```
- **Prefill** con lo ya recogido en el cuestionario, para que el usuario no repita datos:
  `name` (paso 1), `notes` (composición de los pasos 4, 5, 6, 7 y 8), y el teléfono del paso 3 en un
  campo personalizado del tipo de evento. Se pasa por query string del embed
  (`?name=…&notes=…&metadata[budget]=…`), con todos los valores `encodeURIComponent`.
- **Tipo de evento:** videollamada de 30 minutos (a confirmar, Anexo D), con Google Meet o el
  proveedor que se configure en Cal.com. La confirmación y el recordatorio los envía Cal.com; la web
  no manda correos.
- **Después de reservar:** escuchar el evento `bookingSuccessful` del embed y mostrar una pantalla de
  cierre propia: titular display `NOS VEMOS PRONTO`, resumen de día y hora, y un
  botón secundario para volver al inicio. Limpiar entonces el `sessionStorage` del briefing.
- **Fallback sin JS o si el embed falla:** un enlace directo `https://cal.com/<usuario>/<evento>`
  visible siempre bajo el calendario ("¿No ves el calendario? Reserva aquí"), con
  `target="_blank" rel="noopener"`.
- **Accesibilidad:** el embed vive dentro de un contenedor con `aria-label` descriptivo; en el caso A
  (popup) se aplica trampa de foco y cierre con `Esc`; el iframe recibe un `title`.
- **Altura:** mínimo `560px` en móvil y `640px` en desktop, con el contenedor en `min-block-size` y
  scroll interno propio del embed — el fondo de la página no debe hacer scroll simultáneo.

### 12.3 Superficie pública que esta fase debe exponer

```js
// src/main.js
export function openBriefing(): void   // stub en fase 1
export function openCalendar(): void   // stub en fase 1
```

Y en el marcado, los atributos `data-action="briefing"` y `data-action="calendar"` como puntos de
anclaje estables. **No los renombres en fases posteriores.**

---

## 13. Arquitectura de archivos y entregables

```
/
├─ index.html               → header + hero, marcado semántico, CSS crítico inline
├─ assets/
│  ├─ css/
│  │  ├─ tokens.css         → §2 y §3 y §4 como custom properties en :root
│  │  ├─ base.css           → reset, tipografía base, ::selection, focus-visible
│  │  └─ hero.css           → header + hero + botones
│  ├─ js/
│  │  ├─ main.js            → bootstrap, stubs openBriefing/openCalendar
│  │  ├─ progress.js        → barra de progreso con rAF
│  │  └─ reveal.js          → cascada de entrada
│  └─ fonts/                → .woff2 autoalojados (opcional pero recomendado)
└─ marca-personal/
   └─ PROMPT-HERO.md        → este documento
```

**Entregables de esta fase:**

1. `index.html` con header y hero completos, en español.
2. `tokens.css` con **todos** los tokens de §2, §3 y §4 declarados en `:root`. Ninguna literal de
   color, tamaño de fuente o espaciado suelta en el resto del CSS — si aparece una, es un bug.
3. JS mínimo: estado de scroll del header, barra de progreso, cascada de entrada y los dos stubs
   de §12.3.
4. README breve indicando cómo cambiar el copy, cómo cambiar la familia display y dónde se conectará
   Cal.com.
5. **Nada más.** Sin "sobre mí", sin proyectos, sin testimonios, sin footer todavía.

---

## 14. Checklist de QA antes de dar por cerrado el hero

**Visual**

- [ ] El H1 rompe en 3–4 líneas en móvil y 2–3 en desktop, sin palabras huérfanas.
- [ ] Más del 55% del viewport del hero es negro vacío.
- [ ] El acento ámbar aparece en 3 elementos como máximo.
- [ ] No hay ni un `#FFFFFF` en todo el CSS.
- [ ] Ninguna esquina redondeada por encima de 2px; ninguna sombra difusa.

**Responsive**

- [ ] 360×640, 390×844, 430×932, 768×1024, 1280×800, 1920×1080 revisados uno a uno.
- [ ] Móvil en horizontal (por ejemplo 844×390) no rompe ni obliga a hacer scroll para ver los CTAs.
- [ ] Cero scroll horizontal en cualquier ancho entre 320 y 2560px.
- [ ] Safari iOS: la altura del hero no salta al ocultarse/mostrarse la barra del navegador (`svh`).

**Accesibilidad**

- [ ] Navegación completa solo con teclado, en el orden esperado, con foco siempre visible.
- [ ] Skip link presente y funcional.
- [ ] VoiceOver/NVDA: el H1 se lee como una frase continua.
- [ ] Contrastes verificados con herramienta en las 5 combinaciones críticas.
- [ ] `prefers-reduced-motion` respetado por completo.
- [ ] Zoom al 200% sin pérdida de contenido.

**Funcional**

- [ ] El header cambia de estado al pasar de 24px de scroll y vuelve al reposo al subir.
- [ ] La barra de progreso llega exactamente al 100% al final de la página.
- [ ] Los dos CTAs disparan sus stubs y, con JS deshabilitado, tienen fallback usable.

**Rendimiento**

- [ ] Lighthouse mobile: Performance ≥ 95, Accessibility 100, Best Practices ≥ 95, SEO ≥ 95.
- [ ] CLS exactamente 0, incluso con las fuentes bloqueadas.
- [ ] Ningún script de terceros en el primer render.

---

## 15. Anti-patrones: qué NO hacer

- Hero centrado con **foto redonda** y `"Hola, soy ___ 👋"`. Es la plantilla de portfolio genérica
  que este diseño existe para evitar.
- Degradados morados/azules, blobs, mallas, partículas, fondos animados, estrellas, ruido.
- **Glassmorphism** o `backdrop-filter` en el header.
- Una tercera familia tipográfica, o un segundo color de acento "solo para este detalle".
- Cursor personalizado, scroll suavizado con librería (Lenis/Locomotive), o scroll-jacking.
- Marquee/ticker de logos de tecnologías en el hero.
- Copy de relleno tipo "Transformando ideas en experiencias digitales" o "Llevo tu negocio al
  siguiente nivel".
- Botones tipo cápsula (`border-radius: 999px`) o con `box-shadow` de color.
- Contadores animados, "typewriter effect" en el H1, o texto que rota entre varias palabras.
- Implementar el cuestionario o el embed de Cal.com en esta fase. **Solo los botones y sus stubs.**
- Cargar el script de Cal.com en el `<head>`.
- Dejar literales de color o tamaño fuera de `tokens.css`.

---

## Anexo A — CSS de referencia (tokens listos para pegar)

```css
:root {
  color-scheme: dark;

  /* ─── Primitivos ─────────────────────────────── */
  --black-950:#000; --black-900:#0A0A0A; --black-850:#0B0B0B;
  --black-800:#121212; --black-700:#1C1C1C; --black-600:#2A2A2A;
  --cream-100:#F5F1E8; --cream-200:#E4DFD4;
  --grey-400:#9A968E;  --grey-600:#5C5952;
  --amber-400:#F2B457; --amber-500:#E8A33D; --amber-600:#C98A2C;
  --red-500:#E5533D;   --green-500:#5BB98C;

  /* ─── Semánticos ─────────────────────────────── */
  --bg:var(--black-950);
  --bg-elev-1:var(--black-850);
  --bg-elev-2:var(--black-800);
  --border:var(--black-700);
  --border-strong:var(--black-600);
  --fg:var(--cream-100);
  --fg-muted:var(--grey-400);
  --fg-faint:var(--grey-600);
  --accent:var(--amber-500);
  --accent-hover:var(--amber-400);
  --accent-press:var(--amber-600);
  --on-accent:var(--black-900);
  --on-cream:var(--black-900);
  --focus-ring:var(--amber-500);

  /* ─── Tipografía ─────────────────────────────── */
  --font-display:"Anton","Archivo Black","Arial Narrow Bold",Impact,sans-serif;
  --font-text:"Poppins","Outfit",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;

  --fs-display:clamp(3.25rem,11vw,9rem);
  --fs-h2:clamp(2rem,6vw,4rem);
  --fs-h3:clamp(1.5rem,3.5vw,2.25rem);
  --fs-lead:clamp(1.05rem,2.2vw,1.375rem);
  --fs-body:1rem;
  --fs-small:.875rem;
  --fs-ui:.9375rem;
  --fs-eyebrow:.75rem;
  --fs-counter:1rem;

  /* ─── Espaciado ──────────────────────────────── */
  --space-1:4px;  --space-2:8px;   --space-3:12px;  --space-4:16px;
  --space-5:24px; --space-6:32px;  --space-7:40px;  --space-8:56px;
  --space-9:72px; --space-10:96px; --space-11:128px;--space-12:176px;

  /* ─── Layout ─────────────────────────────────── */
  --container-max:1240px;
  --gutter:clamp(20px,5vw,64px);
  --header-h:72px;

  /* ─── Movimiento ─────────────────────────────── */
  --ease:cubic-bezier(.22,1,.36,1);
  --dur-fast:180ms;
  --dur-base:240ms;
  --dur-slow:520ms;
}

@media (min-width:1024px){ :root{ --header-h:88px; } }

@media (prefers-contrast:more){
  :root{ --fg-muted:var(--cream-200); --border:var(--border-strong); }
}

*,*::before,*::after{ box-sizing:border-box; }
html{ background:var(--bg); }
body{
  margin:0; background:var(--bg); color:var(--fg);
  font-family:var(--font-text); font-size:var(--fs-body); line-height:1.6;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}
::selection{ background:var(--accent); color:var(--on-accent); }
:focus-visible{ outline:2px solid var(--focus-ring); outline-offset:2px; }

.hero__title{
  font-family:var(--font-display); font-weight:400;
  font-size:var(--fs-display); line-height:.9; letter-spacing:-.02em;
  text-transform:uppercase; margin:0; hyphens:none;
}
.hero__line{ display:block; overflow:hidden; }
.hero__line > span{ display:block; will-change:transform; }

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{
    animation-duration:.01ms!important; animation-iteration-count:1!important;
    transition-duration:.01ms!important; scroll-behavior:auto!important;
  }
  .progress{ display:none; }
}
```

---

## Anexo B — Marcado de referencia

```html
<a class="skip-link" href="#hero-title">Saltar al contenido</a>

<header class="header" data-header>
  <a class="header__brand" href="/" aria-label="Nombre — inicio">
    <svg class="brand__mascot" width="32" height="32" viewBox="0 0 64 64"
         fill="currentColor" aria-hidden="true" focusable="false">…</svg>
    <span class="wordmark">NOMBRE</span>
  </a>

  <button type="button" class="btn btn--primary header__cta" data-action="calendar">
    <span>Contacto</span>
    <svg width="16" height="16" aria-hidden="true" focusable="false">…</svg>
  </button>
</header>

<main>
  <section class="hero" aria-labelledby="hero-title">
    <p class="hero__eyebrow">DISEÑO Y DESARROLLO WEB · BARCELONA</p>

    <h1 class="hero__title" id="hero-title">
      <span class="hero__line"><span>WEBS QUE</span></span>
      <span class="hero__line"><span>NO PARECEN</span></span>
      <span class="hero__line"><span>PLANTILLAS</span></span>
    </h1>

    <p class="hero__lead">Diseño y construyo webs a medida para marcas y profesionales que necesitan destacar.</p>

    <div class="hero__actions">
      <button type="button" class="btn btn--primary"   data-action="briefing">Empezar un proyecto</button>
      <button type="button" class="btn btn--secondary" data-action="calendar">Agendar una llamada</button>
    </div>

    <p class="hero__note">Respuesta en menos de 24 h · Sin compromiso</p>
  </section>
</main>

<div class="progress" aria-hidden="true"><span class="progress__bar" data-progress></span></div>
```

---

## Anexo C — JS de referencia

```js
// main.js — stubs y bootstrap
export function openBriefing(){
  console.info('briefing:open');           // fase 2: abre el overlay de 9 pasos
  // fallback sin JS de fase 2:
  // window.location.href = '/briefing';
}

export function openCalendar(){
  console.info('calendar:open');           // fase 2: carga perezosa del embed de Cal.com
  // fallback: window.open('https://cal.com/<usuario>/<evento>', '_blank', 'noopener');
}

document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-action]');
  if (!el) return;
  if (el.dataset.action === 'briefing') openBriefing();
  if (el.dataset.action === 'calendar') openCalendar();
});

// Header con scroll — sentinel, no listener de scroll
const sentinel = document.createElement('div');
sentinel.style.cssText = 'position:absolute;top:0;height:24px;width:1px;';
document.body.prepend(sentinel);
new IntersectionObserver(
  ([entry]) => document.querySelector('[data-header]')
                 .classList.toggle('is-scrolled', !entry.isIntersecting)
).observe(sentinel);

// Barra de progreso — solo transform, dentro de rAF
const bar = document.querySelector('[data-progress]');
let ticking = false;
addEventListener('scroll', () => {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const max = document.documentElement.scrollHeight - innerHeight;
    const p = max > 0 ? Math.min(scrollY / max, 1) : 0;
    bar.style.transform = `scaleX(${p.toFixed(3)})`;
    ticking = false;
  });
}, { passive: true });
```

---

## Anexo D — Decisiones abiertas

Confirmar con el cliente antes de cerrar la fase:

1. **Nombre de marca y wordmark exacto** que acompaña a la mascota, y quién entrega el **SVG
   vectorizado** del logo (o si se vectoriza a partir del JPG facilitado).
2. **Familia display definitiva**: Anton (por defecto), Archivo Black o Bebas Neue.
3. **Copy real** del eyebrow, H1, lead y nota, con sus saltos de línea.
4. **Usuario y slug del evento de Cal.com** (`cal.com/<usuario>/<evento>`).
5. **Duración del tipo de evento de Cal.com** (30 min por defecto) y proveedor de videollamada.
   Los 9 pasos del cuestionario ya están cerrados en §12.1.2.
6. Si el hero muestra **disponibilidad real** o esas columnas quedan vacías.
7. Si se autoalojan las fuentes (recomendado para rendimiento y RGPD) o se sirven desde Google Fonts.
8. **Destino de las respuestas** del cuestionario: endpoint propio, webhook de n8n, correo o CRM.
9. Si el presupuesto se muestra en **USD** (como en la referencia) o se localiza a **EUR**.

> **Nota de referencia:** samu-webart.com no era accesible desde el entorno donde se redactó este
> documento (bloqueo del proxy de red), por lo que su aportación —estructura general, escala
> tipográfica y ritmo de página— está formulada aquí como **parámetros explícitos y ajustables**
> en lugar de como una copia verificada. Si algún detalle no coincide con la referencia real,
> ajústalo en §3 y §4 y el resto del documento sigue siendo válido.
