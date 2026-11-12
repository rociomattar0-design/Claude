"""Editables para Canva de las piezas de imprenta: etiquetas, tarjeta del kit y stickers.
PDF con texto vivo (Kalnia / Cormorant Garamond) y logo + símbolos en vector. Medidas reales en mm."""
import subprocess

from fase3_stickers import TEXTO_SELLO
from marca import PALETA as P, RAIZ, contorno
from simbolos import contorno_simbolo
from tipo import Fuente

AQUI = RAIZ / "_herramientas"
TMP = AQUI / "_tmp"
F = (RAIZ / "_fuentes" / "estaticas").as_uri()

CSS = f"""
@font-face{{font-family:"Kalnia";src:url("{F}/Kalnia-Light.ttf");font-weight:300}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Medium.ttf");font-weight:500}}
@font-face{{font-family:"Cormorant Garamond";src:url("{F}/CormorantGaramond-Italic.ttf");font-weight:400;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
.page{{position:relative;overflow:hidden;width:var(--w);height:var(--h);break-after:page}}
.abs{{position:absolute}} .c{{left:0;right:0;text-align:center}} .c svg{{display:inline-block}} svg{{display:block}}
.caps{{font-family:"Cormorant Garamond";font-weight:500;letter-spacing:.18em;font-variant-numeric:lining-nums;line-height:1.2}}
.it{{font-family:"Cormorant Garamond";font-style:italic;font-weight:400;line-height:1.1}}
"""


def marca_svg(texto, color, ancho, op=1):
    d, (x0, y0, x1, y1) = contorno(texto)
    h = ancho * (y1 - y0) / (x1 - x0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}mm" height="{h:.3f}mm" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}">'
            f'<path fill="{P[color]}" opacity="{op}" d="{d}"/></svg>')


def simbolo_svg(nombre, color, alto):
    d, (x0, y0, x1, y1) = contorno_simbolo(nombre)
    w = alto * (x1 - x0) / (y1 - y0)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{alto}mm" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}">'
            f'<path fill="{P[color]}" d="{d}"/></svg>')


def doc(titulo, w, h, secciones):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{titulo}</title>'
            f'<style>{CSS}@page{{size:{w}mm {h}mm;margin:0}}:root{{--w:{w}mm;--h:{h}mm}}</style></head>'
            f'<body data-ancho="{w}" data-alto="{h}" data-unidad="mm">{"".join(secciones)}</body></html>')


def exportar(nombre, html, destino):
    TMP.mkdir(exist_ok=True)
    destino.parent.mkdir(parents=True, exist_ok=True)
    ruta = TMP / f"{nombre}.html"
    ruta.write_text(html, encoding="utf-8")
    subprocess.run(["node", str(AQUI / "exportar_html.js"), str(ruta), "-", str(destino)], check=True)
    ruta.unlink()
    print("ok", destino.name)


# ───────────────────────── etiquetas 55 × 97 mm ─────────────────────────
def etiquetas():
    W, H = 55, 97
    agujero = lambda col: (f'<div class="abs" style="left:{W/2-2.7}mm;top:5.6mm;width:5.4mm;height:5.4mm;border-radius:50%;'
                           f'border:.2mm solid {P[col]}"></div>')
    filas = ""
    for lab, y in (("PIEZA", 46.6), ("MATERIAL", 53.0), ("TERMINACIÓN", 59.4), ("PIEDRA", 65.8)):
        filas += (f'<p class="caps abs" style="left:7.6mm;top:{y}mm;font-size:1.75mm;color:{P["bordo"]}">{lab}</p>'
                  f'<p class="it abs" style="right:7.6mm;top:{y - .55}mm;font-size:2.5mm;color:{P["bordo"]}">[completar]</p>'
                  f'<div class="abs" style="left:7.6mm;right:7.6mm;top:{y + 3.2}mm;height:.1mm;background:{P["bordo"]};opacity:.55"></div>')
    frente = f'''<section class="page" data-nombre="etiqueta_frente" style="background:{P["crema"]}">
  {agujero("bordo")}
  <div class="abs c" style="top:25.2mm">{marca_svg("bravissima", "bordo", 39.5)}</div>
  <p class="it abs c" style="top:33.2mm;font-size:2.85mm;color:{P["bordo"]}">hecho para mujeres bravas</p>
  <div class="abs" style="left:15.5mm;right:15.5mm;top:40.6mm;height:.12mm;background:{P["bordo"]}"></div>
  {filas}
  <p class="caps abs c" style="top:85.4mm;font-size:1.6mm;color:{P["bordo"]}">HECHO A MANO EN CÓRDOBA</p>
  <p class="caps abs c" style="top:88.4mm;font-size:1.6mm;color:{P["bordo"]}">ARGENTINA</p>
</section>'''
    dorso = f'''<section class="page" data-nombre="etiqueta_dorso" style="background:{P["bordo"]}">
  {agujero("crema")}
  <div class="abs c" style="top:35.6mm">{marca_svg("bss", "vino", 28.2)}</div>
  <p class="it abs c" style="top:60.6mm;font-size:3.25mm;color:{P["oro"]}">hecho para mujeres bravas</p>
  <div class="abs" style="left:23.3mm;right:23.3mm;top:69.1mm;height:.13mm;background:{P["oro"]}"></div>
  <p class="caps abs c" style="top:86.2mm;font-size:1.6mm;color:{P["crema"]}">MUJERES BRAVAS</p>
</section>'''
    exportar("etiquetas", doc("bravissima — etiquetas colgantes 55×97 mm", W, H, [frente, dorso]),
             RAIZ / "02_mockups" / "editable_canva" / "bravissima_etiquetas_55x97mm_editable.pdf")


# ───────────────────────── tarjeta del kit 120 × 76 mm ─────────────────────────
def tarjetas():
    W, H = 120, 76
    secs = []
    for nombre, fondo, relieve, op, tinta in (("crema", "crema", "rosa", 0.75, "bordo"), ("rosa", "rosa", "bordo", 0.22, "vino")):
        secs.append(f'''<section class="page" data-nombre="tarjeta_{nombre}" style="background:{P[fondo]}">
  <div class="abs c" style="top:26.4mm">{marca_svg("bravissima", relieve, 46, op)}</div>
  <p class="it abs c" style="top:39.2mm;font-size:4.4mm;color:{P[tinta]}">hecho para mujeres bravas</p>
  <p class="caps abs c" style="top:63.6mm;font-size:2.5mm;letter-spacing:.12em;color:{P[tinta]}">@[usuario]</p>
</section>''')
    exportar("tarjetas", doc("bravissima — tarjeta kit influencers 120×76 mm", W, H, secs),
             RAIZ / "02_mockups" / "editable_canva" / "bravissima_tarjeta-kit_120x76mm_editable.pdf")


# ───────────────────────── stickers ─────────────────────────
def _anillos(lado, radios, color):
    c = lado / 2
    return (f'<svg class="abs" style="left:0;top:0" xmlns="http://www.w3.org/2000/svg" width="{lado}mm" height="{lado}mm" viewBox="0 0 {lado} {lado}">'
            + "".join(f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{P[color]}" stroke-width="{g}"/>' for r, g in radios) + "</svg>")


def _frase_circular(lado, color):
    c = lado / 2
    d, _ = Fuente("corm500").circulo(TEXTO_SELLO, c, c, 17.55, tracking=0.18)
    return (f'<svg class="abs" style="left:0;top:0" xmlns="http://www.w3.org/2000/svg" width="{lado}mm" height="{lado}mm" viewBox="0 0 {lado} {lado}">'
            f'<path fill="{P[color]}" d="{d}"/></svg>')


def _centro(svg_html, lado, alto_mm, dy=0.0):
    return f'<div class="abs c" style="top:{lado / 2 - alto_mm / 2 + dy:.2f}mm">{svg_html}</div>'


def stickers():
    L = 54  # Ø50 + 2 mm de sangrado por lado: el troquel circular va centrado
    corte = lambda col: (f'<div class="abs" style="left:2mm;top:2mm;width:50mm;height:50mm;border-radius:50%;border:.1mm dashed {P[col]};opacity:.5"></div>')
    sello = [(23.3, 0.45), (22.0, 0.22), (15.4, 0.22)]
    alto_bss = 17.5 * 772 / 1450
    circ = [
        f'''<section class="page" data-nombre="s01" style="background:{P["bordo"]}">{corte("crema")}{_anillos(L, [(22.6, .3)], "oro")}
  {_centro(simbolo_svg("cardo", "oro", 29), L, 29, .3)}</section>''',
        f'''<section class="page" data-nombre="s02" style="background:{P["crema"]}">{corte("bordo")}{_anillos(L, sello, "bordo")}{_frase_circular(L, "bordo")}
  {_centro(marca_svg("bss", "bordo", 17.5), L, alto_bss, .3)}</section>''',
        f'''<section class="page" data-nombre="s03" style="background:{P["rosa"]}">{corte("vino")}{_anillos(L, [(22.6, .25)], "vino")}
  {_centro(simbolo_svg("cardo", "vino", 15.5), L, 15.5, -6.6)}
  <div class="abs c" style="top:{L / 2 + 8.4 - 2.3:.2f}mm">{marca_svg("bravissima", "vino", 31)}</div></section>''',
        f'''<section class="page" data-nombre="s06" style="background:{P["vino"]}">{corte("crema")}{_anillos(L, [(22.6, .3)], "oro")}
  {_centro(simbolo_svg("llama", "oro", 19), L, 19, -4.6)}
  <p class="it abs c" style="top:{L / 2 + 8.6:.2f}mm;font-size:5mm;color:{P["oro"]}">gracias, brava</p></section>''',
        f'''<section class="page" data-nombre="s07" style="background:{P["crema"]}">{corte("bordo")}{_anillos(L, sello, "bordo")}{_frase_circular(L, "bordo")}
  {_centro(simbolo_svg("cardo", "bordo", 21.5), L, 21.5, .2)}</section>''',
        f'''<section class="page" data-nombre="s08" style="background:{P["vino"]}">{corte("crema")}{_anillos(L, [(22.6, .3)], "rosa")}
  {_centro(simbolo_svg("cardo", "rosa", 29), L, 29, .3)}</section>''',
    ]
    exportar("stickers_circulos", doc("bravissima — stickers círculo Ø50 mm", L, L, circ),
             RAIZ / "03_stickers" / "editable_canva" / "bravissima_stickers-circulos_50mm_editable.pdf")

    W, H = 74, 34
    ovalo = lambda col: (f'<svg class="abs" style="left:0;top:0" xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
                         f'<ellipse cx="37" cy="17" rx="33" ry="13" fill="none" stroke="{P[col]}" stroke-width=".22"/>'
                         f'<ellipse cx="37" cy="17" rx="35" ry="15" fill="none" stroke="{P[col]}" stroke-width=".1" stroke-dasharray=".8 .8" opacity=".5"/></svg>')
    tam = 43.0 / Fuente("cormi").ancho("hecho para mujeres bravas", 1.0)
    ov = [
        f'''<section class="page" data-nombre="s04" style="background:{P["bordo"]}">{ovalo("crema")}
  <div class="abs c" style="top:{17 - 5.4 - 4:.2f}mm">{simbolo_svg("llama-chica", "crema", 8)}</div>
  <p class="it abs c" style="top:{17 + 5.4 - tam * 0.8:.2f}mm;font-size:{tam:.2f}mm;line-height:1;color:{P["crema"]}">hecho para mujeres bravas</p></section>''',
        f'''<section class="page" data-nombre="s05" style="background:{P["crema"]}">{ovalo("bordo")}
  <div class="abs" style="left:{37 - 21 - 4.6:.2f}mm;top:{17 + .2 - 6.25:.2f}mm">{simbolo_svg("cardo-chico", "bordo", 12.5)}</div>
  <div class="abs" style="left:{37 + 6.2 - 16:.2f}mm;top:{17 - 2 - 2.37:.2f}mm">{marca_svg("bravissima", "bordo", 32)}</div>
  <p class="caps abs" style="left:{37 + 6.2 - 20:.2f}mm;width:40mm;text-align:center;top:{17 + 6.4 - 1.9:.2f}mm;font-size:2mm;color:{P["bordo"]}">HECHO A MANO EN CÓRDOBA</p></section>''',
    ]
    exportar("stickers_ovalos", doc("bravissima — stickers óvalo 70×30 mm", W, H, ov),
             RAIZ / "03_stickers" / "editable_canva" / "bravissima_stickers-ovalos_70x30mm_editable.pdf")


if __name__ == "__main__":
    etiquetas()
    tarjetas()
    stickers()
    if TMP.exists() and not any(TMP.iterdir()):
        TMP.rmdir()
