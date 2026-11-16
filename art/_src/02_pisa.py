"""02-pisa：比萨斜塔。竖幅。单位米。高 56m，底径 15.5m，向右倾约 4°。
圆柱用余弦投影画柱廊：每圈 30 根柱，正面可见约一半，越靠两侧越密，表现圆柱体积。"""
import math, sys
from lineart import Canvas, OUTER, INNER
cv = Canvas("竖", seed=2)
TILT = math.radians(4.0)
pts_all = []


def T(x, z):  # 绕塔基中心倾斜
    return (x * math.cos(TILT) + z * math.sin(TILT), -x * math.sin(TILT) + z * math.cos(TILT))


def L(pts, w=INNER):
    cv.line([T(x, z) for x, z in pts], w)


R = 7.7
# 底层：盲拱 + 基座台阶
L([(-R - 0.6, 0), (-R - 0.6, 1.0), (R + 0.6, 1.0), (R + 0.6, 0)], OUTER)
storeys = [(1.0, 11.3)] + [(11.3 + 6.6 * i, 11.3 + 6.6 * (i + 1)) for i in range(6)]
for k, (z0, z1) in enumerate(storeys):
    L([(-R, z0), (-R, z1)], OUTER); L([(R, z0), (R, z1)], OUTER)
    # 楼层檐口（略凸出）
    L([(-R - 0.45, z1), (R + 0.45, z1)], OUTER)
    L([(-R - 0.45, z1 - 0.55), (R + 0.45, z1 - 0.55)], INNER)
    n = 15 if k == 0 else 30
    angs = [-90 + 360 / n * i for i in range(n // 2 + 1)]
    xs = [R * math.sin(math.radians(a)) for a in angs]
    zc = z1 - 0.55
    spring = z0 + (z1 - z0) * (0.68 if k == 0 else 0.62)
    for a, b in zip(xs, xs[1:]):
        if abs(b - a) < 0.35:
            continue
        top = spring + (b - a) / 2 * 0.95
        # 柱
        if k > 0:
            L([(a, z0 + 0.6), (a, spring)])
        else:
            L([(a, z0), (a, spring)])
        # 拱
        L([(a + (b - a) / 2 * (1 - math.cos(math.pi * i / 10)), spring + (b - a) / 2 * 0.95 * math.sin(math.pi * i / 10))
           for i in range(11)])
    if k > 0:  # 每层廊道的栏杆线
        L([(-R, z0 + 0.6), (R, z0 + 0.6)])
# 钟楼：较窄
Rb = 5.6
z0, z1 = storeys[-1][1], storeys[-1][1] + 5.2
L([(-Rb, z0), (-Rb, z1), (Rb, z1), (Rb, z0)], OUTER)
L([(-Rb - 0.4, z1), (Rb + 0.4, z1)], OUTER)
for a in (-50, -15, 15, 50):
    x = Rb * math.sin(math.radians(a))
    w = 0.9 * math.cos(math.radians(a))
    L([(x - w, z0 + 0.8), (x - w, z0 + 3.2)] + [(x - w * math.cos(math.pi * i / 8), z0 + 3.2 + w * math.sin(math.pi * i / 8)) for i in range(9)]
      + [(x + w, z0 + 0.8)])
# 地面
cv.line([(-R - 4, 0), (R + 5, 0)], OUTER)
cv.save(sys.argv[1])
