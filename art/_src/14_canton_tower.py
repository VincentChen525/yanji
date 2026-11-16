"""14-canton-tower：广州塔。竖幅。单位米。塔身 454m + 天线到 600m。
双曲面：每根斜柱在三维里是直线，投影到立面仍是直线；一组斜柱交织出收腰的轮廓。
底部椭圆 80x60m，顶部椭圆 54x41m，顶面略倾斜。"""
import math, sys
from lineart import Canvas, OUTER, INNER
cv = Canvas("竖", seed=14)
L = cv.line
HT = 454.0
TW = math.radians(125)
N = 16


def top_z(x):  # 顶部倾斜：左高右低
    return HT - 6 * x / 27.0


cols = []
for i in range(N):
    th = 2 * math.pi * i / N
    xb = 40 * math.cos(th)
    xt = 27 * math.cos(th + TW)
    cols.append((xb, xt))
    L([(xb, 0), (xt, top_z(xt))])


def env(z):
    t = z / HT
    return max(abs(xb + (xt - xb) * t) for xb, xt in cols)


# 外轮廓（包络）
for s in (-1, 1):
    L([(s * env(HT * i / 60), HT * i / 60 if i < 60 else top_z(s * env(HT))) for i in range(61)], OUTER)
# 横向环梁
for k in range(1, 12):
    z = HT * k / 12
    w = env(z)
    L([(-w, z), (w, z)])
L([(-env(0), 0), (env(0), 0)], OUTER)
L([(-env(HT), top_z(-env(HT))), (env(HT), top_z(env(HT)))], OUTER)
L([(-52, 0), (52, 0)], OUTER)
# 天线：格构底段 + 细杆
L([(-6, HT - 2), (-3, 520), (3, 520), (6, HT - 2)], OUTER)
for z in range(462, 520, 12):
    a = 6 - 3 * (z - 454) / 66; b = 6 - 3 * (z + 12 - 454) / 66
    L([(-a, z), (b, min(z + 12, 520))]); L([(a, z), (-b, min(z + 12, 520))])
L([(-1.2, 520), (-0.5, 600), (0.5, 600), (1.2, 520)], OUTER)
for z in (545, 570):
    L([(-1.0, z), (1.0, z)])
cv.save(sys.argv[1])
