"""Kit de marca para Canva: logo, isotipo, símbolos, íconos, sello, paleta y tipografías
como elementos editables (vectores + texto vivo), en un PDF de varias páginas 1920×1080."""
import subprocess

from marca import PALETA as P, RAIZ, contorno
from simbolos import contorno_simbolo
from tipo import sello

DEST = RAIZ / "01_logo" / "editable_canva"
AQUI = RAIZ / "_herramientas"
F = (RAIZ / "_fuentes" / "estaticas").as_uri()
W, H = 1920, 1080


def vec(d, caja, color, cx, cy, ancho=None, alto=None):
    x0, y0, x1, y1 = caja
    s = ancho / (x1 - x0) if ancho else alto / (y1 - y0)
    return (f'<path fill="{P.get(color, color)}" transform="translate({cx - s * (x0 + x1) / 2:.2f} {cy - s * (y0 + y1) / 2:.2f}) scale({s:.6f})" d="{d}"/>')


def logo(t, color, cx, cy, ancho=None, alto=None):
    d, caja = contorno(t)
    return vec(d, caja, color, cx, cy, ancho, alto)


def simb(n, color, cx, cy, alto):
    d, caja = contorno_simbolo(n)
    return vec(d, caja, color, cx, cy, alto=alto)


def txt(t, x, y, size, color, fam="Cormorant Garamond", peso=400, it=False, ancla="start", track=0.0):
    ls = f' letter-spacing="{track * size:.2f}"' if track else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{peso}" font-style="{"italic" if it else "normal"}" '
            f'fill="{P.get(color, color)}" text-anchor="{ancla}"{ls} style="font-variant-numeric:lining-nums">{t}</text>')


def caja(x, y, w, h, color):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{P.get(color, color)}"/>'


def rotulo(t):
    return txt(t, 80, 92, 22, "bordo", peso=500, track=0.18) + caja(80, 112, 1760, 1.5, "bordo")


def pagina(nombre, cuerpo, fondo="crema"):
    return (f'<section class="page" data-nombre="{nombre}"><svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{caja(0, 0, W, H, fondo)}{cuerpo}</svg></section>')


def construir():
    pags = []
    # 1 · logotipo
    c = rotulo("LOGOTIPO · bravissima")
    c += caja(80, 150, 1760, 470, "#FFFFFF") + logo("bravissima", "bordo", 960, 385, ancho=1100)
    for i, (fondo, tinta) in enumerate((("bordo", "crema"), ("vino", "crema"), ("rosa", "vino"))):
        x = 80 + i * 597
        c += caja(x, 650, 566, 340, fondo) + logo("bravissima", tinta, x + 283, 820, ancho=420)
    c += txt("Elementos editables: hacé clic sobre el logo y cambiale el color. No lo estires ni separes la ss.", 80, 1040, 22, "negro", it=True)
    pags.append(pagina("01_logotipo", c))

    # 2 · isotipo
    c = rotulo("ISOTIPO · bss")
    c += caja(80, 150, 860, 840, "#FFFFFF") + logo("bss", "bordo", 510, 570, ancho=600)
    c += caja(980, 150, 420, 410, "bordo") + logo("bss", "crema", 1190, 355, ancho=260)
    c += caja(1420, 150, 420, 410, "vino") + logo("bss", "crema", 1630, 355, ancho=260)
    c += caja(980, 580, 420, 410, "rosa") + logo("bss", "vino", 1190, 785, ancho=260)
    c += caja(1420, 580, 420, 410, "#FFFFFF") + f'<circle cx="1630" cy="770" r="160" fill="{P["bordo"]}"/>' + logo("bss", "crema", 1630, 770, ancho=190)
    c += txt("foto de perfil", 1630, 970, 20, "bordo", it=True, ancla="middle")
    pags.append(pagina("02_isotipo", c))

    # 3 · símbolos
    c = rotulo("SÍMBOLOS · CARDO (EMBLEMA) Y LLAMA (SECUNDARIO)")
    c += caja(80, 150, 560, 840, "#FFFFFF") + simb("cardo", "bordo", 360, 540, 600)
    c += caja(660, 150, 560, 840, "bordo") + simb("cardo", "oro", 940, 540, 600)
    c += caja(1240, 150, 600, 410, "vino") + simb("llama", "oro", 1540, 355, 300)
    c += caja(1240, 580, 600, 410, "#FFFFFF") + simb("llama", "bordo", 1400, 785, 280)
    c += simb("cardo-chico", "bordo", 1610, 760, 150) + simb("llama-chica", "bordo", 1750, 785, 110)
    c += txt("versión chica", 1680, 960, 20, "bordo", it=True, ancla="middle")
    pags.append(pagina("03_simbolos", c))

    # 4 · íconos de destacados
    c = rotulo("ÍCONOS · DESTACADOS Y WEB")
    for i, (n, t) in enumerate((("llama", "NUEVO"), ("icono-aros", "AROS"), ("icono-collares", "COLLARES"), ("icono-anillos", "ANILLOS"), ("icono-cuidados", "CUIDADOS"))):
        x = 80 + i * 357
        c += caja(x, 150, 330, 400, "#FFFFFF") + simb(n, "bordo", x + 165, 330, 220) + txt(t, x + 165, 515, 22, "bordo", peso=500, ancla="middle", track=0.18)
        c += f'<circle cx="{x + 165}" cy="790" r="150" fill="{P["bordo"]}"/>' + simb(n, "crema", x + 165, 775, 150)
    pags.append(pagina("04_iconos", c))

    # 5 · sello
    c = rotulo("SELLO · FRASE EN MAYÚSCULA")
    c += caja(80, 150, 860, 840, "#FFFFFF") + sello(510, 570, 380, color=P["bordo"])
    c += caja(980, 150, 860, 840, "bordo") + sello(1410, 570, 380, color=P["crema"])
    pags.append(pagina("05_sello", c))

    # 6 · paleta y tipografías (texto vivo)
    c = rotulo("PALETA Y TIPOGRAFÍAS")
    nombres = [("bordo", "Bordó", "crema"), ("vino", "Vino", "crema"), ("crema", "Crema", "negro"), ("rosa", "Rosa empolvado", "negro"),
               ("oro", "Oro viejo", "negro"), ("casinegro", "Casi negro", "crema")]
    for i, (k, n, t) in enumerate(nombres):
        x = 80 + i * 297
        borde = f'<rect x="{x}" y="150" width="272" height="420" fill="none" stroke="{P["bordo"]}" stroke-opacity=".3"/>' if k == "crema" else ""
        c += caja(x, 150, 272, 420, k) + borde + txt(n, x + 22, 205, 30, t, fam="Kalnia", peso=300) + txt(P[k], x + 22, 545, 22, t, peso=500, track=0.12)
    c += txt("colección fuego", 80, 720, 96, "bordo", fam="Kalnia", peso=300)
    c += txt("KALNIA LIGHT · títulos y nombres de piezas", 80, 770, 20, "bordo", peso=500, track=0.18)
    c += txt("hecho para mujeres bravas", 980, 700, 64, "bordo", it=True)
    c += txt("CORMORANT GARAMOND ITÁLICA · slogan y frases", 980, 770, 20, "bordo", peso=500, track=0.18)
    c += txt("Cormorant Garamond regular para los textos: cada pieza se hace a mano en el taller, una por una.", 80, 880, 30, "negro")
    c += txt("HECHO A MANO EN CÓRDOBA · DATOS Y ETIQUETAS EN MAYÚSCULA CON ESPACIADO 0.18", 80, 950, 22, "bordo", peso=500, track=0.18)
    pags.append(pagina("06_paleta-y-tipografias", c))

    css = (f'@font-face{{font-family:"Kalnia";src:url("{F}/Kalnia-Light.ttf");font-weight:300}}'
           f'@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Regular.ttf");font-weight:400}}'
           f'@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Medium.ttf");font-weight:500}}'
           f'@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Italic.ttf");font-weight:400;font-style:italic}}'
           f'*{{margin:0;padding:0}}.page{{width:{W}px;height:{H}px;break-after:page;overflow:hidden}}svg{{display:block}}'
           f'@page{{size:{W}px {H}px;margin:0}}')
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>bravissima — kit de marca editable</title><style>{css}</style></head>'
            f'<body data-ancho="{W}" data-alto="{H}" data-unidad="px">{"".join(pags)}</body></html>')
    DEST.mkdir(parents=True, exist_ok=True)
    tmp = AQUI / "_tmp_kit.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(["node", str(AQUI / "exportar_html.js"), str(tmp), "-", str(DEST / "bravissima_kit-de-marca_editable.pdf")], check=True)
    tmp.unlink()
    print("ok kit", len(pags), "páginas")


if __name__ == "__main__":
    construir()
