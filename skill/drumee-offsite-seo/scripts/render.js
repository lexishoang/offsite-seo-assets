// Render HTML files to PNG. Usage: node render.js jobs.json
// jobs.json: [{"html": "path.html", "out": "path.png", "w": 1400, "h": 788, "scale": 1}]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h === 'auto' ? 800 : j.h }, deviceScaleFactor: j.scale || 1 });
    await page.goto('file://' + path.resolve(j.html));
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(200);
    const h = j.h === 'auto' ? await page.evaluate(() => document.querySelector('.stage').getBoundingClientRect().height) : j.h;
    if (j.h === 'auto') await page.setViewportSize({ width: j.w, height: Math.ceil(h) });
    fs.mkdirSync(path.dirname(path.resolve(j.out)), { recursive: true });
    await page.screenshot({ path: j.out, clip: { x: 0, y: 0, width: j.w, height: Math.ceil(h) } });
    await page.close();
    console.log('rendered', j.out);
  }
  await browser.close();
})();
