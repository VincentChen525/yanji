"""07-giza：胡夫金字塔，略偏一角看，露出两个面。横幅。单位米。高 139m，底边 230m。
用简单的三维正交投影（略带俯视）算出两面，水平石层线随面走向；塔尖略钝。"""
import math, sys, random
from lineart import Canvas, OUTER, INNER
cv = Canvas("横", seed=7)
L = cv.line
A = math.radians(28)      # 绕竖轴转角
TILT = 0.14               # 俯视程度：深度对竖直位置的影响
HB, HT = 115.0, 139.0


def proj(x, y, z):  # x 右，y 远，z 上
    xr = x * math.cos(A) - y * math.sin(A)
    yr = x * math.sin(A) + y * math.cos(A)
    return (xr, z - yr * TILT)


corners = [(-HB, -HB), (HB, -HB), (HB, HB), (-HB, HB)]
cp = [proj(x, y, 0) for x, y in corners]
front = min(range(4), key=lambda i: cp[i][1])    # 最低的那个角离观者最近
lft, rgt = (front - 1) % 4, (front + 1) % 4
TOPF = 0.965   # 钝顶


def at(c, f):  # 沿角到塔尖的棱，高度比例 f
    x, y = corners[c]
    return proj(x * (1 - f), y * (1 - f), HT * f)


apex_l, apex_r, apex_f = at(lft, TOPF), at(rgt, TOPF), at(front, TOPF)
L([cp[lft], apex_l, apex_f, apex_r, cp[rgt]], OUTER)
L([cp[lft], cp[front], cp[rgt]], OUTER)
L([cp[front], apex_f], OUTER)
# 石层线：越往上越密一点点；局部断开显得残损
rnd = random.Random(3)
n = 26
for k in range(1, n):
    f = (k / n) ** 1.05 * TOPF
    for c in (lft, rgt):
        p, q = at(c, f), at(front, f)
        if rnd.random() < 0.25:
            t = rnd.uniform(0.25, 0.7)
            m1 = (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
            m2 = (p[0] + (q[0] - p[0]) * (t + 0.08), p[1] + (q[1] - p[1]) * (t + 0.08))
            L([p, m1]); L([m2, q])
        else:
            L([p, q])
# 地面：一条细沙线
L([(cp[lft][0] - 45, cp[lft][1]), (cp[lft][0] - 4, cp[lft][1])])
L([(cp[rgt][0] + 4, cp[rgt][1]), (cp[rgt][0] + 45, cp[rgt][1])])
cv.save(sys.argv[1])
