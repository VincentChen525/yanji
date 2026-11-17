#!/usr/bin/env python3
"""把 art/*.svg 的线描转成岩迹里用的路径数据，并生成分享卡要用的贴纸素材。

产物：
1. shengji-prototype.html 里的 ART / ART2 / AW / AX（山页、线路图用的线描路径）。
2. brand/share/sticker-<n>.png：29 个山峰/建筑的透明贴纸（白色剪影 + 线稿）。
3. shengji-prototype.html 里的 SHARE_STICKER_NUM / SHARE_STICKER_POLY / SHARE_STICKER_ASPECT
   （分享卡按当前目标取贴纸和剪影；改 art 后重跑本脚本即可，不要手改这些常量）。

依赖：Pillow、numpy、scipy（只用 ndimage 的膨胀/填洞/连通域）。
贴纸是从 art/<stem>.png 的线稿抠剪影；新增一张图时，svg 和 png 都要放进 art/，再运行本脚本。
用法：python3 build_art.py
"""
import json
import math
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / 'shengji-prototype.html'
STICKER_DIR = ROOT / 'brand' / 'share'
STICKER_WIDTH = 760  # 2x 分享卡里 380 宽的贴纸
NAMES = {
    '01-tiantan': '天坛祈年殿', '02-pisa': '比萨斜塔', '03-sydney-opera': '悉尼歌剧院', '04-taj-mahal': '泰姬陵',
    '05-liberty': '自由女神像', '06-big-ben': '大本钟', '07-giza': '吉萨金字塔', '08-eiffel': '埃菲尔铁塔',
    '09-tokyo-tower': '东京塔', '10-empire-state': '帝国大厦', '11-oriental-pearl': '东方明珠', '12-taipei-101': '台北 101',
    '13-cn-tower': '多伦多电视塔', '14-canton-tower': '广州塔', '15-burj-khalifa': '哈利法塔', '16-table-mountain': '桌山',
    '17-taishan': '泰山', '18-huangshan': '黄山', '19-huashan': '华山', '20-el-capitan': '酋长岩', '21-half-dome': '半穹顶',
    '22-emeishan': '峨眉山', '23-fuji': '富士山', '24-matterhorn': '马特洪峰', '25-mont-blanc': '勃朗峰', '26-yulong': '玉龙雪山',
    '27-kilimanjaro': '乞力马扎罗', '28-k2': '乔戈里峰', '29-everest': '珠穆朗玛',
}
TOL = 0.09  # 化简容差，单位是高 100 的格子
MAXW = 420  # 太宽的山（桌山、乞力马扎罗）横向压到这个宽度，否则在卡片里只剩一条缝
POLY_STEP = 6  # 贴纸剪影采样步长（像素）


def simplify(pts, tol):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        best, bi = 0, None
        for i in range(a + 1, b):
            x, y = pts[i]
            d = abs(dx * (y1 - y) - dy * (x1 - x)) / L if L else math.hypot(x - x1, y - y1)
            if d > best:
                best, bi = d, i
        if bi is not None and best > tol:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


def num(v):
    s = f'{v:.1f}'
    return s[:-2] if s.endswith('.0') else s


def convert(svg):
    paths = []
    for sw, d in re.findall(r'<path stroke-width="([\d.]+)" d="([^"]*)"', svg):
        for sub in re.findall(r'M([^M]*)', d):
            pts = [tuple(map(float, p.split(','))) for p in re.findall(r'-?[\d.]+,-?[\d.]+', sub)]
            if pts:
                paths.append((float(sw), pts))
    # 图里自带的地面线不要：山页自己会画地面，留着只会把格子撑宽
    ys = [p[1] for _, ps in paths for p in ps]
    y0, y1 = min(ys), max(ys)
    def ground(ps):
        xs, yy = [p[0] for p in ps], [p[1] for p in ps]
        return min(yy) > y0 + (y1 - y0) * 0.975 and (max(xs) - min(xs)) > 6 * (max(yy) - min(yy) + 1)
    paths = [(sw, ps) for sw, ps in paths if not ground(ps)]
    allp = [p for _, ps in paths for p in ps]
    minx, maxx = min(p[0] for p in allp), max(p[0] for p in allp)
    miny, maxy = min(p[1] for p in allp), max(p[1] for p in allp)
    k = 100 / (maxy - miny)
    top = [p[0] for p in allp if p[1] - miny < (maxy - miny) * 0.004]
    ax = sum(top) / len(top)
    kx = k * min(1, MAXW / ((maxx - minx) * k))
    w = round((maxx - minx) * kx)
    heavy, light = [], []
    for sw, pts in paths:
        q = simplify([((x - minx) * kx, (y - miny) * k) for x, y in pts], TOL)
        d = 'M' + 'L'.join(f'{num(x)} {num(y)}' for x, y in q)
        (heavy if sw >= 5 else light).append(d)
    return ''.join(heavy), ''.join(light), w, round((ax - minx) * kx, 1)


def make_sticker(png_path, out_path, np, ndi, Image):
    """从 art/<stem>.png 生成透明贴纸：剪影内保留白底和线稿，剪影外透明。"""
    im = Image.open(png_path).convert('RGBA')
    a = np.array(im)
    gray = np.array(im.convert('L'))
    mask = gray < 225
    m = ndi.binary_dilation(mask, iterations=3)
    f = ndi.binary_fill_holes(m)
    lab, n = ndi.label(f)
    if n > 1:
        sizes = ndi.sum(f, lab, range(1, n + 1))
        f = lab == (1 + int(np.argmax(sizes)))
    ys, xs = np.where(f)
    x0, x1 = max(0, xs.min() - 3), min(im.width - 1, xs.max() + 3)
    y0, y1 = max(0, ys.min() - 3), min(im.height - 1, ys.max() + 3)
    crop = a[y0:y1 + 1, x0:x1 + 1].copy()
    cm = f[y0:y1 + 1, x0:x1 + 1]
    crop[..., 3] = np.where(cm, 255, 0)
    out = Image.fromarray(crop, 'RGBA')
    if out.width != STICKER_WIDTH:
        h = round(out.height * STICKER_WIDTH / out.width)
        out = out.resize((STICKER_WIDTH, h), Image.LANCZOS)
    out.save(out_path)
    return out


def sticker_shape(out_path, np, Image):
    """从贴纸 alpha 取外轮廓（上边界 + 底边），归一化到 0..1。"""
    im = Image.open(out_path).convert('RGBA')
    a = np.array(im)[..., 3]
    W, H = im.size
    mask = a > 8
    top, base = [], 0
    for x in range(0, W + 1, POLY_STEP):
        col = np.where(mask[:, min(x, W - 1)])[0]
        if len(col):
            top.append((x, int(col.min())))
            base = max(base, int(col.max()))
    poly = [(x / W, y / H) for x, y in top] + [(1, base / H), (0, base / H)]
    clean = []
    for p in poly:
        if not clean or abs(p[0] - clean[-1][0]) > 1e-4 or abs(p[1] - clean[-1][1]) > 1e-4:
            clean.append(p)
    return [[round(x, 4), round(y, 4)] for x, y in clean], round(W / H, 4)


def replace_between(s, begin, end, new):
    if begin in s:
        i = s.index(begin)
        j = s.index(end, i) + len(end)
        return s[:i] + new + s[j:]
    return s


def main():
    try:
        import numpy as np
        from PIL import Image
        from scipy import ndimage as ndi
    except ImportError as e:
        raise SystemExit(f'需要 Pillow / numpy / scipy 才能生成贴纸：{e}')

    STICKER_DIR.mkdir(parents=True, exist_ok=True)
    art, art2, aw, axs = [], [], [], []
    nums, polys, aspects = {}, {}, {}
    for idx, (stem, name) in enumerate(NAMES.items(), start=1):
        h, l, w, ax = convert((ROOT / 'art' / f'{stem}.svg').read_text())
        art.append(f" '{name}':'{h}'")
        art2.append(f" '{name}':'{l}'")
        aw.append(f"'{name}':{w}")
        axs.append(f"'{name}':{num(ax)}")
        png = ROOT / 'art' / f'{stem}.png'
        if png.exists():
            out = STICKER_DIR / f'sticker-{idx}.png'
            make_sticker(png, out, np, ndi, Image)
            poly, aspect = sticker_shape(out, np, Image)
            nums[name] = idx
            polys[name] = poly
            aspects[name] = aspect
            print(f'{name:<8} w={w:<4} 顶点x={ax:6.1f}  粗 {len(h):>6}  细 {len(l):>6}  贴纸 {out.name} {len(poly)}点')
        else:
            print(f'{name:<8} 跳过贴纸：缺 {png}')

    block = ('/*ART-BEGIN 由 build_art.py 从 art/*.svg 生成，不要手改*/\n'
             '// 每个目标的线描：画在 w×100 的格子里，地面在下（y=100），最高点在 (AX,0)。ART 是外轮廓（粗线），ART2 是内部结构（细线）\n'
             'const ART={\n' + ',\n'.join(art) + '};\nconst ART2={\n' + ',\n'.join(art2) + '};\n'
             'const AW={' + ','.join(aw) + '};\nconst AX={' + ','.join(axs) + '};\n'
             'const artOf=n=>({d:ART[n],d2:ART2[n],w:AW[n]||100,ax:AX[n]==null?(AW[n]||100)/2:AX[n]});\n/*ART-END*/\n')
    sticker = ('/*STICKER-BEGIN 由 build_art.py 从 art/*.png 生成，不要手改*/\n'
               'const SHARE_STICKER_NUM=' + json.dumps(nums, ensure_ascii=False, separators=(',', ':')) + ';\n'
               'const SHARE_STICKER_POLY=' + json.dumps(polys, ensure_ascii=False, separators=(',', ':')) + ';\n'
               'const SHARE_STICKER_ASPECT=' + json.dumps(aspects, ensure_ascii=False, separators=(',', ':')) + ';\n'
               '/*STICKER-END*/\n')

    s = HTML.read_text(encoding='utf-8')
    if '/*ART-BEGIN' in s:
        i, j = s.index('/*ART-BEGIN'), s.index('/*ART-END*/\n') + len('/*ART-END*/\n')
    else:  # 第一次：替换掉手写的那一段
        i = s.index('// 每个目标的线描：画在 100×100 的格子里')
        j = s.index('// 小人的两个姿势')
    s = s[:i] + block + s[j:]
    if '/*STICKER-BEGIN' in s:
        s = replace_between(s, '/*STICKER-BEGIN', '/*STICKER-END*/\n', sticker)
    else:  # 第一次：插到分享卡代码前
        k = s.index('/* ---------- 分享卡')
        s = s[:k] + sticker + '\n' + s[k:]
    HTML.write_text(s, encoding='utf-8')
    print('写入 ART', len(block), '字符；STICKER', len(sticker), '字符；贴纸', len(nums), '张')


if __name__ == '__main__':
    main()
