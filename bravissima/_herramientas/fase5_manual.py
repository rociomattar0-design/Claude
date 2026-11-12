"""FASE 5 — Manual de marca (PDF A4 horizontal, texto vivo)."""
import subprocess

from PIL import Image

from marca import PALETA as P, PALETA_CMYK as K, RAIZ, alto_b, contorno
from simbolos import contorno_simbolo
from tipo import Fuente

OUT = RAIZ / "05_manual"
SRC = OUT / "fuente"
IMG = SRC / "img"
AQUI = RAIZ / "_herramientas"
W, H = 1684, 1191  # px de diseño (proporción A4 apaisado)

NOMBRES = {"bordo": "Bordó", "vino": "Vino", "crema": "Crema", "rosa": "Rosa empolvado", "oro": "Oro viejo", "casinegro": "Casi negro"}


# ───────────────────────── recursos ─────────────────────────
def img(origen, nombre, ancho=1500, recorte=None):
    IMG.mkdir(parents=True, exist_ok=True)
    im = Image.open(RAIZ / origen).convert("RGB")
    if recorte:
        w, h = im.size
        im = im.crop((int(recorte[0] * w), int(recorte[1] * h), int(recorte[2] * w), int(recorte[3] * h)))
    im.thumbnail((ancho, ancho), Image.LANCZOS)
    im.save(IMG / f"{nombre}.jpg", quality=86)
    return f"img/{nombre}.jpg"


def marca_svg(texto, color, ancho=None, alto=None, estilo="", op=1):
    d, (x0, y0, x1, y1) = contorno(texto)
    if ancho:
        alto = ancho * (y1 - y0) / (x1 - x0)
    else:
        ancho = alto * (x1 - x0) / (y1 - y0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho:.1f}" height="{alto:.1f}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" '
            f'style="{estilo}"><path fill="{P.get(color, color)}" opacity="{op}" d="{d}"/></svg>')


def simbolo_svg(nombre, color, alto, estilo="", op=1):
    d, (x0, y0, x1, y1) = contorno_simbolo(nombre)
    w = alto * (x1 - x0) / (y1 - y0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}" height="{alto}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" '
            f'style="{estilo}"><path fill="{P.get(color, color)}" opacity="{op}" d="{d}"/></svg>')


def marca_ok(ok=True, t=26):
    if ok:
        return (f'<svg width="{t}" height="{t}" viewBox="0 0 26 26"><circle cx="13" cy="13" r="12" fill="none" stroke="{P["bordo"]}" stroke-width="1.2"/>'
                f'<path d="M7.5 13.5l3.8 3.8 7.4-8.2" fill="none" stroke="{P["bordo"]}" stroke-width="1.6"/></svg>')
    return (f'<svg width="{t}" height="{t}" viewBox="0 0 26 26"><circle cx="13" cy="13" r="12" fill="{P["bordo"]}"/>'
            f'<path d="M8.5 8.5l9 9M17.5 8.5l-9 9" fill="none" stroke="{P["crema"]}" stroke-width="1.6"/></svg>')


CSS = f"""
@font-face{{font-family:"Kalnia";src:url("../../_fuentes/estaticas/Kalnia-Light.ttf");font-weight:300}}
@font-face{{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Medium.ttf");font-weight:500}}
@font-face{{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Italic.ttf");font-weight:400;font-style:italic}}
@font-face{{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-LightItalic.ttf");font-weight:300;font-style:italic}}
:root{{--bordo:#5E1A24;--vino:#3A0F16;--crema:#EFE7DD;--rosa:#D9B8AE;--oro:#B8955A;--negro:#150B0D}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:#666}}
svg{{display:block}}
.page{{position:relative;width:{W}px;height:{H}px;overflow:hidden;break-after:page;margin:0 auto;background:var(--crema);
  font-family:"Cormorant Garamond";font-size:23px;line-height:1.42;color:var(--negro);font-variant-numeric:lining-nums}}
.osc{{background:var(--bordo);color:var(--crema)}} .osc2{{background:var(--vino);color:var(--crema)}}
.hd,.ft{{position:absolute;left:96px;right:96px;display:flex;justify-content:space-between;align-items:baseline}}
.hd{{top:58px}} .ft{{bottom:50px}}
.caps{{font-weight:500;letter-spacing:.18em;font-size:15px;line-height:1.5}}
.it{{font-style:italic}}
.k{{font-family:"Kalnia";font-weight:300;letter-spacing:-.01em;line-height:1.04}}
.cuerpo{{position:absolute;top:136px;left:96px;right:96px;bottom:118px}}
h1{{font-family:"Kalnia";font-weight:300;letter-spacing:-.01em;font-size:72px;line-height:1.04;color:var(--bordo)}}
.osc h1,.osc2 h1{{color:var(--crema)}}
h3{{font-weight:500;letter-spacing:.18em;font-size:15px;line-height:1.5;color:var(--bordo);margin-bottom:8px}}
.osc h3,.osc2 h3{{color:var(--oro)}}
.bajada{{font-style:italic;font-size:31px;line-height:1.25;color:var(--bordo)}}
.osc .bajada,.osc2 .bajada{{color:var(--crema)}}
p+p{{margin-top:.6em}}
.regla{{height:1.5px;background:var(--bordo)}} .osc .regla,.osc2 .regla{{background:var(--oro)}}
.g{{display:grid;gap:36px}}
.abs{{position:absolute}}
.centro{{display:flex;align-items:center;justify-content:center}}
.tarj{{position:relative;display:flex;align-items:center;justify-content:center}}
.pie{{font-weight:500;letter-spacing:.18em;font-size:13px;line-height:1.5}}
.foto{{width:100%;height:100%;object-fit:cover;display:block}}
ul{{list-style:none}} li{{padding-left:22px;position:relative}} li+li{{margin-top:.35em}}
li:before{{content:"";position:absolute;left:0;top:.62em;width:10px;height:1.5px;background:var(--bordo)}}
.osc li:before,.osc2 li:before{{background:var(--oro)}}
"""

_n = [0]


def pag(seccion, cuerpo, clase="", pie=True):
    _n[0] += 1
    n = _n[0]
    hd = (f'<div class="hd caps"><span>BRAVISSIMA · MANUAL DE MARCA</span><span>{seccion.upper()}</span></div>' if pie else "")
    ft = (f'<div class="ft"><span class="k" style="font-size:22px">{n:02d}</span>'
          f'<span class="it" style="font-size:20px">hecho para mujeres bravas</span></div>' if pie else "")
    return f'<section class="page {clase}" data-nombre="p{n:02d}">{hd}{cuerpo}{ft}</section>'


def titulo(t, bajada="", ancho=None):
    b = f'<p class="bajada" style="margin-top:14px;{f"max-width:{ancho}px" if ancho else ""}">{bajada}</p>' if bajada else ""
    return f'<h1>{t}</h1>{b}'


# ───────────────────────── páginas ─────────────────────────
def portada():
    return pag("", f'''
  <div class="abs" style="inset:44px;border:1.5px solid var(--oro)"></div>
  <div class="abs centro" style="left:0;right:0;top:170px">{simbolo_svg("cardo", "oro", 210)}</div>
  <div class="abs centro" style="left:0;right:0;top:468px">{marca_svg("bravissima", "crema", ancho=820)}</div>
  <p class="abs it" style="left:0;right:0;top:640px;text-align:center;font-size:44px">hecho para mujeres bravas</p>
  <div class="abs" style="left:{W/2-70}px;top:760px;width:140px;height:1.5px;background:var(--oro)"></div>
  <p class="abs caps" style="left:0;right:0;top:800px;text-align:center;font-size:19px">MANUAL DE MARCA</p>
  <p class="abs caps" style="left:0;right:0;top:1040px;text-align:center;font-size:14px">JOYERÍA DE AUTOR · CÓRDOBA, ARGENTINA · VERSIÓN 1.0 · 2026</p>
''', "osc", pie=False)


INDICE = ["Esencia", "Slogan y manifiesto", "Logotipo", "Construcción", "Isotipo", "Símbolos", "Versiones de color", "Usos incorrectos",
          "Paleta", "Tipografía", "Texturas", "Etiquetas", "Packaging", "Redes", "Tono de voz", "Fotografía"]


def indice():
    filas = ""
    for i, t in enumerate(INDICE):
        filas += (f'<div style="display:flex;align-items:baseline;gap:22px;padding:13px 0;border-bottom:1px solid rgba(94,26,36,.28)">'
                  f'<span class="k" style="font-size:22px;color:var(--bordo);width:44px">{i + 3:02d}</span>'
                  f'<span style="font-size:27px">{t}</span></div>')
    return pag("Índice", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1.5fr;gap:90px">
  <div>{titulo("índice")}<p class="bajada" style="margin-top:22px">Todo lo que hace que una pieza, una caja o un posteo se reconozcan como nuestros.</p>
  <div style="margin-top:250px">{simbolo_svg("cardo", "bordo", 250)}</div></div>
  <div style="columns:2;column-gap:60px;padding-top:14px">{filas}</div></div>''')


def esencia():
    pilares = [("DE AUTOR", "Cada pieza se diseña y se firma. No seguimos tendencias: proponemos."),
               ("HECHO A MANO", "Sale de un taller, de dos manos y de mucho fuego. Se nota y queremos que se note."),
               ("POCAS, CON IDENTIDAD", "Preferimos que elijas una pieza que te represente antes que diez que no digan nada."),
               ("COMUNIDAD", "No tenemos clientas: tenemos mujeres bravas. Las nombramos, las mostramos, les agradecemos.")]
    cajas = "".join(f'<div style="border-top:1.5px solid var(--bordo);padding-top:16px"><h3>{t}</h3><p style="font-size:22px">{d}</p></div>' for t, d in pilares)
    return pag("Esencia", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1.25fr;gap:90px">
  <div>{titulo("esencia", "Joyería y accesorios de autor, hechos a mano en taller, en Córdoba.")}
    <div style="margin-top:44px"><h3>QUÉ HACEMOS</h3>
    <p>Piezas en alpaca, bronce y cobre, con terminación dorada y plateada y piedras naturales. Se venden online —Instagram y web— y en pop-ups.</p></div>
    <div style="margin-top:30px"><h3>PARA QUIÉN</h3>
    <p>Para una mujer segura, de 25 a 55, que se viste para ella y elige pocas piezas pero con identidad.</p></div>
    <div style="margin-top:30px"><h3>LANZAMIENTO</h3><p>3 de diciembre de 2026.</p></div>
    <div style="margin-top:56px">{simbolo_svg("cardo", "bordo", 170, op=0.9)}</div>
  </div>
  <div><h3>PERSONALIDAD</h3>
    <p class="k" style="font-size:54px;color:var(--bordo);margin:6px 0 40px">segura, cálida,<br>con actitud.</p>
    <div class="g" style="grid-template-columns:1fr 1fr;gap:34px 44px">{cajas}</div>
  </div></div>''')


def manifiesto():
    return pag("Slogan y manifiesto", f'''<div class="cuerpo g" style="grid-template-columns:1.15fr 1fr;gap:100px;align-items:center">
  <div><h3>EL SLOGAN</h3>
    <p style="font-style:italic;font-weight:300;font-size:138px;line-height:.98;margin-top:10px">hecho para<br>mujeres<br>bravas</p>
    <p style="margin-top:44px;max-width:560px;font-size:21px;opacity:.9">Se escribe siempre en minúscula y en Cormorant Garamond itálica. No lleva punto final ni signos. A la comunidad la llamamos <span class="it">mujeres bravas</span>.</p></div>
  <div><h3>EL MANIFIESTO</h3>
    <div style="font-size:27px;line-height:1.5;margin-top:10px">
    <p>No hacemos joyas para gustarle a todo el mundo.</p>
    <p>Hacemos piezas para la que ya sabe quién es. Para la que se viste para ella. Para la que elige pocas cosas, pero las elige con el cuerpo entero.</p>
    <p>Cada pieza sale de un taller, de dos manos y de mucho fuego. Tiene marcas, tiene peso, tiene carácter. Como vos.</p>
    <p class="it" style="color:var(--oro)">Metal noble, piedra natural y actitud.</p></div>
    <div style="margin-top:36px">{simbolo_svg("llama", "oro", 84)}</div></div></div>''', "osc2")


def logotipo():
    return pag("Logotipo", f'''<div class="cuerpo">
  <div class="g" style="grid-template-columns:1fr 2.1fr;gap:80px;height:100%">
   <div>{titulo("logotipo")}
    <p style="margin-top:30px">El nombre escrito en minúscula, en <b style="font-weight:500">Kalnia Light 300</b>. Letra líquida, de contraste alto y terminales en gota.</p>
    <p>Su gesto distintivo es la <span class="it">doble s fundida</span>: las dos s se tocan y forman una sola forma. Es lo que hace que la palabra sea un logo y no solo un texto.</p>
    <div style="margin-top:34px"><h3>REGLA DE ORO</h3><p>Usá siempre el archivo del logo. Nunca lo reescribas con la tipografía: la fusión de la ss no existe en el teclado.</p></div>
    <div style="margin-top:28px"><h3>ARCHIVOS</h3><p style="font-size:20px">01_logo/ · SVG, PDF y PNG en bordó, crema, vino y negro.</p></div>
   </div>
   <div class="g" style="grid-template-rows:1.55fr 1fr;gap:24px">
     <div class="tarj" style="background:#fff">{marca_svg("bravissima", "bordo", ancho=760)}</div>
     <div class="g" style="grid-template-columns:1fr 1fr;gap:24px">
       <div class="tarj osc">{marca_svg("bravissima", "crema", ancho=360)}</div>
       <div class="tarj" style="background:var(--rosa)">{marca_svg("bravissima", "vino", ancho=360)}</div>
     </div>
   </div>
  </div></div>''')


def construccion():
    d, (x0, y0, x1, y1) = contorno("bravissima")
    hb = alto_b()
    sx0 = contorno("bravi")[1][2] + 4
    sx1 = contorno("braviss")[1][2] + 4
    m = 1250
    lineas = ""
    for y, lab in ((y0, "ASCENDENTE"), (-500, "ALTURA DE X"), (0, "LÍNEA DE BASE")):
        lineas += (f'<line x1="{x0 - m}" x2="{x1 + 80}" y1="{y}" y2="{y}" stroke="{P["oro"]}" stroke-width="6"/>'
                   f'<text x="{x0 - m}" y="{y - 30}" font-family="Cormorant Garamond" font-weight="500" font-size="78" letter-spacing="14" fill="{P["bordo"]}">{lab}</text>')
    diag1 = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - m - 30} {y0 - 360} {x1 - x0 + m + 140} {y1 - y0 + 760}" width="100%">'
             f'<rect x="{sx0}" y="{y0 - 80}" width="{sx1 - sx0}" height="{y1 - y0 + 160}" fill="{P["rosa"]}" opacity=".5"/>'
             f'{lineas}<path fill="{P["bordo"]}" d="{d}"/>'
             f'<line x1="{(sx0 + sx1) / 2}" x2="{(sx0 + sx1) / 2}" y1="{y1 + 90}" y2="{y1 + 200}" stroke="{P["bordo"]}" stroke-width="6"/>'
             f'<text x="{(sx0 + sx1) / 2}" y="{y1 + 320}" text-anchor="middle" font-family="Cormorant Garamond" font-style="italic" font-size="120" fill="{P["bordo"]}">doble ss: primera s a −0.14 em · resto de la palabra a −0.01 em</text>'
             f'</svg>')
    d_sueltas = Fuente("kalnia").path("ss", 1000, 0, 0, tracking=0.02)
    d_fund, _ = contorno("ss")
    comp = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -600 2500 700" width="100%">'
            f'<path fill="{P["bordo"]}" opacity=".35" d="{d_sueltas}"/>'
            f'<g transform="translate(1420 0)"><path fill="{P["bordo"]}" d="{d_fund}"/></g></svg>')
    db, (b0, by0, b1, by1) = contorno("b")
    cota = lambda X, Y0, Y1: (f'<line x1="{X}" x2="{X}" y1="{Y0}" y2="{Y1}" stroke="{P["bordo"]}" stroke-width="7"/>'
                              f'<line x1="{X - 50}" x2="{X + 50}" y1="{Y0}" y2="{Y0}" stroke="{P["bordo"]}" stroke-width="7"/>'
                              f'<line x1="{X - 50}" x2="{X + 50}" y1="{Y1}" y2="{Y1}" stroke="{P["bordo"]}" stroke-width="7"/>')
    s2 = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - hb - 60} {y0 - hb - 60} {x1 - x0 + 2 * hb + 120} {y1 - y0 + 2 * hb + 120}" width="100%">'
          f'<rect x="{x0 - hb}" y="{y0 - hb}" width="{x1 - x0 + 2 * hb}" height="{y1 - y0 + 2 * hb}" fill="{P["rosa"]}" opacity=".45"/>'
          f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#fff"/>'
          f'<rect x="{x0 - hb}" y="{y0 - hb}" width="{x1 - x0 + 2 * hb}" height="{y1 - y0 + 2 * hb}" fill="none" stroke="{P["oro"]}" stroke-width="9" stroke-dasharray="44 28"/>'
          f'<path fill="{P["bordo"]}" d="{d}"/>'
          f'<g opacity=".45"><path fill="{P["bordo"]}" transform="translate({x1 + (hb - (b1 - b0)) / 2 - b0} {y0 - hb - by0 + 0})" d="{db}"/></g>'
          f'{cota(x1 + hb / 2 - 230, y0 - hb, y0)}'
          f'</svg>')
    return pag("Construcción", f'''<div class="cuerpo g" style="grid-template-columns:1fr 2.2fr;gap:70px">
   <div>{titulo("construcción")}
    <p style="margin-top:30px">El logotipo se arma con dos valores de espaciado. La primera s de la doble ss lleva un tracking de <b style="font-weight:500">−0.14 em</b>: así las dos s se tocan y se funden. El resto de la palabra lleva <b style="font-weight:500">−0.01 em</b>.</p>
    <div style="margin-top:30px"><h3>ÁREA DE SEGURIDAD</h3><p>Alrededor del logo queda libre un espacio igual al <span class="it">alto de la b</span>. Ahí no entra texto, borde ni foto con detalle.</p></div>
    <div style="margin-top:26px"><h3>TAMAÑO MÍNIMO</h3><p>Logotipo: 30 mm en impresos · 140 px en pantalla.<br>Isotipo: 8 mm · 40 px.</p></div>
   </div>
   <div class="g" style="grid-template-rows:1fr 1.05fr;gap:22px">
     <div style="background:#fff;padding:10px 40px;display:flex;align-items:center">{diag1}</div>
     <div class="g" style="grid-template-columns:1fr 1.3fr;gap:22px">
       <div style="background:#fff;padding:30px 34px 22px;display:flex;flex-direction:column;justify-content:space-between">
         <div style="padding-top:70px">{comp}</div>
         <div style="display:flex;justify-content:space-between;font-size:19px"><span style="display:flex;gap:10px;align-items:center">{marca_ok(False, 22)} <span class="it">ss separadas</span></span><span style="display:flex;gap:10px;align-items:center">{marca_ok(True, 22)} <span class="it">ss fundidas: una sola forma</span></span></div></div>
       <div style="background:#fff;padding:18px 30px;display:flex;flex-direction:column;justify-content:center">{s2}
         <p class="pie" style="text-align:center;margin-top:10px;color:var(--bordo)">ÁREA DE SEGURIDAD = ALTO DE LA «b»</p></div>
     </div>
   </div></div>''')


def isotipo():
    usos = [("FOTO DE PERFIL", f'<div style="width:150px;height:150px;border-radius:50%;background:var(--bordo)" class="centro">{marca_svg("bss", "crema", ancho=78)}</div>'),
            ("SELLO", f'<div style="width:150px;height:150px;border-radius:50%;border:1.5px solid var(--bordo);outline:1px solid var(--bordo);outline-offset:5px" class="centro">{marca_svg("bss", "bordo", ancho=74)}</div>'),
            ("RELIEVE", f'<div style="width:150px;height:150px;background:var(--bordo)" class="centro">{marca_svg("bss", "vino", ancho=84)}</div>'),
            ("FAVICON", f'<div style="width:150px;height:150px" class="centro"><div style="width:64px;height:64px;border-radius:14px;background:var(--bordo)" class="centro">{marca_svg("bss", "crema", ancho=40)}</div></div>')]
    cajas = "".join(f'<div style="text-align:center"><div class="centro" style="height:170px">{s}</div><p class="pie" style="margin-top:12px;color:var(--bordo)">{t}</p></div>' for t, s in usos)
    return pag("Isotipo", f'''<div class="cuerpo g" style="grid-template-columns:1fr 2.1fr;gap:80px">
   <div>{titulo("isotipo")}
    <p style="margin-top:30px">La versión corta del nombre: <span class="it">b + ss</span>, en la misma tipografía, el mismo peso y con la misma fusión de la doble s.</p>
    <p>Se usa donde el logotipo completo no entra o no hace falta: la foto de perfil, los sellos, el relieve de las etiquetas y el favicon.</p>
    <div style="margin-top:30px"><h3>TAMAÑO MÍNIMO</h3><p>8 mm en impresos · 40 px en pantalla.</p></div>
    <div style="margin-top:24px"><h3>ÁREA DE SEGURIDAD</h3><p>El alto de la b, igual que en el logotipo.</p></div>
   </div>
   <div class="g" style="grid-template-rows:1.4fr 1fr;gap:24px">
     <div class="g" style="grid-template-columns:1.4fr 1fr;gap:24px">
       <div class="tarj" style="background:#fff">{marca_svg("bss", "bordo", ancho=430)}</div>
       <div class="tarj osc">{marca_svg("bss", "crema", ancho=250)}</div></div>
     <div style="background:#fff;display:grid;grid-template-columns:repeat(4,1fr);align-items:center;padding:0 20px">{cajas}</div>
   </div></div>''')


def simbolos():
    return pag("Símbolos", f'''<div class="cuerpo g" style="grid-template-columns:1fr 2.1fr;gap:80px">
   <div>{titulo("símbolos")}
    <p style="margin-top:30px">Dos dibujos propios acompañan al logo. Comparten su carácter: contraste entre trazo grueso y fino, y terminaciones en gota.</p>
    <div style="margin-top:26px"><h3>EL CARDO · EMBLEMA PRINCIPAL</h3><p>La flor brava de las sierras: hermosa, con espinas, crece sola y no se deja arrancar. Va en stickers, sellos, packaging y cierres.</p></div>
    <div style="margin-top:22px"><h3>LA LLAMA · SÍMBOLO SECUNDARIO</h3><p>El fuego de adentro —y el del taller— con una gota en el centro: la piedra. Va en agradecimientos, acentos y detalles.</p></div>
    <div style="margin-top:22px"><h3>JERARQUÍA</h3><p style="font-size:21px">Logotipo → isotipo → cardo → llama. Los símbolos acompañan al nombre; nunca lo reemplazan.</p></div>
   </div>
   <div class="g" style="grid-template-rows:1.7fr 1fr;gap:24px">
     <div class="g" style="grid-template-columns:1.25fr 1fr;gap:24px">
       <div class="tarj" style="background:#fff">{simbolo_svg("cardo", "bordo", 400)}</div>
       <div class="tarj osc2">{simbolo_svg("llama", "oro", 300)}</div></div>
     <div class="g" style="grid-template-columns:1.25fr 1fr;gap:24px">
       <div style="background:#fff;display:flex;align-items:center;justify-content:space-around;padding:0 30px">
         <div style="text-align:center"><div class="centro" style="height:120px;gap:34px">{simbolo_svg("cardo", "bordo", 110)}{simbolo_svg("cardo-chico", "bordo", 56)}</div><p class="pie" style="color:var(--bordo);margin-top:14px">NORMAL · VERSIÓN CHICA (MENOS DE 12 MM)</p></div>
         <div style="text-align:center"><div class="centro" style="height:120px;gap:34px">{simbolo_svg("llama", "bordo", 100)}{simbolo_svg("llama-chica", "bordo", 50)}</div><p class="pie" style="color:var(--bordo);margin-top:14px">NORMAL · CHICA (MENOS DE 10 MM)</p></div></div>
       <div class="tarj" style="background:var(--rosa);flex-direction:column;gap:20px">{simbolo_svg("cardo", "vino", 96)}{marca_svg("bravissima", "vino", ancho=250)}</div></div>
   </div></div>''')


def versiones():
    v = [("crema", "bordo", "BORDÓ SOBRE CREMA · PRINCIPAL", "bordo"), ("bordo", "crema", "CREMA SOBRE BORDÓ", "crema"), ("rosa", "vino", "VINO SOBRE ROSA EMPOLVADO", "vino"),
         ("vino", "crema", "CREMA SOBRE VINO", "crema"), ("casinegro", "crema", "CREMA SOBRE CASI NEGRO", "crema"), ("#FFFFFF", "negro", "NEGRO 100 % · SOLO PRODUCCIÓN (CLICHÉS)", "negro")]
    cajas = ""
    for fondo, tinta, lab, col in v:
        borde = "border:1px solid rgba(94,26,36,.25);" if fondo in ("crema", "#FFFFFF") else ""
        cajas += (f'<div class="tarj" style="background:{P.get(fondo, fondo)};{borde}flex-direction:column;gap:26px">{marca_svg("bravissima", tinta, ancho=330)}{marca_svg("bss", tinta, ancho=92)}'
                  f'<p class="pie abs" style="left:20px;bottom:14px;color:{P.get(col, col)}">{lab}</p></div>')
    return pag("Versiones de color", f'''<div class="cuerpo" style="display:flex;flex-direction:column;gap:28px">
   <div style="display:flex;justify-content:space-between;align-items:flex-end">{titulo("versiones de color")}
   <p style="max-width:640px;font-size:21px">El logo es de un solo color y siempre de la paleta. El oro viejo no se usa como tinta del logo: aparece solo como foil. Sobre fotos, elegí crema o bordó según el contraste.</p></div>
   <div class="g" style="grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr;gap:22px;flex:1">{cajas}</div></div>''')


def incorrectos():
    d, (x0, y0, x1, y1) = contorno("bravissima")
    vb = f'viewBox="{x0 - 500} {y0 - 900} {x1 - x0 + 1000} {y1 - y0 + 1800}"'
    base = f'<path fill="{P["bordo"]}" d="{d}"/>'
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    d_sep = Fuente("kalnia").path("bravissima", 1000, 0, 0, tracking=0.06)
    casos = [
        ("No estirar ni comprimir", f'<svg {vb} width="100%"><g transform="translate({cxm} {cym}) scale(1.05 1.9) translate({-cxm} {-cym})">{base}</g></svg>', "#fff"),
        ("No rotar", f'<svg {vb} width="100%"><g transform="rotate(-14 {cxm} {cym})">{base}</g></svg>', "#fff"),
        ("No separar la ss ni reescribirlo", f'<svg {vb} width="100%"><path fill="{P["bordo"]}" transform="translate({cxm - 2900} 0)" d="{d_sep}"/></svg>', "#fff"),
        ("No usar colores fuera de la paleta", f'<svg {vb} width="100%"><path fill="#2E6FB5" d="{d}"/></svg>', "#fff"),
        ("No agregar sombras ni efectos", f'<svg {vb} width="100%"><path fill="#000" opacity=".28" transform="translate(70 80)" d="{d}"/><path fill="#000" opacity=".14" transform="translate(120 140)" d="{d}"/>{base}</svg>', "#fff"),
        ("No usar sobre fondos sin contraste", f'<svg {vb} width="100%">{base}</svg>', P["vino"]),
        ("No encerrarlo ni invadir su área", f'<svg {vb} width="100%"><rect x="{x0 - 110}" y="{y0 - 110}" width="{x1 - x0 + 220}" height="{y1 - y0 + 220}" rx="120" fill="none" stroke="{P["bordo"]}" stroke-width="40"/>{base}</svg>', "#fff"),
        ("No usarlo en contorno", f'<svg {vb} width="100%"><path fill="none" stroke="{P["bordo"]}" stroke-width="8" d="{d}"/></svg>', "#fff"),
    ]
    cajas = "".join(f'<div style="display:flex;flex-direction:column;gap:12px"><div class="tarj" style="background:{bg};flex:1;padding:0 26px">{s}'
                    f'<div class="abs" style="right:12px;top:12px">{marca_ok(False)}</div></div><p style="font-size:20px" class="it">{t}</p></div>' for t, s, bg in casos)
    return pag("Usos incorrectos", f'''<div class="cuerpo" style="display:flex;flex-direction:column;gap:26px">
   <div style="display:flex;justify-content:space-between;align-items:flex-end">{titulo("usos incorrectos")}
   <p style="max-width:600px;font-size:21px">El logo no se toca. Si una pieza no funciona con el logo tal como es, lo que se cambia es la pieza. Lo mismo vale para el isotipo y los símbolos.</p></div>
   <div class="g" style="grid-template-columns:repeat(4,1fr);grid-template-rows:1fr 1fr;gap:22px 22px;flex:1">{cajas}</div></div>''')


def paleta():
    orden = [("bordo", "Principal. Fondos, tinta del logo, textos destacados.", 34),
             ("crema", "Papel y fondo. El aire de la marca.", 34),
             ("vino", "Fondos profundos y base del foil.", 12),
             ("rosa", "Apoyo: tarjetas, bloques de foto, detalles.", 12),
             ("oro", "Solo foil y detalles finos. Nunca en bloques grandes.", 4),
             ("casinegro", "Contraste: textos largos y fondos de foto.", 4)]
    cajas = ""
    for k, uso, _ in orden:
        hx = P[k]
        r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
        c, m, y, kk = K[k]
        claro = k in ("crema", "rosa", "oro")
        tx = P["casinegro"] if claro else P["crema"]
        cajas += (f'<div style="display:flex;flex-direction:column"><div style="background:{hx};flex:1;padding:22px 24px;color:{tx};display:flex;flex-direction:column;justify-content:space-between;'
                  f'{"border:1px solid rgba(94,26,36,.25);" if k == "crema" else ""}">'
                  f'<p class="k" style="font-size:36px">{NOMBRES[k]}</p><p style="font-size:19px;line-height:1.3">{uso}</p></div>'
                  f'<div style="padding:14px 2px 0;font-size:18px;line-height:1.5"><p><span class="pie" style="color:var(--bordo);display:inline-block;width:64px">HEX</span>{hx}</p>'
                  f'<p><span class="pie" style="color:var(--bordo);display:inline-block;width:64px">RGB</span>{r} · {g} · {b}</p>'
                  f'<p><span class="pie" style="color:var(--bordo);display:inline-block;width:64px">CMYK</span>{c} · {m} · {y} · {kk}</p></div></div>')
    barra = "".join(f'<div style="background:{P[k]};flex:{p};{"border:1px solid rgba(94,26,36,.25);" if k == "crema" else ""}"></div>' for k, _, p in orden)
    return pag("Paleta", f'''<div class="cuerpo" style="display:flex;flex-direction:column;gap:24px">
   <div style="display:flex;justify-content:space-between;align-items:flex-end">{titulo("paleta")}
   <p style="max-width:640px;font-size:21px">Seis colores, ni uno más. Los CMYK son de referencia para papel estucado: pedí siempre prueba de color. Para el oro viejo, la primera opción es foil (hot stamping), no tinta.</p></div>
   <div class="g" style="grid-template-columns:repeat(6,1fr);gap:18px;flex:1">{cajas}</div>
   <div><h3>PROPORCIÓN DE USO</h3><div style="display:flex;height:26px;gap:0">{barra}</div></div></div>''')


def tipografia():
    return pag("Tipografía", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1fr;gap:70px">
   <div style="display:flex;flex-direction:column">{titulo("tipografía")}
     <div style="margin-top:34px;border-top:1.5px solid var(--bordo);padding-top:18px;flex:1">
       <div style="display:flex;justify-content:space-between;align-items:baseline"><h3>KALNIA · LIGHT 300</h3><span class="pie" style="color:var(--bordo)">GOOGLE FONTS · OFL</span></div>
       <p class="k" style="font-size:190px;color:var(--bordo);line-height:1">Aa</p>
       <p class="k" style="font-size:31px;color:var(--bordo);line-height:1.3;margin-top:6px">abcdefghijklmnñopqrstuvwxyz<br>0123456789 · áéíóú</p>
       <p style="margin-top:20px;font-size:21px">Para el logo, los títulos y los nombres de las piezas. Siempre en peso Light, casi siempre en minúscula, con tracking −0.01 em.</p>
     </div></div>
   <div style="display:flex;flex-direction:column;padding-top:8px">
     <div style="border-top:1.5px solid var(--bordo);padding-top:18px">
       <div style="display:flex;justify-content:space-between;align-items:baseline"><h3>CORMORANT GARAMOND</h3><span class="pie" style="color:var(--bordo)">GOOGLE FONTS · OFL</span></div>
       <div style="display:flex;gap:44px;align-items:baseline;color:var(--bordo)"><span style="font-size:120px;line-height:1.1">Aa</span><span class="it" style="font-size:120px;line-height:1.1">Aa</span><span style="font-size:42px;font-weight:500;letter-spacing:.18em">AA</span></div>
       <p style="font-size:21px;margin-top:8px">Para todos los textos. <span class="it">Itálica</span> para el slogan y las frases. MAYÚSCULAS con espaciado de 0.18 em para etiquetas y datos.</p>
     </div>
     <div style="margin-top:26px;border-top:1.5px solid var(--bordo);padding-top:18px;flex:1"><h3>JERARQUÍA</h3>
       <div style="display:grid;grid-template-columns:190px 1fr;gap:15px 20px;align-items:baseline;margin-top:8px">
        <span class="pie" style="color:var(--bordo)">TÍTULO</span><span class="k" style="font-size:50px;color:var(--bordo)">colección fuego</span>
        <span class="pie" style="color:var(--bordo)">NOMBRE DE PIEZA</span><span class="k" style="font-size:30px;color:var(--bordo)">[nombre de la pieza]</span>
        <span class="pie" style="color:var(--bordo)">FRASE · SLOGAN</span><span class="it" style="font-size:32px;color:var(--bordo)">hecho para mujeres bravas</span>
        <span class="pie" style="color:var(--bordo)">TEXTO</span><span style="font-size:22px;line-height:1.35">Cada pieza se hace a mano en el taller, una por una. Por eso ninguna es idéntica a otra.</span>
        <span class="pie" style="color:var(--bordo)">ETIQUETA · DATO</span><span style="font-weight:500;letter-spacing:.18em;font-size:16px">HECHO A MANO EN CÓRDOBA · MATERIAL · [COMPLETAR]</span>
       </div></div>
   </div></div>''')


def texturas():
    fotos = [(img("02_mockups/01_relieve-seco_logo_crema.png", "tex1"), "RELIEVE SECO", "Sobre papel de algodón crema. Sin tinta: solo la forma."),
             (img("02_mockups/02_relieve-tono-sobre-tono_isotipo_bordo.png", "tex2", recorte=(0.08, 0.2, 0.92, 0.76)), "TONO SOBRE TONO", "El isotipo en relieve sobre cartulina bordó."),
             (img("02_mockups/03_foil-oro-viejo_logo_vino.png", "tex3"), "FOIL ORO VIEJO", "Hot stamping mate sobre vino. Nunca oro espejo."),
             (img("02_mockups/04_sello-tinta-bordo_lienzo-crudo.png", "tex4", recorte=(0.08, 0.2, 0.92, 0.76)), "SELLO EN TINTA", "Tinta bordó sobre lienzo crudo, bolsas y papel de seda.")]
    cajas = "".join(f'<div style="display:flex;flex-direction:column;gap:10px;min-height:0"><div style="flex:1;min-height:0"><img class="foto" src="{s}"></div>'
                    f'<div style="display:flex;gap:18px;align-items:baseline"><span class="pie" style="color:var(--bordo);white-space:nowrap">{t}</span><span class="it" style="font-size:19px">{d}</span></div></div>' for s, t, d in fotos)
    return pag("Texturas", f'''<div class="cuerpo" style="display:flex;flex-direction:column;gap:22px">
   <div style="display:flex;justify-content:space-between;align-items:flex-end">{titulo("texturas")}
   <p style="max-width:660px;font-size:21px">La marca se toca antes de leerse. El logo casi nunca va impreso plano: va en relieve, en foil o sellado a mano. Papeles con cuerpo, telas crudas, acabados mate.</p></div>
   <div class="g" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:18px 22px;flex:1;min-height:0">{cajas}</div></div>''')


def etiquetas():
    f = img("02_mockups/05_etiquetas-colgantes_frente-y-dorso.png", "etiquetas", recorte=(0.12, 0.0, 0.94, 1.0))
    return pag("Etiquetas", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1.75fr;gap:70px">
   <div>{titulo("etiquetas")}
    <p style="margin-top:28px">La etiqueta colgante es la primera página de cada pieza: dice qué es, de qué está hecha y de dónde viene.</p>
    <div style="margin-top:24px"><h3>FRENTE · CREMA</h3><ul style="font-size:21px"><li>Logotipo en bordó con relieve.</li><li>Slogan en itálica.</li><li>Datos en mayúsculas espaciadas: pieza, material, terminación y piedra.</li><li>«Hecho a mano en Córdoba, Argentina».</li></ul></div>
    <div style="margin-top:22px"><h3>DORSO · BORDÓ</h3><ul style="font-size:21px"><li>Isotipo en relieve tono sobre tono.</li><li>Slogan en foil oro viejo.</li></ul></div>
    <div style="margin-top:22px"><h3>MATERIALES SUGERIDOS</h3><ul style="font-size:21px"><li>Cartulina de 350 g o más, 55 × 97 mm, puntas redondeadas.</li><li>Ojalillo dorado. Cinta de raso fina, bordó o crema.</li></ul></div>
   </div>
   <div style="min-height:0"><img class="foto" src="{f}"></div></div>''')


def packaging():
    a = img("02_mockups/06a_kit-influencers_dos-kits_lino.png", "pack1")
    b = img("02_mockups/06b_kit-influencers_detalle_fondo-oscuro.png", "pack2", recorte=(0.02, 0.05, 0.9, 0.98))
    st = "".join(f'<img src="{img("03_stickers/png/" + n + ".png", "st" + str(i), 300)}" style="height:112px;border-radius:50%">' if "ovalo" not in n else ""
                 for i, n in enumerate(["01_circulo-bordo_cardo-oro_50mm", "07_sello-crema_cardo_50mm", "06_circulo-vino_llama-gracias-brava_50mm", "03_circulo-rosa_cardo-logo-vino_50mm"]))
    return pag("Packaging", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1.9fr;gap:60px">
   <div>{titulo("packaging")}
    <p style="margin-top:26px">Abrir un pedido tiene que sentirse como recibir una carta de alguien que te conoce.</p>
    <div style="margin-top:22px"><h3>EL KIT</h3><ul style="font-size:21px"><li>Sobre-bolsa bordó.</li><li>Tarjeta crema o rosa con el logo en relieve seco, el slogan y el @ de quien lo recibe.</li><li>Cinta de raso crema, con moño.</li><li>Sticker de cierre con el cardo.</li></ul></div>
    <div style="margin-top:22px"><h3>STICKERS</h3><p style="font-size:21px">Cardo en foil sobre bordó para cerrar; sello crema para papel de seda; «gracias, brava» con la llama para el interior.</p></div>
    <div style="display:flex;gap:16px;margin-top:20px">{st}</div>
   </div>
   <div class="g" style="grid-template-rows:1fr 1fr;gap:18px;min-height:0">
     <div style="min-height:0"><img class="foto" src="{a}"></div><div style="min-height:0"><img class="foto" src="{b}"></div></div></div>''')


def redes():
    def t(n, w):
        return f'<img src="{img("04_redes/png/" + n + ".png", "r_" + n[:12], 900)}" style="width:{w}px;display:block">'
    dest = "".join(f'<div style="text-align:center"><div style="width:92px;height:92px;border-radius:50%;overflow:hidden;border:1px solid rgba(94,26,36,.3)"><img src="{img("04_redes/png/destacado_%02d_%s.png" % (i + 1, n), "d" + str(i), 500, recorte=(0.27, 0.355, 0.73, 0.615))}" style="width:100%;height:100%;object-fit:cover"></div>'
                   f'<p style="font-size:16px;margin-top:6px">{n}</p></div>'
                   for i, n in enumerate(["nuevo", "aros", "collares", "anillos", "cuidados"]))
    return pag("Redes", f'''<div class="cuerpo g" style="grid-template-columns:1fr 2.55fr;gap:56px">
   <div>{titulo("redes")}
    <p style="margin-top:26px">El feed alterna tres tipos de pieza: <span class="it">fondo pleno con tipografía</span>, <span class="it">foto de producto</span> y <span class="it">mujeres bravas</span>.</p>
    <div style="margin-top:22px"><h3>REGLAS</h3><ul style="font-size:21px"><li>Fondos solo en bordó, vino, crema o rosa.</li><li>Un mensaje por pieza. Mucho aire.</li><li>Fechas y títulos en Kalnia; frases en itálica; datos en mayúsculas.</li><li>Perfil: isotipo crema sobre bordó.</li><li>Destacados: íconos propios sobre crema.</li></ul></div>
    <div style="margin-top:22px"><h3>PLANTILLAS</h3><p style="font-size:21px">04_redes/ · PNG finales y PDF editables para Canva.</p></div>
   </div>
   <div style="display:flex;flex-direction:column;gap:22px">
     <div style="display:flex;gap:20px">{t("post_01_lanzamiento_03-12", 315)}{t("post_02_slogan", 315)}{t("post_03_plantilla-producto", 315)}</div>
     <div style="display:flex;gap:20px;align-items:stretch">
       {t("story_01_lanzamiento_cuenta-regresiva", 230)}{t("story_02_mujeres-bravas_foto-clienta", 230)}
       <div style="flex:1;background:#fff;padding:26px 24px;display:flex;flex-direction:column;justify-content:center;gap:26px">
         <div style="display:flex;gap:20px;align-items:center"><div style="width:104px;height:104px;border-radius:50%;background:var(--bordo);flex:none" class="centro">{marca_svg("bss", "crema", ancho=56)}</div>
           <div><p style="font-weight:500;font-size:22px">bravissima</p><p class="it" style="font-size:18px;line-height:1.3">Joyería de autor · Córdoba<br><span style="color:var(--bordo)">hecho para mujeres bravas</span></p></div></div>
         <div style="display:flex;gap:4px;justify-content:space-between">{dest}</div>
         <p class="pie" style="color:var(--bordo);text-align:center">PERFIL Y DESTACADOS</p></div>
     </div>
   </div></div>''')


def tono():
    si_no = [("Elegí pocas. Elegí bien.", "¡¡Aprovechá las súper ofertas!!"),
             ("Hecha a mano en nuestro taller de Córdoba.", "Productos artesanales de excelente calidad."),
             ("Esta pieza no pide permiso.", "Un accesorio ideal para toda ocasión."),
             ("Gracias, brava.", "¡Gracias por tu compra, que la disfrutes mucho!")]
    filas = "".join(f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;padding:20px 0;border-bottom:1px solid rgba(239,231,221,.25)">'
                    f'<div style="display:flex;gap:14px;align-items:flex-start"><svg width="22" height="22" viewBox="0 0 26 26" style="flex:none;margin-top:6px"><circle cx="13" cy="13" r="12" fill="none" stroke="{P["oro"]}" stroke-width="1.2"/><path d="M7.5 13.5l3.8 3.8 7.4-8.2" fill="none" stroke="{P["oro"]}" stroke-width="1.6"/></svg><span class="it" style="font-size:29px">{a}</span></div>'
                    f'<div style="display:flex;gap:14px;align-items:flex-start;opacity:.6"><svg width="22" height="22" viewBox="0 0 26 26" style="flex:none;margin-top:6px"><circle cx="13" cy="13" r="12" fill="none" stroke="{P["crema"]}" stroke-width="1.2"/><path d="M8.5 8.5l9 9M17.5 8.5l-9 9" fill="none" stroke="{P["crema"]}" stroke-width="1.4"/></svg><span style="font-size:23px;text-decoration:line-through">{b}</span></div></div>' for a, b in si_no)
    rasgos = [("SEGURA", "Afirmamos. No pedimos permiso ni disculpas, no prometemos de más."), ("CÁLIDA", "Hablamos de vos, de cerca, como una amiga que sabe."), ("CON ACTITUD", "Frases cortas. Punto final. Un poco de filo.")]
    r = "".join(f'<div style="border-top:1.5px solid var(--oro);padding-top:14px"><h3>{t}</h3><p style="font-size:24px">{d}</p></div>' for t, d in rasgos)
    return pag("Tono de voz", f'''<div class="cuerpo g" style="grid-template-columns:1fr 1.35fr;gap:80px">
   <div>{titulo("tono de voz", "Hablamos como una brava le habla a otra.")}
     <div class="g" style="gap:30px;margin-top:48px">{r}</div>
     <div style="margin-top:60px">{simbolo_svg("llama", "oro", 96)}</div></div>
   <div><h3>CÓMO ESCRIBIMOS</h3>
     <ul style="font-size:24px;margin-top:6px"><li>Español rioplatense, siempre con voseo: <span class="it">elegí, mirá, llevátela.</span></li><li>El slogan y «mujeres bravas», siempre en minúscula.</li><li><span class="it">Brava</span> es el nombre de quien nos lee: «gracias, brava».</li><li>Sin diminutivos, sin signos en cadena, sin promesas vacías.</li><li>No inventamos datos: si no sabemos el material o el precio, no lo decimos.</li></ul>
     <div style="margin-top:34px"><div style="display:grid;grid-template-columns:1fr 1fr;gap:26px"><h3>DECIMOS</h3><h3>NO DECIMOS</h3></div>{filas}</div>
   </div></div>''', "osc")


def fotografia():
    tomas = [("rosa", "vino", "01 · PRODUCTO", "Una pieza por foto, sobre lino, papel crema o piedra."),
             ("bordo", "crema", "02 · EN USO", "Primer plano de oreja, cuello o manos. Piel real."),
             ("vino", "crema", "03 · TALLER", "Manos, fuego, herramientas. El proceso sin maquillaje."),
             ("crema", "bordo", "04 · BRAVAS", "Retrato de clientas reales, mirando a cámara.")]
    cajas = ""
    for i, (bg, tx, t, d) in enumerate(tomas):
        span = "grid-row:span 2;" if i == 0 else ""
        tam = 260 if i == 0 else 130
        cajas += (f'<div style="{span}background:{P[bg]};{"border:1px solid rgba(94,26,36,.3);" if bg == "crema" else ""}display:flex;flex-direction:column;padding:22px;color:{P[tx]}">'
                  f'<div class="centro" style="flex:1">{simbolo_svg("cardo", tx, tam, op=0.2)}</div><div><p class="pie">{t}</p><p class="it" style="font-size:20px;line-height:1.3;margin-top:4px">{d}</p></div></div>')
    return pag("Fotografía", f'''<div class="cuerpo g" style="grid-template-columns:1fr 2fr;gap:70px">
   <div>{titulo("fotografía")}
    <p style="margin-top:26px">La foto tiene que parecerse a la pieza: cálida, hecha a mano y sin vueltas.</p>
    <div style="margin-top:22px"><h3>SÍ</h3><ul style="font-size:21px"><li>Luz natural, lateral, de tarde. Sombras suaves.</li><li>Fondos de la paleta y materiales nobles.</li><li>Encuadres cerrados, con aire alrededor.</li><li>Tonos cálidos: que el dorado se vea dorado.</li></ul></div>
    <div style="margin-top:22px"><h3>NO</h3><ul style="font-size:21px"><li>Flash directo y fondo blanco de catálogo.</li><li>Filtros fríos o piel retocada.</li><li>Fotos de banco de imágenes ni de otras marcas.</li><li>Objetos que compitan con la pieza.</li></ul></div>
    <p class="pie" style="margin-top:26px;color:var(--bordo)">LOS BLOQUES SON GUÍAS DE ENCUADRE, NO FOTOS.</p>
   </div>
   <div class="g" style="grid-template-columns:1.2fr 1fr 1fr;grid-template-rows:1fr 1fr;gap:18px">{cajas}</div></div>''')


def cierre():
    return pag("", f'''
  <div class="abs centro" style="left:0;right:0;top:210px">{simbolo_svg("llama", "oro", 150)}</div>
  <p class="abs" style="left:0;right:0;top:430px;text-align:center;font-style:italic;font-weight:300;font-size:150px;line-height:1">gracias, brava</p>
  <div class="abs" style="left:{W/2-70}px;top:660px;width:140px;height:1.5px;background:var(--oro)"></div>
  <div class="abs centro" style="left:0;right:0;top:730px">{marca_svg("bravissima", "crema", ancho=380)}</div>
  <p class="abs caps" style="left:0;right:0;top:860px;text-align:center;font-size:15px">@[USUARIO] · [WEB] · CÓRDOBA, ARGENTINA</p>
  <p class="abs it" style="left:0;right:0;top:1060px;text-align:center;font-size:20px;opacity:.8">Ante la duda: menos elementos, más aire, y el logo tal como es.</p>
''', "osc2", pie=False)


def construir():
    _n[0] = 0
    paginas = [portada(), indice(), esencia(), manifiesto(), logotipo(), construccion(), isotipo(), simbolos(), versiones(), incorrectos(),
               paleta(), tipografia(), texturas(), etiquetas(), packaging(), redes(), tono(), fotografia(), cierre()]
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>bravissima — manual de marca</title>'
            f'<style>{CSS}@page{{size:297mm 210mm;margin:0}}@media print{{html{{zoom:{1122.52 / W:.6f}}}html,body{{background:none}}}}</style></head><body>{"".join(paginas)}</body></html>')
    SRC.mkdir(parents=True, exist_ok=True)
    (SRC / "manual.html").write_text(html, encoding="utf-8")
    js = f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {W}, height: {H} }} }});
  await p.goto('file://{SRC / "manual.html"}');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  await p.pdf({{ path: '{OUT / "bravissima_manual-de-marca.pdf"}', preferCSSPageSize: true, printBackground: true,
                 margin: {{ top: 0, right: 0, bottom: 0, left: 0 }} }});
  await b.close();
}})();"""
    tmp = AQUI / "_tmp_manual.js"
    tmp.write_text(js)
    subprocess.run(["node", str(tmp)], check=True)
    tmp.unlink()
    print("ok", len(paginas), "páginas")


if __name__ == "__main__":
    construir()
