"""Hoja de vista previa de la Fase 1."""
from marca import PALETA, RAIZ, svg, contorno, alto_b, UPM
F = RAIZ / "_fuentes"
logo = lambda c: svg("bravissima", c, pad=6)[0]
iso = lambda c: svg("bss", c, pad=6)[0]
celdas = [("bordo", "crema", "Bordó #5E1A24 · principal"), ("crema", "bordo", "Crema #EFE7DD · sobre bordó"),
          ("vino", "rosa", "Vino #3A0F16 · sobre rosa"), ("negro", "#FFFFFF", "Negro 100 % · cliché relieve / hot stamping")]
def bg(k): return PALETA.get(k, k)
cards = "".join(f'''<div class="card" style="background:{bg(f)}"><div class="l">{logo(PALETA[c])}</div>
<div class="i">{iso(PALETA[c])}</div><p style="color:{PALETA['crema'] if f=='bordo' else PALETA['casinegro']}">{t}</p></div>''' for c, f, t in celdas)
# detalle de construcción de la ss
d, (x0, y0, x1, y1) = contorno("bss")
hb = alto_b()
det = f'''<svg viewBox="{x0-hb*1.08:.0f} {y0-hb*1.08:.0f} {x1-x0+hb*2.16:.0f} {y1-y0+hb*2.16:.0f}">
<rect x="{x0-hb:.0f}" y="{y0-hb:.0f}" width="{x1-x0+2*hb:.0f}" height="{y1-y0+2*hb:.0f}" fill="none"/>
<rect x="{x0-hb:.0f}" y="{y0-hb:.0f}" width="{x1-x0+2*hb:.0f}" height="{y1-y0+2*hb:.0f}" fill="none" stroke="#B8955A" stroke-width="10" stroke-dasharray="40 26"/>
<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" fill="none" stroke="#D9B8AE" stroke-width="7"/>
<line x1="{x0-hb:.0f}" x2="{x1+hb:.0f}" y1="0" y2="0" stroke="#D9B8AE" stroke-width="7"/>
<line x1="{x0-hb:.0f}" x2="{x1+hb:.0f}" y1="-500" y2="-500" stroke="#D9B8AE" stroke-width="7"/>
<path d="{d}" fill="#5E1A24"/></svg>'''
html = f'''<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:Corm;src:url("{F}/CormorantGaramond[wght].ttf")}}
@font-face{{font-family:CormI;src:url("{F}/CormorantGaramond-Italic[wght].ttf")}}
body{{margin:0;background:#EFE7DD;font-family:Corm;color:#150B0D;width:1600px;font-variant-numeric:lining-nums}}
header{{padding:70px 80px 30px;display:flex;justify-content:space-between;align-items:end}}
h1{{font-weight:400;font-size:20px;letter-spacing:.18em;text-transform:uppercase;margin:0}}
.sl{{font-family:CormI;font-size:26px;color:#5E1A24}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:0 80px}}
.card{{height:360px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:40px;position:relative}}
.card .l svg{{width:420px;height:auto;display:block}} .card .i svg{{height:72px;width:auto;display:block}}
.card p{{position:absolute;bottom:14px;left:22px;margin:0;font-size:14px;letter-spacing:.18em;text-transform:uppercase}}
.det{{margin:24px 80px 80px;display:grid;grid-template-columns:1.3fr 1fr;gap:24px}}
.det .a{{background:#fff;padding:20px;display:flex;align-items:center;justify-content:center}} .det .a svg{{width:100%;height:400px}}
.det .b{{padding:10px 20px;font-size:19px;line-height:1.5}} .det .b b{{font-weight:600;letter-spacing:.18em;text-transform:uppercase;font-size:14px}}
</style><header><h1>Bravissima · Fase 1 · Logotipo e isotipo</h1><span class="sl">hecho para mujeres bravas</span></header>
<div class="grid">{cards}</div>
<div class="det"><div class="a">{det}</div><div class="b">
<p><b>Construcción</b><br>Kalnia Light 300, texto convertido a contornos. Primera <i>s</i> con tracking −0.14 em: las dos s se tocan y se unen en una sola forma (unión booleana, sin solapes). Resto de la palabra −0.01 em.</p>
<p><b>Área de seguridad</b> <span style="color:#B8955A">(línea punteada)</span><br>Igual al alto de la «b» ({hb:.0f} u.) alrededor del isotipo y del logotipo.</p>
<p><b>Tamaño mínimo</b><br>Logotipo 30 mm / 140 px · Isotipo 8 mm / 40 px.</p></div></div>'''
(RAIZ / "_herramientas" / "_tmp_preview1.html").write_text(html, encoding="utf-8")
