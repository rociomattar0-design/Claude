"""FASE 3 — Stickers: diseños vectoriales, planilla A4 con troquel y marcas de corte.

Cada sticker se describe una sola vez (en mm, origen en el centro, eje Y hacia abajo)
y se exporta a:
  · SVG (RGB, capas: sangrado / impresion / hot-stamping-oro / troquel)
  · PDF de imprenta (CMYK + tintas planas "HOT STAMPING ORO" y "CutContour")
  · PNG de vista previa
"""
import cairosvg
from reportlab.lib.colors import CMYKColor, CMYKColorSep
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as rlcanvas

from marca import PALETA as P, PALETA_CMYK as K, RAIZ, contorno
from tipo import Fuente
from vector import dibujar_rl, transformar

OUT = RAIZ / "03_stickers"
SANGRADO = 2.0  # mm
FOIL = "HOT STAMPING ORO"
TEXTO_SELLO = "HECHO PARA MUJERES BRAVAS · BRAVISSIMA · "


# ───────────────────────── primitivas ─────────────────────────
def marca_d(texto, cx, cy, ancho):
    d, (x0, y0, x1, y1) = contorno(texto)
    s = ancho / (x1 - x0)
    return transformar(d, s, cx - s * (x0 + x1) / 2, cy - s * (y0 + y1) / 2)


def texto_d(clave, txt, size, x, y, tracking=0.0, align="center"):
    return Fuente(clave).path(txt, size, x, y, tracking=tracking, align=align)


def texto_circulo_d(clave, txt, r, tracking, inicio=0.0):
    d, size = Fuente(clave).circulo(txt, 0, 0, r, tracking=tracking, inicio=inicio)
    return d


class Sticker:
    def __init__(self, nombre, titulo, forma, fondo):
        self.nombre, self.titulo = nombre, titulo
        self.forma = forma  # ("c", r) o ("e", rx, ry)
        self.fondo = fondo
        self.ops = []  # (capa, tipo, datos, color)

    def trazo(self, d, color, capa="imp"):
        self.ops.append((capa, "d", d, color))
        return self

    def anillo(self, inset, ancho, color, capa="imp"):
        self.ops.append((capa, "anillo", (inset, ancho), color))
        return self

    @property
    def caja(self):
        f = self.forma
        return (f[1], f[1]) if f[0] == "c" else (f[1], f[2])

    @property
    def tiene_foil(self):
        return any(o[0] == "foil" for o in self.ops)


def _forma_svg(forma, extra=0.0, **attrs):
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    if forma[0] == "c":
        return f'<circle cx="0" cy="0" r="{forma[1] + extra:.3f}" {a}/>'
    return f'<ellipse cx="0" cy="0" rx="{forma[1] + extra:.3f}" ry="{forma[2] + extra:.3f}" {a}/>'


def sticker_svg(s, sangrado=True, troquel=True, cx=0.0, cy=0.0, aislado=True):
    """Fragmento (o documento) SVG en mm."""
    imp, foil = [], []
    for capa, tipo, datos, color in s.ops:
        dest = foil if capa == "foil" else imp
        if tipo == "d":
            dest.append(f'<path fill="{P[color]}" d="{datos}"/>')
        else:
            inset, ancho = datos
            dest.append(_forma_svg(s.forma, -inset, fill="none", stroke=P[color], stroke_width=f"{ancho:.3f}"))
    g = [f'<g transform="translate({cx:.3f} {cy:.3f})">']
    if sangrado:
        g.append(f'<g id="sangrado">{_forma_svg(s.forma, SANGRADO, fill=P[s.fondo])}</g>')
    else:
        g.append(f'<g id="fondo">{_forma_svg(s.forma, 0, fill=P[s.fondo])}</g>')
    g.append(f'<g id="impresion">{"".join(imp)}</g>')
    if foil:
        g.append(f'<g id="hot-stamping-oro">{"".join(foil)}</g>')
    if troquel:
        g.append(f'<g id="troquel">{_forma_svg(s.forma, 0, fill="none", stroke="#EC008C", stroke_width="0.1")}</g>')
    g.append("</g>")
    cuerpo = "".join(g)
    if not aislado:
        return cuerpo
    rx, ry = s.caja
    m = SANGRADO + 1 if sangrado else 0.2
    w, h = 2 * (rx + m), 2 * (ry + m)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}mm" height="{h:.2f}mm" '
            f'viewBox="{-rx - m:.3f} {-ry - m:.3f} {w:.3f} {h:.3f}"><title>bravissima — {s.titulo}</title>{cuerpo}</svg>')


# ───────────────────────── PDF CMYK ─────────────────────────
def _cmyk(clave):
    c, m_, y, k = K[clave]
    return CMYKColor(c / 100, m_ / 100, y / 100, k / 100)


def _sep_foil():
    c, m_, y, k = K["oro"]
    return CMYKColorSep(c / 100, m_ / 100, y / 100, k / 100, spotName=FOIL, density=1)


def _sep_troquel():
    return CMYKColorSep(0, 1, 0, 0, spotName="CutContour", density=1)


def _forma_rl(c, forma, extra, fill, stroke):
    if forma[0] == "c":
        c.circle(0, 0, forma[1] + extra, stroke=stroke, fill=fill)
    else:
        rx, ry = forma[1] + extra, forma[2] + extra
        c.ellipse(-rx, -ry, rx, ry, stroke=stroke, fill=fill)


def sticker_rl(c, s, cx, cy, solo_foil=False, troquel=True):
    """Dibuja el sticker centrado en (cx, cy) mm. El canvas debe estar en mm con Y hacia abajo."""
    c.saveState()
    c.translate(cx, cy)
    if not solo_foil:
        c.setFillColor(_cmyk(s.fondo))
        _forma_rl(c, s.forma, SANGRADO, 1, 0)
    for capa, tipo, datos, color in s.ops:
        if solo_foil and capa != "foil":
            continue
        if solo_foil:
            col = CMYKColor(0, 0, 0, 1)
        elif capa == "foil":
            col = _sep_foil()
            c.setFillOverprint(True)
            c.setStrokeOverprint(True)
        else:
            col = _cmyk(color)
        if tipo == "d":
            c.setFillColor(col)
            dibujar_rl(c, datos)
        else:
            inset, ancho = datos
            c.setStrokeColor(col)
            c.setLineWidth(ancho)
            _forma_rl(c, s.forma, -inset, 0, 1)
        c.setFillOverprint(False)
        c.setStrokeOverprint(False)
    if troquel and not solo_foil:
        c.setStrokeOverprint(True)
        c.setStrokeColor(_sep_troquel())
        c.setLineWidth(0.25 / mm * 0.3528 * mm / 1)  # 0.25 pt expresado en mm
        c.setLineWidth(0.088)
        _forma_rl(c, s.forma, 0, 0, 1)
        c.setStrokeOverprint(False)
    c.restoreState()


def marcas_corte(c, cx, cy, rx, ry, largo=3.0, sep=1.0):
    """Marcas de corte en las esquinas de la caja del troquel (registro: 100 % CMYK)."""
    c.saveState()
    c.setStrokeColor(CMYKColor(1, 1, 1, 1))
    c.setLineWidth(0.1)
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = cx + sx * rx, cy + sy * ry
            c.line(x + sx * sep, y, x + sx * (sep + largo), y)
            c.line(x, y + sy * sep, x, y + sy * (sep + largo))
    c.restoreState()


def nuevo_pdf(ruta, w, h, titulo):
    c = rlcanvas.Canvas(str(ruta), pagesize=(w * mm, h * mm))
    c.setTitle(f"bravissima — {titulo}")
    c.setAuthor("bravissima")
    c.translate(0, h * mm)
    c.scale(mm, -mm)
    return c


# ───────────────────────── diseños ─────────────────────────
def disenios():
    S = []
    # 1. círculo bordó Ø50 · isotipo oro (hot stamping)
    s = Sticker("01_circulo-bordo_isotipo-oro_50mm", "círculo bordó, isotipo oro", ("c", 25), "bordo")
    s.anillo(2.4, 0.3, "oro", "foil")
    s.trazo(marca_d("bss", 0, 0.4, 25), "oro", "foil")
    S.append(s)

    # 2. sello crema Ø50 · slogan en círculo
    s = Sticker("02_sello-crema_slogan_50mm", "sello crema, frase en círculo", ("c", 25), "crema")
    s.anillo(1.7, 0.45, "bordo").anillo(3.0, 0.22, "bordo").anillo(9.6, 0.22, "bordo")
    s.trazo(texto_circulo_d("corm500", TEXTO_SELLO, 17.55, 0.18), "bordo")
    s.trazo(marca_d("bss", 0, 0.3, 17.5), "bordo")
    S.append(s)

    # 3. círculo rosa Ø50 · logotipo vino
    s = Sticker("03_circulo-rosa_logo-vino_50mm", "círculo rosa, logotipo vino", ("c", 25), "rosa")
    s.trazo(marca_d("bravissima", 0, 0, 36.0), "vino")
    S.append(s)

    # 4. óvalo bordó 70×30 · slogan
    s = Sticker("04_ovalo-bordo_slogan_70x30mm", "óvalo bordó, slogan", ("e", 35, 15), "bordo")
    s.anillo(2.0, 0.22, "crema")
    tam = 50.0 / Fuente("cormi").ancho("hecho para mujeres bravas", 1.0)
    s.trazo(texto_d("cormi", "hecho para mujeres bravas", tam, 0, tam * 0.22), "crema")
    S.append(s)

    # 5. óvalo crema 70×30 · logo + hecho a mano en Córdoba
    s = Sticker("05_ovalo-crema_logo-cordoba_70x30mm", "óvalo crema, logo y hecho a mano en Córdoba", ("e", 35, 15), "crema")
    s.anillo(2.0, 0.22, "bordo")
    s.trazo(marca_d("bravissima", 0, -2.2, 38.0), "bordo")
    s.trazo(texto_d("corm500", "HECHO A MANO EN CÓRDOBA", 2.35, 0, 7.6, tracking=0.18), "bordo")
    S.append(s)

    # 6. círculo vino Ø50 · isotipo oro + "gracias, brava"
    s = Sticker("06_circulo-vino_gracias-brava_50mm", "círculo vino, isotipo oro y gracias, brava", ("c", 25), "vino")
    s.anillo(2.4, 0.3, "oro", "foil")
    s.trazo(marca_d("bss", 0, -3.4, 20.0), "oro", "foil")
    s.trazo(texto_d("cormi", "gracias, brava", 5.0, 0, 11.2), "oro", "foil")
    S.append(s)
    return S


# ───────────────────────── salida ─────────────────────────
def exportar():
    S = disenios()
    for sub in ("svg", "pdf", "png", "hot-stamping"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    for s in S:
        rx, ry = s.caja
        (OUT / "svg" / f"{s.nombre}.svg").write_text(sticker_svg(s), encoding="utf-8")
        # PDF de imprenta: sangrado + troquel + marcas
        m = SANGRADO + 6
        c = nuevo_pdf(OUT / "pdf" / f"{s.nombre}.pdf", 2 * (rx + m), 2 * (ry + m), s.titulo)
        sticker_rl(c, s, rx + m, ry + m)
        marcas_corte(c, rx + m, ry + m, rx, ry, largo=3, sep=SANGRADO + 0.5)
        c.showPage(); c.save()
        if s.tiene_foil:
            c = nuevo_pdf(OUT / "hot-stamping" / f"{s.nombre}_placa-foil.pdf", 2 * (rx + m), 2 * (ry + m), s.titulo + " — placa hot stamping")
            sticker_rl(c, s, rx + m, ry + m, solo_foil=True)
            marcas_corte(c, rx + m, ry + m, rx, ry, largo=3, sep=SANGRADO + 0.5)
            c.showPage(); c.save()
        # vista previa: solo la forma troquelada
        prev = sticker_svg(s, sangrado=False, troquel=False)
        cairosvg.svg2png(bytestring=prev.encode(), write_to=str(OUT / "png" / f"{s.nombre}.png"),
                         output_width=1200 if rx >= ry else None, output_height=None if rx >= ry else 1200)
    planilla(S)
    return S


# Planilla A4 · 9 círculos de Ø50 + 4 óvalos de 70×30
POSICIONES = [
    (0, 45, 45), (1, 105, 45), (2, 165, 45),
    (5, 45, 105), (0, 105, 105), (1, 165, 105),
    (2, 45, 165), (5, 105, 165), (0, 165, 165),
    (3, 60, 216), (4, 150, 216),
    (4, 60, 256), (3, 150, 256),
]


def planilla(S):
    W, H = 210, 297
    c = nuevo_pdf(OUT / "bravissima_planilla-stickers_A4.pdf", W, H, "planilla de stickers A4")
    for i, x, y in POSICIONES:
        sticker_rl(c, S[i], x, y)
    for i, x, y in POSICIONES:
        rx, ry = S[i].caja
        marcas_corte(c, x, y, rx, ry, largo=2.5, sep=1.0)
    # rótulo técnico (fuera de la zona de stickers)
    c.setFillColor(CMYKColor(0, 0, 0, 0.8))
    corm = Fuente("corm500")
    for txt, y in (("BRAVISSIMA · PLANILLA DE STICKERS · A4 · SANGRADO 2 MM · TROQUEL: CUTCONTOUR · FOIL: HOT STAMPING ORO", 9.5),):
        dibujar_rl(c, corm.path(txt, 2.2, W / 2, y, tracking=0.18, align="center"))
    c.showPage()
    c.save()

    # versión SVG + PNG 300 dpi
    frag = "".join(sticker_svg(S[i], cx=x, cy=y, aislado=False) for i, x, y in POSICIONES)
    marcas = []
    for i, x, y in POSICIONES:
        rx, ry = S[i].caja
        for sx in (-1, 1):
            for sy in (-1, 1):
                X, Y = x + sx * rx, y + sy * ry
                marcas.append(f'<line x1="{X + sx:.2f}" y1="{Y}" x2="{X + sx * 3.5:.2f}" y2="{Y}"/>'
                              f'<line x1="{X}" y1="{Y + sy:.2f}" x2="{X}" y2="{Y + sy * 3.5:.2f}"/>')
    rot = Fuente("corm500").path("BRAVISSIMA · PLANILLA DE STICKERS · A4 · SANGRADO 2 MM · TROQUEL: CUTCONTOUR · FOIL: HOT STAMPING ORO",
                                 2.2, W / 2, 9.5, tracking=0.18, align="center")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">'
           f'<rect width="210" height="297" fill="#fff"/>{frag}'
           f'<g id="marcas-de-corte" stroke="#000" stroke-width="0.1">{"".join(marcas)}</g>'
           f'<path fill="#333" d="{rot}"/></svg>')
    (OUT / "bravissima_planilla-stickers_A4.svg").write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(OUT / "bravissima_planilla-stickers_A4_300dpi.png"),
                     output_width=2480, output_height=3508)


if __name__ == "__main__":
    exportar()
    print("ok")
