# Prompt detallado — Hero, colores y tipografías
Web de marca personal · Referencias: samu-webart.com (estructura + tipografía) y southprojects.dev (flujo de preguntas + agenda con Cal.com)

> Este documento es **solo el prompt del hero + sistema de color y tipografía**.
> El cuestionario de 9 pasos y la integración de Cal.com se especifican en fases posteriores;
> aquí únicamente se define el CTA que los dispara.

---

## 0. Contexto para quien ejecute el prompt

Eres un desarrollador front-end senior con criterio de dirección de arte. Construye **únicamente la
sección hero** de una web de marca personal (one-page, dark mode nativo, mobile-first). Stack:
HTML semántico + CSS moderno (custom properties, `clamp()`, grid/flex) y JS mínimo (sin framework
obligatorio; si se usa, Next.js + Tailwind con los tokens definidos abajo). Sin librerías de UI
pesadas. Animaciones con CSS/`IntersectionObserver` o GSAP si hace falta secuenciar.

La web debe **sentirse como un estudio, no como un CV**: tipografía enorme, mucho negro, un solo
acento cálido, y una sensación de producto cuidado.

---

## 1. Sistema de color

Paleta oscura de alto contraste, tomada del lenguaje visual de South Projects (negro puro + crema +
ámbar) y aplicable a una marca personal.

| Token | Valor | Uso |
|---|---|---|
| `--bg` | `#000000` | Fondo global del hero y de toda la página |
| `--bg-elev` | `#0B0B0B` | Superficies elevadas: tarjetas, dropdowns, barra sticky |
| `--surface-line` | `#1C1C1C` | Bordes sutiles, separadores, hairlines |
| `--fg` | `#F5F1E8` | Texto principal (crema, **no** blanco puro) |
| `--fg-muted` | `#9A968E` | Subtítulos, descripciones, labels secundarios |
| `--fg-faint` | `#5C5952` | Metadatos, contadores, texto deshabilitado |
| `--accent` | `#E8A33D` | Ámbar: acento único de marca (CTA principal, contador, subrayados, foco) |
| `--accent-hover` | `#F2B457` | Hover del acento |
| `--accent-press` | `#C98A2C` | Estado activo/pressed |
| `--on-accent` | `#0A0A0A` | Texto sobre superficie ámbar |
| `--focus-ring` | `#E8A33D` | Anillo de foco, 2px + 2px de offset |

Reglas de color, no negociables:

1. **Un solo acento.** El ámbar aparece como máximo en 3 elementos del hero (CTA primario, un
   detalle tipográfico, el indicador de scroll). Nada más lleva color.
2. **Nada de blanco puro.** Todo texto claro usa `--fg` (`#F5F1E8`); el blanco `#FFF` produce halo
   sobre negro puro y rompe la calidez de la paleta.
3. **Sin degradados de marca, sin glassmorphism, sin sombras de color.** Profundidad por
   espaciado y contraste tipográfico, no por efectos.
4. **Contraste:** todo texto ≥ 4.5:1 sobre `--bg`. `--fg-faint` solo para texto no esencial ≥ 14px.
5. **Botón secundario** = fondo transparente + borde `1px solid var(--fg)`; **botón primario** =
   fondo `--fg` (crema) con texto negro en reposo, y fondo `--accent` cuando el paso está
   "activo/validado" (mismo patrón que South Projects: el Next se vuelve ámbar al ser accionable).
6. Respeta `prefers-color-scheme`: el diseño es dark-first y **no** ofrece tema claro; declara
   `color-scheme: dark` para que los controles nativos hereden.

---

## 2. Sistema tipográfico

Dos familias. Una display condensada y muy pesada para titulares, una grotesque geométrica y neutra
para todo lo demás.

### Familias

- **Display / titulares:** condensada, ultra-bold, mayúsculas.
  Elección: **Anton** (Google Fonts) o, si se quiere más carácter, **Archivo Black** /
  **Bebas Neue**. Fallback: `"Anton", "Archivo Black", "Haettenschweiler", "Impact", sans-serif`.
  Se usa **siempre en `text-transform: uppercase`**, con `letter-spacing: -0.01em` y
  `line-height: 0.92`.
- **Texto / UI:** grotesque geométrica de bordes redondeados.
  Elección: **Poppins** (400/500/600) o **Outfit**. Fallback:
  `"Poppins", "Outfit", -apple-system, "Segoe UI", sans-serif`. `line-height: 1.55`,
  `letter-spacing: 0`.

Cargar solo los pesos usados (display 400 único; texto 400/500/600), `font-display: swap`,
preconnect a `fonts.gstatic.com`, y subset latin + latin-ext (hay contenido en ES/CA).

### Escala (fluida, mobile → desktop)

| Rol | Familia | Tamaño | Peso | Tracking / Leading |
|---|---|---|---|---|
| `--fs-hero` (H1) | Display | `clamp(3.25rem, 11vw, 9rem)` | 400 (la fuente ya es black) | `-0.02em` / `0.9` |
| `--fs-h2` | Display | `clamp(2rem, 6vw, 4rem)` | 400 | `-0.01em` / `0.95` |
| `--fs-lead` (subtítulo hero) | Texto | `clamp(1.05rem, 2.2vw, 1.375rem)` | 400 | `0` / `1.5` |
| `--fs-body` | Texto | `1rem` | 400 | `0` / `1.6` |
| `--fs-ui` (botones, nav) | Texto | `0.9375rem` | 500 | `0.01em` / `1` |
| `--fs-eyebrow` | Texto | `0.75rem` | 600 | `0.18em` uppercase / `1` |

El H1 debe **romper línea de forma intencionada** (`<br>` o `max-width` en `ch`), nunca quedar al
azar; en móvil, 3–4 líneas; en desktop, 2–3. Aplica `text-wrap: balance` al subtítulo.

---

## 3. El hero — especificación

### 3.1 Estructura (de arriba abajo)

1. **Barra superior fija/absoluta**, mismo patrón que las capturas de South Projects:
   - Izquierda: **wordmark** en tipografía display, mayúsculas, `#F5F1E8` — el nombre de marca
     personal — seguido de un pequeño glifo/símbolo ámbar como firma (equivalente al sol de South).
   - Centro-derecha: **conmutador de idioma `ES / EN`**, activo en `--accent`, inactivo en
     `--fg-faint`, separados por una barra `/`. Persiste la elección en `localStorage`.
   - Derecha: **botón secundario** (crema sólido, texto negro) con la acción de contacto rápido.
   - Altura ~72px móvil / 88px desktop. Fondo transparente que pasa a `--bg` con hairline
     `--surface-line` al hacer scroll > 24px.
2. **Espacio negativo generoso** antes del titular: mínimo `18vh` en desktop, `12vh` en móvil.
   El vacío es parte del diseño; no lo rellenes.
3. **Eyebrow** (opcional, una línea): rol + ubicación en `--fs-eyebrow`, `--fg-muted`,
   p. ej. `DISEÑO Y DESARROLLO WEB · BARCELONA`.
4. **H1**: 4–7 palabras, tipografía display gigante, `--fg`, centrado en móvil y alineado a la
   izquierda en desktop (≥1024px). Una sola palabra clave puede ir en `--accent` — como máximo una.
5. **Subtítulo** (`--fs-lead`, `--fg-muted`): 1–2 frases, máximo ~62 caracteres por línea,
   `max-width: 34ch`. Dice qué haces y para quién, sin adjetivos vacíos.
6. **Fila de CTAs**, con el patrón exacto de las capturas:
   - **Primario — "Empezar un proyecto"**: bloque ancho, esquinas rectas (`border-radius: 2px`),
     fondo `--fg`, texto `--on-accent`, `--fs-ui`; en hover pasa a `--accent`. Ancho completo en
     móvil (`width: 100%`, alto 64px), auto en desktop con `padding: 20px 36px`.
     **Acción:** abre el cuestionario de 9 pasos (fase posterior).
   - **Secundario — "Agendar una llamada"**: mismo tamaño, fondo transparente, borde
     `1px solid var(--fg)`, texto `--fg`. **Acción:** abre el popup de **Cal.com** (fase posterior).
   - En móvil se apilan (primario arriba, gap 12px); en desktop van en fila con gap 16px.
7. **Indicador de progreso/scroll**: hairline de 3px anclada al borde inferior del viewport, con un
   segmento ámbar que crece con el scroll de la página — es el mismo elemento que en las capturas
   marca `1/9`, reutilizado aquí como barra de progreso de lectura. Ocúltalo si
   `prefers-reduced-motion: reduce`.

### 3.2 Layout y medidas

- Contenedor: `max-width: 1240px`, `margin-inline: auto`, `padding-inline: clamp(20px, 5vw, 64px)`.
- Altura del hero: `min-height: 100svh` (usa `svh`, no `vh`, por la barra de Safari iOS),
  con `display: grid; align-content: center`.
- Ritmo vertical entre bloques del hero: eyebrow → H1 `24px`; H1 → subtítulo `28px`;
  subtítulo → CTAs `40px` (escalar ×1.25 en desktop).
- Rejilla de 12 columnas en ≥1024px: el bloque de texto ocupa columnas 1–8; las 4 restantes quedan
  **vacías a propósito** o alojan un detalle discreto (año, disponibilidad, un `●` ámbar con
  "Disponible para proyectos").

### 3.3 Movimiento

- **Entrada:** eyebrow, líneas del H1, subtítulo y CTAs aparecen en cascada con
  `opacity 0→1` + `translateY(24px→0)`, `520ms`, `cubic-bezier(.22,1,.36,1)`, stagger de `70ms`.
  Las líneas del H1 se animan **una por una** con `overflow: hidden` en cada línea (efecto máscara).
- **Hover CTA:** transición de `background-color` y `color` en `180ms ease-out`. Sin escalados,
  sin rebotes.
- **Cursor:** nada de cursores personalizados que rompan accesibilidad.
- **`prefers-reduced-motion: reduce`:** todo aparece en su estado final, sin transformaciones.

### 3.4 Accesibilidad y semántica

- `<header>` para la barra, `<main>` → `<section aria-labelledby="hero-title">`, un único `<h1>`.
- CTAs como `<button>` si abren overlays (cuestionario / popup de Cal), nunca `<a href="#">`.
- Foco visible siempre: `outline: 2px solid var(--focus-ring); outline-offset: 2px`.
- El conmutador de idioma es un grupo de botones con `aria-pressed`, y actualiza `<html lang>`.
- Contenido bilingüe **ES/EN** desde el primer commit: textos en un objeto/JSON de copys, jamás
  incrustados a mano en el marcado.

### 3.5 Rendimiento

- Sin imágenes en el hero, o una sola, en `AVIF/WebP`, `loading="eager"`, `fetchpriority="high"`,
  con `width`/`height` explícitos.
- Objetivo: LCP < 1.8s en 4G, CLS = 0, JS del hero < 8KB comprimido.
- Fuentes con `<link rel="preload" as="font" crossorigin>` para el archivo display.

---

## 4. Entregable esperado de esta fase

1. `index.html` con la barra superior y el hero completo, en ES/EN.
2. `styles.css` (o equivalente) con **todos los tokens del §1 y §2 declarados como custom
   properties en `:root`** — ninguna literal de color o tamaño suelta en el resto del CSS.
3. JS mínimo: conmutador de idioma, estado de scroll de la barra, barra de progreso, animación de
   entrada, y dos handlers `onClick` **stub** (`openBriefing()` y `openCalendar()`) listos para
   conectar el cuestionario de 9 pasos y Cal.com en la siguiente fase.
4. Sin secciones adicionales: nada de "sobre mí", proyectos, footer o testimonios todavía.

---

## 5. Qué NO hacer

- Nada de plantillas genéricas de portfolio, hero centrado con foto redonda, o "Hi, I'm ___ 👋".
- Nada de degradados morados, blobs, partículas o fondos animados.
- Nada de más de dos familias tipográficas ni de un segundo color de acento.
- No inventar copy de relleno tipo "Transformando ideas en experiencias digitales".
- No implementar todavía el cuestionario ni la integración de Cal.com: solo los botones y sus stubs.
