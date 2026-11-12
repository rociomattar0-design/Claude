"""
Bravissima — motor de render para mockups.
Trabaja con mapas de altura y luz direccional en espacio lineal:
papel (fibra + grano), relieve seco, foil metálico, tinta, telas
(lienzo y lino), cintas de raso y sombras de contacto.
"""
import io
import math

import cairosvg
import cv2
import numpy as np
from PIL import Image

cv2.setNumThreads(4)
F32 = np.float32


# ───────────────────────── color ─────────────────────────
def srgb2lin(c):
    c = np.asarray(c, F32)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).astype(F32)


def lin2srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055).astype(F32)


def col(h):
    return srgb2lin([int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)])


# ───────────────────────── utilidades ─────────────────────────
def blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s) if s > 0 else a


def suave(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def svg_alfa(cuerpo, w, h):
    """Rasteriza un fragmento SVG (en px) y devuelve su canal alfa 0..1."""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{cuerpo}</svg>'
    png = cairosvg.svg2png(bytestring=svg.encode())
    return np.asarray(Image.open(io.BytesIO(png)).convert("RGBA"))[..., 3].astype(F32) / 255


def ruido(h, w, celda, seed):
    rng = np.random.default_rng(seed)
    celda = max(celda, 1.0)
    gh, gw = int(math.ceil(h / celda)) + 3, int(math.ceil(w / celda)) + 3
    g = rng.random((gh, gw), dtype=F32)
    big = cv2.resize(g, (int(gw * celda), int(gh * celda)), interpolation=cv2.INTER_CUBIC)
    o = int(celda)
    return big[o:o + h, o:o + w]


def fbm(h, w, celda, octavas=5, seed=0, gan=0.5):
    tot = np.zeros((h, w), F32)
    amp, s = 1.0, 0.0
    for o in range(octavas):
        tot += amp * ruido(h, w, celda / 2 ** o, seed * 31 + o)
        s += amp
        amp *= gan
    n = tot / s
    return (n - n.mean()) / (n.std() + 1e-6)


def fibras(h, w, n, largo, seed, grosor=1):
    rng = np.random.default_rng(seed)
    c = np.zeros((h, w), np.uint8)
    for _ in range(n):
        x, y = rng.uniform(0, w), rng.uniform(0, h)
        a = rng.uniform(0, math.pi)
        L = largo * rng.uniform(0.3, 1.2)
        curv = rng.normal(0, 0.5)
        pts = []
        for t in np.linspace(-0.5, 0.5, 6):
            aa = a + curv * t
            pts.append((x + math.cos(aa) * L * t, y + math.sin(aa) * L * t))
        cv2.polylines(c, [np.int32(np.array(pts) * 16)], False, int(rng.uniform(90, 255)), grosor, cv2.LINE_AA, 4)
    return c.astype(F32) / 255


def desplazar(a, dx, dy):
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(a, M, (a.shape[1], a.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


# ───────────────────────── materiales ─────────────────────────
def papel(h, w, hexc, seed, fibra=1.0, grano=1.0, nubes=1.0, var=0.035):
    """Papel de algodón: formación nubosa, grano fino y fibras."""
    nub = fbm(h, w, max(h, w) / 6, 6, seed)
    gr = fbm(h, w, 2.2, 2, seed + 7)
    fib = blur(fibras(h, w, int(h * w / 2500 * fibra), 26, seed + 3), 0.6)
    H = 0.55 * nubes * blur(nub, 2) + 0.075 * grano * gr + 0.30 * fib
    A = col(hexc)[None, None, :] * (1 + var * nub[..., None] * 0.6 + 0.008 * gr[..., None] + 0.035 * fib[..., None])
    return A.astype(F32), H.astype(F32)


def tejido(h, w, hexc, seed, periodo=9.0, var=0.06, pliegues=0.0, motas=0.0, irregular=1.0):
    """Tela de tafetán (lienzo / lino): urdimbre y trama que se cruzan."""
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    # el tejido nunca es perfectamente recto
    dx = fbm(h, w, 260, 3, seed + 1) * periodo * 0.55 * irregular
    dy = fbm(h, w, 260, 3, seed + 2) * periodo * 0.55 * irregular
    X, Y = xx + dx, yy + dy
    ix, iy = np.floor(X / periodo), np.floor(Y / periodo)
    fx, fy = X / periodo - ix, Y / periodo - iy
    rng = np.random.default_rng(seed)
    grosor_col = rng.uniform(0.75, 1.15, 4096).astype(F32)
    grosor_fil = rng.uniform(0.75, 1.15, 4096).astype(F32)
    tc = grosor_col[(ix.astype(int)) % 4096]
    tf = grosor_fil[(iy.astype(int)) % 4096]
    slub_v = 1 + 0.22 * fbm(h, w, 40, 2, seed + 5) * irregular
    perfil_v = np.clip(np.sin(np.pi * np.clip((fx - 0.5) / (0.92 * tc) + 0.5, 0, 1)), 0, 1) ** 0.7 * slub_v
    perfil_h = np.clip(np.sin(np.pi * np.clip((fy - 0.5) / (0.92 * tf) + 0.5, 0, 1)), 0, 1) ** 0.7
    arriba = ((ix + iy) % 2).astype(F32)
    ondula_v = 0.5 + 0.5 * np.cos(np.pi * (2 * fy - 1)) * (2 * arriba - 1)
    ondula_h = 0.5 - 0.5 * np.cos(np.pi * (2 * fx - 1)) * (2 * arriba - 1)
    hv = perfil_v * (0.55 + 0.45 * ondula_v)
    hh = perfil_h * (0.55 + 0.45 * ondula_h)
    H = np.maximum(hv, hh) * periodo * 0.16
    tono = np.where(hv > hh, tc, tf) - 0.95
    A = col(hexc)[None, None, :] * (1 + var * (tono[..., None] * 2.2 + 0.4 * fbm(h, w, 300, 3, seed + 9)[..., None]))
    A *= (0.86 + 0.14 * np.maximum(hv, hh))[..., None]
    if motas:
        m = (ruido(h, w, 2.2, seed + 13) > 1 - 0.0025 * motas).astype(F32)
        m = blur(cv2.dilate(m, np.ones((2, 5), np.uint8)), 0.8)
        A *= (1 - 0.45 * np.clip(m, 0, 1))[..., None]
    if pliegues:
        H = H + pliegues * blur(fbm(h, w, 700, 3, seed + 21), 30) * 40
    return A.astype(F32), H.astype(F32)


def relieve(m, escala, alto=1.0):
    """Perfil de relieve seco a partir de una máscara (0..1). escala ~ grosor de trazo en px."""
    return (alto * (0.72 * blur(m, escala * 0.11) + 0.28 * blur(m, escala * 0.38))).astype(F32)


# ───────────────────────── escena ─────────────────────────
class Escena:
    """Composición por capas: albedo lineal, altura (px), materiales y sombras."""

    def __init__(self, A, H, brillo=0.03):
        self.h, self.w = H.shape
        self.A = A.copy()
        self.H = H.copy()
        self.raso = np.zeros_like(H)
        self.metal = np.zeros_like(H)
        self.brillo = np.full_like(H, brillo)  # especular de papel / tela
        self.luz = np.array([-0.55, -0.72, 0.62], F32)

    def sombra(self, alfa, elev, fuerza=1.0):
        d = self.luz[:2] / np.linalg.norm(self.luz[:2])
        occ = np.zeros_like(alfa)
        for k_off, k_sig, k_op in ((0.45, 0.30, 0.45), (1.2, 1.0, 0.28), (3.0, 3.2, 0.22)):
            off = elev * k_off
            occ += k_op * desplazar(blur(alfa, max(0.7, elev * k_sig)), -d[0] * off, -d[1] * off)
        self.A *= np.clip(1 - fuerza * occ, 0, 1)[..., None]

    def capa(self, alfa, A, H, z=0.0, elev=None, sobre=False, raso=0.0, metal=None, brillo=0.03, sombra=1.0):
        """alfa: cobertura · A: albedo (h,w,3) · H: altura local · z: altura sobre la mesa.
        sobre=True apoya la capa sobre lo que ya hay (cintas que se adaptan)."""
        if sombra:
            self.sombra(alfa, elev if elev is not None else max(z, 2.0), sombra)
        base = blur(self.H, 7) if sobre else 0.0
        a3 = alfa[..., None]
        self.A = self.A * (1 - a3) + A * a3
        ah = suave(0.0, 1.0, blur(alfa, 3.0)) * alfa if sobre else alfa  # las telas apoyan el borde, el cartón no
        self.H = self.H * (1 - ah) + (base + z + H) * ah
        self.raso = self.raso * (1 - alfa) + raso * alfa
        self.metal = self.metal * (1 - alfa) + (metal if metal is not None else 0.0) * alfa
        self.brillo = self.brillo * (1 - alfa) + brillo * alfa

    def revelar(self, ruta, exposicion=1.0, caida=0.22, vineta=0.28, grano=0.012, ambiente=0.38,
                oro=("#5A4224", "#B8955A", "#F1DFB0"), calidez=(1.02, 1.0, 0.975), seed=1, escala_final=None):
        H = self.H.astype(F32)
        gy, gx = np.gradient(blur(H, 0.7))
        nx, ny = -gx, -gy
        inv = 1 / np.sqrt(nx * nx + ny * ny + 1)
        L = self.luz / np.linalg.norm(self.luz)
        ndl = np.clip((nx * L[0] + ny * L[1] + L[2]) * inv, 0, None)
        dif = ambiente + (1 - ambiente) * ndl / L[2]
        Hv = L + np.array([0, 0, 1], F32)
        Hv /= np.linalg.norm(Hv)
        ndh = np.clip((nx * Hv[0] + ny * Hv[1] + Hv[2]) * inv, 0, 1)
        flat = Hv[2]
        spec = self.brillo * ndh ** 10 / flat ** 10 * 0.6 + self.raso * (0.02 * ndh ** 8 + 0.16 * ndh ** 45)

        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(F32)
        u, v = xx / self.w, yy / self.h
        campo = 1.12 - caida * (0.62 * u + 0.38 * v) * 1.6
        r = np.sqrt(((u - 0.5) * 1.1) ** 2 + ((v - 0.5) * 1.1) ** 2)
        campo *= 1 - vineta * np.clip(r, 0, 1) ** 2.2

        img = self.A * dif[..., None] + spec[..., None] * np.array([1.0, 0.97, 0.92], F32)

        if self.metal.max() > 0:
            env = 0.5 + 0.30 * fbm(self.h, self.w, 520, 3, seed + 40) + 0.16 * np.sin((u * 3.1 + v * 1.7) * math.pi)
            t = np.clip(0.18 + 0.55 * env + 0.55 * (ndl / L[2] - 1) + 0.9 * ndh ** 30 - 0.35 * (1 - ndl / L[2]).clip(0), 0, 1)
            t = t + 0.035 * fbm(self.h, self.w, 1.4, 1, seed + 41)
            c0, c1, c2 = (col(x) for x in oro)
            t3 = np.clip(t, 0, 1)[..., None]
            met = np.where(t3 < 0.5, c0 + (c1 - c0) * (t3 / 0.5), c1 + (c2 - c1) * ((t3 - 0.5) / 0.5))
            met = met * 1.15 + (ndh ** 80)[..., None] * 0.55
            img = img * (1 - self.metal[..., None]) + met * self.metal[..., None]

        img *= campo[..., None] * exposicion * np.array(calidez, F32)
        out = lin2srgb(img)
        out += np.random.default_rng(seed).normal(0, grano, out.shape).astype(F32)
        out = np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8)
        im = Image.fromarray(out)
        if escala_final:
            im = im.resize(escala_final, Image.LANCZOS)
        im.save(ruta, optimize=True)
        return im


# ───────────────────────── objetos ─────────────────────────
def colocar(arrs, W, H, cx, cy, ang):
    """Lleva capas en espacio local (tamaño w×h) a la escena, rotadas `ang` grados."""
    h, w = arrs[0].shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, 1.0)
    M[0, 2] += cx - w / 2
    M[1, 2] += cy - h / 2
    return [cv2.warpAffine(a, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) for a in arrs]


def catmull(puntos, paso=1.5):
    P = np.array(puntos, F32)
    P = np.vstack([P[0] * 2 - P[1], P, P[-1] * 2 - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        n = max(2, int(np.linalg.norm(p2 - p1) / paso))
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2])
    return np.array(out, F32)


def cinta(W, H, puntos, ancho, hexc, seed=0, muesca_ini=False, muesca_fin=True, giro=0.25, ss=2, pellizco=(0.0, 0.0)):
    """Cinta de raso a lo largo de una curva. Devuelve (alfa, albedo, altura)."""
    c = catmull(puntos, 1.2) * ss
    t = np.gradient(c, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True) + 1e-6
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    largo = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c, axis=0), axis=1))])
    rng = np.random.default_rng(seed)
    fase = rng.uniform(0, 6.28)
    tw = 1 - giro * (0.5 - 0.5 * np.cos(largo / (ancho * ss * 7.5) + fase)) ** 3
    total = largo[-1]
    k = ancho * ss * 1.3
    tw = tw * (1 - pellizco[0] * np.exp(-(largo / k) ** 2) - pellizco[1] * np.exp(-((total - largo) / k) ** 2))
    wv = ancho * ss * tw / 2
    Lp, Rp = c + n * wv[:, None], c - n * wv[:, None]
    Ws, Hs = W * ss, H * ss
    m = np.zeros((Hs, Ws), np.uint8)
    umap = np.zeros((Hs, Ws), F32)
    for i in range(len(c) - 1):
        q = np.int32(np.array([Lp[i], Lp[i + 1], Rp[i + 1], Rp[i]]) * 4)
        cv2.fillConvexPoly(m, q, 255, cv2.LINE_8, 2)
        cv2.fillConvexPoly(umap, q, float(largo[i]), cv2.LINE_8, 2)

    def muesca(i, sgn):
        o = t[i] * sgn
        ex = 6 * ss
        tri = np.array([Lp[i] + n[i] * ex + o * ex, Rp[i] - n[i] * ex + o * ex, c[i] - o * ancho * ss * 0.6])
        cv2.fillConvexPoly(m, np.int32(tri * 4), 0, cv2.LINE_8, 2)

    if muesca_fin:
        muesca(len(c) - 1, 1)
    if muesca_ini:
        muesca(0, -1)
    a = cv2.resize(m.astype(F32) / 255, (W, H), interpolation=cv2.INTER_AREA)
    u = cv2.resize(umap, (W, H), interpolation=cv2.INTER_AREA) / ss / np.maximum(a, 1e-3)
    dt = cv2.distanceTransform((a > 0.5).astype(np.uint8), cv2.DIST_L2, 5)
    perfil = np.clip(dt / (ancho * 0.5), 0, 1)
    Hc = (0.25 * np.sqrt(perfil) + 0.75) * ancho * 0.04
    Hc += np.sin(u / (ancho * 3.2) + fase) * ancho * 0.035 * a
    Hc = blur(Hc, 1.0)
    pel = np.zeros_like(u)
    if pellizco[0] or pellizco[1]:
        kk = ancho * 1.3
        pel = pellizco[0] * np.exp(-(u / kk) ** 2) + pellizco[1] * np.exp(-((total / ss - u) / kk) ** 2)
    lin = (1 + 0.02 * np.sin(u / (ancho * 1.7) + fase)) * (1 - 0.35 * pel)
    A = col(hexc)[None, None, :] * lin[..., None]
    return a, A.astype(F32), Hc.astype(F32)


def mono(W, H, centro, esc, hexc, ancho, seed=0, rot=None):
    """Moño de raso: dos lazos, dos colas con corte en V y nudo. Devuelve lista de cintas (de abajo a arriba)."""
    cx, cy = centro
    if rot:
        c, s_, (ox, oy) = rot
        P = lambda x, y: (ox + (x * c - y * s_) * esc, oy + (x * s_ + y * c) * esc)
    else:
        P = lambda x, y: (cx + x * esc, cy + y * esc)
    colas = [
        [P(-0.03, 0.02), P(-0.16, 0.38), P(-0.30, 0.78), P(-0.36, 1.05)],
        [P(0.03, 0.02), P(0.18, 0.40), P(0.27, 0.80), P(0.42, 1.08)],
    ]
    lazos = [
        [P(-0.02, -0.02), P(-0.30, -0.27), P(-0.70, -0.36), P(-1.00, -0.24), P(-1.06, 0.02),
         P(-0.86, 0.22), P(-0.46, 0.20), P(-0.02, 0.03)],
        [P(0.02, -0.02), P(0.32, -0.29), P(0.72, -0.33), P(1.01, -0.20), P(1.05, 0.05),
         P(0.84, 0.24), P(0.44, 0.19), P(0.02, 0.03)],
    ]
    nudo = [P(-0.012, -0.10), P(0.0, 0.0), P(0.012, 0.10)]
    out = []
    for i, cc in enumerate(colas):
        out.append(("cola", cinta(W, H, cc, ancho, hexc, seed + i, muesca_fin=True, giro=0.3, pellizco=(0.55, 0.0))))
    for i, ll in enumerate(lazos):
        out.append(("lazo", cinta(W, H, ll, ancho, hexc, seed + 10 + i, muesca_fin=False, giro=0.2, pellizco=(0.6, 0.6))))
    out.append(("nudo", cinta(W, H, nudo, ancho * 0.95, hexc, seed + 20, muesca_fin=False, giro=0.0)))
    return out
