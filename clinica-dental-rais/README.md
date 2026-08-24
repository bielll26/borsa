# Clínica Dental RAIS · página principal

Reconstrucción de la portada de <https://www.clinicadentalrais.es> como sitio estático,
sin dependencias ni proceso de compilación.

## Contenido

| Fichero | Qué hay dentro |
| --- | --- |
| `index.html` | Estructura y textos de la página principal, con los iconos SVG en línea |
| `styles.css` | Paleta, tipografía, maquetación, estados de interacción y animaciones |
| `script.js` | Comportamiento: menú, apariciones al hacer scroll, contadores, carrusel, acordeón, formulario y cookies |

## Verlo

Basta con abrir `index.html` en el navegador. Para servirlo por HTTP:

```bash
python3 -m http.server 8080 --directory clinica-dental-rais
# http://localhost:8080
```

## Secciones

Barra de contacto y selector de idioma · cabecera fija con desplegable de especialidades ·
hero · marquesina de marcas · contadores · historia de la clínica · las ocho especialidades ·
por qué DentalRAIS · casos de éxito con comparador antes/después · equipo y homenaje a la
Dra. Alicia Rais · tecnología · opiniones · banda de financiación · preguntas frecuentes ·
contacto con formulario y mapa · pie · botones flotantes y aviso de cookies.

## Animaciones

- Cabecera que se encoge y proyecta sombra al bajar, con barra de progreso de lectura.
- Entrada escalonada del hero, subrayado que se dibuja solo y paralaje suave de los elementos flotantes.
- Apariciones al entrar en pantalla (`IntersectionObserver`) en cuatro direcciones, con retardos por tarjeta.
- Contadores que se animan la primera vez que se ven.
- Marquesina infinita de marcas que se detiene al pasar el ratón.
- Comparador antes/después arrastrable (ratón, táctil y teclado) con un gesto de bienvenida.
- Carrusel de opiniones con reproducción automática, puntos, arrastre y pausa al pasar el ratón.
- Acordeón de preguntas frecuentes, menú lateral con entrada escalonada y aviso de cookies deslizante.

Todo el movimiento se desactiva con `prefers-reduced-motion: reduce`.

## Imágenes

Las fotografías se dejan como marcadores (`.ph`): recuadros con textura y una etiqueta que
indica qué imagen va en cada hueco. Para sustituirlos basta con poner un `<img>` en su lugar.

## Tipografías

Se cargan Fraunces y Manrope desde Google Fonts, con alternativas del sistema si no hay red.
