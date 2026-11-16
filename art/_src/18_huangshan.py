"""18-huangshan：黄山。横幅。单位 km（示意）。
一群高低不一的花岗岩石柱（从云海中升起，前面的挡住后面的），左下前景岩台上一株迎客松，柱脚有两三道云海线。"""
import sys, random, math
from lineart import Canvas, OUTER, INNER, ridge, catmull, pine_flat, clip_runs
cv = Canvas("横", seed=18)
CLOUD = 0.35
rnd = random.Random(18)


def spire(xc, w, top, sd):
    """花岗岩石柱：块状节理形成的折线轮廓——直边、错落的小台阶，顶部或尖峭或方钝。"""
    r = random.Random(sd)
    base = CLOUD + r.uniform(-0.03, 0.03)
    h = top - base
    lean = r.uniform(-0.05, 0.05)
    lp, rp = [(xc - w / 2, base)], [(xc + w / 2, base)]
    nseg = 5
    for i in range(1, nseg + 1):
        f = i / (nseg + 1)
        wf = w / 2 * (1 - 0.6 * f ** 1.4)
        zl = base + h * f + r.uniform(-0.03, 0.03)
        zr = base + h * f + r.uniform(-0.03, 0.03)
        xl = xc - wf + lean * f
        xr = xc + wf + lean * f
        # 台阶：先竖直上到节理面，再水平内收一小段
        if r.random() < 0.3:
            lp += [(lp[-1][0] + r.uniform(-0.01, 0.01), zl), (xl, zl + r.uniform(0.0, 0.02))]
        else:
            lp.append((xl, zl))
        if r.random() < 0.3:
            rp += [(rp[-1][0] + r.uniform(-0.01, 0.01), zr), (xr, zr + r.uniform(0.0, 0.02))]
        else:
            rp.append((xr, zr))
    tx = xc + lean + r.uniform(-0.12, 0.12) * w
    kind = sd % 3
    if kind == 0:      # 尖峭
        cap = [lp[-1], (tx - w * 0.06, top - h * 0.03), (tx, top), (tx + w * 0.05, top - h * 0.05), rp[-1]]
    elif kind == 1:    # 方钝岩块
        cap = [lp[-1], (lp[-1][0] + w * 0.02, top - 0.02), (tx - w * 0.1, top), (tx + w * 0.12, top - 0.015),
               (rp[-1][0] - w * 0.02, top - 0.05), rp[-1]]
    else:              # 斜削
        cap = [lp[-1], (tx - w * 0.15, top - h * 0.06), (tx + w * 0.02, top), rp[-1]]
    return ridge(lp, 0.05, sd) + cap[1:-1] + ridge(list(reversed(rp)), 0.05, sd + 5)


# 由前到后
specs = [(-0.25, 0.55, 1.6), (0.62, 0.5, 1.3), (1.35, 0.6, 1.0),
         (0.2, 0.5, 2.05), (-0.85, 0.55, 1.25), (1.0, 0.42, 1.8),
         (-1.4, 0.5, 0.95), (1.75, 0.45, 1.35), (-0.55, 0.4, 1.75)]
# 迎客松与前景岩台（最前）
ledge = ridge([(-2.45, 0.0), (-2.4, 0.4), (-2.1, 0.62), (-1.75, 0.66), (-1.5, 0.55), (-1.35, 0.3), (-1.3, 0.0)], 0.03, 99)
def pad(cx, cz, w, sd):
    r = random.Random(sd)
    ph = w * 0.22
    top = [(cx - w / 2 + w * i / 6, cz + ph * math.sin(math.pi * i / 6) ** 0.6 + (r.uniform(0, 0.25) * ph if 0 < i < 6 else 0)) for i in range(7)]
    bot = [(cx + w / 2, cz), (cx + w * 0.15, cz - ph * 0.25), (cx - w * 0.2, cz - ph * 0.2), (cx - w / 2, cz)]
    return catmull(top, 4) + catmull(bot, 4)[1:]


# 迎客松：干从岩台斜出，一根长枝向右水平伸出（“迎客”的手臂），叶团扁平
trunk = catmull([(-1.9, 0.64), (-1.82, 0.85), (-1.9, 1.05), (-1.82, 1.25)], 6)
arm = catmull([(-1.86, 0.98), (-1.6, 1.0), (-1.3, 0.96), (-1.0, 0.98), (-0.75, 0.95)], 6)
twig = catmull([(-1.84, 1.15), (-2.05, 1.2), (-2.2, 1.18)], 4)
pl = [trunk, arm, twig]
pp = [pad(-1.8, 1.27, 0.42, 1), pad(-1.55, 1.04, 0.38, 2), pad(-1.18, 1.0, 0.36, 3), pad(-0.85, 0.99, 0.32, 4), pad(-2.15, 1.2, 0.3, 5)]
FRONT = [ledge + [(-1.3, -1), (-2.45, -1)]] + pp
polys = []
for i, (xc, w, top) in enumerate(specs):
    sp = spire(xc, w, top, 30 + i)
    hide = FRONT + polys
    cv.line(sp, OUTER, hide=hide)
    # 竖向节理裂隙 + 少量横向节理
    for k in range(2):
        x = xc + w * rnd.uniform(-0.25, 0.25)
        zt = top - (top - CLOUD) * rnd.uniform(0.12, 0.3)
        cv.line([(x, zt), (x + rnd.uniform(-0.02, 0.02), (zt + CLOUD) / 2), (x + rnd.uniform(-0.02, 0.02), CLOUD + rnd.uniform(0.04, 0.3))],
                INNER, hide=hide + [[(xc - w, top + 1), (xc + w, top + 1), (xc + w, CLOUD), (xc - w, CLOUD)][:0] or [(0, 0), (0, 0), (0, 0)]])
    polys.append(sp)
    # 有的柱顶长几株小松
    if i in (0, 3, 5):
        l, p = pine_flat(xc - w * 0.05, top - 0.03, 0.26, 1 if i % 2 else -1, 40 + i)
        for ln in l: cv.line(ln, INNER, hide=FRONT + polys[:-1])
        for q in p: cv.line(q, INNER, closed=True, hide=FRONT + polys[:-1])
# 云海：几道长波浪线，被前景岩台挡住
for z, amp, sd in [(CLOUD, 0.025, 1), (CLOUD - 0.09, 0.02, 2), (CLOUD - 0.18, 0.018, 3)]:
    pts = [(-2.5 + 4.6 * i / 40, z + amp * math.sin(i * 1.3 + sd) + rnd.uniform(-0.008, 0.008)) for i in range(41)]
    cv.smooth(pts, INNER, n=4, hide=FRONT)
# 前景岩台与松
cv.line(ledge, OUTER, hide=pp)
for x0 in (-2.2, -1.9, -1.6):
    cv.line(ridge([(x0, 0.55), (x0 + 0.05, 0.3), (x0, 0.05)], 0.05, int(x0 * 10) + 70), INNER, hide=pp)
for ln in pl: cv.line(ln, OUTER, hide=pp)
for q in pp: cv.line(q, INNER, closed=True)
cv.save(sys.argv[1])
