"""Hoja de vista previa de la Fase 4."""
from PIL import Image, ImageDraw, ImageFont

from marca import RAIZ

D = RAIZ / "04_redes" / "png"
F = str(RAIZ / "_fuentes") + "/"
W, H = 2600, 2130
bg, cn, ink = (0xEF, 0xE7, 0xDD), (0x15, 0x0B, 0x0D), (0x5E, 0x1A, 0x24)
c = Image.new("RGB", (W, H), (0xE4, 0xD9, 0xCC))
d = ImageDraw.Draw(c)
f1 = ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 26)
f2 = ImageFont.truetype(F + "CormorantGaramond-Italic400.ttf", 40)
f3 = ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 19)


def track(xy, t, f, fill, tr=0.18):
    x, y = xy
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill, features=["lnum"])
        x += d.textlength(ch, font=f, features=["lnum"]) + tr * f.size


def pega(nombre, x, y, w, rot=None):
    im = Image.open(D / f"{nombre}.png").convert("RGB")
    h = int(w * im.height / im.width)
    c.paste(im.resize((w, h), Image.LANCZOS), (x, y))
    return h


def circulo(nombre, x, y, diam, zona):
    im = Image.open(D / f"{nombre}.png").convert("RGB").crop(zona).resize((diam * 2, diam * 2), Image.LANCZOS)
    m = Image.new("L", (diam * 2, diam * 2), 0)
    ImageDraw.Draw(m).ellipse((0, 0, diam * 2 - 1, diam * 2 - 1), fill=255)
    im = im.resize((diam, diam), Image.LANCZOS)
    m = m.resize((diam, diam), Image.LANCZOS)
    c.paste(im, (x, y), m)


track((70, 80), "BRAVISSIMA · FASE 4 · REDES", f1, cn)
tw = d.textlength("hecho para mujeres bravas", font=f2)
d.text((W - 70 - tw, 66), "hecho para mujeres bravas", font=f2, fill=ink)
# posts
track((70, 160), "POSTS · 1080 × 1350", f3, cn)
for i, n in enumerate(["post_01_lanzamiento_03-12", "post_02_slogan", "post_03_plantilla-producto"]):
    pega(n, 70 + i * 560, 200, 530)
# stories
track((1770, 160), "STORIES · 1080 × 1920", f3, cn)
for i, n in enumerate(["story_01_lanzamiento_cuenta-regresiva", "story_02_mujeres-bravas_foto-clienta"]):
    pega(n, 1770 + i * 395, 200, 372)
# perfil + destacados, como se ven en Instagram
y0 = 1010
track((70, y0), "ASÍ SE VE EN EL PERFIL · FOTO DE PERFIL + DESTACADOS", f3, cn)
d.rounded_rectangle((70, y0 + 44, 1690, y0 + 44 + 300), radius=18, fill=(255, 255, 255))
circulo("perfil_isotipo-crema-sobre-bordo", 130, y0 + 90, 250, (0, 0, 1080, 1080))
fb = ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 34)
fi = ImageFont.truetype(F + "CormorantGaramond-Italic400.ttf", 30)
d.text((430, y0 + 130), "bravissima", font=fb, fill=cn)
d.text((430, y0 + 180), "Joyería de autor · Córdoba, Argentina", font=fi, fill=cn)
d.text((430, y0 + 220), "hecho para mujeres bravas", font=fi, fill=ink)
d.text((430, y0 + 260), "@[usuario] · [web]", font=fi, fill=(120, 110, 110))
for i, n in enumerate(["nuevo", "aros", "collares", "anillos", "cuidados"]):
    x = 880 + i * 158
    d.ellipse((x - 5, y0 + 135, x + 125, y0 + 265), outline=(200, 190, 185), width=2)
    circulo(f"destacado_{i + 1:02d}_{n}", x, y0 + 140, 120, (290, 680, 790, 1180))
    tw = d.textlength(n, font=ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 22))
    d.text((x + 60 - tw / 2, y0 + 280), n, font=ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 22), fill=cn)
# destacados completos
track((70, 1400), "PORTADAS DE DESTACADOS · 1080 × 1920", f3, cn)
for i, n in enumerate(["nuevo", "aros", "collares", "anillos", "cuidados"]):
    pega(f"destacado_{i + 1:02d}_{n}", 70 + i * 330, 1440, 310)
track((1770, 1400), "FOTO DE PERFIL · 1080 × 1080", f3, cn)
pega("perfil_isotipo-crema-sobre-bordo", 1770, 1440, 551)
c.save(RAIZ / "04_redes" / "_vista_previa_fase4.jpg", quality=90)
