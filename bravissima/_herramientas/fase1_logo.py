"""FASE 1 — Logotipo e isotipo en vector (SVG, PDF, PNG 1000/3000 px)."""
import cairosvg

from marca import PALETA, RAIZ, svg

SALIDA = RAIZ / "01_logo"
PIEZAS = {"logotipo": "bravissima", "isotipo": "bss"}
VERSIONES = ["bordo", "crema", "vino", "negro"]
PAD = 6  # unidades de fuente: margen mínimo para que el antialias no se corte

for sub in ("svg", "pdf", "png"):
    (SALIDA / sub).mkdir(parents=True, exist_ok=True)

for pieza, texto in PIEZAS.items():
    for v in VERSIONES:
        nombre = f"bravissima_{pieza}_{v}"
        s, (w, h) = svg(texto, PALETA[v], pad=PAD, titulo=f"bravissima — {pieza}")
        (SALIDA / "svg" / f"{nombre}.svg").write_text(s, encoding="utf-8")
        # PDF vectorial a escala real de diseño: 1 unidad = 0.05 pt (logotipo ≈ 60 mm)
        cairosvg.svg2pdf(bytestring=s.encode(), write_to=str(SALIDA / "pdf" / f"{nombre}.pdf"), scale=0.05 * 4 / 3)
        for px in (1000, 3000):
            kw = {"output_width": px} if w >= h else {"output_height": px}
            cairosvg.svg2png(bytestring=s.encode(), write_to=str(SALIDA / "png" / f"{nombre}_{px}px.png"), **kw)
        print("ok", nombre, f"{w:.0f}x{h:.0f}")
