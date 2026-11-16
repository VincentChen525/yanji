"""11-oriental-pearl：东方明珠。竖幅。单位米。总高 468m。
三根斜撑 + 三根立柱托起下球（中心约 90m）与上球（约 263m），柱间一串小球，顶部太空舱小球，长天线。"""
import math, sys
from lineart import Canvas, OUTER, INNER
cv = Canvas("竖", seed=11)
L = cv.line
R1, Z1 = 25.0, 92.0       # 下球
R2, Z2 = 22.5, 263.0      # 上球
R3, Z3 = 7.5, 350.0       # 太空舱
balls = [(Z1, R1), (Z2, R2), (Z3, R3)]


def sphere_poly(zc, r, n=48):
    return [(r * math.cos(2 * math.pi * i / n), zc + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


hide = [sphere_poly(z, r) for z, r in balls]
# 立柱：正面看到左右两根 + 中间一根（后面那根被挡），柱径 9m
for xc in (-11, 11, 0):
    for e in (-4.5, 4.5):
        L([(xc + e, 0), (xc + e, Z2 - R2 * 0.5)], INNER if xc == 0 else OUTER, hide=hide)
# 三根斜撑：两侧外撇 + 正中一根（朝向观者）
for s in (-1, 1):
    L([(s * 50, 0), (s * 14, Z1 - R1 * 0.75)], OUTER, hide=hide)
    L([(s * 42, 0), (s * 7, Z1 - R1 * 0.9)], OUTER, hide=hide)
    L([(s * 46, 0), (s * 10.5, Z1 - R1 * 0.82)], INNER, hide=hide)
L([(-60, 0), (60, 0)], OUTER)
# 球体 + 纬线带
for zc, r in balls:
    cv.poly(sphere_poly(zc, r), OUTER)
    for f in (-0.55, -0.18, 0.18, 0.55):
        hw_ = r * math.sqrt(1 - f * f)
        cv.smooth([(-hw_, zc + f * r), (0, zc + f * r - r * 0.06), (hw_, zc + f * r)], n=8)
# 下球与上球之间的小球串（5 个），在两根立柱之间
small = []
for i in range(5):
    zc = 140 + i * 18
    small.append(sphere_poly(zc, 5.2))
for i, p in enumerate(small):
    cv.poly(p, INNER)
# 上球以上：单筒身到太空舱
for s in (-1, 1):
    L([(s * 5.5, Z2 + R2 * 0.6), (s * 4.5, Z3 - R3)], OUTER, hide=hide)
# 天线：分段收细
L([(-3.2, Z3 + R3), (-2.2, 395), (-1.2, 395), (-0.6, 468), (0.6, 468), (1.2, 395), (2.2, 395), (3.2, Z3 + R3)], OUTER)
for z in (372, 385, 410, 430):
    L([(-2.6 if z < 395 else -1.0, z), (2.6 if z < 395 else 1.0, z)])
# 底座裙楼一圈
L([(-36, 0), (-36, 9), (36, 9), (36, 0)], OUTER, hide=None)
cv.save(sys.argv[1])
