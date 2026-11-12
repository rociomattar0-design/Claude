// Exporta un HTML con varias <section class="page"> a PNG (una por página) y a un PDF editable (texto vivo).
// Uso: node exportar_html.js plantilla.html carpeta_png salida.pdf [escala_png]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [html, dirPng, pdf, escala = '1'] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: +escala });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const pages = await p.locator('.page').all();
  let w = 0, h = 0;
  for (const el of pages) {
    const nombre = await el.getAttribute('data-nombre');
    const box = await el.boundingBox();
    w = box.width; h = box.height;
    if (dirPng !== '-') await el.screenshot({ path: path.join(dirPng, nombre + '.png') });
  }
  if (pdf && pdf !== '-') {
    const unidad = await p.evaluate(() => document.body.dataset.unidad || 'px');
    const dims = await p.evaluate(() => [document.body.dataset.ancho, document.body.dataset.alto]);
    await p.pdf({ path: pdf, width: dims[0] + unidad, height: dims[1] + unidad, printBackground: true,
                  margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  }
  await b.close();
})();
