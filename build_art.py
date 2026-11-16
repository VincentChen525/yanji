#!/usr/bin/env python3
"""把 art/*.svg 的线描转成绳迹里用的路径数据，写回 shengji-prototype.html。

每张图缩放到高 100 的格子里，地面在 y=100，最高点在 (AX, 0)，AX 记在 AX 表里。图里自带的地面线会去掉。
粗线（外轮廓）进 ART，细线（内部结构）进 ART2，格子宽度进 AW。
用法：python3 build_art.py
"""
import re, math, pathlib

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / 'shengji-prototype.html'
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
    ax = sum(top) / len(top)  # 最高点的 x
    kx = k * min(1, MAXW / ((maxx - minx) * k))
    w = round((maxx - minx) * kx)
    heavy, light = [], []
    for sw, pts in paths:
        q = simplify([((x - minx) * kx, (y - miny) * k) for x, y in pts], TOL)
        d = 'M' + 'L'.join(f'{num(x)} {num(y)}' for x, y in q)
        (heavy if sw >= 5 else light).append(d)
    return ''.join(heavy), ''.join(light), w, round((ax - minx) * kx, 1)


def main():
    art, art2, aw, axs = [], [], [], []
    for stem, name in NAMES.items():
        h, l, w, ax = convert((ROOT / 'art' / f'{stem}.svg').read_text())
        art.append(f" '{name}':'{h}'")
        art2.append(f" '{name}':'{l}'")
        aw.append(f"'{name}':{w}")
        axs.append(f"'{name}':{num(ax)}")
        print(f'{name:<8} w={w:<4} 顶点x={ax:6.1f}  粗 {len(h):>6}  细 {len(l):>6}')
    block = ('/*ART-BEGIN 由 build_art.py 从 art/*.svg 生成，不要手改*/\n'
             '// 每个目标的线描：画在 w×100 的格子里，地面在下（y=100），最高点在 (AX,0)。ART 是外轮廓（粗线），ART2 是内部结构（细线）\n'
             'const ART={\n' + ',\n'.join(art) + '};\nconst ART2={\n' + ',\n'.join(art2) + '};\n'
             'const AW={' + ','.join(aw) + '};\nconst AX={' + ','.join(axs) + '};\n'
             'const artOf=n=>({d:ART[n],d2:ART2[n],w:AW[n]||100,ax:AX[n]==null?(AW[n]||100)/2:AX[n]});\n/*ART-END*/\n')
    s = HTML.read_text(encoding='utf-8')
    if '/*ART-BEGIN' in s:
        i, j = s.index('/*ART-BEGIN'), s.index('/*ART-END*/\n') + len('/*ART-END*/\n')
    else:  # 第一次：替换掉手写的那一段
        i = s.index('// 每个目标的线描：画在 100×100 的格子里')
        j = s.index('// 小人的两个姿势')
    HTML.write_text(s[:i] + block + s[j:], encoding='utf-8')
    print('写入', len(block), '字符')


if __name__ == '__main__':
    main()
