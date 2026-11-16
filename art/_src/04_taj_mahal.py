"""04-taj-mahal：泰姬陵正立面。横幅。单位米。
方形高台 + 四角宣礼塔；主体为倒角方形，正中高耸的尖拱大门（pishtaq）；四个小亭（chhatri）围绕洋葱形主穹顶。"""
import math, sys
from lineart import Canvas, OUTER, INNER, catmull
cv = Canvas("横", seed=4)
L, S = cv.line, cv.smooth


def pointed_arch(xc, z0, zs, half, w=INNER):
    """尖拱：两侧竖直到起拱点 zs，再以两段圆弧交于尖顶。"""
    pts = [(xc - half, z0), (xc - half, zs)]
    r = half * 1.6
    for i in range(1, 9):
        a = math.acos((r - half) / r) * (1 - i / 8)
        pts.append((xc + half - r * math.cos(math.acos((r - half) / r) - (math.acos((r - half) / r) - 0) * 0) * 0 - half + (r - r * math.cos(math.acos((r - half) / r) * i / 8)) - 0, 0))
    # 简化：用三点平滑近似尖拱
    apex = zs + half * 1.25
    left = catmull([(xc - half, zs), (xc - half * 0.82, zs + half * 0.62), (xc - half * 0.4, zs + half * 1.05), (xc, apex)], 5)
    right = [(2 * xc - x, z) for x, z in reversed(left)]
    L([(xc - half, z0)] + left + right[1:] + [(xc + half, z0)], w)


# 高台
L([(-50, 0), (-50, 6.5), (50, 6.5), (50, 0)], OUTER)
L([(-55, 0), (55, 0)], OUTER)
for i in range(22):
    x = -48 + 96 * (i + 0.5) / 22
    pointed_arch(x, 0.8, 3.5, 1.2)
# 宣礼塔
for s in (-1, 1):
    xc = s * 46
    L([(xc - 2.8, 6.5), (xc - 2.1, 44)], OUTER); L([(xc + 2.8, 6.5), (xc + 2.1, 44)], OUTER)
    for z in (19, 31.5):
        w = 2.8 - 0.7 * (z - 6.5) / 37.5
        L([(xc - w - 1.0, z), (xc + w + 1.0, z), (xc + w + 1.0, z + 0.9), (xc - w - 1.0, z + 0.9), (xc - w - 1.0, z)], INNER)
    L([(xc - 3.3, 44), (xc + 3.3, 44), (xc + 3.3, 45), (xc - 3.3, 45), (xc - 3.3, 44)], OUTER)
    for x in (-2.0, 0, 2.0):
        L([(xc + x, 45), (xc + x, 48.5)])
    L([(xc - 2.8, 48.5), (xc + 2.8, 48.5)], OUTER)
    S([(xc - 2.6, 48.5), (xc - 2.4, 50.5), (xc - 1.2, 52), (xc, 52.6), (xc + 1.2, 52), (xc + 2.4, 50.5), (xc + 2.6, 48.5)], OUTER, n=5)
    L([(xc, 52.6), (xc, 54)])
# 主体立面
W = 28.5
L([(-W, 6.5), (-W, 34), (W, 34), (W, 6.5)], OUTER)
for x in (-22.5, 22.5):  # 倒角面分界
    L([(x, 6.5), (x, 34)])
L([(-W, 33), (W, 33)])
# 中央大门
L([(-9, 6.5), (-9, 40.5), (9, 40.5), (9, 6.5)], OUTER)
L([(-8, 7), (-8, 39.5), (8, 39.5), (8, 7)])
pointed_arch(0, 6.5, 25, 6.0, OUTER)
pointed_arch(0, 6.5, 13, 2.6)
L([(-6, 25), (6, 25)])
for s in (-1, 1):  # 大门两侧小尖塔
    L([(s * 9, 40.5), (s * 9, 43.5)], OUTER); L([(s * 9.8, 40.5), (s * 9.8, 43.5)], OUTER)
    S([(s * 8.7, 43.5), (s * 9.4, 45.0), (s * 10.1, 43.5)], OUTER, n=4)
# 两侧双层小尖拱
for s in (-1, 1):
    for xc in (s * 15.75, s * 25.5):
        half = 3.3 if abs(xc) < 20 else 2.0
        for z0, zs in ((7.5, 15.5), (20.5, 27.5)):
            pointed_arch(xc, z0, zs, half)
# 小亭
for s in (-1, 1):
    xc = s * 18.5
    L([(xc - 4.2, 34), (xc - 4.2, 35), (xc + 4.2, 35), (xc + 4.2, 34)], OUTER)
    for x in (-3.4, -1.1, 1.1, 3.4):
        L([(xc + x, 35), (xc + x, 39.5)])
    L([(xc - 4.2, 39.5), (xc + 4.2, 39.5)], OUTER)
    S([(xc - 3.9, 39.5), (xc - 4.2, 41.5), (xc - 2.8, 43.6), (xc, 44.6), (xc + 2.8, 43.6), (xc + 4.2, 41.5), (xc + 3.9, 39.5)], OUTER, n=5)
    L([(xc, 44.6), (xc, 46.4)])
# 主穹顶：鼓座 + 洋葱顶 + 尖饰
L([(-12, 40.5), (-12, 47.5)], OUTER); L([(12, 40.5), (12, 47.5)], OUTER)
L([(-12.6, 47.5), (12.6, 47.5)], OUTER)
dome = [(-12.3, 47.5), (-14.0, 51.5), (-13.6, 56.5), (-10.8, 61.5), (-6.0, 65.3), (-2.0, 67.3), (0, 68.3)]
S(dome, OUTER, n=8); S([(-x, z) for x, z in dome], OUTER, n=8)
S([(-2.4, 66.5), (0, 67.0), (2.4, 66.5)], n=4)
L([(0, 68.3), (0, 74.5)], OUTER)
for z, r in ((69.6, 0.9), (71.3, 0.65)):
    cv.circle(0, z, r)
S([(-0.9, 73), (0, 74.8), (0.9, 73)], n=3)
cv.save(sys.argv[1])
