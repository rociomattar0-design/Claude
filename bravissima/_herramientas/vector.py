"""Utilidades vectoriales: parsear trazados SVG (los que generan fontTools/pathops),
transformarlos y dibujarlos en reportlab (PDF CMYK)."""
import re

_TOK = re.compile(r"[MLHVCQTZmlhvcqtz]|-?(?:\d+\.?\d*|\.\d+)(?:[eE]-?\d+)?")


def segmentos(d):
    """Devuelve una lista de (op, puntos) absolutos: M, L, C (cúbicas), Z."""
    t = _TOK.findall(d)
    i, cmd = 0, None
    cx = cy = sx = sy = 0.0
    out = []

    def n():
        nonlocal i
        v = float(t[i])
        i += 1
        return v

    while i < len(t):
        if t[i].isalpha():
            cmd = t[i]
            i += 1
            if cmd in "Zz":
                out.append(("Z", ()))
                cx, cy = sx, sy
                continue
        if cmd == "M":
            cx, cy = n(), n()
            sx, sy = cx, cy
            out.append(("M", ((cx, cy),)))
            cmd = "L"
        elif cmd == "L":
            cx, cy = n(), n()
            out.append(("L", ((cx, cy),)))
        elif cmd == "H":
            cx = n()
            out.append(("L", ((cx, cy),)))
        elif cmd == "V":
            cy = n()
            out.append(("L", ((cx, cy),)))
        elif cmd == "C":
            p = (n(), n()), (n(), n()), (n(), n())
            out.append(("C", p))
            cx, cy = p[2]
        elif cmd == "Q":
            qx, qy, x, y = n(), n(), n(), n()
            c1 = (cx + 2 / 3 * (qx - cx), cy + 2 / 3 * (qy - cy))
            c2 = (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y))
            out.append(("C", (c1, c2, (x, y))))
            cx, cy = x, y
        else:
            raise ValueError(f"comando no soportado: {cmd}")
    return out


def transformar(d, s=1.0, tx=0.0, ty=0.0):
    f = lambda p: f"{p[0] * s + tx:.4f} {p[1] * s + ty:.4f}"
    partes = []
    for op, pts in segmentos(d):
        partes.append(op + (" ".join(f(p) for p in pts) if pts else ""))
    return " ".join(partes)


def dibujar_rl(canvas, d):
    p = canvas.beginPath()
    for op, pts in segmentos(d):
        if op == "M":
            p.moveTo(*pts[0])
        elif op == "L":
            p.lineTo(*pts[0])
        elif op == "C":
            p.curveTo(*pts[0], *pts[1], *pts[2])
        else:
            p.close()
    canvas.drawPath(p, stroke=0, fill=1, fillMode=1)  # 1 = nonzero
