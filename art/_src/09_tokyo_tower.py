"""09-tokyo-tower：东京塔正立面。竖幅。单位米。总高 333m，塔脚宽约 80m。
与埃菲尔铁塔区分：腿几乎是直线、塔身更瘦更硬；主展望台为方盒；天线很长；塔脚间有矮楼。"""
import math, sys
from lineart import Canvas, OUTER, INNER
cv = Canvas("竖", seed=9)
L = cv.line


def hw(z):  # 外缘半宽：近乎直线，底部略外撇
    return 5.5 + 34.5 * (1 - z / 250.0) ** 1.35 if z < 250 else 5.5


def iw(z):  # 腿内缘，约 70m 处合拢
    return 0 if z >= 70 else hw(z) * 0.62 * (1 - (z / 70.0) ** 1.6)


MAIN0, MAIN1, TOP0, TOP1 = 145.0, 160.0, 246.0, 253.0
for s in (-1, 1):
    for z0, z1 in ((18, MAIN0), (MAIN1, TOP0)):
        L([(s * hw(z0 + (z1 - z0) * i / 30), z0 + (z1 - z0) * i / 30) for i in range(31)], OUTER)
    L([(s * iw(18 + 52 * i / 20), 18 + 52 * i / 20) for i in range(21)], OUTER)


def panels(z0, z1, n):
    zs = [z0 + (z1 - z0) * i / n for i in range(n + 1)]
    for a, b in zip(zs, zs[1:]):
        for s in (-1, 1):
            ia, ib = iw(a), iw(b)
            oa, ob = hw(a), hw(b)
            if ib > 0:
                L([(s * ia, a), (s * ob, b)]); L([(s * oa, a), (s * ib, b)])
            else:  # 合拢后：每侧两格，中线分隔
                ma, mb = oa / 2, ob / 2
                L([(0, a), (s * mb, b)]); L([(s * ma, a), (0, b)])
                L([(s * ma, a), (s * ob, b)]); L([(s * oa, a), (s * mb, b)])
                L([(s * ma, a), (s * mb, b)])
        if b < z1:
            L([(-hw(b), b), (hw(b), b)]) if iw(b) == 0 else [L([(s * iw(b), b), (s * hw(b), b)]) for s in (-1, 1)]
    if iw(z1) == 0:
        L([(0, z0 if iw(z0) == 0 else 70), (0, z1)])


panels(18, 70, 3)
panels(70, MAIN0, 5)
panels(MAIN1, TOP0, 7)
# 主展望台：两层方盒
w0 = hw(MAIN0) + 4
cv.rect(-w0, MAIN0, w0, MAIN1, OUTER)
L([(-w0, (MAIN0 + MAIN1) / 2), (w0, (MAIN0 + MAIN1) / 2)])
for i in range(1, 8):
    x = -w0 + 2 * w0 * i / 8
    L([(x, MAIN0 + 1), (x, MAIN1 - 1)])
# 特别展望台
cv.rect(-9, TOP0, 9, TOP1, OUTER)
L([(-9, (TOP0 + TOP1) / 2), (9, (TOP0 + TOP1) / 2)])
# 天线：先一段细格构，再一根杆
L([(-4.2, TOP1), (-2.0, 292)], OUTER); L([(4.2, TOP1), (2.0, 292)], OUTER)
for z in range(258, 292, 8):
    a = 4.2 - 2.2 * (z - TOP1) / 39; b = 4.2 - 2.2 * (z + 8 - TOP1) / 39
    L([(-a, z), (b, z + 8)]); L([(a, z), (-b, z + 8)])
L([(-2.0, 292), (2.0, 292)], OUTER)
L([(0, 292), (0, 333)], OUTER)
L([(-1.2, 310), (1.2, 310)])
# 塔脚间矮楼（FootTown）
cv.rect(-46, 0, 46, 18, OUTER)
for z in (6, 12):
    L([(-46, z), (46, z)])
for i in range(1, 12):
    x = -46 + 92 * i / 12
    L([(x, 1), (x, 17)])
L([(-56, 0), (56, 0)], OUTER)
cv.save(sys.argv[1])
