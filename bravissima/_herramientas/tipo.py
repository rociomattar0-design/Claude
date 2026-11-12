"""
Bravissima — tipografía a contornos.
Convierte cualquier texto (Kalnia / Cormorant Garamond) a trazados SVG,
con tracking, alineación y texto en círculo. Así ningún archivo final
depende de tener las fuentes instaladas.
"""
import math
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from marca import RAIZ, contorno

FUENTES_DIR = RAIZ / "_fuentes"

_ESTATICAS = {
    "kalnia": ("Kalnia[wdth,wght].ttf", {"wght": 300, "wdth": 100}, "Kalnia-Light300.ttf"),
    "corm": ("CormorantGaramond[wght].ttf", {"wght": 400}, "CormorantGaramond-Regular400.ttf"),
    "corm500": ("CormorantGaramond[wght].ttf", {"wght": 500}, "CormorantGaramond-Medium500.ttf"),
    "corm600": ("CormorantGaramond[wght].ttf", {"wght": 600}, "CormorantGaramond-SemiBold600.ttf"),
    "cormi": ("CormorantGaramond-Italic[wght].ttf", {"wght": 400}, "CormorantGaramond-Italic400.ttf"),
    "cormi300": ("CormorantGaramond-Italic[wght].ttf", {"wght": 300}, "CormorantGaramond-LightItalic300.ttf"),
}


def _ruta(clave):
    var, coords, est = _ESTATICAS[clave]
    p = FUENTES_DIR / est
    if not p.exists():
        instancer.instantiateVariableFont(TTFont(FUENTES_DIR / var), coords).save(p)
    return p


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Fuente:
    _cache = {}

    def __new__(cls, clave):
        if clave not in cls._cache:
            o = super().__new__(cls)
            p = _ruta(clave)
            o.tt = TTFont(p)
            o.gs = o.tt.getGlyphSet()
            o.order = o.tt.getGlyphOrder()
            o.upm = o.tt["head"].unitsPerEm
            o.hb = hb.Font(hb.Face(hb.Blob.from_file_path(str(p))))
            o.cap = o.tt["OS/2"].sCapHeight
            o.xh = o.tt["OS/2"].sxHeight
            cls._cache[clave] = o
        return cls._cache[clave]

    def _shape(self, txt):
        buf = hb.Buffer()
        buf.add_str(txt)
        buf.guess_segment_properties()
        hb.shape(self.hb, buf, {"kern": True, "liga": True, "lnum": True})
        return [(self.order[i.codepoint], p.x_advance) for i, p in zip(buf.glyph_infos, buf.glyph_positions)]

    def ancho(self, txt, size, tracking=0.0):
        g = self._shape(txt)
        return (sum(a for _, a in g) + tracking * self.upm * (len(g) - 1)) * size / self.upm

    def path(self, txt, size, x=0.0, y=0.0, tracking=0.0, align="left"):
        """Trazado SVG del texto. (x, y) = punto de la línea de base según align."""
        s = size / self.upm
        w = self.ancho(txt, size, tracking)
        x0 = x - {"left": 0, "center": w / 2, "right": w}[align]
        pen = SVGPathPen(None, ntos=_fmt)
        cx = 0.0
        for nombre, adv in self._shape(txt):
            self.gs[nombre].draw(TransformPen(pen, (s, 0, 0, -s, x0 + cx * s, y)))
            cx += adv + tracking * self.upm
        return pen.getCommands()

    def circulo(self, txt, cx, cy, r, tracking=0.18, size=None, inicio=0.0, adentro=False):
        """Texto sobre un círculo (línea de base en radio r), leyendo en sentido horario.
        Si size es None, se calcula para que el texto cubra los 360° exactos."""
        g = self._shape(txt)
        unidades = sum(a for _, a in g) + tracking * self.upm * len(g)
        if size is None:
            size = 2 * math.pi * r * self.upm / unidades
        s = size / self.upm
        pen = SVGPathPen(None, ntos=_fmt)
        arco = 0.0
        for nombre, adv in g:
            mid = arco + adv * s / 2
            th = inicio + mid / r
            px, py = cx + r * math.sin(th), cy - r * math.cos(th)
            c, sn = math.cos(th), math.sin(th)
            # T(p) · R(th) · T(-adv/2, 0) · S(s, -s)
            a, b, cc, d = c * s, sn * s, sn * s, -c * s
            e = px + c * (-adv * s / 2)
            f = py + sn * (-adv * s / 2)
            self.gs[nombre].draw(TransformPen(pen, (a, b, cc, d, e, f)))
            arco += (adv + tracking * self.upm) * s
        return pen.getCommands(), size


def marca(texto, cx, cy, ancho=None, alto=None, fill="#000", extra=""):
    """Logotipo/isotipo centrado en (cx, cy), escalado por ancho o alto."""
    d, (x0, y0, x1, y1) = contorno(texto)
    s = ancho / (x1 - x0) if ancho else alto / (y1 - y0)
    tx = cx - s * (x0 + x1) / 2
    ty = cy - s * (y0 + y1) / 2
    return f'<path fill="{fill}" {extra} transform="translate({_fmt(tx)} {_fmt(ty)}) scale({s:.6f})" d="{d}"/>'


def marca_caja(texto, ancho=None, alto=None):
    d, (x0, y0, x1, y1) = contorno(texto)
    s = ancho / (x1 - x0) if ancho else alto / (y1 - y0)
    return (x1 - x0) * s, (y1 - y0) * s


def sello(cx, cy, R, color="#000", texto="HECHO PARA MUJERES BRAVAS · BRAVISSIMA · "):
    """Sello: isotipo en círculo doble con texto circular. R = radio exterior."""
    lw = R * 0.018
    corm = Fuente("corm500")
    r_txt = R * 0.755  # línea de base del texto
    d_txt, size = corm.circulo(texto, cx, cy, r_txt, tracking=0.18)
    partes = [
        f'<circle cx="{cx}" cy="{cy}" r="{R - lw / 2:.2f}" fill="none" stroke="{color}" stroke-width="{lw:.2f}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{R * 0.925:.2f}" fill="none" stroke="{color}" stroke-width="{lw * 0.6:.2f}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="{R * 0.66:.2f}" fill="none" stroke="{color}" stroke-width="{lw * 0.6:.2f}"/>',
        f'<path fill="{color}" d="{d_txt}"/>',
        marca("bss", cx, cy, ancho=R * 0.80, fill=color),
    ]
    return "".join(partes)
