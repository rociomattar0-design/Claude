"""FASE 4 — Redes: plantillas HTML → PNG finales + PDF editables (texto vivo, para Canva)."""
import subprocess

from marca import PALETA as P, RAIZ, contorno
from simbolos import contorno_simbolo

OUT = RAIZ / "04_redes"
HTML = OUT / "plantillas_html"
EDIT = OUT / "editable_canva"
AQUI = RAIZ / "_herramientas"

CSS = """
@font-face{font-family:"Kalnia";src:url("../../_fuentes/estaticas/Kalnia-Light.ttf");font-weight:300}
@font-face{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Regular.ttf");font-weight:400}
@font-face{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Medium.ttf");font-weight:500}
@font-face{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-Italic.ttf");font-weight:400;font-style:italic}
@font-face{font-family:"Cormorant Garamond";src:url("../../_fuentes/estaticas/CormorantGaramond-LightItalic.ttf");font-weight:300;font-style:italic}
:root{--bordo:#5E1A24;--vino:#3A0F16;--crema:#EFE7DD;--rosa:#D9B8AE;--oro:#B8955A;--negro:#150B0D}
*{margin:0;padding:0;box-sizing:border-box}
html,body{background:#777}
.page{position:relative;overflow:hidden;width:var(--w);height:var(--h);break-after:page;margin:0 auto}
.abs{position:absolute}
.c{left:0;right:0;text-align:center}
.c svg{display:inline-block}
svg{display:block}
.k{font-family:"Kalnia";font-weight:300;letter-spacing:-.01em;line-height:1}
.caps{font-family:"Cormorant Garamond";font-weight:500;letter-spacing:.18em;font-variant-numeric:lining-nums;line-height:1.3}
.it{font-family:"Cormorant Garamond";font-style:italic;font-weight:400;line-height:1.1}
.itl{font-family:"Cormorant Garamond";font-style:italic;font-weight:300}
.bordo{color:var(--bordo)}.vino{color:var(--vino)}.crema{color:var(--crema)}.oro{color:var(--oro)}.negro{color:var(--negro)}
.bg-bordo{background:var(--bordo)}.bg-vino{background:var(--vino)}.bg-crema{background:var(--crema)}.bg-rosa{background:var(--rosa)}
.linea{position:absolute;height:1.5px}
"""


def marca_svg(texto, color, ancho):
    d, (x0, y0, x1, y1) = contorno(texto)
    h = ancho * (y1 - y0) / (x1 - x0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{h:.1f}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" '
            f'role="img" aria-label="{texto}"><path fill="{P.get(color, color)}" d="{d}"/></svg>')


def simbolo_svg(nombre, color, alto, opacidad=1):
    d, (x0, y0, x1, y1) = contorno_simbolo(nombre)
    w = alto * (x1 - x0) / (y1 - y0)
    op = f' opacity="{opacidad}"' if opacidad != 1 else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.1f}" height="{alto}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" '
            f'role="img" aria-label="{nombre}"><path fill="{P.get(color, color)}"{op} d="{d}"/></svg>')


def documento(titulo, w, h, secciones):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<style>{CSS}@page{{size:{w}px {h}px;margin:0}}:root{{--w:{w}px;--h:{h}px}}</style></head>'
            f'<body data-ancho="{w}" data-alto="{h}" data-unidad="px">{"".join(secciones)}</body></html>')


# ───────────────────────── posts 1080 × 1350 ─────────────────────────
def posts():
    lanz = f'''<section class="page bg-bordo" data-nombre="post_01_lanzamiento_03-12">
  <div class="abs" style="inset:44px;border:1.5px solid var(--oro)"></div>
  <div class="abs c" style="top:128px">{simbolo_svg("cardo", "oro", 200)}</div>
  <p class="caps abs c crema" style="top:392px;font-size:30px">LANZAMIENTO</p>
  <h1 class="k abs c crema" style="top:438px;font-size:330px">03.12</h1>
  <div class="linea" style="top:838px;left:480px;width:120px;background:var(--oro)"></div>
  <p class="it abs c crema" style="top:880px;font-size:64px">hecho para mujeres bravas</p>
  <p class="caps abs c crema" style="top:990px;font-size:23px">3 DE DICIEMBRE DE 2026 · CÓRDOBA, ARGENTINA</p>
  <div class="abs c" style="top:1162px">{marca_svg("bravissima", "crema", 330)}</div>
</section>'''
    slogan = f'''<section class="page bg-crema" data-nombre="post_02_slogan">
  <p class="caps abs bordo" style="top:92px;left:90px;font-size:22px">JOYERÍA DE AUTOR</p>
  <p class="caps abs bordo" style="top:92px;right:90px;font-size:22px">CÓRDOBA · ARGENTINA</p>
  <div class="linea" style="top:150px;left:90px;right:90px;background:var(--bordo)"></div>
  <p class="itl abs bordo" style="top:262px;left:82px;font-size:236px;line-height:.96">hecho para<br>mujeres<br>bravas</p>
  <div class="linea" style="top:1118px;left:90px;right:90px;background:var(--bordo)"></div>
  <div class="abs" style="left:90px;top:1160px">{simbolo_svg("llama", "bordo", 110)}</div>
  <div class="abs" style="right:90px;top:1192px">{marca_svg("bravissima", "bordo", 320)}</div>
</section>'''
    producto = f'''<section class="page bg-crema" data-nombre="post_03_plantilla-producto">
  <div class="abs bg-rosa" style="top:0;left:0;width:1080px;height:910px"></div>
  <div class="abs c" style="top:215px">{simbolo_svg("cardo", "vino", 420, 0.14)}</div>
  <p class="caps abs c vino" style="top:700px;font-size:22px">FOTO DE LA PIEZA</p>
  <p class="it abs c vino" style="top:742px;font-size:30px">reemplazá este bloque por tu foto</p>
  <p class="caps abs bordo" style="top:968px;left:90px;font-size:21px">NUEVO · COLECCIÓN [COMPLETAR]</p>
  <h2 class="k abs bordo" style="top:1020px;left:86px;font-size:84px">[nombre de la pieza]</h2>
  <div class="linea" style="top:1150px;left:90px;width:900px;background:var(--bordo)"></div>
  <p class="caps abs negro" style="top:1180px;left:90px;font-size:21px">MATERIAL · [COMPLETAR]</p>
  <p class="caps abs negro" style="top:1222px;left:90px;font-size:21px">PRECIO · $ [COMPLETAR]</p>
  <div class="abs" style="right:90px;top:1186px">{marca_svg("bss", "bordo", 120)}</div>
</section>'''
    return documento("bravissima — posts 1080×1350", 1080, 1350, [lanz, slogan, producto])


# ───────────────────────── stories 1080 × 1920 ─────────────────────────
def _esquinas(x, y, w, h, color, L=46, g=1.5):
    e = []
    for (cx, cy, bx, by) in ((x, y, "left", "top"), (x + w - L, y, "right", "top"),
                             (x, y + h - L, "left", "bottom"), (x + w - L, y + h - L, "right", "bottom")):
        e.append(f'<div class="abs" style="left:{cx}px;top:{cy}px;width:{L}px;height:{L}px;'
                 f'border-{bx}:{g}px solid var(--{color});border-{by}:{g}px solid var(--{color})"></div>')
    return "".join(e)


def stories():
    lanz = f'''<section class="page bg-vino" data-nombre="story_01_lanzamiento_cuenta-regresiva">
  <div class="abs c" style="top:262px">{marca_svg("bravissima", "crema", 320)}</div>
  <div class="abs c" style="top:392px">{simbolo_svg("cardo", "oro", 170)}</div>
  <p class="caps abs c crema" style="top:626px;font-size:32px">LANZAMIENTO</p>
  <h1 class="k abs c crema" style="top:676px;font-size:350px">03.12</h1>
  <p class="it abs c crema" style="top:1066px;font-size:66px">hecho para mujeres bravas</p>
  <p class="caps abs c oro" style="top:1206px;font-size:24px">FALTA MUY POCO</p>
  {_esquinas(170, 1262, 740, 280, "oro")}
  <p class="it abs c crema" style="top:1380px;font-size:30px;opacity:.55">tu sticker de cuenta regresiva va acá</p>
</section>'''
    brava = f'''<section class="page bg-crema" data-nombre="story_02_mujeres-bravas_foto-clienta">
  <p class="caps abs c bordo" style="top:262px;font-size:26px">COMUNIDAD</p>
  <h1 class="k abs c bordo" style="top:312px;font-size:112px">mujeres bravas</h1>
  <div class="abs" style="left:122px;top:486px;width:836px;height:936px;border:1.5px solid var(--bordo)"></div>
  <div class="abs bg-rosa" style="left:140px;top:504px;width:800px;height:900px"></div>
  <div class="abs c" style="top:760px">{simbolo_svg("cardo", "vino", 300, 0.14)}</div>
  <p class="caps abs c vino" style="top:1110px;font-size:22px">FOTO DE LA CLIENTA</p>
  <p class="it abs c vino" style="top:1150px;font-size:30px">reemplazá este bloque por su foto</p>
  <p class="it abs c bordo" style="top:1452px;font-size:52px">así la lleva una brava</p>
  <p class="caps abs c bordo" style="top:1530px;font-size:26px">@[USUARIO]</p>
</section>'''
    return documento("bravissima — stories 1080×1920", 1080, 1920, [lanz, brava])


# ───────────────────────── perfil 1080 × 1080 ─────────────────────────
def perfil():
    s = f'''<section class="page bg-bordo" data-nombre="perfil_isotipo-crema-sobre-bordo">
  <div class="abs c" style="top:398px">{marca_svg("bss", "crema", 520)}</div>
</section>'''
    return documento("bravissima — foto de perfil", 1080, 1080, [s])


# ───────────────────────── destacados 1080 × 1920 ─────────────────────────
DESTACADOS = [("nuevo", "llama"), ("aros", "icono-aros"), ("collares", "icono-collares"),
              ("anillos", "icono-anillos"), ("cuidados", "icono-cuidados")]


def destacados():
    secs = []
    for i, (nombre, icono) in enumerate(DESTACADOS, 1):
        secs.append(f'''<section class="page bg-crema" data-nombre="destacado_{i:02d}_{nombre}">
  <div class="abs c" style="top:790px">{simbolo_svg(icono, "bordo", 270)}</div>
  <p class="caps abs c bordo" style="top:1102px;font-size:40px">{nombre.upper()}</p>
</section>''')
    return documento("bravissima — portadas de destacados", 1080, 1920, secs)


CONJUNTOS = {
    "posts": (posts, "bravissima_posts_1080x1350"),
    "stories": (stories, "bravissima_stories_1080x1920"),
    "perfil": (perfil, "bravissima_perfil_1080x1080"),
    "destacados": (destacados, "bravissima_destacados_1080x1920"),
}

if __name__ == "__main__":
    for d in (HTML, EDIT, OUT / "png"):
        d.mkdir(parents=True, exist_ok=True)
    for clave, (fn, base) in CONJUNTOS.items():
        ruta = HTML / f"{clave}.html"
        ruta.write_text(fn(), encoding="utf-8")
        subprocess.run(["node", str(AQUI / "exportar_html.js"), str(ruta), str(OUT / "png"),
                        str(EDIT / f"{base}_editable.pdf")], check=True)
        print("ok", clave)
