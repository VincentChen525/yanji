"""24-matterhorn：马特洪峰，从采尔马特看。方幅。单位 km（示意）。
参考照片：峰顶为略向左勾的尖岩头；正对观者的霍恩利山脊把左（东壁，受光）右（北壁）两面分开，
山脊中段有平缓的“肩”；右侧兹穆特脊下段也有一处肩；两壁有斜向岩层与积雪的岩台；山脚冰川。"""
import sys, random
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull, glacier_marks
cv = Canvas("方", seed=24, sx=0.8)
rnd = random.Random(24)
# 峰顶岩头向左探出成“鹰嘴”：左侧先外凸、再向内回收（下方有内凹），然后才是东脊
head = [(0.0, 1.0), (-0.045, 0.99), (-0.1, 0.968), (-0.082, 0.948), (-0.088, 0.92), (-0.095, 0.895)]
left = head + ridge([(-0.095, 0.895), (-0.15, 0.82), (-0.23, 0.7), (-0.3, 0.6), (-0.37, 0.53),
              (-0.48, 0.42), (-0.61, 0.29), (-0.75, 0.14), (-0.87, 0.0)], 0.018, 1)[1:]
right = ridge([(0.0, 1.0), (0.04, 0.985), (0.075, 0.955), (0.15, 0.86), (0.25, 0.74), (0.33, 0.63), (0.38, 0.575), (0.43, 0.55),
               (0.5, 0.47), (0.61, 0.33), (0.74, 0.17), (0.88, 0.0)], 0.018, 2)
sil = list(reversed(left)) + right[1:]
SKY = sky(sil)
cv.line(sil, OUTER)
cv.line([(-0.98, 0), (1.0, 0)], OUTER)
hornli = ridge([(-0.02, 0.995), (-0.03, 0.9), (-0.01, 0.84), (0.02, 0.74), (0.07, 0.6), (0.1, 0.55), (0.15, 0.52), (0.2, 0.43), (0.26, 0.28), (0.31, 0.15)], 0.012, 3)
cv.line(hornli, OUTER)


def x_at(line, z):
    for (x0, z0), (x1, z1) in zip(line, line[1:]):
        if (z0 - z) * (z1 - z) <= 0 and z0 != z1:
            return x0 + (x1 - x0) * (z - z0) / (z1 - z0)
    return line[-1][0]


# 东壁上一道次脊（弗尔根脊在壁面上的投影）
cv.line(ridge([(-0.1, 0.85), (-0.13, 0.7), (-0.19, 0.5), (-0.25, 0.32)], 0.025, 4), INNER, hide=[SKY])
# 斜向岩层/雪台：每面 9 道，短而断续，左面向左下，右面向右下
for k in range(9):
    z = 0.2 + k * 0.08 + rnd.uniform(-0.015, 0.015)
    xh, xl, xr = x_at(hornli, z), x_at(left, z), x_at(right, z)
    for side, xe in ((-1, xl), (1, xr)):
        span = abs(xe - xh)
        a = xh + side * span * rnd.uniform(0.1, 0.35)
        b = a + side * span * rnd.uniform(0.18, 0.35)
        cv.line([(a, z), ((a + b) / 2, z - abs(b - a) * 0.12), (b, z - abs(b - a) * 0.3)], INNER, hide=[SKY])
# 北壁的冰槽：几道近乎平行于山脊的细长线
for z0, f in [(0.85, 0.35), (0.75, 0.6), (0.62, 0.45)]:
    xa, xb = x_at(hornli, z0), x_at(right, z0)
    x0 = xa + (xb - xa) * f
    cv.line([(x0, z0), (x0 + 0.06, z0 - 0.18)], INNER, hide=[SKY])
# 山脚冰川：上缘线 + 竖向冰裂
gl = ridge([(-0.74, 0.12), (-0.4, 0.17), (0.0, 0.14), (0.4, 0.17), (0.76, 0.12)], 0.02, 10)
cv.line(gl, INNER, hide=[SKY])
glacier_marks(cv, -0.65, 0.68, 0.14, 0.02, seed=24)
cv.save(sys.argv[1])
