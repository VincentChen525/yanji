"""25-mont-blanc：勃朗峰，从霞慕尼看。横幅。单位 km（示意）。
浑圆厚重的雪穹顶峰（不是尖峰），两侧肩部；左侧低处一排尖锐的岩针（aiguilles）；冰川舌带冰裂缝顺坡流下。"""
import sys, random, math
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull
cv = Canvas("横", seed=25, sx=0.72)
rnd = random.Random(25)
needles = [(-2.75, 0.5), (-2.55, 0.72), (-2.4, 0.6), (-2.22, 0.86), (-2.08, 0.7), (-1.92, 0.95), (-1.78, 0.8), (-1.6, 1.02)]
pts = [(-3.2, 0.0), (-3.0, 0.3)]
for i, (x, z) in enumerate(needles):
    pts += [(x - 0.06, z - 0.18), (x - 0.015, z), (x + 0.02, z - 0.02), (x + 0.07, z - 0.2)]
sil = pts + ridge([(-1.5, 0.85), (-1.15, 1.08), (-0.95, 1.16), (-0.72, 1.1), (-0.45, 1.28), (-0.2, 1.24)], 0.025, 1) + \
      catmull([(-0.2, 1.24), (0.1, 1.36), (0.4, 1.44), (0.7, 1.45), (1.0, 1.4), (1.3, 1.3), (1.6, 1.24), (1.9, 1.22), (2.1, 1.16)], 6)[1:] + \
      ridge([(2.1, 1.16), (2.35, 0.98), (2.6, 0.8), (3.0, 0.5), (3.4, 0.22), (3.7, 0.0)], 0.03, 2)[1:]
SKY = sky(sil)
cv.line(sil, OUTER)
cv.line([(-3.3, 0), (3.8, 0)], OUTER)
# 岩针的竖裂与底部岩坡
for x, z in needles:
    cv.line([(x - 0.012, z - 0.05), (x - 0.02, z - 0.16)], INNER, hide=[SKY])
# 雪线以下的岩肋（分隔冰川）
for pts_, sd in [([(-0.95, 1.12), (-0.9, 0.8), (-0.75, 0.5), (-0.7, 0.2)], 4), ([(-0.45, 1.25), (-0.35, 0.9), (-0.3, 0.6)], 5),
                 ([(1.25, 1.3), (1.15, 1.0), (1.2, 0.7), (1.1, 0.35)], 6), ([(1.9, 1.2), (1.85, 0.9), (2.0, 0.6), (2.1, 0.3)], 7)]:
    cv.line(ridge(pts_, 0.04, sd), INNER, hide=[SKY])
# 博松冰川舌：从峰顶下方流向左下
def tongue(ctrl, w0, w1, sd):
    """冰川舌：从雪原中流出（顶端不封口），两侧边缘不规则、宽窄起伏；
    冰裂缝为成组的短弧，弧心朝下游凸出，只占舌宽的一部分；末端为参差的冰塔前缘。"""
    r = random.Random(sd)
    path = catmull(ctrl, 6)
    L_, R_ = [], []
    for i, (x, z) in enumerate(path):
        t = i / (len(path) - 1)
        w = (w0 + (w1 - w0) * t) * (1 + 0.25 * math.sin(t * 7 + sd))
        (xa, za), (xb, zb) = path[max(0, i - 1)], path[min(len(path) - 1, i + 1)]
        dx, dz = xb - xa, zb - za
        n = math.hypot(dx, dz) or 1
        nx, nz = -dz / n, dx / n
        L_.append((x + nx * w, z + nz * w))
        R_.append((x - nx * w, z - nz * w))
    k0 = 3  # 顶端几段不画，表示从雪原里流出
    cv.line(ridge(L_[k0:], 0.04, sd), INNER, hide=[SKY]); cv.line(ridge(R_[k0:], 0.04, sd + 1), INNER, hide=[SKY])
    # 末端冰塔前缘：锯齿
    a, b = L_[-1], R_[-1]
    zig = [a]
    for j in range(1, 6):
        f = j / 6
        px, pz = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        zig.append((px, pz - (0.04 if j % 2 else 0.0) - r.uniform(0, 0.02)))
    zig.append(b)
    cv.line(zig, INNER)
    # 冰裂缝：沿舌身若干组
    for i in range(k0 + 2, len(path) - 3, 4):
        (x, z) = path[i]
        la, ra = L_[i], R_[i]
        for m in range(r.randint(1, 3)):
            f0 = r.uniform(0.05, 0.3); f1 = f0 + r.uniform(0.4, 0.6)
            f1 = min(f1, 0.92)
            off = m * 0.045
            p0 = (la[0] + (ra[0] - la[0]) * f0, la[1] + (ra[1] - la[1]) * f0 - off)
            p1 = (la[0] + (ra[0] - la[0]) * f1, la[1] + (ra[1] - la[1]) * f1 - off)
            mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 0.022)
            cv.smooth([p0, mid, p1], INNER, n=4)


tongue([(0.5, 1.32), (0.38, 1.12), (0.18, 0.92), (0.08, 0.72), (-0.08, 0.5), (-0.12, 0.3), (-0.25, 0.14)], 0.24, 0.15, 8)
tongue([(1.55, 1.2), (1.62, 1.0), (1.52, 0.78), (1.6, 0.5)], 0.17, 0.1, 9)
# 穹顶上的几道雪檐/风纹
for x0, z0, x1, z1 in [(0.0, 1.3, 0.55, 1.36), (0.65, 1.38, 1.15, 1.32), (1.4, 1.2, 1.95, 1.16)]:
    cv.smooth([(x0, z0), ((x0 + x1) / 2, (z0 + z1) / 2 + 0.02), (x1, z1)], INNER, n=6)
cv.save(sys.argv[1])
