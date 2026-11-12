"""
Bravissima — propuestas de símbolo (emblema).
Cada símbolo se construye con geometría propia (círculos, curvas y trazos de
grosor variable) y se une en un solo contorno. Comparten el ADN de Kalnia:
contraste grueso/fino y terminales en gota.
Coordenadas: caja ~1000 u., centro (0,0), eje Y hacia abajo.
"""
import math

import numpy as np
import pathops
from fontTools.pens.svgPathPen import SVGPathPen

from vector import transformar

K = 0.5522847498


def _circ(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo((cx + rx, cy))
    pen.curveTo((cx + rx, cy + K * ry), (cx + K * rx, cy + ry), (cx, cy + ry))
    pen.curveTo((cx - K * rx, cy + ry), (cx - rx, cy + K * ry), (cx - rx, cy))
    pen.curveTo((cx - rx, cy - K * ry), (cx - K * rx, cy - ry), (cx, cy - ry))
    pen.curveTo((cx + K * rx, cy - ry), (cx + rx, cy - K * ry), (cx + rx, cy))
    pen.closePath()
    return p


def _poly(pts):
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo(pts[0])
    for q in pts[1:]:
        pen.lineTo(q)
    pen.closePath()
    return p


def _bez(cmds):
    p = pathops.Path()
    pen = p.getPen()
    for c in cmds:
        if c[0] == "M":
            pen.moveTo(c[1])
        elif c[0] == "L":
            pen.lineTo(c[1])
        elif c[0] == "C":
            pen.curveTo(c[1], c[2], c[3])
        else:
            pen.closePath()
    return p


def _spline(puntos, paso=4.0):
    P = np.array(puntos, float)
    P = np.vstack([P[0] * 2 - P[1], P, P[-1] * 2 - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(2, int(np.linalg.norm(p2 - p1) / paso))
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out)


def _trazo(puntos, perfil):
    """Trazo de grosor variable. perfil = [(t, ancho), ...] con t en 0..1 del largo."""
    c = _spline(puntos)
    t = np.gradient(c, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-9
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
    s /= s[-1]
    pt, pw = zip(*perfil)
    # interpolación suave del grosor
    w = np.interp(s, pt, pw)
    k = np.ones(15) / 15
    w = np.convolve(np.pad(w, 7, mode="edge"), k, mode="valid")
    L, R = c + n * w[:, None] / 2, c - n * w[:, None] / 2
    return _poly([tuple(q) for q in L] + [tuple(q) for q in R[::-1]])


def U(*ps):
    r = pathops.Path()
    for p in ps:
        r = pathops.op(r, p, pathops.PathOp.UNION, fix_winding=True)
    return r


def D(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE, fix_winding=True)


def _rot(p, ang, cx=0.0, cy=0.0):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    q = pathops.Path()
    pen = q.getPen()
    from fontTools.pens.transformPen import TransformPen
    p.draw(TransformPen(pen, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy)))
    return q


# ───────────────────────── A · la brava (mujer + joya) ─────────────────────────
def la_brava():
    """El símbolo de Venus leído como un aro con colgante: mujer y joya en un mismo signo."""
    aro = D(_circ(0, -215, 250), _circ(0, -215, 186, 229))
    tallo = _poly([(-11, 25), (11, 25), (11, 330), (-11, 330)])
    cruz = U(_poly([(-150, 159), (150, 159), (150, 181), (-150, 181)]), _circ(-158, 170, 31), _circ(158, 170, 31))
    gota = _bez([("M", (0, 290)), ("C", (26, 352), (66, 392), (66, 436)), ("C", (66, 474), (36, 500), (0, 500)),
                 ("C", (-36, 500), (-66, 474), (-66, 436)), ("C", (-66, 392), (-26, 352), (0, 290)), ("Z",)])
    return U(aro, tallo, cruz, gota)


# ───────────────────────── B · la serpiente (fuerza, renacer, la S) ─────────────────────────
def serpiente():
    """Una serpiente que dibuja la S de bravissima: poder, renacer y un clásico de la joyería."""
    pts = [(196, -352), (120, -438), (-10, -474), (-140, -436), (-226, -322), (-196, -182), (-50, -72),
           (120, 24), (236, 160), (226, 318), (104, 436), (-60, 462), (-196, 404), (-268, 286), (-236, 176), (-150, 150)]
    perfil = [(0.0, 34), (0.06, 40), (0.16, 60), (0.34, 104), (0.50, 118), (0.66, 96), (0.80, 58),
              (0.90, 30), (0.97, 14), (1.0, 6)]
    cuerpo = _trazo(pts, perfil)
    # cabeza en gota, mirando hacia abajo
    cabeza = _bez([("M", (0, -70)), ("C", (34, -62), (52, -30), (50, 6)), ("C", (48, 44), (22, 74), (0, 92)),
                   ("C", (-22, 74), (-48, 44), (-50, 6)), ("C", (-52, -30), (-34, -62), (0, -70)), ("Z",)])
    cabeza = _rot(cabeza, -38)
    from fontTools.pens.transformPen import TransformPen
    q = pathops.Path(); cabeza.draw(TransformPen(q.getPen(), (1, 0, 0, 1, 222, -322)))
    lengua = U(_trazo([(262, -262), (284, -226), (300, -196)], [(0, 9), (1, 3)]),
               _trazo([(262, -262), (270, -222), (272, -190)], [(0, 9), (1, 3)]))
    ojo = _circ(216, -330, 9)
    return D(U(cuerpo, q, lengua), ojo)


# ───────────────────────── C · la llama (fuego interior + gema) ─────────────────────────
def llama():
    """Una llama con una gota adentro: el fuego de adentro y la piedra de la joya."""
    def forma(pen_T=None):
        return [("M", (10, 490)),
                ("C", (-200, 490), (-330, 350), (-300, 140)),
                ("C", (-276, -30), (-110, -110), (-150, -330)),
                ("C", (-80, -290), (-30, -230), (-10, -150)),
                ("C", (30, -260), (40, -390), (-20, -500)),
                ("C", (140, -400), (280, -180), (305, 80)),
                ("C", (330, 320), (200, 490), (10, 490)),
                ("Z",)]
    fuera = _bez(forma())
    from fontTools.pens.transformPen import TransformPen
    dentro = pathops.Path()
    k, ox, oy = 0.76, 110, 215
    fuera.draw(TransformPen(dentro.getPen(), (k, 0, 0, k, ox * (1 - k), oy * (1 - k))))
    gota = _bez([("M", (60, 150)), ("C", (92, 232), (150, 272), (150, 338)), ("C", (150, 392), (110, 428), (60, 428)),
                 ("C", (10, 428), (-30, 392), (-30, 338)), ("C", (-30, 272), (28, 232), (60, 150)), ("Z",)])
    return U(D(fuera, dentro), gota)


# ───────────────────────── D · el cardo (la flor brava) ─────────────────────────
def cardo():
    """La flor del cardo: crece sola en las sierras, es hermosa y no se deja arrancar."""
    partes = []
    n = 13
    for i in range(n):
        a = -66 + 132 * i / (n - 1)
        largo = 415 - 80 * abs(a) / 66 - (38 if i % 2 else 0)
        rayo = _poly([(-12, -40), (0, -40 - largo), (12, -40)])
        partes.append(_rot(rayo, a, 0, 10))
    bulbo = _bez([("M", (-150, -10)), ("C", (-90, -52), (90, -52), (150, -10)), ("C", (190, 90), (120, 240), (0, 252)),
                  ("C", (-120, 240), (-190, 90), (-150, -10)), ("Z",)])
    # escamas: cortes finos en diagonal
    cortes = []
    for k in (-1, 1):
        for off in (-70, 10, 90):
            cortes.append(_rot(_poly([(-260, off - 5), (260, off - 5), (260, off + 5), (-260, off + 5)]), 38 * k, 0, 100))
    bulbo = D(bulbo, U(*cortes))
    tallo = _poly([(-11, 240), (11, 240), (11, 500), (-11, 500)])
    hoja = _bez([("M", (0, 462)), ("C", (-74, 448), (-160, 394), (-222, 306)), ("C", (-136, 344), (-52, 384), (0, 414)), ("Z",)])
    hoja2 = _bez([("M", (0, 392)), ("C", (62, 382), (136, 336), (186, 262)), ("C", (114, 292), (44, 326), (0, 352)), ("Z",)])
    return U(*partes, bulbo, tallo, hoja, hoja2)


SIMBOLOS = {
    "la-brava": (la_brava, "LA BRAVA", "mujer + joya"),
    "serpiente": (serpiente, "LA SERPIENTE", "fuerza y renacer"),
    "llama": (llama, "LA LLAMA", "fuego interior"),
    "cardo": (cardo, "EL CARDO", "la flor brava"),
}
_cache = {}


def contorno_simbolo(nombre):
    if nombre not in _cache:
        p = SIMBOLOS[nombre][0]()
        p.simplify(fix_winding=True)
        pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        p.draw(pen)
        _cache[nombre] = (pen.getCommands(), p.bounds)
    return _cache[nombre]


def simbolo_d(nombre, cx, cy, alto=None, ancho=None):
    """Trazado del símbolo centrado en (cx, cy), escalado por alto o ancho."""
    d, (x0, y0, x1, y1) = contorno_simbolo(nombre)
    s = alto / (y1 - y0) if alto else ancho / (x1 - x0)
    return transformar(d, s, cx - s * (x0 + x1) / 2, cy - s * (y0 + y1) / 2)


def simbolo_caja(nombre, alto):
    _, (x0, y0, x1, y1) = contorno_simbolo(nombre)
    s = alto / (y1 - y0)
    return (x1 - x0) * s, alto
