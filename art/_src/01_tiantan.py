"""01-tiantan：天坛祈年殿正立面。方幅。单位米。
三层汉白玉圆台（每层带栏杆）+ 中央御路台阶；殿身三重檐圆攒尖，檐口外翘，顶部鎏金宝顶。"""
import math, sys
from lineart import Canvas, OUTER, INNER, catmull
cv = Canvas("方", seed=1)
L, S = cv.line, cv.smooth
# 圆台三层：(底, 顶, 半宽)
tiers = [(0, 2.2, 45), (2.2, 4.4, 39), (4.4, 6.6, 33)]
stair = 5.0
for z0, z1, w in tiers:
    for s in (-1, 1):
        L([(s * stair, z0), (s * w, z0), (s * w, z1), (s * stair, z1)], OUTER if z0 == 0 else OUTER)
    # 栏杆：扶手线 + 望柱
    L([(-w + 0.3, z1 + 1.1), (-stair, z1 + 1.1)]); L([(stair, z1 + 1.1), (w - 0.3, z1 + 1.1)])
    n = int((w - stair) / 2.2)
    for s in (-1, 1):
        for i in range(n + 1):
            x = s * (stair + (w - stair - 0.3) * i / n)
            L([(x, z1), (x, z1 + 1.45)])
    # 台面下沿石线
    L([(-w, z0 + 0.6), (-stair, z0 + 0.6)]); L([(stair, z0 + 0.6), (w, z0 + 0.6)])
# 中央御路台阶
L([(-stair, 0), (-stair, 6.6)], OUTER); L([(stair, 0), (stair, 6.6)], OUTER)
cv.rect(-1.8, 0, 1.8, 6.6)
for i in range(1, 12):
    z = 6.6 * i / 12
    L([(-stair, z), (-1.8, z)]); L([(1.8, z), (stair, z)])
L([(-50, 0), (50, 0)], OUTER)
# 殿身
Z0 = 6.6
def eave(zb, w_tip, w_top, h, w_drum):
    """一重檐：檐口外翘的弧线屋面 + 檐下斗拱带。"""
    # 屋面轮廓（左右）
    for s in (-1, 1):
        S([(s * w_top, zb + h), (s * (w_top + (w_tip - w_top) * 0.45), zb + h * 0.55),
           (s * (w_tip - 0.6), zb + 0.5), (s * (w_tip + 0.3), zb + 0.9)], OUTER, n=8)
    # 檐口下沿：中间略低、两端起翘
    S([(-w_tip - 0.3, zb + 0.9), (-w_tip + 1.5, zb), (0, zb - 0.3), (w_tip - 1.5, zb), (w_tip + 0.3, zb + 0.9)], OUTER, n=10)
    # 瓦垄
    for i in range(-6, 7):
        f = i / 6.5
        S([(f * w_top, zb + h - 0.2), (f * (w_top + (w_tip - w_top) * 0.5), zb + h * 0.5), (f * (w_tip - 1.2), zb + 0.2)], n=5)
    # 斗拱带
    L([(-w_drum, zb - 0.3), (-w_drum, zb - 1.3), (w_drum, zb - 1.3), (w_drum, zb - 0.3)])
    for i in range(1, 14):
        x = -w_drum + 2 * w_drum * i / 14
        L([(x, zb - 1.3), (x, zb - 0.5)])
# 一层殿身：槅扇门
L([(-13, Z0 + 1.0), (-13, Z0 + 9.5)], OUTER); L([(13, Z0 + 1.0), (13, Z0 + 9.5)], OUTER)
L([(-14, Z0), (-14, Z0 + 1.0), (14, Z0 + 1.0), (14, Z0)], OUTER)
for i in range(1, 10):
    x = -13 + 26 * i / 10
    L([(x, Z0 + 1.0), (x, Z0 + 9.5)])
L([(-13, Z0 + 6.8), (13, Z0 + 6.8)])
eave(Z0 + 10.8, 18.5, 11.5, 3.6, 13)
# 二层
L([(-10.5, Z0 + 14.4), (-10.5, Z0 + 18.0)], OUTER); L([(10.5, Z0 + 14.4), (10.5, Z0 + 18.0)], OUTER)
for i in range(1, 8):
    x = -10.5 + 21 * i / 8
    L([(x, Z0 + 14.6), (x, Z0 + 18.0)])
eave(Z0 + 19.3, 15.0, 8.5, 3.2, 10.5)
# 三层 + 攒尖顶
L([(-8.0, Z0 + 22.5), (-8.0, Z0 + 26.0)], OUTER); L([(8.0, Z0 + 26.0), (8.0, Z0 + 22.5)], OUTER)
for i in range(1, 6):
    x = -8 + 16 * i / 6
    L([(x, Z0 + 22.7), (x, Z0 + 26.0)])
zb = Z0 + 27.3
for s in (-1, 1):
    S([(0, zb + 8.6), (s * 3.5, zb + 6.2), (s * 7.5, zb + 3.2), (s * 11.3, zb + 0.5), (s * 12.3, zb + 0.9)], OUTER, n=8)
S([(-12.3, zb + 0.9), (-10.8, zb), (0, zb - 0.3), (10.8, zb), (12.3, zb + 0.9)], OUTER, n=10)
for i in range(-5, 6):
    f = i / 5.5
    S([(f * 1.0, zb + 8.3), (f * 5.5, zb + 4.2), (f * 10.5, zb + 0.2)], n=5)
L([(-8, zb - 0.3), (-8, zb - 1.3), (8, zb - 1.3), (8, zb - 0.3)])
# 宝顶
cv.rect(-1.0, zb + 8.6, 1.0, zb + 9.6)
cv.circle(0, zb + 11.0, 1.5, OUTER)
L([(0, zb + 12.5), (0, zb + 13.6)], OUTER)
cv.save(sys.argv[1])
