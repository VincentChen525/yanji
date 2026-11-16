"""23-fuji：富士山（河口湖方向）。横幅 1536x1024。单位：km（示意）。
参考：Wikimedia Commons 河口湖/大涌谷方向照片——
  · 山顶为较宽的平台，火山口边缘微有起伏；
  · 上半坡近乎直线（约 33–37°），下部才明显外撇成凹曲线；
  · 雪线不是规则锯齿，而是顺着放射状冲沟向下伸出的长短不一的雪舌，两侧雪舌更长；
  · 雪面上有细密的放射状冲沟，山腰散布小寄生火山。
宽高比约 3.4:1（照片约 3.8:1，略作收紧以利构图）。
"""
import math
import random
import sys
from lineart import Canvas, OUTER, INNER

H = 3.7               # 山顶高度
C = 0.40              # 山顶平台半宽
L_LEFT = 5.85         # 左坡水平长度（平台边到山脚）
L_RIGHT = 6.05        # 右坡略长，略带不对称
P = 1.22              # 坡面凹度
TAIL = 0.12

cv = Canvas("横", seed=23)
random.seed(230)


def bump(x, x0, w, a):
    return a * math.exp(-((x - x0) / w) ** 2)


def h(x):
    if abs(x) <= C:
        return H
    L = L_LEFT if x < 0 else L_RIGHT
    u = min(1.0, (abs(x) - C) / L)
    z = H * (1 - u) ** P
    # 左下坡两座小寄生火山，右坡一处缓肩
    z += bump(x, -4.3, 0.28, 0.10) + bump(x, -5.0, 0.22, 0.06)
    return z


def x_on_slope(z, side):
    L = L_LEFT if side < 0 else L_RIGHT
    return side * (C + (1 - (z / H) ** (1 / P)) * L)


# ---------- 外轮廓 ----------
N = 120
xl0, xr0 = -C - L_LEFT, C + L_RIGHT
left = [(xl0 - TAIL, 0)] + [(xl0 + (-C - xl0) * i / N, h(xl0 + (-C - xl0) * i / N)) for i in range(N + 1)]
right = [(C + (xr0 - C) * i / N, h(C + (xr0 - C) * i / N)) for i in range(N + 1)] + [(xr0 + TAIL, 0)]
rim = [(-C, H), (-0.31, H + 0.05), (-0.22, H + 0.03), (-0.15, H + 0.065), (-0.05, H + 0.02),
       (0.05, H + 0.035), (0.16, H - 0.005), (0.27, H + 0.03), (C, H)]
cv.line(left, OUTER)
cv.smooth(rim, OUTER, n=5)
cv.line(right, OUTER)

# ---------- 坡面坐标 ----------
# f ∈ [-1, 1]：在同一高度上横跨山体的比例位置。f 固定的线就是视觉上的坡面落水线，
# 雪舌、冲沟都沿这种线走，自然地随山体向下张开，且永远不会画出轮廓。
def P_(f, z):
    return (f * abs(x_on_slope(z, 1 if f >= 0 else -1)), z)


def fall_line(f, z0, z1, n=8):
    return [P_(f, z0 + (z1 - z0) * i / n) for i in range(n + 1)]


# ---------- 雪舌 ----------
n_t = 10
tongues = []
for i in range(n_t):
    f = -0.9 + 1.8 * (i + 0.5) / n_t + random.uniform(-0.03, 0.03)
    edge = abs(f)
    tip = random.uniform(0.42, 0.52) + 0.12 * edge ** 2
    if i in (2, 6):
        tip -= random.uniform(0.07, 0.1)
    df = 1.8 / n_t * random.uniform(0.34, 0.42)
    tongues.append((f, tip * H, df))

snow = []
for i, (f, zt, df) in enumerate(tongues):
    zr = random.uniform(0.63, 0.68) * H
    if i == 0:
        snow.append(P_(-1.0, zr + 0.06))
    s_last = zr + 0.06
    snow += [P_(f - df, zr), P_(f - df * 0.62, (zr * 0.55 + zt * 0.45)), P_(f - df * 0.2, zt + 0.07),
             P_(f, zt), P_(f + df * 0.22, zt + 0.08), P_(f + df * 0.6, (zr * 0.5 + zt * 0.5)), P_(f + df, zr)]
    if i < n_t - 1:
        fn = (f + df + tongues[i + 1][0] - tongues[i + 1][2]) / 2
        snow.append(P_(fn, random.uniform(0.68, 0.72) * H))
snow.append(P_(1.0, 0.0))
snow[-1] = P_(1.0, s_last)
cv.line(snow, INNER)

# ---------- 冲沟：只在约一半雪舌中央，止于舌身中段 ----------
for i, (f, zt, df) in enumerate(tongues):
    if abs(f) > 0.75 or i % 2:
        continue
    z0 = H - random.uniform(0.25, 0.4)
    cv.line(fall_line(f, z0, zt + (0.66 * H - zt) * 0.35), INNER)
for i, (f, zt, df) in enumerate(tongues):          # 雪线以下延续成一小段
    if i in (2, 5, 7):
        z1 = zt - random.uniform(0.15, 0.22)
        cv.line(fall_line(f, z1, z1 - random.uniform(0.35, 0.5)), INNER)

# ---------- 山腰坡面纹理：沿落水线的稀疏短线 ----------
for f, z0, ln in [(-0.66, 1.2, 0.45), (-0.36, 0.75, 0.42), (-0.82, 0.62, 0.35),
                  (0.58, 1.1, 0.45), (0.3, 0.7, 0.4), (0.8, 0.55, 0.32)]:
    cv.line(fall_line(f, z0, z0 - ln), INNER)

cv.save(sys.argv[1])
