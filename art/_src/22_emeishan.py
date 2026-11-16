"""22-emeishan：峨眉山金顶。横幅。单位 km（示意）。
不对称：左侧长而缓的林坡升到顶部，右端戛然而止为巨大的垂直绝壁（带横向岩层）；
崖边一座小殿和多面普贤金像（为可辨认，尺寸放大约 3 倍）；崖下几道云海线。"""
import sys, random, math
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull
cv = Canvas("横", seed=22)
rnd = random.Random(22)
CL = 0.35
EDGE = 1.45
sil = ridge([(-3.0, CL), (-2.3, 0.55), (-1.5, 0.8), (-0.7, 1.02), (0.2, 1.2), (0.9, 1.3), (EDGE, 1.34)], 0.025, 1) + \
      ridge([(EDGE, 1.34), (EDGE + 0.03, 1.0), (EDGE + 0.05, 0.65), (EDGE + 0.08, CL)], 0.01, 2)[1:]
SKY = sky(sil)
# 崖顶边缘：从左坡中段斜上到崖角，边缘以下为岩壁
rim = ridge([(-0.3, 1.02), (0.4, 1.14), (1.0, 1.24), (EDGE, 1.33)], 0.015, 3)
FACE = rim + [(EDGE + 0.08, CL), (-0.3, CL)]
# 金像与小殿
bx = 1.3
statue = [(bx - 0.035, 1.33), (bx + 0.035, 1.33), (bx + 0.035, 1.4), (bx + 0.022, 1.4), (bx + 0.022, 1.45),
          (bx + 0.01, 1.47), (bx + 0.01, 1.52), (bx - 0.01, 1.52), (bx - 0.01, 1.47), (bx - 0.022, 1.45), (bx - 0.022, 1.4), (bx - 0.035, 1.4)]
tx = 1.05
hall = [(tx - 0.09, 1.28), (tx + 0.09, 1.28), (tx + 0.09, 1.34), (tx + 0.12, 1.345), (tx + 0.04, 1.4), (tx - 0.04, 1.4), (tx - 0.12, 1.345), (tx - 0.09, 1.34)]
FRONT = [statue, hall]
cv.line(sil, OUTER, hide=FRONT)
cv.line(rim, INNER, hide=FRONT)
# 岩壁：横向岩层（断续）+ 竖裂
for k in range(9):
    z = CL + 0.06 + k * 0.095
    xs = [x for x, zz in rim if zz >= z + 0.04]
    if not xs:
        continue
    x0 = max(min(xs), -0.25)
    x = x0
    while x < EDGE:
        ln = rnd.uniform(0.12, 0.35)
        cv.line([(x, z + rnd.uniform(-0.01, 0.01)), (min(x + ln, EDGE + 0.05), z + 0.012)], INNER, hide=[SKY] + FRONT)
        x += ln + rnd.uniform(0.04, 0.1)
for x in (0.1, 0.45, 0.75, 1.05, 1.3):
    zt = max(z for xx, z in rim if xx <= x + 0.02) - 0.02
    cv.line(ridge([(x, zt), (x + 0.02, (zt + CL) / 2), (x + 0.03, CL)], 0.03, int(x * 100) + 40), INNER, hide=[SKY] + FRONT)
# 左坡：树冠起伏的短弧
for i in range(26):
    x = -2.8 + i * 0.12 + rnd.uniform(-0.03, 0.03)
    zt = max(z for xx, z in sil if xx <= x + 0.001)
    if x > -0.35:
        break
    for d in (0.08, 0.2):
        z = zt - d - rnd.uniform(0, 0.08)
        if z > CL + 0.03:
            cv.line(catmull([(x - 0.04, z), (x, z + 0.025), (x + 0.04, z)], 4), INNER)
# 金像
L = cv.line
L([(bx - 0.035, 1.33), (bx - 0.035, 1.4), (bx + 0.035, 1.4), (bx + 0.035, 1.33)], OUTER)
L([(bx - 0.035, 1.365), (bx + 0.035, 1.365)])
L(catmull([(bx - 0.022, 1.4), (bx - 0.025, 1.43), (bx - 0.012, 1.455), (bx + 0.012, 1.455), (bx + 0.025, 1.43), (bx + 0.022, 1.4)], 4))
for cx, cz, r in [(bx, 1.47, 0.011), (bx - 0.012, 1.488, 0.008), (bx + 0.012, 1.488, 0.008), (bx, 1.506, 0.008), (bx, 1.522, 0.006)]:
    cv.circle(cx, cz, r)
# 小殿
L([(tx - 0.09, 1.28), (tx - 0.09, 1.34), (tx + 0.09, 1.34), (tx + 0.09, 1.28)], OUTER)
L(catmull([(tx - 0.12, 1.345), (tx - 0.06, 1.37), (tx - 0.04, 1.4), (tx + 0.04, 1.4), (tx + 0.06, 1.37), (tx + 0.12, 1.345)], 4), OUTER)
L([(tx - 0.12, 1.345), (tx + 0.12, 1.345)])
for x in (-0.05, 0, 0.05):
    L([(tx + x, 1.285), (tx + x, 1.335)])
# 云海
for z, amp, sd in [(CL, 0.02, 1), (CL - 0.08, 0.016, 2), (CL - 0.16, 0.014, 3)]:
    pts = [(-3.1 + 4.9 * i / 40, z + amp * math.sin(i * 1.1 + sd * 2) + rnd.uniform(-0.006, 0.006)) for i in range(41)]
    cv.smooth(pts, INNER, n=4)
cv.save(sys.argv[1])
