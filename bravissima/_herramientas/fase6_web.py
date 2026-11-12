"""FASE 6 — Prototipo web (HTML estático, mobile first). Genera las 7 páginas con el mismo encabezado y pie."""
from marca import RAIZ

OUT = RAIZ / "06_web" / "prototipo"

PAGINAS = [  # (archivo, texto del menú)
    ("index.html", "inicio"),
    ("colecciones.html", "colecciones"),
    ("mujeres-bravas.html", "mujeres bravas"),
    ("la-founder.html", "la founder"),
    ("cuidados.html", "cuidados"),
    ("contacto.html", "contacto"),
]

ICONO_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 7h18M3 12h18M3 17h12"/></svg>'
ICONO_CERRAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 5l14 14M19 5L5 19"/></svg>'
ICONO_BOLSA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M5 8h14l-1.2 12.5H6.2z"/>'
               '<path d="M9 10V6.5a3 3 0 016 0V10"/></svg>')


def nav(actual, clase="nav"):
    items = [p for p in PAGINAS if p[0] != "index.html"]
    return "".join(f'<a href="{a}"{" aria-current=\"page\"" if a == actual else ""}>{t}</a>' for a, t in items)


def pagina(archivo, titulo, descripcion, cuerpo):
    izq = [p for p in PAGINAS[1:4]]
    der = [p for p in PAGINAS[4:]]
    link = lambda a, t: f'<a href="{a}"{" aria-current=\"page\"" if a == archivo else ""}>{t}</a>'
    html = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{descripcion}">
<meta name="theme-color" content="#5E1A24">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fuentes/Kalnia-Light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="estilos.css">
</head>
<body>
<p class="barra">lanzamiento <strong>03.12</strong> · <span data-dias>faltan pocos días</span></p>

<header class="header">
  <div class="contenedor">
    <button class="icono-btn menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{ICONO_MENU}</button>
    <nav class="nav izq" aria-label="Principal">{"".join(link(a, t) for a, t in izq)}</nav>
    <a class="logo" href="index.html" aria-label="bravissima, inicio"><img src="img/logo-bordo.svg" alt="bravissima" width="160" height="24"></a>
    <div class="derecha">
      <nav class="nav" aria-label="Secundaria">{"".join(link(a, t) for a, t in der)}</nav>
      <a class="icono-btn carrito" href="#" aria-label="Carrito">{ICONO_BOLSA}<span class="cuenta" hidden>0</span></a>
    </div>
  </div>
</header>

<div class="menu-mobile" id="menu" aria-hidden="true">
  <button class="icono-btn cerrar" aria-label="Cerrar menú">{ICONO_CERRAR}</button>
  <nav aria-label="Menú">{"".join(link(a, t) for a, t in PAGINAS)}</nav>
  <div class="pie-menu">
    <img src="img/cardo-oro.svg" alt="" width="70" height="90">
    <p class="frase" style="font-size:24px">hecho para mujeres bravas</p>
    <p class="caps">@[usuario] · Córdoba, Argentina</p>
  </div>
</div>

<main>
{cuerpo}
</main>

<footer class="footer">
  <div class="contenedor">
    <div class="marca-pie">
      <img class="cardo" src="img/cardo-oro.svg" alt="" width="64" height="80">
      <img class="logo" src="img/logo-crema.svg" alt="bravissima" width="210" height="32">
      <p class="frase" style="font-size:24px;margin:0">hecho para mujeres bravas</p>
    </div>
    <div class="cols">
      <div><h4 class="caps">tienda</h4><ul><li><a href="colecciones.html#artesanal">artesanal</a></li><li><a href="colecciones.html#fiesta">fiesta</a></li><li><a href="colecciones.html#capsulas">cápsulas</a></li><li><a href="colecciones.html">todas las piezas</a></li></ul></div>
      <div><h4 class="caps">bravissima</h4><ul><li><a href="la-founder.html">la founder</a></li><li><a href="mujeres-bravas.html">mujeres bravas</a></li><li><a href="cuidados.html">cuidados</a></li></ul></div>
      <div><h4 class="caps">ayuda</h4><ul><li><a href="contacto.html">contacto</a></li><li><a href="contacto.html#preguntas">envíos y cambios</a></li><li><a href="contacto.html#popups">pop-ups</a></li></ul></div>
      <div><h4 class="caps">seguinos</h4><ul><li><a href="#">Instagram @[usuario]</a></li><li><a href="#">WhatsApp [completar]</a></li></ul></div>
    </div>
    <div class="legal"><span>Joyería de autor · hecha a mano en Córdoba, Argentina</span><span>© 2026 bravissima · [web]</span></div>
  </div>
</footer>

<p class="aviso">prototipo · fotos de ejemplo</p>
<script src="app.js"></script>
</body>
</html>
'''
    (OUT / archivo).write_text(html, encoding="utf-8")
    print("ok", archivo)


# ───────────────────────── piezas reutilizables ─────────────────────────
def foto(texto, clase=""):
    return f'<div class="foto {clase}" role="img" aria-label="Lugar para foto: {texto}"><span>{texto}</span></div>'


COLS = {"artesanal": "artesanal", "fiesta": "fiesta", "capsulas": "cápsulas"}


def tarjeta(i, col, nuevo=False):
    etiqueta = '<span class="etiqueta-mini">nuevo</span>' if nuevo else ""
    return (f'<a class="producto" href="producto.html" data-coleccion="{col}">'
            f'<div style="position:relative">{foto(f"foto pieza {i:02d}")}{etiqueta}</div>'
            f'<span class="col">{COLS[col]}</span>'
            f'<span class="nombre">[nombre de la pieza]</span>'
            f'<span class="precio">$ [completar]</span></a>')


# ───────────────────────── páginas ─────────────────────────
def inicio():
    cuerpo = f'''
<section class="fondo-bordo hero">
  <div class="contenedor">
    <img class="cardo" src="img/cardo-oro.svg" alt="" width="120" height="150">
    <p class="caps oro">joyería de autor · Córdoba</p>
    <h1 class="frase-xl">hecho para<br>mujeres bravas</h1>
    <p class="bajada">Piezas hechas a mano en taller: alpaca, bronce y cobre, terminación dorada y plateada, piedras naturales.</p>
    <div class="acciones"><a class="btn" href="colecciones.html">ver colecciones</a><a class="btn btn-linea" href="mujeres-bravas.html">mujeres bravas</a></div>
  </div>
</section>

<section class="fondo-vino seccion-s centro">
  <div class="contenedor">
    <p class="caps oro">lanzamiento</p>
    <p class="titulo t-xl" style="margin-top:6px">03.12</p>
    <div class="cuenta-regresiva" aria-label="Cuenta regresiva al lanzamiento">
      <div><b data-cuenta="dias">00</b><small>días</small></div>
      <div><b data-cuenta="horas">00</b><small>horas</small></div>
      <div><b data-cuenta="minutos">00</b><small>min</small></div>
      <div><b data-cuenta="segundos">00</b><small>seg</small></div>
    </div>
    <p class="frase" style="font-size:22px;margin-top:18px">3 de diciembre de 2026</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="cabecera centro"><p class="caps bordo">colecciones</p><h2 class="titulo t-l">elegí pocas, elegí bien</h2></div>
    <div class="grilla-3">
      <a class="coleccion" href="colecciones.html#artesanal">{foto("foto colección artesanal")}<h3 class="titulo t-m">artesanal</h3><p>Las piezas de todos los días, con marcas de taller.</p></a>
      <a class="coleccion" href="colecciones.html#fiesta">{foto("foto colección fiesta", "oscura")}<h3 class="titulo t-m">fiesta</h3><p>Para las noches que piden brillo.</p></a>
      <a class="coleccion" href="colecciones.html#capsulas">{foto("foto colección cápsulas")}<h3 class="titulo t-m">cápsulas</h3><p>Series cortas que no se repiten.</p></a>
    </div>
  </div>
</section>

<section class="fondo-crema2 seccion">
  <div class="contenedor dos-col">
    <div>
      <p class="caps bordo">el manifiesto</p>
      <p class="titulo t-l" style="margin:12px 0 22px">no hacemos joyas para gustarle a todo el mundo.</p>
      <p>Hacemos piezas para la que ya sabe quién es. Para la que se viste para ella. Para la que elige pocas cosas, pero las elige con el cuerpo entero.</p>
      <p>Cada pieza sale de un taller, de dos manos y de mucho fuego. Tiene marcas, tiene peso, tiene carácter. Como vos.</p>
      <a class="link-caps bordo" href="la-founder.html">conocé el taller</a>
    </div>
    <div>{foto("foto del taller · manos trabajando", "oscura alta")}</div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="cabecera" style="flex-direction:row;justify-content:space-between;align-items:flex-end">
      <div><p class="caps bordo">recién salidas del taller</p><h2 class="titulo t-l" style="margin-top:8px">nuevas</h2></div>
      <a class="link-caps bordo" href="colecciones.html">ver todas</a>
    </div>
    <div class="grilla">{tarjeta(1, "artesanal", True)}{tarjeta(2, "fiesta", True)}{tarjeta(3, "capsulas", True)}{tarjeta(4, "artesanal", True)}</div>
  </div>
</section>

<section class="fondo-rosa seccion">
  <div class="contenedor">
    <div class="cabecera centro"><p class="caps bordo">comunidad</p><h2 class="titulo t-l">mujeres bravas</h2>
      <p class="bajada bordo" style="max-width:560px">No tenemos clientas: tenemos mujeres bravas. Mostranos cómo llevás tu pieza.</p></div>
    <div class="bravas-grilla">
      {"".join(f'<figure class="brava" style="margin:0">{foto("foto de clienta", "oscura" if i % 2 else "")}<figcaption>@[usuario]</figcaption></figure>' for i in range(4))}
    </div>
    <div class="centro" style="margin-top:34px"><a class="btn" href="mujeres-bravas.html">ver a las bravas</a></div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor dos-col">
    <div>{foto("retrato de la founder", "alta")}</div>
    <div>
      <p class="caps bordo">la founder</p>
      <h2 class="titulo t-l" style="margin:10px 0 18px">[nombre]</h2>
      <p class="bajada bordo">«[Una frase tuya sobre por qué hacés lo que hacés.]»</p>
      <p>Diseña y hace cada pieza en su taller de Córdoba. [Completar con dos o tres líneas sobre vos.]</p>
      <a class="link-caps bordo" href="la-founder.html">leer su historia</a>
    </div>
  </div>
</section>

<section class="fondo-bordo seccion centro">
  <div class="contenedor">
    <img src="img/llama-oro.svg" alt="" width="60" height="80" style="margin:0 auto 18px;width:60px">
    <h2 class="frase" style="font-size:clamp(34px,7vw,56px)">sumate a las bravas</h2>
    <p class="bajada" style="margin:14px auto 26px;max-width:520px">Enterate primero del lanzamiento, de los pop-ups y de las cápsulas que no se repiten.</p>
    <form class="form" style="max-width:460px;margin:0 auto" onsubmit="return false">
      <div class="campo"><label class="caps" for="mail-home">tu email</label><input id="mail-home" type="email" placeholder="brava@email.com" style="border-color:var(--crema);color:var(--crema)"></div>
      <button class="btn btn-ancho" type="submit">quiero enterarme</button>
    </form>
  </div>
</section>
'''
    pagina("index.html", "bravissima · joyería de autor · hecho para mujeres bravas",
           "Joyería y accesorios de autor, hechos a mano en Córdoba. Alpaca, bronce y cobre, terminación dorada y plateada, piedras naturales.", cuerpo)


def colecciones():
    orden = ["artesanal", "fiesta", "capsulas", "artesanal", "fiesta", "capsulas", "artesanal", "fiesta", "capsulas", "artesanal", "fiesta", "capsulas"]
    cuerpo = f'''
<section class="seccion-s">
  <div class="contenedor">
    <p class="migas"><a href="index.html">inicio</a> · colecciones</p>
    <div class="cabecera"><h1 class="titulo t-xl">colecciones</h1>
      <p class="bajada bordo" style="max-width:640px">Tres maneras de llevar una pieza de autor. Todas hechas a mano, ninguna idéntica a otra.</p></div>
    <div class="grilla-3" style="margin-bottom:56px">
      <a class="coleccion" href="#artesanal" onclick="document.querySelector('[data-filtro=artesanal]').click()">{foto("artesanal", "apaisada")}<h2 class="titulo t-m">artesanal</h2><p>Las piezas de todos los días, con marcas de taller.</p></a>
      <a class="coleccion" href="#fiesta" onclick="document.querySelector('[data-filtro=fiesta]').click()">{foto("fiesta", "oscura apaisada")}<h2 class="titulo t-m">fiesta</h2><p>Para las noches que piden brillo.</p></a>
      <a class="coleccion" href="#capsulas" onclick="document.querySelector('[data-filtro=capsulas]').click()">{foto("cápsulas", "apaisada")}<h2 class="titulo t-m">cápsulas</h2><p>Series cortas que no se repiten.</p></a>
    </div>
    <hr class="regla" style="margin-bottom:32px">
    <div class="filtros" role="group" aria-label="Filtrar por colección">
      <button data-filtro="todas" aria-pressed="true">todas</button>
      <button data-filtro="artesanal" aria-pressed="false">artesanal</button>
      <button data-filtro="fiesta" aria-pressed="false">fiesta</button>
      <button data-filtro="capsulas" aria-pressed="false">cápsulas</button>
    </div>
    <div class="grilla">{"".join(tarjeta(i + 1, c, i < 2) for i, c in enumerate(orden))}</div>
  </div>
</section>
'''
    pagina("colecciones.html", "colecciones · bravissima", "Colecciones artesanal, fiesta y cápsulas: joyería de autor hecha a mano en Córdoba.", cuerpo)


def producto():
    cuerpo = f'''
<section class="seccion-s">
  <div class="contenedor">
    <p class="migas"><a href="index.html">inicio</a> · <a href="colecciones.html">colecciones</a> · [colección]</p>
    <div class="producto-layout">
      <div class="galeria">
        <div class="principal">{foto("foto 1 de la pieza")}</div>
        <div class="miniaturas">
          {"".join(f'<button aria-label="Ver foto {i + 1}" aria-current="{str(i == 0).lower()}">{foto(str(i + 1), "oscura" if i == 2 else "")}</button>' for i in range(4))}
        </div>
      </div>
      <div class="ficha">
        <p class="caps bordo">[colección] · hecho a mano</p>
        <h1 class="titulo t-l">[nombre de la pieza]</h1>
        <p class="precio">$ [completar]</p>
        <p class="frase bordo" style="font-size:22px">[Una línea que cuente la pieza: qué tiene de brava.]</p>
        <div>
          <div class="dato"><span class="caps">material</span><span>[completar]</span></div>
          <div class="dato"><span class="caps">terminación</span><span>[completar]</span></div>
          <div class="dato"><span class="caps">piedra</span><span>[completar]</span></div>
          <div class="dato"><span class="caps">medidas</span><span>[completar]</span></div>
        </div>
        <div class="campo"><label class="caps" for="variante">opción</label>
          <select id="variante"><option>[completar opciones]</option></select></div>
        <div class="fila-compra">
          <div class="cantidad" aria-label="Cantidad"><button data-paso="-" aria-label="Restar">−</button><output>1</output><button data-paso="+" aria-label="Sumar">+</button></div>
          <button class="btn" data-agregar>agregar al carrito</button>
        </div>
        <a class="btn btn-linea" href="contacto.html">consultar por WhatsApp</a>
        <p class="nota">Cada pieza se hace a mano: puede tener pequeñas diferencias con la foto. Eso la hace única.</p>
        <div class="acordeon">
          <details open><summary>la pieza</summary><div class="contenido"><p>[Descripción de la pieza: inspiración, cómo se usa, con qué combina.]</p></div></details>
          <details><summary>materiales y medidas</summary><div class="contenido"><p>Material: [completar]<br>Terminación: [completar]<br>Piedra: [completar]<br>Medidas: [completar]<br>Peso: [completar]</p></div></details>
          <details><summary>cuidados</summary><div class="contenido"><p>Guardala seca y separada, lejos del perfume y del agua. <a href="cuidados.html">Ver la guía completa de cuidados</a>.</p></div></details>
          <details><summary>envíos y cambios</summary><div class="contenido"><p>[Completar: zonas y tiempos de envío, costo, retiro, política de cambios.]</p></div></details>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="seccion fondo-crema2">
  <div class="contenedor">
    <div class="cabecera"><p class="caps bordo">para combinar</p><h2 class="titulo t-l">también te puede gustar</h2></div>
    <div class="grilla">{tarjeta(5, "artesanal")}{tarjeta(6, "fiesta")}{tarjeta(7, "capsulas")}{tarjeta(8, "artesanal")}</div>
  </div>
</section>
'''
    pagina("producto.html", "[nombre de la pieza] · bravissima", "Pieza de autor hecha a mano en Córdoba.", cuerpo)


def bravas():
    cuerpo = f'''
<section class="fondo-bordo hero">
  <div class="contenedor">
    <img class="cardo" src="img/cardo-oro.svg" alt="" width="120" height="150">
    <p class="caps oro">comunidad</p>
    <h1 class="titulo t-xl" style="margin:12px 0 20px">mujeres bravas</h1>
    <p class="bajada">Son las que se visten para ellas, las que eligen pocas piezas pero con identidad. Acá las mostramos.</p>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="cabecera centro"><p class="caps bordo">así la llevan</p><h2 class="titulo t-l">nuestras bravas</h2></div>
    <div class="bravas-grilla">
      {"".join(f'<figure class="brava" style="margin:0">{foto("foto de clienta", "oscura" if i in (1, 4, 6) else "")}<figcaption>@[usuario] · [pieza]</figcaption></figure>' for i in range(8))}
    </div>
  </div>
</section>

<section class="fondo-crema2 seccion">
  <div class="contenedor dos-col">
    <div class="cita">«[Testimonio real de una clienta: qué sintió al recibir o usar su pieza.]»<p class="caps" style="margin-top:14px;color:var(--negro)">— [nombre], @[usuario]</p></div>
    <div class="cita">«[Otro testimonio real. Mejor corto y con sus palabras.]»<p class="caps" style="margin-top:14px;color:var(--negro)">— [nombre], @[usuario]</p></div>
  </div>
</section>

<section class="seccion centro">
  <div class="contenedor" style="max-width:720px">
    <img src="img/llama-bordo.svg" alt="" width="56" height="74" style="margin:0 auto 18px;width:56px">
    <h2 class="titulo t-l">¿sos una brava?</h2>
    <p class="bajada bordo" style="margin:16px 0 26px">Subí una foto con tu pieza y etiquetanos en Instagram (@[usuario]). Las elegidas aparecen acá.</p>
    <a class="btn" href="#">ir a Instagram</a>
  </div>
</section>
'''
    pagina("mujeres-bravas.html", "mujeres bravas · bravissima", "La comunidad de mujeres bravas que llevan bravissima.", cuerpo)


def founder():
    pasos = [("diseño", "Cada pieza empieza en papel. [Contá cómo nace una idea.]"),
             ("taller", "Se corta, se forja, se suelda y se lima a mano. [Completar con tu proceso real.]"),
             ("terminación", "Dorado o plateado, pulido y piedra natural. [Completar.]"),
             ("tus manos", "Se envuelve como una carta y viaja hasta vos.")]
    cuerpo = f'''
<section class="seccion">
  <div class="contenedor dos-col">
    <div>{foto("retrato de la founder", "alta")}</div>
    <div>
      <p class="caps bordo">la founder</p>
      <h1 class="titulo t-xl" style="margin:10px 0 18px">[nombre]</h1>
      <p class="bajada bordo">«[Una frase tuya que resuma por qué hacés bravissima.]»</p>
      <p>Hola, soy [nombre]. [Contá acá cómo empezaste, qué te llevó al metal y al taller, y por qué bravissima es para mujeres bravas.]</p>
      <p>[Segundo párrafo: tu formación o tu camino, lo que te inspira, Córdoba.]</p>
      <p class="frase bordo" style="font-size:26px;margin-top:20px">[firma]</p>
    </div>
  </div>
</section>

<section class="fondo-vino seccion">
  <div class="contenedor">
    <div class="cabecera"><p class="caps oro">el taller</p><h2 class="titulo t-l">de dos manos y mucho fuego</h2></div>
    <div class="pasos">
      {"".join(f'<div class="paso" style="border-color:var(--oro)"><span class="num" style="color:var(--oro)">0{i + 1}</span><h3 class="titulo t-s">{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(pasos))}
    </div>
  </div>
</section>

<section class="seccion">
  <div class="contenedor">
    <div class="grilla-3">{foto("foto del taller", "cuadrada")}{foto("herramientas", "oscura cuadrada")}{foto("pieza en proceso", "cuadrada")}</div>
  </div>
</section>
'''
    pagina("la-founder.html", "la founder · bravissima", "Quién diseña y hace cada pieza de bravissima, en su taller de Córdoba.", cuerpo)


def cuidados():
    items = [
        ("icono-cuidados", "alpaca, bronce y cobre", ["Con el tiempo y el contacto con la piel se oscurecen: es natural en estos metales.",
                                                     "Limpialas con un paño suave y seco después de usarlas.",
                                                     "Si se oscurecen, un paño de pulir joyas les devuelve el brillo."]),
        ("llama", "terminación dorada y plateada", ["Ponete la pieza al final: después del perfume, la crema y el maquillaje.",
                                                   "Sacátela para bañarte, nadar, hacer deporte o lavar los platos.",
                                                   "No uses productos abrasivos ni limpiadores de plata comunes."]),
        ("icono-anillos", "piedras naturales", ["Evitá golpes y cambios bruscos de temperatura.",
                                               "No las mojes ni las expongas a productos químicos.",
                                               "Cada piedra es única: su color y sus marcas son parte de la pieza."]),
        ("icono-collares", "cómo guardarlas", ["En un lugar seco, cada una en su bolsita y separada de las demás.",
                                              "Los collares, abrochados y estirados, para que no se enreden.",
                                              "Un saquito de sílica en el joyero ayuda a que no se oxiden."]),
    ]
    filas = "".join(f'<div class="cuidado"><img src="img/{ic}-bordo.svg" alt="" width="46" height="60"><div><h2 class="titulo t-m">{t}</h2>'
                    f'<ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div></div>' for ic, t, li in items)
    cuerpo = f'''
<section class="seccion-s">
  <div class="contenedor" style="max-width:860px">
    <p class="migas"><a href="index.html">inicio</a> · cuidados</p>
    <div class="cabecera"><h1 class="titulo t-xl">cuidados</h1>
      <p class="bajada bordo">Una pieza hecha a mano dura muchos años si la tratás como lo que es: algo tuyo.</p></div>
    {filas}
    <p class="nota" style="margin-top:28px">[Revisá estas recomendaciones con tu proceso real: según la terminación y el sellado que uses, pueden cambiar.]</p>
    <div style="margin-top:36px" class="acciones"><a class="btn" href="contacto.html">tengo una consulta</a></div>
  </div>
</section>
'''
    pagina("cuidados.html", "cuidados · bravissima", "Cómo cuidar tus piezas de alpaca, bronce y cobre, con terminación dorada o plateada y piedras naturales.", cuerpo)


def contacto():
    cuerpo = f'''
<section class="seccion-s">
  <div class="contenedor">
    <p class="migas"><a href="index.html">inicio</a> · contacto</p>
    <div class="dos-col" style="align-items:start">
      <div>
        <h1 class="titulo t-xl">contacto</h1>
        <p class="bajada bordo" style="margin:16px 0 30px">Escribinos por lo que quieras: una pieza, un regalo, un pedido especial.</p>
        <div class="canales">
          <a class="canal" href="#"><span class="caps">whatsapp</span><span>[completar]</span></a>
          <a class="canal" href="#"><span class="caps">instagram</span><span>@[usuario]</span></a>
          <a class="canal" href="#"><span class="caps">email</span><span>[completar]</span></a>
          <div class="canal"><span class="caps">taller</span><span>Córdoba, Argentina</span></div>
        </div>
      </div>
      <form class="form">
        <div class="campo"><label class="caps" for="nombre">nombre</label><input id="nombre" required autocomplete="name"></div>
        <div class="campo"><label class="caps" for="email">email</label><input id="email" type="email" required autocomplete="email"></div>
        <div class="campo"><label class="caps" for="motivo">motivo</label><select id="motivo"><option>consulta por una pieza</option><option>pedido especial</option><option>envíos y cambios</option><option>pop-ups</option><option>otro</option></select></div>
        <div class="campo"><label class="caps" for="mensaje">mensaje</label><textarea id="mensaje" rows="5" required></textarea></div>
        <button class="btn" type="submit">enviar</button>
      </form>
    </div>
  </div>
</section>

<section class="fondo-bordo seccion" id="popups">
  <div class="contenedor dos-col">
    <div><p class="caps oro">pop-ups</p><h2 class="titulo t-l" style="margin-top:8px">vení a probártelas</h2>
      <p class="bajada" style="margin-top:14px">Cada tanto armamos pop-ups para que veas y toques las piezas.</p></div>
    <div class="canales">
      <div class="canal" style="border-color:rgba(239,231,221,.3)"><span class="caps oro">[fecha]</span><span>[lugar · Córdoba]</span></div>
      <div class="canal" style="border-color:rgba(239,231,221,.3)"><span class="caps oro">[fecha]</span><span>[lugar]</span></div>
    </div>
  </div>
</section>

<section class="seccion" id="preguntas">
  <div class="contenedor" style="max-width:860px">
    <div class="cabecera"><p class="caps bordo">preguntas frecuentes</p><h2 class="titulo t-l">antes de comprar</h2></div>
    <div class="acordeon">
      <details><summary>¿hacen envíos a todo el país?</summary><div class="contenido"><p>[Completar.]</p></div></details>
      <details><summary>¿cuánto tarda en llegar?</summary><div class="contenido"><p>[Completar.]</p></div></details>
      <details><summary>¿puedo cambiar una pieza?</summary><div class="contenido"><p>[Completar política de cambios.]</p></div></details>
      <details><summary>¿hacen piezas a pedido?</summary><div class="contenido"><p>[Completar.]</p></div></details>
      <details><summary>¿qué medios de pago aceptan?</summary><div class="contenido"><p>[Completar.]</p></div></details>
    </div>
  </div>
</section>
'''
    pagina("contacto.html", "contacto · bravissima", "Escribile a bravissima: consultas, pedidos especiales y pop-ups.", cuerpo)


if __name__ == "__main__":
    inicio(); colecciones(); producto(); bravas(); founder(); cuidados(); contacto()
