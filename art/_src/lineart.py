"""共用线描工具。
用法：在任意模型单位（米/公里）下画线，save() 时自动按包围盒缩放到画面里留 6% 边距、
水平垂直居中，再转成像素并加手绘抖动。所以线宽、抖动在所有图里都是同一像素值，整套一致。
画幅：竖 1024x1536，方 1024x1024，横 1536x1024。
"""
import math
import random

INK = "#1F1D19"
OUTER, INNER = 6.0, 3.4
SIZES = {"竖": (1024, 1536), "方": (1024, 1024), "横": (1536, 1024)}
MARGIN = 0.06


class Canvas:
    def __init__(self, fmt, seed=1, sx=1.0):
        """sx：横向缩放（<1 让山更陡峭），在出图时统一施加。"""
        self.sx = sx
        self.w, self.h = SIZES[fmt]
        self.strokes = []
        self.seed = seed

    def line(self, pts, w=INNER, closed=False, hide=None):
        """hide: 前景多边形列表（模型坐标），落在其中的线段会被擦掉（消隐）。"""
        pts = list(pts)
        if closed:
            pts = pts + [pts[0]]
        if hide:
            for run in clip_runs(pts, hide):
                self.strokes.append((run, w))
        else:
            self.strokes.append((pts, w))

    def smooth(self, pts, w=INNER, n=10, closed=False, hide=None):
        self.line(catmull(pts, n, closed), w, hide=hide)

    def poly(self, pts, w=INNER, hide=None):
        self.line(pts, w, closed=True, hide=hide)

    def sym(self, pts, w=INNER, hide=None, smooth=False):
        """画一条线及其左右镜像。"""
        f = self.smooth if smooth else self.line
        f(pts, w, hide=hide)
        f([(-x, z) for x, z in pts], w, hide=hide)

    def rect(self, x0, z0, x1, z1, w=INNER, hide=None):
        self.poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], w, hide=hide)

    def circle(self, cx, cz, r, w=INNER, rz=None, a0=0, a1=360, n=36):
        rz = r if rz is None else rz
        k = max(4, int(n * abs(a1 - a0) / 360))
        self.line([(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / k)),
                    cz + rz * math.sin(math.radians(a0 + (a1 - a0) * i / k))) for i in range(k + 1)], w)

    def save(self, path):
        random.seed(self.seed)
        if self.sx != 1.0:
            self.strokes = [([(x * self.sx, z) for x, z in p], w) for p, w in self.strokes]
            self.sx = 1.0
        xs = [x for p, _ in self.strokes for x, _ in p]
        zs = [z for p, _ in self.strokes for _, z in p]
        x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
        aw, ah = self.w * (1 - 2 * MARGIN), self.h * (1 - 2 * MARGIN)
        s = min(aw / (x1 - x0 or 1), ah / (z1 - z0 or 1))
        ox = self.w / 2 - (x0 + x1) / 2 * s
        oy = self.h / 2 + (z0 + z1) / 2 * s
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',
               f'<g fill="none" stroke="{INK}" stroke-linecap="round" stroke-linejoin="round">']
        for p, w in self.strokes:
            px = [(ox + x * s, oy - z * s) for x, z in p]
            px = wobble(px, 0.7 if w >= OUTER else 0.45)
            d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in px)
            out.append(f'<path stroke-width="{w}" d="{d}"/>')
        out += ["</g>", "</svg>"]
        open(path, "w").write("\n".join(out))
        print(path, len(self.strokes), "strokes")


def inside(pt, poly):
    x, y = pt
    c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def densify(pts, step):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(1, n + 1)]
    return out


def clip_runs(pts, polys):
    """把折线中位于任一多边形内部的部分去掉，返回可见的若干段。"""
    xs = [x for x, _ in pts]; ys = [y for _, y in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1
    d = densify(pts, span / 400)
    runs, cur = [], []
    for p in d:
        if any(inside(p, q) for q in polys):
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        else:
            cur.append(p)
    if len(cur) > 1:
        runs.append(cur)
    return runs


def ridge(ctrl, rough=0.12, seed=0, depth=5):
    """自然山脊：在控制点之间做分形中点位移。rough 为相对段长的起伏幅度。"""
    rnd = random.Random(seed)
    pts = list(ctrl)
    for lv in range(depth):
        new = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            L = math.hypot(x1 - x0, y1 - y0)
            off = rnd.uniform(-1, 1) * rough * L
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            nx, ny = -(y1 - y0) / (L or 1), (x1 - x0) / (L or 1)
            new += [(mx + nx * off, my + ny * off), (x1, y1)]
        pts = new
    return pts


def conifer(cx, z, h, w=None, tiers=3):
    """小针叶树轮廓（闭合多边形），返回点列。"""
    w = w or h * 0.32
    pts = [(cx - w * 0.12, z)]
    for i in range(tiers):
        t0 = i / tiers
        zb = z + h * (0.15 + 0.85 * t0)
        wb = w * (1 - 0.55 * t0)
        pts += [(cx - wb, zb), (cx - wb * 0.45, zb + h * 0.85 / tiers * 0.35)]
    pts += [(cx, z + h)]
    right = [(2 * cx - x, y) for x, y in reversed(pts[1:-1])]
    return pts + right + [(cx + w * 0.12, z)]


def catmull(pts, n=10, closed=False):
    if len(pts) < 3:
        return list(pts)
    P = list(pts)
    P = [P[-1]] + P + [P[0], P[1]] if closed else [P[0]] + P + [P[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(P[-2])
    return out


def wobble(pts, amp=0.7):
    """沿法向加平滑低频噪声，两端收敛，模拟钢笔手绘的轻微不规则。"""
    if len(pts) < 2:
        return pts
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
        fade = min(1.0, L[i] / 14, (total - L[i]) / 14)
        off = sum(a * math.sin(L[i] / wl * 6.283 + ph) for a, wl, ph in waves) * fade
        out.append((x + nx * off, y + ny * off))
    return out


def sky(sil, pad=1.0):
    """由山体轮廓线生成“天空”多边形；把它作为 hide 传入，可让山体内部的线不越出轮廓。"""
    xs = [x for x, _ in sil]; zs = [z for _, z in sil]
    top = max(zs) + pad * 10
    return list(sil) + [(max(xs) + pad, sil[-1][1]), (max(xs) + pad, top), (min(xs) - pad, top), (min(xs) - pad, sil[0][1])]


def pine_flat(x, z, h, s=1.0, seed=0):
    """黄山松/泰山松式的平顶松：弯干 + 斜伸的枝 + 几团扁平云朵状叶团。
    返回 (线列表, 叶团多边形列表)。叶团多边形同时用于遮挡后方线条。s=±1 控制主枝朝向。"""
    rnd = random.Random(seed)
    lines, polys = [], []
    top = (x + s * h * 0.1, z + h * 0.92)
    lines.append(catmull([(x, z), (x + s * h * 0.15, z + h * 0.3), (x - s * h * 0.04, z + h * 0.62), top], 6))
    pads = [(top[0], z + h * 0.92, h * 0.5),
            (x + s * h * 0.45, z + h * 0.68, h * 0.55),
            (x - s * h * 0.25, z + h * 0.5, h * 0.38)]
    for k, (cx, cz, w) in enumerate(pads):
        if k:
            lines.append(catmull([(x + s * h * 0.06 * k, z + h * (0.3 + 0.12 * k)), ((x + cx) / 2, cz - h * 0.02), (cx, cz)], 4))
        ph = w * 0.3
        top_pts = []
        n = 6
        for i in range(n + 1):
            t = i / n
            bump = rnd.uniform(0.0, 0.25) * ph if 0 < i < n else 0
            top_pts.append((cx - w / 2 + w * t, cz + ph * math.sqrt(max(0.0, 1 - (2 * t - 1) ** 2)) ** 0.7 + bump))
        bot = [(cx + w / 2, cz), (cx + w * 0.2, cz - ph * 0.18), (cx - w * 0.2, cz - ph * 0.12), (cx - w / 2, cz)]
        poly = catmull(top_pts, 4) + catmull(bot, 4)[1:]
        polys.append(poly)
    return lines, polys


def glacier_marks(cv, x0, x1, z_top, z_bot, seed=0, density=1.0):
    """冰川表面：成簇、长短方向不一的冰裂缝短弧，避免等距“尺子刻度”感。"""
    rnd = random.Random(seed)
    span = x1 - x0
    h = z_top - z_bot
    n_clusters = max(3, int(5 * density))
    for c in range(n_clusters):
        cx = x0 + span * (c + rnd.uniform(0.15, 0.85)) / n_clusters
        cz = z_bot + h * rnd.uniform(0.35, 0.7)
        for k in range(rnd.randint(2, 4)):
            x = cx + rnd.uniform(-0.6, 0.6) * span / n_clusters * 0.5
            z = cz + rnd.uniform(-0.25, 0.25) * h
            w = rnd.uniform(0.25, 0.6) * span / n_clusters * 0.45
            sag = rnd.uniform(0.08, 0.2) * h
            cv.smooth([(x - w, z), (x, z - sag), (x + w, z + rnd.uniform(-0.05, 0.05) * h)], INNER, n=4)
