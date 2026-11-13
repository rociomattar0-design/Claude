"""Mockups editables para Canva: fondo fotográfico vacío + logo y textos como elementos editables.

Cada PDF tiene:
  · una imagen de fondo (la escena renderizada SIN la marca: fondos/*_fondo-vacio.jpg)
  · encima, el logo / isotipo / sello como VECTORES y los textos como TEXTO VIVO,
    en la misma posición y rotación que en el mockup original.
El relieve se imita con tres copias del vector (luz arriba-izquierda, sombra abajo-derecha
y la forma en el color del papel), así sigue siendo editable en Canva.
"""
import subprocess

import numpy as np
from PIL import Image

from fase2_mockups import matriz, pt
from marca import PALETA as P, RAIZ
from tipo import marca, sello

DEST = RAIZ / "02_mockups" / "editable_canva"
FONDOS = DEST / "fondos"
AQUI = RAIZ / "_herramientas"
F = (RAIZ / "_fuentes" / "estaticas").as_uri()

CSS = f"""
@font-face{{font-family:"Kalnia";src:url("{F}/Kalnia-Light.ttf");font-weight:300}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Medium.ttf");font-weight:500}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Italic.ttf");font-weight:400;font-style:italic}}
*{{margin:0;padding:0}}
.page{{position:relative;overflow:hidden;width:var(--w);height:var(--h)}}
.page img{{position:absolute;inset:0;width:100%;height:100%}}
.page svg{{position:absolute;inset:0}}
"""


# ───────────────────────── color ─────────────────────────
def hx(rgb):
    return "#%02X%02X%02X" % tuple(int(round(v)) for v in rgb)


def mezcla(rgb, con, t):
    return [a * (1 - t) + b * t for a, b in zip(rgb, con)]


def muestra(fondo, x, y, r=40):
    """Color mediano del fondo alrededor de (x, y)."""
    a = np.asarray(fondo)[max(0, int(y - r)):int(y + r), max(0, int(x - r)):int(x + r)].reshape(-1, 3)
    return np.median(a, axis=0).tolist()


def relieve(fragmento, base, d, hundido=False, luz=0.42, sombra=0.45):
    """Tres copias del mismo vector: sombra, luz y forma. `fragmento` usa fill="COLOR"."""
    claro = hx(mezcla(base, (255, 255, 255), luz))
    oscuro = hx(mezcla(base, (0, 0, 0), sombra))
    s1, s2 = (-d, d) if hundido else (d, -d)
    return (f'<g transform="translate({s1} {s1})" opacity=".8">{fragmento.replace("COLOR", oscuro)}</g>'
            f'<g transform="translate({s2} {s2})" opacity=".9">{fragmento.replace("COLOR", claro)}</g>'
            f'{fragmento.replace("COLOR", hx(base))}')


def texto(t, x, y, size, color, fam="Cormorant Garamond", peso=400, italica=False, ancla="middle", track=0.0, op=1):
    est = "italic" if italica else "normal"
    ls = f' letter-spacing="{track * size:.2f}"' if track else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size:.2f}" font-weight="{peso}" font-style="{est}" '
            f'fill="{color}" text-anchor="{ancla}"{ls} opacity="{op}" style="font-variant-numeric:lining-nums">{t}</text>')


def rect(x, y, w, h, color, op=1):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{color}" opacity="{op}"/>'


def grupo(cx, cy, w, h, ang, cuerpo):
    """Grupo con coordenadas locales (w×h) centrado en (cx, cy) y rotado como en la escena (ángulo cv2, antihorario)."""
    return f'<g transform="translate({cx - w / 2:.2f} {cy - h / 2:.2f}) rotate({-ang} {w / 2} {h / 2})">{cuerpo}</g>'


# ───────────────────────── salida ─────────────────────────
def exportar(nombre, fondo_jpg, W, H, capas, titulo):
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<style>{CSS}@page{{size:{W}px {H}px;margin:0}}:root{{--w:{W}px;--h:{H}px}}</style></head>'
            f'<body data-ancho="{W}" data-alto="{H}" data-unidad="px"><section class="page" data-nombre="{nombre}">'
            f'<img src="{fondo_jpg.as_uri()}" alt="">'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{capas}</svg>'
            f'</section></body></html>')
    tmp = AQUI / f"_tmp_{nombre}.html"
    tmp.write_text(html, encoding="utf-8")
    pdf = DEST / f"{nombre}_editable.pdf"
    subprocess.run(["node", str(AQUI / "exportar_html.js"), str(tmp), "-", str(pdf)], check=True)
    tmp.unlink()
    print("ok", pdf.name, f"{pdf.stat().st_size / 1e6:.1f} MB")


def fondo(nombre):
    ruta = next(FONDOS.glob(f"{nombre}*_fondo-vacio.jpg"))
    return ruta, Image.open(ruta).convert("RGB")


# ───────────────────────── mockups ─────────────────────────
def m1():
    ruta, im = fondo("01_")
    W, H = im.size
    base = muestra(im, W / 2, H / 2)
    capas = relieve(marca("bravissima", W / 2, H / 2, ancho=1500, fill="COLOR"), base, 3.2, luz=0.55, sombra=0.32)
    exportar("01_relieve-seco_logo_crema", ruta, W, H, capas, "bravissima — relieve seco (editable)")


def m2():
    ruta, im = fondo("02_")
    W, H = im.size
    base = muestra(im, W / 2, H / 2)
    capas = relieve(marca("bss", W / 2, H / 2, ancho=1000, fill="COLOR"), base, 5, luz=0.22, sombra=0.4)
    exportar("02_relieve-tono-sobre-tono_isotipo_bordo", ruta, W, H, capas, "bravissima — tono sobre tono (editable)")


def m3():
    ruta, im = fondo("03_")
    W, H = im.size
    base = muestra(im, W / 2, H / 2)
    oro = marca("bravissima", W / 2, H / 2, ancho=1500, fill="COLOR")
    capas = (f'<g transform="translate(-2.5 -2.5)" opacity=".85">{oro.replace("COLOR", hx(mezcla(base, (0, 0, 0), 0.5)))}</g>'
             f'<g transform="translate(1.5 1.5)" opacity=".9">{oro.replace("COLOR", "#F1DFB0")}</g>'
             f'{oro.replace("COLOR", "#C9A66A")}')
    exportar("03_foil-oro-viejo_logo_vino", ruta, W, H, capas, "bravissima — foil oro viejo (editable)")


def m4():
    ruta, im = fondo("04_")
    W, H = im.size
    capas = f'<g opacity=".86">{sello(W / 2, H / 2 + 20, 760, color=P["bordo"])}</g>'
    exportar("04_sello-tinta-bordo_lienzo-crudo", ruta, W, H, capas, "bravissima — sello en tinta (editable)")


def m5():
    ruta, im = fondo("05_")
    W, H = im.size
    w, h = 780, 1380
    # frente crema
    cx, cy, ang = 1160, 1330, 5.5
    M = matriz(w, h, cx, cy, ang)
    base = muestra(im, *pt(M, w / 2, 395))
    bor = P["bordo"]
    filas = ""
    for lab, y in (("PIEZA", 680), ("MATERIAL", 770), ("TERMINACIÓN", 860), ("PIEDRA", 950)):
        filas += (texto(lab, 108, y, 22, bor, peso=500, ancla="start", track=0.18)
                  + texto("[completar]", w - 108, y + 2, 32, bor, italica=True, ancla="end")
                  + rect(108, y + 22, w - 216, 1.2, bor, 0.55))
    frente = (relieve(marca("bravissima", w / 2, 395, ancho=560, fill="COLOR"), mezcla(base, [int(bor[i:i + 2], 16) for i in (1, 3, 5)], 0.92), 1.6, luz=0.3)
              + texto("hecho para mujeres bravas", w / 2, 505, 40, bor, italica=True)
              + rect(w / 2 - 170, 575, 340, 1.6, bor)
              + filas
              + texto("HECHO A MANO EN CÓRDOBA", w / 2, h - 150, 21, bor, peso=500, track=0.18)
              + texto("ARGENTINA", w / 2, h - 112, 21, bor, peso=500, track=0.18))
    capas = grupo(cx, cy, w, h, ang, frente)
    # dorso bordó
    cx, cy, ang = 2120, 1250, -7.0
    M = matriz(w, h, cx, cy, ang)
    base = muestra(im, *pt(M, w / 2, 610))
    dorso = (relieve(marca("bss", w / 2, 610, ancho=400, fill="COLOR"), base, 2.6, luz=0.2, sombra=0.42)
             + texto("hecho para mujeres bravas", w / 2, 905, 46, "#C9A66A", italica=True)
             + rect(w / 2 - 60, 980, 120, 1.8, "#C9A66A")
             + texto("MUJERES BRAVAS", w / 2, h - 130, 21, P["crema"], peso=500, track=0.18, op=0.92))
    capas += grupo(cx, cy, w, h, ang, dorso)
    exportar("05_etiquetas-colgantes_frente-y-dorso", ruta, W, H, capas, "bravissima — etiquetas colgantes (editable)")


def _tarjeta(im, cx, cy, ang, s, tinta):
    ew, eh = int(1500 * s), int(1020 * s)
    M = matriz(ew, eh, cx, cy, ang)
    tw, th = int(1200 * s), int(760 * s)
    ox, oy = pt(M, ew / 2 + 30 * s, eh / 2 + 55 * s)
    M2 = matriz(tw, th, ox, oy, ang + 1.5)
    lx = tw * 0.60
    base = muestra(im, *pt(M2, lx, th * 0.40))
    cuerpo = (relieve(marca("bravissima", lx, th * 0.40, ancho=tw * 0.38, fill="COLOR"), base, 1.6 * s + 0.6, luz=0.5, sombra=0.3)
              + texto("hecho para mujeres bravas", lx, th * 0.565, th * 0.058, tinta, italica=True)
              + texto("@[usuario]", lx, th * 0.87, th * 0.036, tinta, peso=500, track=0.12))
    return grupo(ox, oy, tw, th, ang + 1.5, cuerpo)


def m6():
    ruta, im = fondo("06a_")
    W, H = im.size
    capas = _tarjeta(im, 1050, 820, 7, 0.86, P["bordo"]) + _tarjeta(im, 2130, 1580, -5, 0.86, P["vino"])
    exportar("06a_kit-influencers_dos-kits_lino", ruta, W, H, capas, "bravissima — kit influencers (editable)")
    ruta, im = fondo("06b_")
    W, H = im.size
    capas = _tarjeta(im, 1720, 1330, -6, 1.8, P["bordo"])
    exportar("06b_kit-influencers_detalle_fondo-oscuro", ruta, W, H, capas, "bravissima — kit detalle (editable)")


if __name__ == "__main__":
    m1(); m2(); m3(); m4(); m5(); m6()
