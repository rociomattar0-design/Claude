# bravissima en Tiendanube

Guía para aplicar la identidad de marca en un tema de Tiendanube. Empezá por el **paso 1** y seguí en orden. Con el panel del tema y un archivo CSS alcanza: no hace falta tocar código del tema.

> Los nombres de los menús de Tiendanube cambian un poco según el tema y las actualizaciones del panel. Si no encontrás algo con el nombre exacto que figura acá, buscá uno parecido en la misma zona.

---

## 1. Elegí un tema con mucho aire

Buscá un tema con estas características:

- Encabezado con el logo **centrado**.
- Fotos de producto grandes, en formato vertical (4:5 o 3:4).
- Pocos adornos: sin bordes redondeados marcados, sin sombras, sin íconos de colores.
- Barra de anuncios arriba, para usarla con "lanzamiento 03.12".

**Cómo probar:** cambiá de tema solo en la vista previa y fijate cómo se ve en el celular. La mayoría de las compras va a llegar desde Instagram, o sea, desde el teléfono.

## 2. Logo y favicon

En el panel del diseño, en la sección **Logo**:

| Qué | Archivo | De dónde |
|---|---|---|
| Logo (fondo claro) | `bravissima_logotipo_bordo_3000px.png` | `01_logo/png/` |
| Logo (fondo oscuro, si el tema lo pide) | `bravissima_logotipo_crema_3000px.png` | `01_logo/png/` |
| Favicon | `icono-512.png` | `06_web/prototipo/img/` |

- **Logo:** subí siempre el PNG de 3000 px; Tiendanube lo achica. Nunca escribas "bravissima" como texto en lugar del logo, porque la doble ss fundida solo existe en el archivo.
- **Tamaño:** si el tema deja elegir el tamaño, usá el **mediano**. El logo tiene que medir al menos 140 px de ancho en pantalla.

## 3. Colores

En el panel del diseño, en la sección **Colores**, cargá estos valores. El paso 4 asegura los mismos colores aunque el tema no tenga todas estas opciones.

| Opción del tema | Color | HEX |
|---|---|---|
| Fondo | Crema | `#EFE7DD` |
| Textos | Casi negro | `#150B0D` |
| Color principal / botones / links | Bordó | `#5E1A24` |
| Texto de los botones | Crema | `#EFE7DD` |
| Barra de anuncios / pie | Vino | `#3A0F16` |
| Detalles / acento | Oro viejo | `#B8955A` |
| Fondos secundarios | Rosa empolvado | `#D9B8AE` |

## 4. CSS personalizado (tipografías y detalles)

La lista de fuentes del panel probablemente no tenga **Kalnia**, por eso las tipografías se cargan por CSS.

1. Buscá en el panel del diseño la opción para editar CSS. Según el tema se llama "Edición de CSS avanzado", "CSS personalizado" o parecido, y suele estar al final de la lista de opciones del diseño.
2. Abrí `06_web/tiendanube/bravissima-tiendanube.css`, copiá **todo** el contenido y pegalo ahí.
   - La línea que empieza con `@import` tiene que quedar **primera**.
   - Si ya había CSS cargado, pegá el nuevo **arriba** de lo anterior.
3. Guardá y mirá la tienda en el celular y en la computadora.

**Qué hace el archivo:**

- Títulos y nombres de producto en **Kalnia Light**, en minúscula.
- Textos en **Cormorant Garamond**, con números alineados.
- Botones bordó con letras crema en mayúscula espaciada. Al pasar el mouse cambian a vino.
- Campos de formulario finos, con borde bordó.
- Barra de anuncios y pie en vino. Los títulos del pie van en oro viejo.
- Fondo rosa empolvado en las fotos mientras cargan.

### Si las tipografías no aparecen

Pasa cuando el tema mete su propio CSS antes que el tuyo y el `@import` queda ignorado.

- **Verificá** que el `@import` sea literalmente la primera línea del cuadro.
- **Si sigue sin andar:** si tu plan permite agregar código al `<head>` (desde herramientas para programadores o códigos externos), pegá esto y borrá la línea del `@import` del CSS:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400&family=Kalnia:wght@300&display=swap">
  ```
- **Plan B:** en la lista de fuentes del tema elegí una serif clásica para los textos (Cormorant Garamond, si está). Los títulos se van a ver distintos, pero el logo no cambia porque es una imagen.

### Si un botón o un título no cambia

Cada tema nombra sus elementos de forma distinta:

1. Hacé clic derecho sobre ese elemento y elegí **Inspeccionar**.
2. Fijate el `class="..."` del elemento.
3. Agregá esa clase en el bloque que corresponda del CSS. Por ejemplo, para un botón: `.btn, .btn-primary, .tu-clase-nueva { ... }`.

## 5. Estructura de la tienda

Armá las categorías y páginas igual que en el prototipo (`06_web/prototipo/`):

| Menú | Tipo en Tiendanube | Contenido |
|---|---|---|
| colecciones | Categorías: **artesanal**, **fiesta**, **cápsulas** | Productos |
| mujeres bravas | Página de contenido | Fotos de clientas + texto (copialo de `mujeres-bravas.html`) |
| la founder | Página de contenido | Tu historia + el taller (`la-founder.html`) |
| cuidados | Página de contenido | Guía de cuidados (`cuidados.html`) |
| contacto | Página de contacto del tema | WhatsApp, Instagram, email, pop-ups |

**Barra de anuncios:** `lanzamiento 03.12 · hecho para mujeres bravas`. Después del lanzamiento, usala para envíos o para el próximo pop-up.

**Home, en este orden** (si el tema deja ordenar secciones):

1. Banner con el slogan.
2. Las tres colecciones.
3. Productos nuevos.
4. Banner de "mujeres bravas".
5. Newsletter: "sumate a las bravas".

## 6. Fichas de producto

Cargá cada pieza siguiendo esta estructura. Completala con los datos reales; no copies los ejemplos tal cual.

- **Nombre:** en minúscula, corto, con personalidad. Ejemplo: `[nombre de la pieza]`.
- **Descripción:**
  1. Una línea que cuente la pieza, en itálica si el editor lo permite.
  2. Un párrafo corto: cómo se usa, con qué combina.
  3. Datos en lista: **material**, **terminación**, **piedra**, **medidas**, **peso**.
  4. Una línea fija: *Cada pieza se hace a mano: puede tener pequeñas diferencias con la foto. Eso la hace única.*
  5. Un link a la página de cuidados.
- **Fotos:** usá la misma proporción en todas (vertical 4:5) y el mismo fondo de la paleta. La primera foto, sobre fondo liso; la segunda, puesta. Seguí las indicaciones de la página de fotografía del manual.
- **Variantes:** solo si existen de verdad (por ejemplo, terminación dorada o plateada).

## 7. Banners

- **Medidas:** cada tema pide medidas distintas para los banners; mirá cuáles muestra el panel al subir la imagen.
- **De dónde sacarlos:** usá como base los posts y stories de `04_redes/`, editándolos en Canva con el PDF editable y cambiando el tamaño del diseño.
- **Banner de escritorio:** horizontal, con el texto a un costado y no en el centro, para que no lo tape el producto.
- **Banner para celular:** si el tema permite cargar uno aparte, hacelo vertical. Si no, dejá el texto grande y centrado.

## 8. Checklist antes del lanzamiento

- [ ] Logo en PNG (no texto) y favicon cargados.
- [ ] Colores del panel cargados y CSS pegado.
- [ ] Tipografías funcionando en celular y computadora.
- [ ] Las tres categorías creadas, con al menos una pieza cada una.
- [ ] Páginas "mujeres bravas", "la founder", "cuidados" y "contacto" creadas.
- [ ] Barra de anuncios con "lanzamiento 03.12".
- [ ] En cada ficha: precio, material, terminación, piedra y medidas reales (nada en [completar]).
- [ ] Datos de contacto, @ de Instagram y dominio cargados.
- [ ] Compra de prueba hecha desde el celular.
