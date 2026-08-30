# Prompt maestro — "Empezar un proyecto"
**Cuestionario de 9 pasos + reserva de videollamada con Cal.com**

Fase 2 del proyecto de marca personal. Depende de **`PROMPT-HERO.md`** (fase 1), que define el
sistema de color, el sistema tipográfico, el espaciado, el header y los stubs `openBriefing()` /
`openCalendar()` sobre los que se engancha todo lo de aquí.

Referencia de comportamiento: **southprojects.dev**. Este documento reproduce ese flujo, adaptado a
la marca personal y **solo en español**.

---

## Índice

0. [Briefing para quien ejecuta el prompt](#0-briefing-para-quien-ejecuta-el-prompt)
1. [Concepto: qué es esta pantalla y qué no](#1-concepto-qué-es-esta-pantalla-y-qué-no)
2. [Arquitectura del flujo](#2-arquitectura-del-flujo)
3. [Chrome común a todos los pasos](#3-chrome-común-a-todos-los-pasos)
4. [Especificación paso a paso](#4-especificación-paso-a-paso)
5. [Componentes de formulario](#5-componentes-de-formulario)
6. [Validación y errores](#6-validación-y-errores)
7. [Estado, persistencia y modelo de datos](#7-estado-persistencia-y-modelo-de-datos)
8. [Envío de las respuestas](#8-envío-de-las-respuestas)
9. [Paso 9 — Cal.com](#9-paso-9--calcom)
10. [Pantalla de cierre](#10-pantalla-de-cierre)
11. [Navegación, teclado y gestos](#11-navegación-teclado-y-gestos)
12. [Movimiento](#12-movimiento)
13. [Accesibilidad](#13-accesibilidad)
14. [Rendimiento](#14-rendimiento)
15. [Anti-spam y privacidad](#15-anti-spam-y-privacidad)
16. [Analítica](#16-analítica)
17. [Arquitectura de archivos y entregables](#17-arquitectura-de-archivos-y-entregables)
18. [Checklist de QA](#18-checklist-de-qa)
19. [Anti-patrones](#19-anti-patrones)
20. [Anexo A — Copy completo](#anexo-a--copy-completo)
21. [Anexo B — CSS de referencia](#anexo-b--css-de-referencia)
22. [Anexo C — Marcado de referencia](#anexo-c--marcado-de-referencia)
23. [Anexo D — JS de referencia](#anexo-d--js-de-referencia)
24. [Anexo E — Decisiones abiertas](#anexo-e--decisiones-abiertas)

---

## 0. Briefing para quien ejecuta el prompt

Implementa el flujo que se abre al pulsar **"Empezar un proyecto"** en el hero: un cuestionario de
**9 pasos, una pregunta por pantalla**, que termina con el usuario reservando una **videollamada en
Cal.com**.

**Reglas de partida:**

- **Reutiliza el sistema de fase 1.** Todos los colores, tamaños tipográficos, espaciados y
  duraciones salen de los tokens ya declarados en `tokens.css`. Si necesitas un valor que no existe,
  añádelo como token; **no** escribas literales.
- **Mismo stack que el hero.** Si la fase 1 se hizo en vanilla, esto va en vanilla. No introduzcas un
  framework para este flujo.
- **Solo español.** Sin conmutador de idioma, sin versión en inglés. `<html lang="es">`.
- **Mobile-first.** El 100% de este flujo se rellena desde el móvil. Diseña a 390px.
- **Sin librerías de formularios** (Formik, react-hook-form, etc.). La validación de 8 campos no
  justifica una dependencia.
- La única dependencia externa admitida es el **embed de Cal.com**, y con carga perezosa.

---

## 1. Concepto: qué es esta pantalla y qué no

**Qué es:** una conversación. Una pregunta a la vez, en pantalla completa, con el titular enorme en
la tipografía display. El usuario debe sentir que está hablando con alguien, no rellenando un
formulario de contacto.

**Qué no es:**

- No es un formulario largo con todos los campos apilados y un botón "Enviar" al final.
- No es un modal pequeño centrado con scroll interno.
- No es una página aparte con su propia navegación y su propio footer.

**Las tres decisiones que definen la sensación:**

1. **Una pregunta por pantalla.** Nunca dos campos de temas distintos a la vez (la excepción es el
   paso 3, donde el país y el número son un solo dato partido en dos controles).
2. **Campos sin caja.** Solo una hairline inferior. El campo no parece un input: parece una línea
   sobre la que escribir.
3. **El botón "Siguiente" cambia de color al validar.** Crema cuando aún no hay respuesta, ámbar
   cuando ya la hay. Es el único feedback de progreso dentro del paso, y hace que avanzar apetezca.

---

## 2. Arquitectura del flujo

### 2.1 Presentación: overlay, no página

El cuestionario se abre como **overlay a pantalla completa** sobre la home, no como navegación a otra
URL. Motivos: la transición es instantánea, no hay recarga y se conserva el contexto.

- Contenedor: `role="dialog" aria-modal="true" aria-labelledby="briefing-title"`,
  `position: fixed; inset: 0; z-index: 200; background: var(--bg);`.
- Al abrir: bloquear el scroll del fondo (`overflow: hidden` en `<html>` + compensar el ancho de la
  barra de scroll con `scrollbar-gutter: stable` para que no salte el layout).
- Al cerrar: restaurar el scroll y devolver el foco al botón que lo abrió.

### 2.2 URL y navegación del navegador

Aunque sea un overlay, **cada paso tiene su entrada en el historial**:

- Al abrir: `history.pushState({step:1}, '', '#/empezar/1')`.
- Al avanzar o retroceder: `pushState` / `popstate` con el paso correspondiente.
- El botón "atrás" del navegador y el gesto de retroceso de iOS **retroceden un paso**, no cierran
  el flujo. Solo al retroceder desde el paso 1 se cierra el overlay.
- Al recargar con un hash `#/empezar/n`: se reabre el overlay en ese paso **si** hay estado guardado
  y los pasos anteriores están completos; si no, se abre en el primer paso incompleto.

### 2.3 Mapa

```
Hero ──[Empezar un proyecto]──► Paso 1 ─► 2 ─► 3 ─► 4 ─► 5 ─► 6 ─► 7 ─► 8
                                                                        │
                                                     POST de respuestas ▼
                                                          Paso 9 · Cal.com
                                                                        │
                                                        bookingSuccessful▼
                                                              Cierre "Nos vemos pronto"
```

---

## 3. Chrome común a todos los pasos

De arriba abajo, idéntico en los 9 pasos:

1. **Header.** El mismo de la home (mascota + wordmark a la izquierda). A la derecha, en lugar del
   CTA de contacto, un **botón crema "← Volver"** que cierra el cuestionario (con confirmación si
   hay respuestas escritas, §11.3). El centro queda vacío.
2. **Contador `n / 9`.** Centrado, sobre el titular, `--fs-counter`, con
   `font-variant-numeric: tabular-nums`. El número actual en `--accent`; la barra `/` y el total en
   `--fg-faint`. Separación con el titular: `--space-7`.
3. **Titular de la pregunta.** Tipografía **display**, mayúsculas, centrado,
   `clamp(2rem, 7vw, 3.25rem)`, `line-height: 0.95`, color `--fg`. Máximo 2 líneas: fuerza el salto
   con `<br>` donde toque, no lo dejes al azar.
4. **Texto de ayuda** (solo en los pasos que lo llevan): `--fs-body`, `--fg-muted`, centrado,
   `max-width: 42ch`, `margin-block-start: var(--space-5)`.
5. **Zona de respuesta.** Centrada, `max-width: 640px`. Separación con el bloque de arriba:
   `--space-9` en desktop, `--space-8` en móvil.
6. **Botones de navegación.** `Atrás` (secundario) y `Siguiente` (primario) en fila, **mismo ancho**
   (`flex: 1 1 0`), `gap: var(--space-4)`, `max-width: 640px`. En el paso 1 no hay `Atrás` y el
   `Siguiente` ocupa todo el ancho. Separación con la zona de respuesta: `--space-9`.
7. **Barra de progreso inferior.** El mismo componente de 3px del hero, con la fuente de progreso
   cambiada a `n / 9`. Transición de `transform: scaleX()` en `320ms var(--ease)` al cambiar de paso.

**Layout vertical:** el bloque completo va centrado con `display: grid; align-content: center;
min-block-size: 100svh; padding-block: calc(var(--header-h) + var(--space-8)) var(--space-10);`.
Si el contenido no cabe (paso 7 en móvil pequeño), el contenedor pasa a `align-content: start` y
permite scroll — **nunca** se comprime el ritmo vertical para forzar que quepa.

---

## 4. Especificación paso a paso

| # | Titular | Ayuda | Control | Obligatorio |
|---|---|---|---|---|
| 1 | ¿CÓMO TE LLAMAS? | — | Texto | Sí (≥ 2 car.) |
| 2 | ¿DE DÓNDE ERES? | — | Texto | Sí |
| 3 | ¿CUÁL ES TU NÚMERO DE WHATSAPP? | Sí | Select país + tel | Sí |
| 4 | NOMBRE DE TU MARCA | — | Texto | Sí |
| 5 | CUÉNTANOS MÁS SOBRE TU MARCA | Sí | Textarea | Sí (≥ 20 car.) |
| 6 | WEB ACTUAL O INSTAGRAM | Sí | Texto | **No** |
| 7 | ¿QUÉ SERVICIO TE INTERESA? | Sí | Checkboxes (múltiple) | Sí (≥ 1) |
| 8 | TU PRESUPUESTO | — | Select | Sí |
| 9 | AGENDA TU VIDEOLLAMADA | Sí | Embed Cal.com | — |

### Paso 1 — Nombre

- `<input type="text" name="nombre" autocomplete="given-name" autocapitalize="words" enterkeyhint="next">`
- Placeholder: vacío. La pregunta ya está en el titular; un placeholder sería redundante.
- Validación: `trim().length >= 2`. Sin números ni caracteres raros obligatorios — hay nombres para
  todo; no inventes reglas de "solo letras".
- Guarda el nombre **tal cual lo escribe**, sin capitalizar por tu cuenta.

### Paso 2 — Procedencia

- `<input type="text" name="lugar" autocomplete="country-name" enterkeyhint="next">`
- Campo libre a propósito: el usuario puede responder "España", "Barcelona" o "Buenos Aires, pero
  vivo en Madrid". No lo conviertas en un desplegable de países.
- Validación: no vacío.

### Paso 3 — WhatsApp

- Ayuda: *"Elige tu país y escribe el número sin el prefijo."*
- **Dos controles apilados**, cada uno con su hairline:
  1. `<select name="pais">` con **bandera + nombre + prefijo** (`🇪🇸 España +34`), chevron `▾` en
     `--fg-muted` a la derecha. Por defecto: **España (+34)**. Lista ordenada con España, México,
     Argentina, Colombia y Chile arriba, y el resto alfabético.
  2. `<input type="tel" name="telefono" inputmode="tel" autocomplete="tel-national" enterkeyhint="next">`
     con placeholder de ejemplo del país seleccionado (`600 00 00 00` para España), que **cambia**
     al cambiar de país.
- Validación: entre 6 y 15 dígitos tras quitar espacios, guiones y paréntesis.
- Se guarda en **E.164** (`+34600000000`) junto con el ISO del país.
- El teclado móvil debe salir numérico: `inputmode="tel"`, no `type="number"` (que trae flechas y
  acepta notación científica).

### Paso 4 — Nombre de la marca

- `<input type="text" name="marca" autocomplete="organization" enterkeyhint="next">`
- Validación: no vacío. Si el usuario no tiene marca todavía, admite cualquier cosa: no es tu
  trabajo juzgarlo.

### Paso 5 — Descripción de la marca

- Ayuda: *"¿En qué sector estás? ¿Cuál es tu producto o servicio? ¿Qué quieres conseguir con él?"*
- `<textarea name="descripcion" rows="1" enterkeyhint="enter">` **autoexpansible**: crece con el
  contenido hasta 8 líneas y a partir de ahí hace scroll interno. Implementación: en `input`, poner
  `style.height='auto'` y luego `style.height = scrollHeight + 'px'`, con un `max-height` en CSS.
- Misma hairline inferior, texto centrado, `--fs-lead`.
- Validación: ≥ 20 caracteres. Si escribe menos, el `Siguiente` sigue en crema (no hay mensaje de
  error hasta que lo pulsa, §6).
- Contador de caracteres discreto en `--fg-faint`, alineado a la derecha bajo la línea, visible
  **solo a partir de 200 caracteres**.
- `Enter` hace salto de línea aquí; se avanza con `Cmd/Ctrl + Enter` o pulsando el botón.

### Paso 6 — Web actual o Instagram

- Ayuda: *"Si aún no tienes, salta este paso."*
- `<input type="text" name="referencia" inputmode="url" autocapitalize="none" autocorrect="off" spellcheck="false" enterkeyhint="next">`
- **Único paso opcional.** El `Siguiente` está en **ámbar desde el inicio** y avanza aunque el campo
  esté vacío. El botón dice `Siguiente`; si el campo está vacío, cámbialo a **`Saltar`** — así queda
  explícito que es opcional sin necesidad de un enlace "omitir" aparte.
- Normalización al guardar: `@usuario` → `https://instagram.com/usuario`; `dominio.com` →
  `https://dominio.com`; una URL completa se deja igual. Nunca rechaces la entrada por formato.

### Paso 7 — Servicio

- Ayuda: *"Puedes elegir más de uno."*
- **Selección múltiple** con checkboxes. Seis opciones:
  `Diseño + Desarrollo Web` · `Landing Page` · `Rediseño de Web` · `E-commerce` · `Branding` ·
  `Otro`
- Cada opción es una **fila completa clicable** (`<label>` envolviendo el `<input type="checkbox">`):
  - `border: 1px solid var(--border)`, `border-radius: 2px`, alto **72px**,
    `padding-inline: var(--space-5)`, `gap: var(--space-4)`.
  - Checkbox cuadrado de 22px, `border: 1px solid var(--fg-faint)`, `border-radius: 2px`.
  - Etiqueta en `--fs-body`, color `--fg`, alineada a la izquierda.
  - Separación entre filas: `--space-3`.
- **Estados:**
  - *Hover / focus-visible:* `border-color: var(--fg)` — la fila se ilumina (es el estado que se ve
    en la referencia).
  - *Seleccionada:* `border-color: var(--accent)`, checkbox relleno de `--accent` con un `✓` en
    `--on-accent`.
  - Transición `160ms ease-out` solo en `border-color` y `background-color`.
- Al marcar **`Otro`**, aparece debajo un campo de texto libre (misma hairline, placeholder
  *"Cuéntanos qué necesitas"*) con una animación de altura de `200ms`. Si se desmarca, el campo
  desaparece y su valor se descarta.
- Validación: al menos una opción marcada. Si `Otro` está marcado, su texto es obligatorio.

### Paso 8 — Presupuesto

- `<select name="presupuesto">` **nativo**, con la misma hairline inferior y chevron `▾`.
  Se usa el nativo a propósito: en móvil abre la rueda del sistema y es accesible sin código extra.
  **Estila solo el disparador**; el desplegable lo pinta el sistema operativo.
- Estado vacío: `Elige una opción…` en `--fg-faint` (`<option value="" disabled selected>`).
- Opciones: `Menos de 750 €` · `750 – 1.500 €` · `1.500 – 3.000 €` · `3.000 – 5.000 €` ·
  `5.000+ €`.
- Validación: valor distinto de `""`.
- **No** añadas una opción "prefiero no decirlo": el rango de presupuesto es justo el dato que hace
  útil este cuestionario.

### Paso 9 — Videollamada

Ver §9. Es la pantalla final y no tiene botón `Siguiente`.

---

## 5. Componentes de formulario

### 5.1 Campo de texto (`.field`)

```
        Texto escrito por el usuario
────────────────────────────────────────────
```

- Sin fondo, sin borde, sin `border-radius`. Solo `border-block-end: 1px solid var(--fg)`.
- Texto **centrado**, `--fs-lead`, color `--fg`, `padding-block: var(--space-3)`.
- Placeholder en `--fg-faint`.
- **Foco:** la hairline pasa a `--accent` en `180ms`, **más** un `outline: 2px solid var(--focus-ring)`
  con `outline-offset: 4px` para teclado. No elimines el outline: el cambio de línea solo no basta
  para WCAG.
- **Error:** hairline en `--red-500` y mensaje debajo (§6).
- Ancho: 100% del contenedor de 640px.
- `-webkit-appearance: none` y `background: transparent` para matar el estilo de iOS.
- **`font-size` mínimo de 16px en móvil**, o Safari iOS hace zoom al enfocar. `--fs-lead` ya lo
  cumple; no lo bajes.

### 5.2 Select (`.field--select`)

- Mismo tratamiento que el campo de texto, con `appearance: none` y un chevron `▾` en SVG
  posicionado a la derecha (`pointer-events: none`).
- El texto del disparador va centrado como el resto.
- En el paso 3 el select del país muestra la bandera como emoji: asegúrate de que la fuente de
  fallback las renderiza (en Windows salen como siglas — es aceptable, no lo compenses con imágenes).

### 5.3 Fila de opción (`.option`)

Especificada en el paso 7. Reutilizable si en el futuro se añaden más pasos de selección.

### 5.4 Botones

Los del sistema de fase 1 (§7 de `PROMPT-HERO.md`), sin cambios:

- `Siguiente` = `.btn--primary`, que pasa a `.is-ready` (ámbar) cuando el paso valida.
- `Atrás` = `.btn--secondary`.
- Alto 64px en móvil, 56px en desktop.

---

## 6. Validación y errores

**Filosofía: validación permisiva, feedback tardío.**

1. **Mientras escribe: nunca marques error.** Solo se actualiza el color del `Siguiente`
   (crema ↔ ámbar). Nada de bordes rojos en cuanto el campo tiene un carácter.
2. **Al pulsar `Siguiente` con el paso inválido:** no avances. Muestra el mensaje de error, pon la
   hairline en `--red-500`, y **mueve el foco al campo**. Además, una sacudida horizontal de 6px de
   amplitud y `240ms` sobre el bloque de respuesta (desactivada con `prefers-reduced-motion`).
3. **El error desaparece** en cuanto el campo vuelve a ser válido, sin esperar a `blur`.
4. **Mensajes** (`--fs-small`, `--red-500`, centrados, `margin-block-start: var(--space-3)`,
   con `role="alert"`):
   - Paso 1: *"Escribe tu nombre para continuar."*
   - Paso 2: *"Dinos de dónde eres."*
   - Paso 3 (país): *"Elige tu país."* · (número): *"Ese número no parece válido. Revísalo, sin el prefijo."*
   - Paso 4: *"¿Cómo se llama tu marca?"*
   - Paso 5: *"Cuéntanos un poco más, con un par de frases nos vale."*
   - Paso 7: *"Elige al menos un servicio."* · (Otro sin texto): *"Cuéntanos qué necesitas."*
   - Paso 8: *"Elige un rango de presupuesto."*
5. **Vincula el mensaje al campo** con `aria-describedby` y marca el campo con
   `aria-invalid="true"` mientras el error esté visible.
6. **Nunca borres lo que el usuario ha escrito** por un fallo de validación.

---

## 7. Estado, persistencia y modelo de datos

### 7.1 Modelo

```js
{
  version: 1,
  paso: 5,                        // paso actual, 1–9
  iniciado: "2026-08-30T09:12:44.021Z",
  respuestas: {
    nombre: "Biel",
    lugar: "España",
    pais: "ES",
    telefono: "+34600000000",
    marca: "Hoop",
    descripcion: "Somos una marca de…",
    referencia: "https://instagram.com/hoop",   // "" si se saltó
    servicios: ["web", "branding"],             // claves estables, no etiquetas
    servicioOtro: "",                           // solo si servicios incluye "otro"
    presupuesto: "1500-3000"                    // clave estable, no la etiqueta visible
  },
  enviado: false,                 // true tras un POST correcto
  reservado: false                // true tras bookingSuccessful
}
```

**Guarda claves estables** (`"1500-3000"`), no las etiquetas visibles: si mañana cambias el copy o la
moneda, los datos históricos siguen siendo comparables.

### 7.2 Persistencia

- En **`sessionStorage`**, clave `briefing`, escrito con *debounce* de 400ms en cada cambio.
- `sessionStorage` y no `localStorage`: son datos personales de un formulario a medio rellenar; que
  mueran al cerrar la pestaña es lo correcto (§15).
- Al abrir el flujo, si hay estado guardado, **reanuda en el primer paso incompleto** y muestra una
  nota discreta bajo el contador: *"Retomamos donde lo dejaste."*, que desaparece a los 4 segundos.
- Al completar la reserva (§10), **borra la clave**.

---

## 8. Envío de las respuestas

**Regla central: las respuestas se envían al terminar el paso 8, antes de mostrar el calendario.**
Si el usuario no llega a reservar, el lead no se pierde.

- Método: `POST` con `fetch`, `Content-Type: application/json`, cuerpo = objeto `respuestas` más
  `iniciado`, `completado` y `origen: "web-hero"`.
- Destino: un endpoint propio o un **webhook de n8n** (a decidir, Anexo E).
- **Nunca bloquees la reserva por un fallo de envío:**
  - Se lanza el POST y **a la vez** se muestra el paso 9. No hay pantalla de espera.
  - Si falla: un reintento a los 2 segundos. Si vuelve a fallar, se marca `pendingSync: true` en
    `sessionStorage` y se reintenta una vez más al completar la reserva. El usuario no ve nada de
    esto.
- **Idempotencia:** genera un `id` (UUID) al iniciar el flujo y mándalo en cada intento, para que un
  reintento no cree un lead duplicado.
- **Timeout** de 8 segundos con `AbortController`.

---

## 9. Paso 9 — Cal.com

### 9.1 Presentación

- Titular: `AGENDA TU VIDEOLLAMADA`.
- Ayuda: *"Elige el día y la hora que mejor te vaya. Te llega la invitación al momento."*
- Contador `9 / 9`, barra de progreso al 100%.
- **Sin botón `Siguiente`.** Solo queda `Atrás` (por si quiere corregir una respuesta), en secundario
  y con menos peso visual.
- El embed va **inline**, ocupando la zona de respuesta, no en popup. En el hero y el header, el
  mismo calendario se abre en **popup**; aquí es el cierre natural del flujo.

### 9.2 Integración

- **Carga perezosa obligatoria:** el `embed.js` de Cal.com se inyecta al **entrar en el paso 9**
  (o al primer clic en el CTA del hero). Jamás en el `<head>` ni en el primer render.
- Configuración:

```js
cal("ui", {
  theme: "dark",
  layout: "month_view",
  hideEventTypeDetails: false,
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
  }
});
```

- **`locale: "es"`** en la configuración del embed, o el calendario sale en inglés aunque el resto de
  la web esté en español.
- **Prefill** con lo ya recogido, para que no repita datos:
  `name` (paso 1), `notes` (composición legible de los pasos 4, 5, 6, 7 y 8), el teléfono del paso 3
  en un campo personalizado del tipo de evento, y `metadata` con las claves estables.
  Todos los valores pasan por `encodeURIComponent`.
- **Tipo de evento:** videollamada de **30 minutos** (a confirmar, Anexo E), con el proveedor de
  vídeo configurado en Cal.com. Los correos de confirmación y recordatorio los manda Cal.com: la web
  **no** envía ningún correo.

### 9.3 Medidas y estados

- Contenedor del embed: `min-block-size: 560px` en móvil, `640px` en ≥1024px, ancho 100% hasta
  `max-width: 900px` (más ancho que los 640px del resto de pasos: el calendario lo necesita).
- **Mientras carga:** un esqueleto propio (rectángulos en `--bg-elev-1` con un pulso de opacidad muy
  suave), nunca un spinner girando ni la pantalla en blanco.
- **Si el script falla o tarda más de 10 segundos:** oculta el esqueleto y muestra el fallback (§9.4)
  como contenido principal, con el texto *"El calendario no ha cargado. Puedes reservar aquí:"*.
- El embed hace **su propio scroll interno**; el fondo de la página no debe hacer scroll a la vez
  (`overscroll-behavior: contain` en el contenedor).

### 9.4 Fallback

Siempre visible, bajo el calendario, en `--fs-small` / `--fg-muted`:

> ¿No ves el calendario? [Reserva aquí](https://cal.com/&lt;usuario&gt;/&lt;evento&gt;)

Con `target="_blank" rel="noopener"`. Con JS deshabilitado, es lo único que se muestra.

---

## 10. Pantalla de cierre

Se activa al recibir el evento **`bookingSuccessful`** del embed.

- Titular display: `NOS VEMOS PRONTO`.
- Debajo, en `--fs-lead` / `--fg-muted`: el **día y la hora** de la reserva, formateados en español
  y en la zona horaria del usuario (*"Jueves 4 de septiembre, 17:00"*), más
  *"Te hemos enviado la invitación por correo."*
- Un botón secundario: `Volver al inicio`, que cierra el overlay.
- La barra de progreso se queda al 100% en `--accent`.
- **Limpieza:** borra la clave `briefing` de `sessionStorage` y quita el hash de la URL con
  `replaceState`.
- Si había un `pendingSync`, lanza aquí el último reintento de envío.
- Sin confeti, sin animaciones de celebración. Un titular grande basta.

---

## 11. Navegación, teclado y gestos

### 11.1 Teclado

| Tecla | Acción |
|---|---|
| `Enter` | Avanza si el paso es válido (en el textarea del paso 5: salto de línea) |
| `Cmd/Ctrl + Enter` | Avanza desde el textarea del paso 5 |
| `Esc` | Cierra el flujo (con confirmación si hay respuestas escritas) |
| `Tab` / `Shift+Tab` | Recorre solo los elementos del overlay (trampa de foco) |
| `Espacio` | Marca/desmarca la opción enfocada en el paso 7 |

### 11.2 Foco

- Al abrir el overlay: foco al **campo del paso 1**, no al header.
- Al cambiar de paso: foco al primer control del paso nuevo, **después** de que termine la
  transición de entrada.
- Al cerrar: foco de vuelta al botón "Empezar un proyecto" del hero.
- **Trampa de foco** activa mientras el overlay esté abierto.

### 11.3 Cierre y confirmación

- Cerrar (botón "← Volver" o `Esc`) con **al menos una respuesta escrita** abre una confirmación
  nativa breve: *"¿Salir del cuestionario? Guardamos tus respuestas por si vuelves."* con
  `Salir` / `Seguir aquí`.
- Si no hay ninguna respuesta, cierra directamente sin preguntar.
- Al salir, el estado **se conserva** en `sessionStorage` (por eso la confirmación puede prometerlo).

### 11.4 Gestos

- **Sin swipe horizontal** entre pasos: interfiere con el gesto de retroceso de iOS y con la
  selección de texto. Se avanza solo con los botones y el teclado.

---

## 12. Movimiento

- **Apertura del overlay:** `opacity 0→1` en `240ms` más `scale(0.98→1)` del bloque de contenido.
- **Cambio de paso (hacia delante):** salida `opacity→0` + `translateX(-24px)` en `200ms`; entrada
  desde `translateX(24px)` en `320ms var(--ease)`, encadenadas (no simultáneas).
- **Hacia atrás:** las mismas transiciones con el eje invertido.
- **Barra de progreso:** `transform: scaleX()` en `320ms var(--ease)`, sincronizada con la entrada
  del paso nuevo.
- **Contador `n/9`:** cambia sin animación de número. Nada de contadores rodando.
- **Aparición del campo "Otro"** (paso 7): altura + opacidad, `200ms`.
- **`prefers-reduced-motion: reduce`:** cambios de paso instantáneos, sin sacudida de error, sin
  animación de la barra (que se actualiza igual, pero sin transición).
- Anima **solo** `opacity` y `transform`. La única excepción admitida es la altura del campo "Otro".

---

## 13. Accesibilidad

1. **`role="dialog" aria-modal="true"`** con `aria-labelledby` apuntando al titular del paso.
2. **El titular de cada paso es un `<h1>`** dentro del diálogo (el `<h1>` del hero queda oculto al
   estar el overlay abierto, así que no hay dos títulos compitiendo en el árbol accesible).
3. **Anuncia el cambio de paso** con una región `aria-live="polite"` que diga *"Paso 5 de 9"* más el
   titular.
4. **Cada control lleva `<label>` asociado**, aunque visualmente el titular haga de etiqueta: usa
   `aria-labelledby` apuntando al titular, o un `<label class="sr-only">`. Un input sin nombre
   accesible es un fallo, por muy claro que sea visualmente.
5. **Errores** con `role="alert"`, `aria-invalid` y `aria-describedby` (§6.5).
6. **Paso 7:** el conjunto va en un `<fieldset>` con `<legend class="sr-only">`; cada opción es un
   checkbox real dentro de un `<label>`. Nada de `div` con `role="checkbox"`.
7. **Paso 8:** `<select>` nativo, sin sustituto custom.
8. **Foco visible** en todos los controles, incluidas las filas de opción.
9. **Áreas táctiles ≥ 44×44px**; las filas de opción ya miden 72px.
10. **El progreso** se expone también de forma textual (el contador `n / 9`), no solo con la barra
    visual, que va `aria-hidden`.
11. **Zoom al 200%** sin pérdida de contenido ni scroll horizontal.
12. **El embed de Cal.com** va en un contenedor con `aria-label` y su iframe con `title`.

---

## 14. Rendimiento

- **Todo el flujo se sirve con el bundle de la home.** Nada de una ruta aparte que descargue otro
  documento: el usuario debe ver el paso 1 al instante tras el clic.
- Peso del JS del cuestionario: **< 14 KB** comprimido, sin contar Cal.com.
- **Cal.com solo se carga en el paso 9** (o al pulsar el CTA de agenda). Si el usuario abandona en el
  paso 4, no ha descargado ni un byte de Cal.com.
- Los 9 pasos viven en el DOM como un solo contenedor que **reemplaza su contenido**, no como 9
  secciones ocultas — ni como 9 componentes montados a la vez.
- Sin `will-change` permanente: se pone al empezar la transición y se quita en `transitionend`.
- El *debounce* de escritura en `sessionStorage` evita escribir en cada pulsación.

---

## 15. Anti-spam y privacidad

- **Honeypot:** un campo oculto (`position: absolute; left: -9999px`, `tabindex="-1"`,
  `autocomplete="off"`) que un humano nunca rellena. Si llega con valor, se descarta el envío en
  silencio (respuesta 200 igualmente, para no dar pistas al bot).
- **Marca de tiempo:** si el flujo se completa en menos de 8 segundos, se marca como sospechoso en el
  envío (no se bloquea: se etiqueta).
- **Sin CAPTCHA.** Rompería el tono del flujo y no hace falta para este volumen.
- **Rate limiting** en el endpoint, no en el cliente.
- **Privacidad:**
  - Aviso discreto bajo el botón del **paso 3** (el primero que recoge un dato de contacto), en
    `--fs-small` / `--fg-faint`: *"Solo usamos tus datos para responderte. Nada de spam."* con
    enlace a la política de privacidad.
  - Los datos viven en `sessionStorage`, no en `localStorage` (§7.2).
  - **No** envíes las respuestas a la analítica. Los eventos de §16 son anónimos: paso alcanzado y
    poco más.
  - Todo el envío por HTTPS. El teléfono es un dato personal: no lo registres en logs del cliente ni
    lo metas en la URL de ninguna redirección.

---

## 16. Analítica

Eventos mínimos, **sin contenido de las respuestas**:

| Evento | Cuándo | Propiedades |
|---|---|---|
| `briefing_open` | Se abre el cuestionario | `origen` (hero / header) |
| `briefing_step` | Se completa un paso | `paso` (1–8) |
| `briefing_abandon` | Se cierra sin terminar | `paso` alcanzado |
| `briefing_submit` | POST correcto | — |
| `calendar_view` | Se muestra el paso 9 | — |
| `booking_success` | Reserva confirmada | — |

El embudo por paso es el dato que dirá qué pregunta está espantando gente. El paso 3 (teléfono) y el
8 (presupuesto) son los sospechosos habituales: vigílalos.

---

## 17. Arquitectura de archivos y entregables

```
assets/js/briefing/
├─ index.js          → apertura/cierre del overlay, historial, orquestación
├─ steps.js          → definición declarativa de los 9 pasos (titular, ayuda, control, validación)
├─ render.js         → pinta el paso actual en el contenedor
├─ state.js          → modelo, persistencia en sessionStorage, debounce
├─ validate.js       → validadores por paso y mensajes de error
├─ submit.js         → POST, reintentos, idempotencia
└─ calendar.js       → carga perezosa de Cal.com, prefill, bookingSuccessful
assets/css/
└─ briefing.css      → overlay, chrome de paso, campos, filas de opción
```

**Los 9 pasos se definen de forma declarativa** en `steps.js`, para que añadir o reordenar preguntas
sea editar un array y no tocar la lógica:

```js
{ id:'marca', titular:'NOMBRE DE TU MARCA', ayuda:null,
  control:{ tipo:'texto', autocomplete:'organization' },
  validar: v => v.trim() ? null : '¿Cómo se llama tu marca?' }
```

**Entregables:**

1. Flujo completo de 9 pasos funcionando desde el CTA del hero, en español.
2. Persistencia, validación, envío con reintentos e idempotencia.
3. Paso 9 con Cal.com inline + popup desde hero/header, con carga perezosa, tema oscuro, `locale: es`
   y prefill.
4. Pantalla de cierre y limpieza de estado.
5. Los stubs `openBriefing()` / `openCalendar()` de fase 1 **sustituidos por la implementación real**,
   manteniendo los mismos nombres y los mismos atributos `data-action`.

---

## 18. Checklist de QA

**Flujo**

- [ ] Los 9 pasos avanzan y retroceden conservando lo escrito.
- [ ] El botón "atrás" del navegador y el gesto de iOS retroceden un paso, no cierran el flujo.
- [ ] Recargar en mitad del cuestionario reanuda en el paso correcto.
- [ ] El paso 6 se puede saltar vacío y el botón dice `Saltar`.
- [ ] Marcar `Otro` en el paso 7 despliega el campo de texto y lo exige.
- [ ] Las respuestas se envían al terminar el paso 8, aunque luego no se reserve.
- [ ] Un fallo del POST no impide llegar al calendario.
- [ ] Tras reservar se ve la pantalla de cierre y `sessionStorage` queda limpio.

**Formularios**

- [ ] El `Siguiente` pasa de crema a ámbar exactamente cuando el paso valida.
- [ ] Ningún campo muestra error mientras se escribe.
- [ ] Los mensajes de error aparecen al pulsar `Siguiente` y mueven el foco al campo.
- [ ] El teclado del móvil es el correcto en cada paso (texto, tel, url).
- [ ] En iOS no hay zoom automático al enfocar ningún campo.
- [ ] El textarea del paso 5 crece con el contenido y para a las 8 líneas.
- [ ] El teléfono se guarda en E.164 con el prefijo del país elegido.

**Visual**

- [ ] Los 9 pasos comparten exactamente el mismo ritmo vertical.
- [ ] El paso 7 cabe en 390×844 sin comprimir el espaciado (con scroll si hace falta).
- [ ] El calendario de Cal.com sale en oscuro, con el ámbar de marca y en español.
- [ ] Ningún color ni tamaño fuera de los tokens de fase 1.

**Accesibilidad**

- [ ] Flujo completo solo con teclado, de principio a fin, con trampa de foco.
- [ ] Lector de pantalla anuncia "Paso n de 9" y el titular en cada cambio.
- [ ] Todos los campos tienen nombre accesible.
- [ ] `prefers-reduced-motion` respetado en transiciones y en la sacudida de error.

**Rendimiento**

- [ ] Cal.com no se descarga hasta el paso 9 o el clic en el CTA de agenda.
- [ ] El paso 1 aparece de inmediato tras el clic, sin petición de red.

---

## 19. Anti-patrones

- Un formulario largo con los 9 campos apilados y un "Enviar" al final. Eso es justo lo contrario de
  esto.
- Barras de progreso con porcentaje (`56%`) en vez del `n / 9`.
- Validar en rojo mientras el usuario escribe.
- Bloquear el avance con un CAPTCHA o pedir email **y** teléfono **y** empresa "por si acaso".
- Pedir el email: **no está en los 9 pasos**; Cal.com ya lo recoge al reservar. No lo añadas.
- Convertir el paso 2 en un desplegable de 195 países.
- Cargar el script de Cal.com en el `<head>` o al abrir el paso 1.
- Guardar el estado en `localStorage` (datos personales que sobreviven al cierre del navegador).
- Confeti, sonidos, o un contador animado en la pantalla de cierre.
- Añadir un paso 10 "¿Cómo nos conociste?". Nueve ya son muchos.
- Reintentar el POST en bucle si el endpoint está caído.

---

## Anexo A — Copy completo

| Slot | Texto |
|---|---|
| Botón cerrar | `← Volver` |
| Contador | `n / 9` |
| P1 titular | `¿CÓMO TE LLAMAS?` |
| P2 titular | `¿DE DÓNDE ERES?` |
| P3 titular | `¿CUÁL ES TU NÚMERO<br>DE WHATSAPP?` |
| P3 ayuda | `Elige tu país y escribe el número sin el prefijo.` |
| P3 aviso | `Solo usamos tus datos para responderte. Nada de spam.` |
| P4 titular | `NOMBRE DE TU MARCA` |
| P5 titular | `CUÉNTANOS MÁS<br>SOBRE TU MARCA` |
| P5 ayuda | `¿En qué sector estás? ¿Cuál es tu producto o servicio? ¿Qué quieres conseguir con él?` |
| P6 titular | `WEB ACTUAL<br>O INSTAGRAM` |
| P6 ayuda | `Si aún no tienes, salta este paso.` |
| P7 titular | `¿QUÉ SERVICIO<br>TE INTERESA?` |
| P7 ayuda | `Puedes elegir más de uno.` |
| P7 opciones | `Diseño + Desarrollo Web` · `Landing Page` · `Rediseño de Web` · `E-commerce` · `Branding` · `Otro` |
| P7 "Otro" | `Cuéntanos qué necesitas` |
| P8 titular | `TU PRESUPUESTO` |
| P8 vacío | `Elige una opción…` |
| P8 opciones | `Menos de 750 €` · `750 – 1.500 €` · `1.500 – 3.000 €` · `3.000 – 5.000 €` · `5.000+ €` |
| P9 titular | `AGENDA TU VIDEOLLAMADA` |
| P9 ayuda | `Elige el día y la hora que mejor te vaya. Te llega la invitación al momento.` |
| P9 fallback | `¿No ves el calendario? Reserva aquí` |
| Botones | `Atrás` · `Siguiente` · `Saltar` |
| Reanudar | `Retomamos donde lo dejaste.` |
| Confirmar salida | `¿Salir del cuestionario? Guardamos tus respuestas por si vuelves.` |
| Cierre titular | `NOS VEMOS PRONTO` |
| Cierre texto | `Te hemos enviado la invitación por correo.` |
| Cierre botón | `Volver al inicio` |

---

## Anexo B — CSS de referencia

```css
.briefing{
  position:fixed; inset:0; z-index:200; background:var(--bg);
  display:grid; align-content:center;
  padding-block:calc(var(--header-h) + var(--space-8)) var(--space-10);
  padding-inline:var(--gutter);
  overflow-y:auto; overscroll-behavior:contain;
}
.briefing__inner{ inline-size:100%; max-inline-size:640px; margin-inline:auto; text-align:center; }

.step__counter{
  font-size:var(--fs-counter); font-weight:500; letter-spacing:.06em;
  font-variant-numeric:tabular-nums; color:var(--fg-faint);
  margin-block-end:var(--space-7);
}
.step__counter b{ color:var(--accent); font-weight:500; }

.step__title{
  font-family:var(--font-display); font-weight:400; text-transform:uppercase;
  font-size:clamp(2rem,7vw,3.25rem); line-height:.95; letter-spacing:-.015em;
  color:var(--fg); margin:0;
}
.step__help{
  font-size:var(--fs-body); color:var(--fg-muted);
  max-inline-size:42ch; margin:var(--space-5) auto 0;
}
.step__answer{ margin-block-start:var(--space-9); }
.step__nav{
  display:flex; gap:var(--space-4); margin-block-start:var(--space-9);
}
.step__nav .btn{ flex:1 1 0; }

/* Campo con hairline inferior */
.field{
  inline-size:100%; background:transparent; border:0;
  border-block-end:1px solid var(--fg); border-radius:0;
  color:var(--fg); font:inherit; font-size:var(--fs-lead);
  text-align:center; padding-block:var(--space-3);
  -webkit-appearance:none; appearance:none;
  transition:border-color var(--dur-fast) ease-out;
}
.field::placeholder{ color:var(--fg-faint); }
.field:focus{ border-block-end-color:var(--accent); }
.field:focus-visible{ outline:2px solid var(--focus-ring); outline-offset:4px; }
.field[aria-invalid="true"]{ border-block-end-color:var(--red-500); }

.field--select{ background-image:url("data:image/svg+xml,…"); /* chevron */
  background-repeat:no-repeat; background-position:right center; }

/* Fila de opción (paso 7) */
.option{
  display:flex; align-items:center; gap:var(--space-4);
  block-size:72px; padding-inline:var(--space-5);
  border:1px solid var(--border); border-radius:2px;
  text-align:start; cursor:pointer;
  transition:border-color 160ms ease-out, background-color 160ms ease-out;
}
.option:hover, .option:focus-within{ border-color:var(--fg); }
.option:has(:checked){ border-color:var(--accent); }
.option__box{
  inline-size:22px; block-size:22px; flex:none;
  border:1px solid var(--fg-faint); border-radius:2px;
  display:grid; place-items:center;
}
.option:has(:checked) .option__box{ background:var(--accent); border-color:var(--accent); color:var(--on-accent); }
.option input{ position:absolute; opacity:0; pointer-events:none; }

.error{ color:var(--red-500); font-size:var(--fs-small); margin-block-start:var(--space-3); }

@media (prefers-reduced-motion:reduce){
  .briefing *{ transition-duration:.01ms!important; animation:none!important; }
}
```

---

## Anexo C — Marcado de referencia

```html
<div class="briefing" role="dialog" aria-modal="true" aria-labelledby="step-title" hidden>
  <header class="header header--briefing"> … ← Volver … </header>

  <div class="briefing__inner">
    <p class="step__counter" aria-hidden="true"><b>5</b> / 9</p>
    <p class="sr-only" aria-live="polite">Paso 5 de 9: Cuéntanos más sobre tu marca</p>

    <h1 class="step__title" id="step-title">Cuéntanos más<br>sobre tu marca</h1>
    <p class="step__help" id="step-help">¿En qué sector estás? ¿Cuál es tu producto o servicio?</p>

    <div class="step__answer">
      <label class="sr-only" for="descripcion">Cuéntanos más sobre tu marca</label>
      <textarea class="field" id="descripcion" name="descripcion" rows="1"
                aria-describedby="step-help" enterkeyhint="enter"></textarea>
      <p class="error" role="alert" hidden></p>
    </div>

    <div class="step__nav">
      <button type="button" class="btn btn--secondary" data-nav="prev">Atrás</button>
      <button type="button" class="btn btn--primary"   data-nav="next">Siguiente</button>
    </div>

    <input class="hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  </div>
</div>
```

---

## Anexo D — JS de referencia

```js
// steps.js — definición declarativa
export const STEPS = [
  { id:'nombre', titular:'¿Cómo te llamas?',
    control:{ tipo:'texto', autocomplete:'given-name', enterkeyhint:'next' },
    validar: v => v.trim().length >= 2 ? null : 'Escribe tu nombre para continuar.' },

  { id:'referencia', titular:'Web actual<br>o Instagram',
    ayuda:'Si aún no tienes, salta este paso.',
    control:{ tipo:'texto', inputmode:'url', autocapitalize:'none' },
    opcional:true,
    normalizar: v => !v ? '' : v.startsWith('@') ? `https://instagram.com/${v.slice(1)}`
                    : /^https?:\/\//.test(v) ? v : `https://${v}`,
    validar: () => null },
  // …
];

// index.js — avance
function next(){
  const step = STEPS[state.paso - 1];
  const error = step.validar(currentValue());
  if (error) return showError(error);          // no avanza, foco al campo, sacudida
  save(step.id, step.normalizar?.(currentValue()) ?? currentValue());
  if (state.paso === 8) submit();              // envía antes de mostrar el calendario
  goTo(state.paso + 1);
}

// calendar.js — carga perezosa
let loaded = false;
export async function mountCalendar(container){
  if (!loaded){
    await import('https://app.cal.com/embed/embed.js');   // solo aquí
    loaded = true;
  }
  Cal('init', { origin:'https://cal.com' });
  Cal('inline', {
    elementOrSelector: container,
    calLink: `${CAL_USER}/${CAL_EVENT}`,
    config: {
      locale: 'es',
      name: state.respuestas.nombre,
      notes: buildNotes(state.respuestas),
      'metadata[presupuesto]': state.respuestas.presupuesto
    }
  });
  Cal('ui', { theme:'dark', layout:'month_view', cssVarsPerTheme:{ dark:{ 'cal-brand':'#E8A33D', /* … */ } } });
  Cal('on', { action:'bookingSuccessful', callback: e => showClosing(e.detail) });
}
```

---

## Anexo E — Decisiones abiertas

1. **Usuario y slug del evento de Cal.com** (`cal.com/<usuario>/<evento>`).
2. **Duración de la videollamada:** 30 minutos por defecto. ¿Se mantiene?
3. **Destino de las respuestas:** endpoint propio, webhook de **n8n**, correo o CRM.
   (El servidor MCP de n8n de esta sesión no conectó, así que no he podido comprobar qué flujos
   tienes montados ahí.)
4. **Moneda del paso 8:** euros (propuesto) o dólares como en la referencia.
5. **Política de privacidad:** URL a la que enlaza el aviso del paso 3.
6. **Preguntas 6–8:** confirmadas a partir de las capturas. ¿Alguna que quieras cambiar antes de
   implementar?
7. Si el aviso de privacidad debe aparecer también en el paso 9 (Cal.com recoge el email).
