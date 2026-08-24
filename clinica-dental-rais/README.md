# Clínica Dental RAIS — réplica de clinicadentalrais.es

Reconstrucción estática (HTML + CSS + JS, sin dependencias) de la página de inicio
de **Clínica Dental RAIS** (Terrassa), hecha a partir de las cuatro grabaciones de
pantalla del sitio original. El dominio está bloqueado por la política de red de
este entorno, así que **todo lo que hay aquí procede de los vídeos**, fotograma a
fotograma: textos, orden de las secciones, colores y animaciones.

## Abrir

Basta con abrir `index.html` en el navegador (no necesita servidor).

## Estructura

`index.html` · `assets/styles.css` · `assets/script.js`

Secciones, en el mismo orden que el original:

1. Barra de idiomas (Català / Español) + redes
2. Cabecera blanca con el logo circular colgando y el botón rosa de menú
3. Hero con pase de imágenes y caja gris azulada («+25 años en Terrassa»)
4. La clínica + CTA de teléfono + dos imágenes con la insignia «+25 Años»
5. Nuestras Especialidades (8 tarjetas con icono de línea y flecha)
6. Bloque de imágenes con la insignia «Eres Único/a»
7. Digital Smile Design + contadores + botón «Casos de Éxito»
8. «Personalización, innovación y excelencia» / «Tu salud dental, nuestra prioridad»
9. «El legado de la Dra. Alicia Rais»
10. Nuestro Equipo
11. Comparador Antes / Después
12. Opiniones de Google (carrusel)
13. Preguntas frecuentes (acordeón)
14. Pie rosa + botón flotante de WhatsApp y de cookies

## Paleta (muestreada de los fotogramas)

| Uso | Color |
|---|---|
| Rosa principal (botones, menú) | `#f98697` |
| Fondo crema | `#fbf1f0` |
| Gris azulado (logo, hero) | `#596174` |
| Insignias oscuras | `#383234` |
| Borde de tarjetas | `#ffe0e1` |
| Filas del acordeón | `#f1f0f5` |
| Rosa del pie | `#fcbabc` |
| Estrellas | `#f4c541` |

## Animaciones reproducidas

- Pase automático del hero con fundido cruzado, zoom lento y cambio de titular.
- Aparición al hacer scroll (opacidad + desplazamiento) con retardo escalonado en rejillas.
- Contadores que suben al entrar en pantalla.
- Menú a pantalla completa con entrada escalonada de los enlaces.
- Hover de tarjetas (elevación + flecha que se desplaza y se rellena).
- Carrusel de opiniones con puntos, arrastre y avance automático.
- Comparador Antes/Después arrastrable (ratón, táctil y teclado).
- Acordeón de FAQ con apertura animada y flecha que gira.
- Insignias flotantes y pulso del botón de WhatsApp.
- Todo se desactiva con `prefers-reduced-motion`.

## Qué no procede del original

- **Imágenes**: marcadores de posición en CSS (el encargo pedía dejar *placeholders*).
- **Tipografía**: el original usa una familia tipo Museo Sans; aquí se usa **Figtree**
  (Google Fonts), la alternativa libre más parecida.
- Cifras finales de los contadores (`10.000+`, `1.500+`, `6`): en los vídeos solo se ven
  valores intermedios de la animación; son una estimación coherente con ellos.
- Cuatro respuestas del acordeón y dos opiniones: en los vídeos solo se leen dos
  respuestas completas (financiación y urgencias) y dos opiniones (Pilar y María Jesús);
  el resto se ha redactado en el mismo tono.
- La ficha de «Mariela Andreotti» del equipo (en el vídeo su tarjeta queda cortada;
  su nombre y su papel al frente de la clínica sí aparecen en el texto del legado).
- Enlaces legales y del menú, que apuntan a anclas o a `#`.
