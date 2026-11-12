"""
Bravissima — núcleo de marca.
Genera los contornos vectoriales del logotipo y del isotipo a partir de
Kalnia Light 300, aplicando el tracking de la marca:
  · primera "s" de la doble ss: -0.14em  (las dos s se funden)
  · resto de la palabra:          -0.01em
Los contornos se unen con una operación booleana (skia-pathops), así la
doble s queda como UNA sola forma, sin solapes internos.
"""
from pathlib import Path

import pathops
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RAIZ = Path(__file__).resolve().parents[1]
FUENTE = RAIZ / "_fuentes" / "Kalnia-Light300.ttf"

PALETA = {
    "bordo": "#5E1A24",
    "vino": "#3A0F16",
    "crema": "#EFE7DD",
    "rosa": "#D9B8AE",
    "oro": "#B8955A",
    "casinegro": "#150B0D",
    "negro": "#000000",  # solo archivos de producción (cliché / hot stamping)
}

TRACK_SS = -0.14
TRACK_RESTO = -0.01

_tt = TTFont(FUENTE)
_gs = _tt.getGlyphSet()
_order = _tt.getGlyphOrder()
UPM = _tt["head"].unitsPerEm
_hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(str(FUENTE))))


def _tracking(texto):
    """Tracking (en em) a sumar después de cada carácter."""
    tr = [TRACK_RESTO] * len(texto)
    i = texto.find("ss")
    if i >= 0:
        tr[i] = TRACK_SS
    return tr


def contorno(texto):
    """Devuelve (path_d, bbox) en unidades de fuente, eje Y hacia abajo,
    con la línea de base en y=0 y el origen x=0 en el inicio del texto."""
    buf = hb.Buffer()
    buf.add_str(texto)
    buf.guess_segment_properties()
    hb.shape(_hbfont, buf, {"kern": True, "liga": False, "calt": False})
    track = _tracking(texto)
    union = pathops.Path()
    x = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        nombre = _order[info.codepoint]
        p = pathops.Path()
        # y invertida para coordenadas SVG
        _gs[nombre].draw(TransformPen(p.getPen(), (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)))
        union = pathops.op(union, p, pathops.PathOp.UNION, fix_winding=True)
        x += pos.x_advance + track[info.cluster] * UPM
    union.simplify(fix_winding=True)
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    union.draw(pen)
    return pen.getCommands(), union.bounds


def alto_b():
    """Alto de la 'b' (área de seguridad de la marca), en unidades de fuente."""
    p = pathops.Path()
    _gs["b"].draw(p.getPen())
    b = p.bounds
    return b[3] - b[1]


def svg(texto, color, pad=0.0, fondo=None, titulo=None):
    """SVG autónomo, con viewBox ajustado al contorno (+ pad en unidades)."""
    d, (x0, y0, x1, y1) = contorno(texto)
    x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
    w, h = x1 - x0, y1 - y0
    t = titulo or texto
    bg = f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fondo}"/>' if fondo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" '
        f'width="{w:.2f}" height="{h:.2f}" role="img" aria-label="{t}">'
        f"<title>{t}</title>{bg}<path fill=\"{color}\" d=\"{d}\"/></svg>"
    ), (w, h)
