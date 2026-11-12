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


# ── Símbolos de marca: cardo (emblema principal) y llama (símbolo secundario)
from simbolos import contorno_simbolo  # noqa: E402

SIMB = {"cardo": "emblema-cardo", "cardo-chico": "emblema-cardo_version-chica",
        "llama": "simbolo-llama", "llama-chica": "simbolo-llama_version-chica"}
for sub in ("svg", "pdf", "png"):
    (SALIDA / "simbolos" / sub).mkdir(parents=True, exist_ok=True)
for clave, base in SIMB.items():
    d, (x0, y0, x1, y1) = contorno_simbolo(clave)
    x0 -= PAD; y0 -= PAD; w = x1 - x0 + PAD; h = y1 - y0 + PAD
    for v in VERSIONES + ["oro"]:
        nombre = f"bravissima_{base}_{v}"
        s_ = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}" width="{w:.2f}" height="{h:.2f}" '
              f'role="img" aria-label="bravissima — {base}"><title>bravissima — {base}</title><path fill="{PALETA[v]}" d="{d}"/></svg>')
        (SALIDA / "simbolos" / "svg" / f"{nombre}.svg").write_text(s_, encoding="utf-8")
        cairosvg.svg2pdf(bytestring=s_.encode(), write_to=str(SALIDA / "simbolos" / "pdf" / f"{nombre}.pdf"), scale=0.15)
        if "chic" in base:
            continue  # la versión chica solo se usa en vector
        for px in (1000, 3000):
            cairosvg.svg2png(bytestring=s_.encode(), write_to=str(SALIDA / "simbolos" / "png" / f"{nombre}_{px}px.png"), output_height=px)
    print("ok", base)
