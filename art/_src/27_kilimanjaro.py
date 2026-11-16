"""27-kilimanjaro：乞力马扎罗，从稀树草原看。横幅。单位 km，竖向夸张 1.8 倍（实景约 10:1）。
极宽缓的火山体，平顶的基博峰，顶缘挂着几片冰川（冰崖用短竖线）；左侧肩上是参差的马文济峰；地平线上两棵平顶金合欢。"""
import sys, random
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull
cv = Canvas("横", seed=27)
VEX = 1.8
def V(pts): return [(x, z * VEX) for x, z in pts]
rnd = random.Random(27)
sil = V(ridge([(-24, 0.0), (-19, 0.9), (-15.5, 2.1), (-14.3, 2.75)], 0.03, 1)
        + [(-13.8, 3.2), (-13.55, 3.05), (-13.3, 3.45), (-13.05, 3.2), (-12.8, 3.4), (-12.45, 3.1), (-12.1, 3.2), (-11.6, 2.95)]
        + ridge([(-11.6, 2.95), (-9.0, 3.0), (-6.5, 3.6), (-4.6, 4.35)], 0.02, 2)
        + catmull([(-4.6, 4.35), (-3.6, 4.68), (-2.0, 4.8), (0.0, 4.86), (2.0, 4.8), (3.2, 4.68), (4.2, 4.38)], 6)[1:]
        + ridge([(4.2, 4.38), (6.5, 3.6), (10.0, 2.4), (14.0, 1.3), (18.0, 0.5), (22.0, 0.0)], 0.02, 3)[1:])
SKY = sky(sil)
cv.line(sil, OUTER)
cv.line([(-25, 0), (23, 0)], OUTER)
# 顶缘冰川：几片，下沿不规则，前缘有冰崖短竖线
for x0, x1, sd in [(-3.9, -2.2, 4), (-1.7, 0.6, 5), (1.0, 2.2, 6), (2.6, 3.6, 7)]:
    r = random.Random(sd)
    top = [(x, 4.86 - 0.012 * x * x * 0.1 - (0.25 if abs(x) > 3.3 else 0.06 if abs(x) > 2.5 else 0.0)) for x in [x0 + (x1 - x0) * i / 8 for i in range(9)]]
    bot = []
    for i in range(9):
        x = x1 - (x1 - x0) * i / 8
        zt = top[8 - i][1]
        bot.append((x, zt - r.uniform(0.18, 0.42)))
    cv.line(V(catmull(bot, 3)), INNER, hide=[SKY])
    for x, z in bot[1:-1:2]:
        cv.line(V([(x, z), (x, z + 0.12)]), INNER, hide=[SKY])
# 坡面：几道长而缓的放射脊线
for pts, sd in [([(-3.0, 4.4), (-6.0, 3.0), (-9.5, 1.6)], 8), ([(-1.0, 4.4), (-2.5, 2.8), (-4.5, 1.2)], 9),
                ([(1.5, 4.4), (3.0, 2.9), (5.5, 1.2)], 10), ([(3.5, 4.2), (7.0, 2.6), (11.0, 1.1)], 11),
                ([(-12.8, 2.9), (-13.5, 2.0), (-14.5, 1.2)], 12)]:
    cv.line(V(ridge(pts, 0.03, sd)), INNER, hide=[SKY])
# 金合欢：平顶伞形树冠 + 分叉的干
def acacia(x, h, w):
    z0 = 0.0
    cz = h
    canopy = catmull([(x - w / 2, cz), (x - w * 0.42, cz + h * 0.16), (x - w * 0.2, cz + h * 0.24), (x + w * 0.05, cz + h * 0.22),
                      (x + w * 0.3, cz + h * 0.25), (x + w * 0.48, cz + h * 0.14), (x + w / 2, cz)], 4)
    cv.line(canopy + [(x + w * 0.2, cz - h * 0.04), (x - w * 0.25, cz - h * 0.03), (x - w / 2, cz)], INNER)
    cv.line([(x, z0), (x + 0.05 * w, h * 0.55), (x - 0.25 * w, cz - h * 0.03)], INNER)
    cv.line([(x + 0.05 * w, h * 0.55), (x + 0.25 * w, cz - h * 0.04)], INNER)
    cv.line([(x + 0.05 * w, h * 0.55), (x + 0.02 * w, cz - h * 0.04)], INNER)
acacia(-8.0, 2.6, 6.4)
acacia(10.0, 2.0, 4.8)
cv.save(sys.argv[1])
