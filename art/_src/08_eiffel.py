"""08-eiffel：埃菲尔铁塔正立面线描。生成 SVG（纯描边），尺寸 1024x1536。
按真实尺寸（米）建模，再映射到画布；线条加极轻的手绘抖动。
"""
import math
import random
import sys

W, H = 1024, 1536
INK = "#1F1D19"
OUTER, INNER = 6.0, 3.4          # 外轮廓 / 内部结构线宽
TOP_M = 330.0                    # 含天线总高（米）
Y_BASE, Y_TOP = H * 0.94, H * 0.06
S = (Y_BASE - Y_TOP) / TOP_M     # 像素/米
CX = W / 2

random.seed(8)


def X(m):
    return CX + m * S


def Y(z):
    return Y_BASE - z * S


# 外轮廓半宽：指数曲线，拟合 底62.5m / 一层≈35m / 二层≈20m / 顶≈7m
def outer(z):
    return 58.5 * math.exp(-z / 88.9) + 4.0


# 腿内侧半宽，约 185m 处四腿合拢
def inner(z):
    if z >= 185:
        return 0.0
    return outer(z) * 0.58 * (1 - (z / 185.0) ** 3)


# ---------- 手绘抖动 ----------
def wobble(pts, amp=0.9):
    """沿折线法向加平滑低频噪声。pts 为像素坐标。"""
    if len(pts) < 2:
        return pts
    # 先加密
    dense = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / 6))
        for i in range(n):
            t = i / n
            dense.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    dense.append(pts[-1])
    L = [0.0]
    for (x0, y0), (x1, y1) in zip(dense, dense[1:]):
        L.append(L[-1] + math.hypot(x1 - x0, y1 - y0))
    total = L[-1] or 1
    waves = [(random.uniform(0.6, 1.0) * amp, random.uniform(220, 520), random.uniform(0, 6.28)) for _ in range(2)]
    out = []
    for i, (x, y) in enumerate(dense):
        j0, j1 = max(0, i - 1), min(len(dense) - 1, i + 1)
        dx, dy = dense[j1][0] - dense[j0][0], dense[j1][1] - dense[j0][1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        # 两端收敛，避免接头错位
        fade = min(1.0, L[i] / 14, (total - L[i]) / 14)
        off = sum(a * math.sin(L[i] / wl * 6.283 + ph) for a, wl, ph in waves) * fade
        out.append((x + nx * off, y + ny * off))
    return out


paths = []


def line(pts_m, w=INNER, jitter=True):
    """pts_m: [(x米, z米)]"""
    pts = [(X(x), Y(z)) for x, z in pts_m]
    if jitter:
        pts = wobble(pts, 0.7 if w == OUTER else 0.45)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    paths.append((d, w))


def curve(f, z0, z1, sign=1, w=INNER, n=60):
    line([(sign * f(z0 + (z1 - z0) * i / n), z0 + (z1 - z0) * i / n) for i in range(n + 1)], w)


# ---------- 平台高度 ----------
P1_LO, P1_HI = 53.0, 62.0
P2_LO, P2_HI = 112.0, 118.0
P3_LO, P3_HI = 268.0, 279.0

for s in (-1, 1):
    # 外轮廓（分段，在平台处断开）
    curve(outer, 0, P1_LO, s, OUTER)
    curve(outer, P1_HI, P2_LO, s, OUTER)
    curve(outer, P2_HI, P3_LO, s, OUTER)
    # 腿内侧
    curve(inner, 0, P1_LO, s, OUTER)
    curve(inner, P1_HI, P2_LO, s, INNER)
    curve(inner, P2_HI, 185, s, INNER)
    # 腿脚底
    line([(s * inner(0), 0), (s * outer(0), 0)], OUTER)


def lattice(z0, z1, n, merged=False):
    """在 z0~z1 之间画 n 格横杆 + X 斜撑。merged 表示四腿已合成单一塔身。"""
    zs = [z0 + (z1 - z0) * (i / n) ** 1.0 for i in range(n + 1)]
    for a, b in zip(zs, zs[1:]):
        if merged or inner(b) <= 0.3:
            xa, xb = outer(a), outer(b)
            line([(-xa, a), (xb, b)])
            line([(xa, a), (-xb, b)])
        else:
            for s in (-1, 1):
                ia, ib = inner(a), inner(b)
                oa, ob = outer(a), outer(b)
                line([(s * ia, a), (s * ob, b)])
                line([(s * oa, a), (s * ib, b)])
    for z in zs[1:-1]:
        if merged or inner(z) <= 0.3:
            line([(-outer(z), z), (outer(z), z)])
        else:
            for s in (-1, 1):
                line([(s * inner(z), z), (s * outer(z), z)])


lattice(0, P1_LO, 4)
lattice(P1_HI, P2_LO, 5)
lattice(P2_HI, 185, 5)
lattice(185, P3_LO, 7, merged=True)

# ---------- 底部大拱 ----------
def arch(r_shrink, top_z, w):
    za = 13.0
    xa = inner(za) - r_shrink
    pts = []
    n = 48
    for i in range(n + 1):
        t = math.pi * i / n
        x = -xa * math.cos(t)
        z = za + (top_z - za) * math.sin(t) ** 0.85
        pts.append((x, z))
    line(pts, w)


arch(0, 47.0, OUTER)
arch(2.2, 44.5, INNER)

# ---------- 平台 ----------
def deck(z0, z1, extra, arches, w=OUTER):
    hw = outer(z0) + extra
    line([(-hw, z0), (hw, z0), (hw, z1), (-hw, z1), (-hw, z0)], w)
    # 栏杆细线 + 一排小拱窗
    zm = z0 + (z1 - z0) * 0.45
    line([(-hw, zm), (hw, zm)])
    step = 2 * hw / arches
    for i in range(arches):
        x0 = -hw + step * i + step * 0.28
        x1 = x0 + step * 0.44
        line([(x0, zm), (x0, z1 - 1.6), ((x0 + x1) / 2, z1 - 0.6), (x1, z1 - 1.6), (x1, zm)])


deck(P1_LO, P1_HI, 3.5, 14)
deck(P2_LO, P2_HI, 2.5, 8)

# ---------- 顶层 + 穹顶 + 天线 ----------
hw3 = 9.0
line([(-hw3, P3_LO), (hw3, P3_LO), (hw3, P3_HI), (-hw3, P3_HI), (-hw3, P3_LO)], OUTER)
for i in range(1, 5):
    x = -hw3 + 2 * hw3 * i / 5
    line([(x, P3_LO + 2.5), (x, P3_HI - 2.0)])
# 灯笼间
line([(-5.0, P3_HI), (-5.0, 287), (5.0, 287), (5.0, P3_HI)], OUTER)
line([(-6.0, 287), (6.0, 287)], OUTER)
# 小穹顶
dome = [(-4.2 * math.cos(math.pi * i / 24), 287 + 5.5 * math.sin(math.pi * i / 24)) for i in range(25)]
line(dome, OUTER)
# 天线（分两节）
line([(0, 292.5), (0, 312)], OUTER)
line([(-1.2, 312), (1.2, 312)], INNER)
line([(0, 312), (0, TOP_M)], INNER + 0.6)

# 地面短线
line([(-outer(0) - 14, 0), (-outer(0) - 2, 0)], INNER)
line([(outer(0) + 2, 0), (outer(0) + 14, 0)], INNER)

# ---------- 输出 ----------
out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<g fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">']
for d, w in paths:
    out.append(f'<path stroke-width="{w}" d="{d}"/>')
out += ["</g>", "</svg>"]
open(sys.argv[1], "w").write("\n".join(out))
print(len(paths), "paths")
