// Uso: node captura.js entrada.html salida.png ancho alto [escala] [selector]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, out, w, h, s = '1', sel] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +s });
  await p.goto('file://' + path.resolve(inp));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  if (sel) await p.locator(sel).screenshot({ path: out, omitBackground: true });
  else await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
