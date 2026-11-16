// 用无头 Chrome 截图：
//   node shoot.mjs shots   按手机尺寸（390×844，3 倍）打开应用，截取各页面的一块真实界面，存到 shots/
//   node shoot.mjs cards   把 cards.html 里每张卡片按 1242×1660 导出成 out/card-01.png …
// 需要先在项目目录起一个本地服务器：python3 -m http.server 8765 --bind 127.0.0.1
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const BASE = 'http://127.0.0.1:8765';
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const sleep = ms => new Promise(r => setTimeout(r, ms));

const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), 'yanji-chrome-'))}`,
  '--no-first-run', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });

let ws, seq = 0;
const pending = new Map();
async function connect() {
  for (let i = 0; i < 50; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find(t => t.type === 'page');
      if (page) { ws = new WebSocket(page.webSocketDebuggerUrl); break }
    } catch { }
    await sleep(200);
  }
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej });
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id) } };
}
function send(method, params = {}) {
  const id = ++seq; ws.send(JSON.stringify({ id, method, params }));
  return new Promise((res, rej) => pending.set(id, m => m.error ? rej(new Error(method + ': ' + m.error.message)) : res(m.result)));
}
async function evaluate(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result.value;
}
async function open(url, w, h, dsf, mobile) {
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: dsf, mobile });
  await send('Page.navigate', { url });
  for (let i = 0; i < 100; i++) { await sleep(100); if (await evaluate('document.readyState') === 'complete') break }
  await evaluate('document.fonts.ready.then(()=>1)');
  await sleep(400);
}
async function shot(file, rect, dsf) {
  await evaluate('document.fonts.ready.then(()=>1)'); await sleep(250);
  const r = await send('Page.captureScreenshot', { format: 'png', clip: { ...rect, scale: 1 }, captureBeyondViewport: true });
  writeFileSync(file, Buffer.from(r.data, 'base64'));
  console.log('saved', file.replace(HERE + '/', ''), Math.round(rect.width * dsf) + '×' + Math.round(rect.height * dsf));
}

// 把手机外框拉长到能一次放下整页，去掉底部导航和浮动按钮（只截中间一块界面，它们会压在内容上）
const TALL = `(()=>{const s=document.createElement('style');s.textContent='.phone{max-height:none!important;height:2600px!important}nav,.fab{display:none!important}main{padding-bottom:40px!important}';document.head.appendChild(s);return 1})()`;
// 取若干元素的外接矩形，左右铺满手机宽度，上下各留 pad
const RECT = (sels, top = 8, bottom = top) => `(()=>{const els=${JSON.stringify(sels)}.map(s=>document.querySelector(s)).filter(Boolean);if(!els.length)throw new Error('not found: ${sels.join(',')}');
  const rs=els.map(e=>e.getBoundingClientRect()),ph=document.querySelector('.phone').getBoundingClientRect();
  const top=Math.min(...rs.map(r=>r.top))-(${top}),bottom=Math.max(...rs.map(r=>r.bottom))+(${bottom});
  return {x:ph.left+scrollX,y:top+scrollY,width:ph.width,height:bottom-top}})()`;
const nav = i => `(()=>{document.querySelectorAll('nav button')[${i}].click();return 1})()`;

async function shots() {
  const D = 3, out = join(HERE, 'shots'); mkdirSync(out, { recursive: true });
  await open(`${BASE}/shengji-prototype.html`, 390, 2600, D, true);
  await evaluate(TALL); await sleep(200);
  // 封面：今天的岩壁图
  await shot(join(out, 'cover.png'), await evaluate(RECT(['#p-today .card'], 8)), D);
  // 今天：统计和今天爬的几条线
  await shot(join(out, 'today.png'), await evaluate(RECT(['#p-today .stats', '#p-today .rrow:last-of-type'], 8)), D);
  // 山：正在爬的这座
  await evaluate(nav(1)); await sleep(2800);
  await shot(join(out, 'mount.png'), await evaluate(RECT(['#mCard'], 6)), D);
  // 阶：站稳的级别和金字塔
  await evaluate(nav(2)); await sleep(300);
  await shot(join(out, 'pyr.png'), await evaluate(RECT(['#p-pyr .big', '#p-pyr .legend'], 4, 6)), D);
  // 迹：点阵和那一天
  await evaluate(nav(3)); await sleep(400);
  await shot(join(out, 'heat.png'), await evaluate(RECT(['#p-review .hscroll', '#histCard'], 8)), D);
  // 迹：看出来的
  await shot(join(out, 'insight.png'), await evaluate(RECT(['#p-review .ins', '#p-review .tile:nth-child(2)'], 6, 4)), D);
  // 记一条：已有线的记录面板
  await evaluate(nav(0)); await sleep(200);
  await evaluate(`(()=>{openSheet('log');const p=document.querySelector('#sheet [data-pick]');if(p)p.click();return 1})()`); await sleep(700);
  await shot(join(out, 'log.png'), await evaluate(RECT(['#sheet h1', '#sheet .save'], 10, 20)), D);
}

async function cards() {
  const out = join(HERE, 'out'); mkdirSync(out, { recursive: true });
  await open(`${BASE}/social/cards.html`, 1242, 1660, 1, false);
  const n = await evaluate('document.querySelectorAll(".card").length');
  for (let i = 0; i < n; i++) {
    const rect = await evaluate(`(()=>{const r=document.querySelectorAll('.card')[${i}].getBoundingClientRect();return {x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height}})()`);
    await shot(join(out, `card-${String(i + 1).padStart(2, '0')}.png`), rect, 1);
  }
}

try {
  await connect(); await send('Page.enable'); await send('Runtime.enable');
  await ({ shots, cards }[process.argv[2]] || (() => { throw new Error('用法：node shoot.mjs shots|cards') }))();
} catch (e) { console.error(e.message); process.exitCode = 1 }
finally { try { ws?.close() } catch { } chrome.kill() }
