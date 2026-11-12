"""Hoja de vista previa de la Fase 3."""
import glob

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from marca import RAIZ

D = RAIZ / "03_stickers"
F = str(RAIZ / "_fuentes") + "/"
W, H = 2400, 2330
bg, cn, ink = (0xEF, 0xE7, 0xDD), (0x15, 0x0B, 0x0D), (0x5E, 0x1A, 0x24)
pl = Image.open(D / "bravissima_planilla-stickers_A4_300dpi.png").convert("RGB")
ph = 1560
plw = int(pl.width * ph / pl.height)
pl = pl.resize((plw, ph), Image.LANCZOS)
c = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(c)
f1 = ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 26)
f2 = ImageFont.truetype(F + "CormorantGaramond-Italic400.ttf", 40)
f3 = ImageFont.truetype(F + "CormorantGaramond-Medium500.ttf", 19)


def track(xy, t, f, fill, tr=0.18):
    x, y = xy
    for ch in t:
        d.text((x, y), ch, font=f, fill=fill, features=["lnum"])
        x += d.textlength(ch, font=f, features=["lnum"]) + tr * f.size


track((60, 80), "BRAVISSIMA · FASE 3 · STICKERS · CARDO + LLAMA", f1, cn)
tw = d.textlength("hecho para mujeres bravas", font=f2)
d.text((W - 60 - tw, 66), "hecho para mujeres bravas", font=f2, fill=ink)
sh = Image.new("L", (plw + 80, ph + 80), 0)
ImageDraw.Draw(sh).rectangle((40, 40, 40 + plw, 40 + ph), fill=90)
sh = sh.filter(ImageFilter.GaussianBlur(18))
c.paste((120, 100, 95), (30, 144), sh)
c.paste(pl, (60, 170))
labels = ["01 · BORDÓ · CARDO EN FOIL", "02 · SELLO · BSS", "03 · ROSA · CARDO + LOGO", "04 · ÓVALO · LLAMA + SLOGAN",
          "05 · ÓVALO · CARDO + LOGO", "06 · VINO · LLAMA EN FOIL", "07 · SELLO · CARDO", "08 · VINO · CARDO ROSA"]
x0 = 60 + plw + 80
cw = (W - x0 - 60) // 2
alto = 520
for k, f in enumerate(sorted(glob.glob(str(D / "png" / "*.png")))):
    im = Image.open(f).convert("RGBA")
    im.thumbnail((cw - 70, 420), Image.LANCZOS)
    col, row = k % 2, k // 2
    x = x0 + col * cw + (cw - im.width) // 2
    y = 190 + row * alto + (420 - im.height) // 2
    a = im.split()[3].filter(ImageFilter.GaussianBlur(10))
    s = Image.new("RGBA", im.size, (60, 30, 30, 0))
    s.putalpha(a.point(lambda v: int(v * 0.35)))
    c.paste(s, (x + 6, y + 10), s)
    c.paste(im, (x, y), im)
    track((x0 + col * cw + 30, 190 + row * alto + 440), labels[k], f3, cn)
# sistema de símbolos al pie de la planilla
y = 170 + ph + 90
track((60, y), "SISTEMA DE SÍMBOLOS", f3, cn)
items = [("emblema-cardo", "CARDO · EMBLEMA PRINCIPAL"), ("simbolo-llama", "LLAMA · SÍMBOLO SECUNDARIO")]
x = 60
for base, lab in items:
    im = Image.open(RAIZ / "01_logo" / "simbolos" / "png" / f"bravissima_{base}_bordo_1000px.png").convert("RGBA")
    im.thumbnail((360, 300), Image.LANCZOS)
    c.paste(im, (x + (360 - im.width) // 2, y + 60), im)
    track((x, y + 392), lab, f3, cn)
    x += 470
c.save(D / "_vista_previa_fase3.jpg", quality=90)
