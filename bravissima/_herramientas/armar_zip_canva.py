"""Arma bravissima_editables_canva.zip con todo lo editable, ordenado para Canva."""
import zipfile

from marca import RAIZ

DEST = RAIZ / "_descargas" / "bravissima_editables_canva.zip"
CONTENIDO = [  # (origen, carpeta dentro del zip, patrón)
    ("COMO_EDITAR_EN_CANVA.txt", "", None),
    ("01_logo/editable_canva", "01_logos_y_simbolos", "*.pdf"),
    ("01_logo/svg", "01_logos_y_simbolos/svg_logo_e_isotipo", "*.svg"),
    ("01_logo/simbolos/svg", "01_logos_y_simbolos/svg_cardo_y_llama", "*.svg"),
    ("01_logo/png", "01_logos_y_simbolos/png_logo_e_isotipo", "*_3000px.png"),
    ("01_logo/simbolos/png", "01_logos_y_simbolos/png_cardo_y_llama", "*_3000px.png"),
    ("02_mockups/editable_canva", "02_mockups_editables", "*.pdf"),
    ("02_mockups/editable_canva/fondos", "02_mockups_editables/fondos_vacios", "*.jpg"),
    ("03_stickers/editable_canva", "03_stickers", "*.pdf"),
    ("03_stickers", "03_stickers/para_imprenta", "bravissima_planilla-stickers_A4.pdf"),
    ("04_redes/editable_canva", "04_redes", "*.pdf"),
    ("04_redes/png", "04_redes/png_finales", "*.png"),
    ("05_manual", "05_manual", "*.pdf"),
    ("_fuentes/estaticas", "fuentes_para_canva_pro", "*.ttf"),
    ("_fuentes", "fuentes_para_canva_pro", "OFL-*.txt"),
]

DEST.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(DEST, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for origen, carpeta, patron in CONTENIDO:
        o = RAIZ / origen
        archivos = [o] if patron is None else sorted(o.glob(patron))
        for f in archivos:
            z.write(f, f"bravissima_editables_canva/{carpeta}/{f.name}".replace("//", "/"))
            n += 1
print(DEST.name, n, "archivos", f"{DEST.stat().st_size / 1e6:.1f} MB")
