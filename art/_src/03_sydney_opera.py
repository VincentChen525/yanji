"""03-sydney-opera：悉尼歌剧院侧立面（从港湾看）。横幅。单位米。
两排帆形壳体（前排略低、后排更高并右移）+ 右端小餐厅壳体，坐在低矮的阶梯式台基上。
壳体之间用消隐处理：后面的壳只画露出来的部分。"""
import math, sys
from lineart import Canvas, OUTER, INNER, catmull
cv = Canvas("横", seed=3)
L, S = cv.line, cv.smooth
BASE = 14.0


def shell(xt, zt):
    h = zt - BASE
    left = catmull([(xt, zt), (xt + 0.03 * h, zt - 0.45 * h), (xt + 0.14 * h, BASE)], 8)
    right = catmull([(xt, zt), (xt + 0.5 * h, zt - 0.12 * h), (xt + 0.86 * h, zt - 0.52 * h), (xt + 1.02 * h, BASE)], 8)
    poly = left + list(reversed(right))
    return left, right, poly, h


front = [(-66, 56), (-40, 47), (-17, 36), (2, 24)]
back = [(-36, 68), (-6, 58), (19, 45), (38, 28)]
rest = [(58, 30), (71, 22)]
order = front + rest + back          # 越靠前越先，后面的被前面的遮挡
polys = []
for i, (xt, zt) in enumerate(order):
    left, right, poly, h = shell(xt, zt)
    hide = polys[:]
    L(left, OUTER, hide=hide)
    L(right, OUTER, hide=hide)
    # 壳面肋线：从尖端放射到底边
    for f in (0.35, 0.58, 0.8):
        rib = catmull([(xt, zt), (xt + (0.03 + 0.47 * f) * h, zt - (0.45 - 0.33 * f) * h),
                       (xt + (0.14 + 0.88 * f) * h, BASE)], 8)
        L(rib, INNER, hide=hide)
    polys.append(poly)
# 台基：前沿 + 阶梯
L([(-100, 0), (-100, BASE), (88, BASE)], OUTER)
L([(-100, BASE - 3), (88, BASE - 3)])
for x in range(-92, 88, 9):
    L([(x, 1), (x, BASE - 3.5)])
for i in range(8):           # 右端大台阶
    x0 = 88 + i * 4.5
    z = BASE - BASE * i / 8
    L([(x0, z), (x0, z - BASE / 8), (x0 + 4.5, z - BASE / 8)], OUTER if i in (0, 7) else INNER)
L([(88, BASE), (88, BASE - BASE / 8)], OUTER)
L([(-106, 0), (130, 0)], OUTER)
cv.save(sys.argv[1])
