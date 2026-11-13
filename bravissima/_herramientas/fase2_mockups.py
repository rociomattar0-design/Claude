"""FASE 2 — Mockups fotorrealistas (mapas de altura + luz)."""
import sys

import numpy as np

from marca import PALETA as P, RAIZ
from render import (Escena, blur, col, colocar, cinta, fbm, mono, papel, relieve, ruido, suave,
                    svg_alfa, tejido, F32)
from tipo import Fuente, marca, sello

OUT = RAIZ / "02_mockups"
OUT.mkdir(exist_ok=True)

# Modo "vacío": las mismas escenas sin la marca (sin logo, textos ni sello).
# Sirven de fondo para los mockups editables en Canva.
VACIO = False


def arte(cuerpo, w, h):
    """Máscara del arte de marca; en modo vacío no se imprime nada."""
    return np.zeros((h, w), F32) if VACIO else svg_alfa(cuerpo, w, h)
BL = "#fff"


def tinta(A, m, hexc, base_hex, opac=0.94):
    """Imprime tinta (multiplicativa) sobre un albedo."""
    filtro = np.clip(col(hexc) / col(base_hex), 0, 1)
    k = (m * opac)[..., None]
    return A * (1 - k) + A * filtro * k


# 1 ─────────────── relieve seco sobre papel crema
def m1():
    W, H = 3000, 2000
    A, Hp = papel(H, W, P["crema"], seed=11)
    m = arte(marca("bravissima", W / 2, H / 2, ancho=1500, fill=BL), W, H)
    E = Escena(A, Hp + relieve(m, 17, 5.5))
    E.revelar(OUT / "01_relieve-seco_logo_crema.png", exposicion=1.04, caida=0.24)


# 2 ─────────────── isotipo tono sobre tono en bordó
def m2():
    W, H = 2400, 2400
    A, Hp = papel(H, W, P["bordo"], seed=21, var=0.05)
    m = arte(marca("bss", W / 2, H / 2, ancho=1000, fill=BL), W, H)
    E = Escena(A, Hp + relieve(m, 30, 7.5), brillo=0.006)
    E.revelar(OUT / "02_relieve-tono-sobre-tono_isotipo_bordo.png", exposicion=1.15, caida=0.26, ambiente=0.30)


# 3 ─────────────── foil oro viejo sobre vino
def m3():
    W, H = 3000, 2000
    A, Hp = papel(H, W, P["vino"], seed=31, var=0.05)
    m = arte(marca("bravissima", W / 2, H / 2, ancho=1500, fill=BL), W, H)
    deboss = -relieve(m, 9, 2.2)
    E = Escena(A, Hp * 0.8 + deboss, brillo=0.004)
    E.metal = np.clip(m * 1.02, 0, 1)
    E.revelar(OUT / "03_foil-oro-viejo_logo_vino.png", exposicion=1.15, caida=0.22, ambiente=0.32, oro=("#6A4E2A", "#C9A66A", "#F6E7BE"))


# 4 ─────────────── sello en tinta bordó sobre lienzo crudo
def m4():
    W, H = 2400, 2400
    A, Hc = tejido(H, W, "#D6C8AF", seed=41, periodo=11, var=0.07, pliegues=0.35, motas=1.0)
    m = arte(sello(W / 2, H / 2 + 20, 760, color=BL), W, H)
    # bordes irregulares + presión despareja + la tinta se queda en los hilos altos
    n_borde = fbm(H, W, 3.5, 2, 44)
    m2 = suave(0.30, 0.70, blur(m, 1.6) + 0.16 * n_borde)
    presion = suave(-1.6, 0.9, fbm(H, W, 900, 3, 45) + 0.35)
    hp = blur(Hc, 0.6) - blur(Hc, 9)
    hilos = suave(np.percentile(hp, 15), np.percentile(hp, 75), hp)
    cob = m2 * (0.72 + 0.28 * hilos) * (0.78 + 0.22 * presion) * 1.12
    cob = np.clip(cob * (1.08 + 0.12 * fbm(H, W, 6, 2, 46)), 0, 1)
    A = tinta(A, cob, P["bordo"], "#D2C4AA", opac=1.0)
    E = Escena(A, Hc)
    E.revelar(OUT / "04_sello-tinta-bordo_lienzo-crudo.png", exposicion=1.05, caida=0.24, ambiente=0.42)


# ─────────────── utilidades de objetos
def matriz(w, h, cx, cy, ang):
    import cv2
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    return M


def pt(M, x, y):
    return (M[0, 0] * x + M[0, 1] * y + M[0, 2], M[1, 0] * x + M[1, 1] * y + M[1, 2])


def warp(M, arrs, W, H):
    import cv2
    return [cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) for a in arrs]


def ojalillo(w, h, cx, cy, r_in, r_out):
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    anillo = suave(r_in - 1, r_in + 1, d) * (1 - suave(r_out - 1, r_out + 1, d))
    perfil = np.clip(np.sin(np.pi * np.clip((d - r_in) / (r_out - r_in), 0, 1)), 0, 1) ** 0.6 * 5.0
    agujero = 1 - suave(r_in - 1, r_in + 1, d)
    return anillo, perfil * anillo, agujero


def pieza_papel(w, h, hexc, seed, forma, var=0.035):
    """Cartón grueso: papel + biselado leve en el canto."""
    A, Hp = papel(h, w, hexc, seed, var=var)
    m = svg_alfa(forma, w, h)
    canto = blur(m, 1.4)
    return m, A, Hp * 0.8 + 1.2 * canto


def cintas_mono(E, W, H, centro, esc, hexc, ancho, ang=0.0, seed=0, z0=0.0):
    import math as _m
    c, s_ = _m.cos(_m.radians(-ang)), _m.sin(_m.radians(-ang))
    pzs = mono(W, H, (0, 0), esc, hexc, ancho, seed, rot=(c, s_, centro))
    for tipo, (a, A, Hc) in pzs:
        z, el = {"cola": (0.6, 3), "lazo": (1.4, 8), "nudo": (2.6, 4)}[tipo]
        E.capa(a, A, Hc, z=z0 + z, elev=el, sobre=True, raso=1.0, brillo=0.02, sombra=0.9)


# 5 ─────────────── etiquetas colgantes (estilo amri)
def etiqueta_frente(w, h, seed):
    r_h = 38
    hy = 118
    forma = f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="34" fill="#fff"/>'
    m, A, Hp = pieza_papel(w, h, P["crema"], seed, forma)
    corm, cormi, cormm = Fuente("corm"), Fuente("cormi"), Fuente("corm500")
    logo = arte(marca("bravissima", w / 2, 395, ancho=560, fill=BL), w, h)
    txt = [f'<path fill="#fff" d="{cormi.path("hecho para mujeres bravas", 40, w/2, 505, align="center")}"/>',
           f'<rect x="{w/2-170}" y="575" width="340" height="1.6" fill="#fff"/>']
    filas = [("PIEZA", 680), ("MATERIAL", 770), ("TERMINACIÓN", 860), ("PIEDRA", 950)]
    for lab, y in filas:
        txt.append(f'<path fill="#fff" d="{cormm.path(lab, 22, 108, y, tracking=0.18)}"/>')
        txt.append(f'<path fill="#fff" d="{cormi.path("[completar]", 32, w-108, y + 2, align="right")}"/>')
        txt.append(f'<rect x="108" y="{y+22}" width="{w-216}" height="1" fill="#fff" opacity=".55"/>')
    txt.append(f'<path fill="#fff" d="{cormm.path("HECHO A MANO EN CÓRDOBA", 21, w/2, h-150, tracking=0.18, align="center")}"/>')
    txt.append(f'<path fill="#fff" d="{cormm.path("ARGENTINA", 21, w/2, h-112, tracking=0.18, align="center")}"/>')
    tin = arte("".join(txt), w, h)
    A = tinta(A, np.clip(tin + logo, 0, 1), P["bordo"], P["crema"], opac=0.96)
    Hp = Hp + relieve(logo, 14, 4.0) - 0.15 * tin
    ani, hani, agu = ojalillo(w, h, w / 2, hy, r_h, r_h * 1.62)
    m = m * (1 - agu)
    return m, A, Hp + hani, ani, (w / 2, hy)


def etiqueta_dorso(w, h, seed):
    r_h = 38
    hy = 118
    forma = f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="34" fill="#fff"/>'
    m, A, Hp = pieza_papel(w, h, P["bordo"], seed, forma, var=0.05)
    cormi, cormm = Fuente("cormi"), Fuente("corm500")
    iso = arte(marca("bss", w / 2, 610, ancho=400, fill=BL), w, h)
    foil = arte(f'<path fill="#fff" d="{cormi.path("hecho para mujeres bravas", 46, w/2, 905, align="center")}"/>'
                    f'<rect x="{w/2-60}" y="980" width="120" height="1.8" fill="#fff"/>', w, h)
    crem = arte(f'<path fill="#fff" d="{cormm.path("MUJERES BRAVAS", 21, w/2, h-130, tracking=0.18, align="center")}"/>', w, h)
    A = A * (1 - crem[..., None] * 0.92) + col(P["crema"]) * 0.92 * crem[..., None]
    Hp = Hp + relieve(iso, 22, 6.0) - relieve(foil, 6, 1.2)
    ani, hani, agu = ojalillo(w, h, w / 2, hy, r_h, r_h * 1.62)
    m = m * (1 - agu)
    return m, A, Hp + hani, np.clip(ani + foil, 0, 1), (w / 2, hy)


def m5():
    W, H = 3200, 2400
    A, Hb = papel(H, W, P["casinegro"], 51, var=0.08, fibra=0.6)
    E = Escena(A, Hb * 0.7, brillo=0.004)
    w, h = 780, 1380
    piezas = [(etiqueta_frente, 1160, 1330, 5.5, P["bordo"], 1),
              (etiqueta_dorso, 2120, 1250, -7.0, P["crema"], 2)]
    for fn, cx, cy, ang, cinta_hex, sd in piezas:
        m, Ae, He, metal, (hx, hy) = fn(w, h, 500 + sd)
        M = matriz(w, h, cx, cy, ang)
        hxs, hys = pt(M, hx, hy)
        # tramo de cinta que pasa por DEBAJO de la etiqueta
        lado = -1 if sd == 1 else 1
        bajo = [(hxs - 40 * lado * 0.3, hys + 60), (hxs, hys), (hxs + 60 * lado, hys - 180), (hxs + 200 * lado, hys - 420), (hxs + 260 * lado, hys - 700), (hxs + 330 * lado, -120)]
        a, Ac, Hc = cinta(W, H, bajo, 44, cinta_hex, seed=sd * 7, muesca_fin=False)
        E.capa(a, Ac, Hc, z=0.6, elev=3, sobre=True, raso=1.0, brillo=0.02)
        mm, AA, HH, MT = warp(M, [m, Ae, He, metal], W, H)
        E.capa(mm, AA, HH, z=3.0, elev=5, metal=MT, brillo=0.025 if sd == 1 else 0.008)
        # tramo por ENCIMA, que cae al costado con corte en V
        sobre = [(hxs, hys), (hxs - 70 * lado, hys - 150), (hxs - 260 * lado, hys - 210), (hxs - 430 * lado, hys - 60),
                 (hxs - 480 * lado, hys + 260), (hxs - 440 * lado, hys + 560)]
        a, Ac, Hc = cinta(W, H, sobre, 44, cinta_hex, seed=sd * 7 + 3, muesca_fin=True)
        yy, xx = np.mgrid[0:H, 0:W].astype(F32)
        d = np.sqrt((xx - hxs) ** 2 + (yy - hys) ** 2)
        a = a * suave(30, 40, d)  # la cinta entra en el agujero
        E.A *= (0.55 + 0.45 * suave(20, 38, d))[..., None]  # sombra dentro del ojalillo
        E.capa(a, Ac, Hc, z=1.0, elev=5, sobre=True, raso=1.0, brillo=0.02)
    E.revelar(OUT / "05_etiquetas-colgantes_frente-y-dorso.png", exposicion=1.08, caida=0.28, vineta=0.38, ambiente=0.36)


# 6 ─────────────── kit influencers (estilo BOMI)
def tarjeta(w, h, hexc, tinta_hex, seed):
    forma = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="6" fill="#fff"/>'
    m, A, Hp = pieza_papel(w, h, hexc, seed, forma, var=0.03)
    cormi, cormm = Fuente("cormi"), Fuente("corm500")
    cx = w * 0.60
    logo = arte(marca("bravissima", cx, h * 0.40, ancho=w * 0.38, fill=BL), w, h)
    txt = arte(f'<path fill="#fff" d="{cormi.path("hecho para mujeres bravas", h * 0.058, cx, h * 0.565, align="center")}"/>'
                   f'<path fill="#fff" d="{cormm.path("@[usuario]", h * 0.036, cx, h * 0.87, tracking=0.12, align="center")}"/>', w, h)
    A = tinta(A, txt, tinta_hex, hexc, opac=0.95)
    Hp = Hp + relieve(logo, w * 0.012, 5.0) - 0.1 * txt
    return m, A, Hp


def sobre_bolsa(w, h, seed):
    forma = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="5" fill="#fff"/>'
    m, A, Hp = pieza_papel(w, h, P["bordo"], seed, forma, var=0.05)
    solapa = svg_alfa(f'<path fill="#fff" d="M2 2 H{w-2} L{w/2+60} {h*0.47} Q{w/2} {h*0.5} {w/2-60} {h*0.47} Z"/>', w, h)
    pliegue = svg_alfa(f'<rect x="0" y="0" width="{w}" height="10" fill="#fff"/>', w, h)
    return m, A, Hp - 0.8 * blur(pliegue, 3), solapa


def kit(E, W, H, cx, cy, ang, s, tarjeta_hex, tinta_hex, seed):
    ew, eh = int(1500 * s), int(1020 * s)
    m, A, Hs, sol = sobre_bolsa(ew, eh, seed)
    M = matriz(ew, eh, cx, cy, ang)
    mm, AA, HH = warp(M, [m, A, Hs], W, H)
    E.capa(mm, AA, HH, z=2.0, elev=4, brillo=0.01)
    (sm,) = warp(M, [sol * m], W, H)
    E.capa(sm, AA, HH, z=3.4, elev=2.2, brillo=0.01, sombra=0.8)
    tw, th = int(1200 * s), int(760 * s)
    m2, A2, H2 = tarjeta(tw, th, tarjeta_hex, tinta_hex, seed + 1)
    ox, oy = pt(M, ew / 2 + 30 * s, eh / 2 + 55 * s)
    M2 = matriz(tw, th, ox, oy, ang + 1.5)
    mm, AA, HH = warp(M2, [m2, A2, H2], W, H)
    E.capa(mm, AA, HH, z=5.5, elev=5, brillo=0.03)
    # cinta vertical que abraza el kit
    rx = 250 * s
    pts = [pt(M, rx + 4 * s * k, eh * t) for k, t in zip([0, 1, 0, -1, 0], [0.0, 0.25, 0.5, 0.75, 1.0])]
    a, Ac, Hc = cinta(W, H, pts, 72 * s, P["crema"], seed=seed + 5, muesca_fin=False, giro=0.08)
    E.capa(a, Ac, Hc, z=0.8, elev=2, sobre=True, raso=1.0, brillo=0.02, sombra=0.7)
    centro = pt(M, rx, eh * 0.40)
    cintas_mono(E, W, H, centro, 255 * s, P["crema"], 66 * s, ang=ang, seed=seed + 9)


def m6():
    W, H = 3200, 2400
    A, Hl = tejido(H, W, "#CDBFA9", seed=61, periodo=6.5, var=0.06, pliegues=0.25, motas=0.4)
    E = Escena(A, Hl, brillo=0.02)
    kit(E, W, H, 1050, 820, 7, 0.86, P["crema"], P["bordo"], 600)
    kit(E, W, H, 2130, 1580, -5, 0.86, P["rosa"], P["vino"], 700)
    E.revelar(OUT / "06a_kit-influencers_dos-kits_lino.png", exposicion=1.04, caida=0.26, vineta=0.3)

    W, H = 3000, 2400
    A, Hb = papel(H, W, P["casinegro"], 62, var=0.08, fibra=0.6)
    E = Escena(A, Hb * 0.7, brillo=0.004)
    kit(E, W, H, 1720, 1330, -6, 1.8, P["crema"], P["bordo"], 800)
    E.revelar(OUT / "06b_kit-influencers_detalle_fondo-oscuro.png", exposicion=1.1, caida=0.3, vineta=0.42, ambiente=0.34)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--vacio" in args:
        args.remove("--vacio")
        VACIO = True
        OUT = RAIZ / "02_mockups" / "editable_canva" / "_fondos_png"
        OUT.mkdir(parents=True, exist_ok=True)
    for nombre in args or ["m1", "m2", "m3", "m4", "m5", "m6"]:
        print("render", nombre, flush=True)
        globals()[nombre]()
