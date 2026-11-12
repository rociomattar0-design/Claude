"""FASE 3 (revisión) — lámina de propuestas de símbolo aplicado a stickers."""
import cairosvg

from fase3_stickers import Sticker, TEXTO_SELLO, sticker_svg, texto_circulo_d
from marca import PALETA as P, RAIZ
from simbolos import SIMBOLOS, simbolo_d, contorno_simbolo
from tipo import Fuente, marca

OUT = RAIZ / "03_stickers" / "propuestas_simbolo"
OUT.mkdir(parents=True, exist_ok=True)
corm, cormi = Fuente("corm500"), Fuente("cormi")


def stickers_de(n):
    a = Sticker("a", "", ("c", 25), "bordo")
    a.anillo(2.4, 0.3, "oro", "foil").trazo(simbolo_d(n, 0, 0, alto=27), "oro", "foil")
    b = Sticker("b", "", ("c", 25), "crema")
    b.anillo(1.7, 0.45, "bordo").anillo(3.0, 0.22, "bordo").anillo(9.6, 0.22, "bordo")
    b.trazo(texto_circulo_d("corm500", TEXTO_SELLO, 17.55, 0.18), "bordo").trazo(simbolo_d(n, 0, 0, alto=21), "bordo")
    c = Sticker("c", "", ("c", 25), "rosa")
    c.anillo(2.4, 0.3, "vino").trazo(simbolo_d(n, 0, 0, alto=27), "vino")
    d = Sticker("d", "", ("c", 25), "vino")
    d.anillo(2.4, 0.3, "rosa").trazo(simbolo_d(n, 0, 0, alto=27), "rosa")
    return [a, b, c, d]


W, H = 2600, 1870
col_w, x0 = 590, 120
partes = [f'<rect width="{W}" height="{H}" fill="{P["crema"]}"/>',
          f'<path fill="{P["casinegro"]}" d="{corm.path("BRAVISSIMA · PROPUESTAS DE SÍMBOLO", 28, x0, 110, tracking=0.18)}"/>',
          f'<path fill="{P["bordo"]}" d="{cormi.path("hecho para mujeres bravas", 42, W - x0, 112, align="right")}"/>']
ESC = 4.5  # px por mm
for i, (n, (_, nombre, idea)) in enumerate(SIMBOLOS.items()):
    cx = x0 + col_w * i + col_w / 2 - 15
    letra = "ABCD"[i]
    partes.append(f'<rect x="{cx - 265}" y="170" width="530" height="1.5" fill="{P["bordo"]}"/>')
    partes.append(f'<path fill="{P["casinegro"]}" d="{corm.path(f"{letra} · {nombre}", 24, cx, 225, tracking=0.18, align="center")}"/>')
    partes.append(f'<path fill="{P["bordo"]}" d="{cormi.path(idea, 34, cx, 270, align="center")}"/>')
    partes.append(f'<path fill="{P["bordo"]}" d="{simbolo_d(n, cx, 540, alto=400)}"/>')
    # convivencia con el logotipo
    partes.append(f'<path fill="{P["bordo"]}" d="{simbolo_d(n, cx, 890, alto=120)}"/>')
    partes.append(marca("bravissima", cx, 1010, ancho=300, fill=P["bordo"]))
    partes.append(f'<path fill="{P["bordo"]}" d="{cormi.path("hecho para mujeres bravas", 24, cx, 1070, align="center")}"/>')
    # stickers 2×2
    for k, s in enumerate(stickers_de(n)):
        sx = cx + (-1 if k % 2 == 0 else 1) * 132
        sy = 1290 + (k // 2) * 262
        frag = sticker_svg(s, sangrado=False, troquel=False, aislado=False)
        partes.append(f'<ellipse cx="{sx + 5}" cy="{sy + 9}" rx="{25 * ESC}" ry="{25 * ESC}" fill="#3A0F16" opacity=".13"/>')
        partes.append(f'<g transform="translate({sx} {sy}) scale({ESC})">{frag}</g>')
    # símbolo suelto en SVG
    d, (bx0, by0, bx1, by1) = contorno_simbolo(n)
    (OUT / f"simbolo_{letra}_{n}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bx0 - 20:.0f} {by0 - 20:.0f} {bx1 - bx0 + 40:.0f} {by1 - by0 + 40:.0f}">'
        f'<title>bravissima — {nombre.lower()}</title><path fill="{P["bordo"]}" d="{d}"/></svg>', encoding="utf-8")
pie = "Cada símbolo: solo · con el logotipo · en sticker bordó + oro · sello crema (frase en mayúscula) · rosa + vino · vino + rosa"
partes.append(f'<path fill="{P["casinegro"]}" d="{cormi.path(pie, 26, W / 2, 1800, align="center")}"/>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(partes)}</svg>'
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "propuestas_simbolo.png"))
print("ok")
