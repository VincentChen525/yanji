"""20-el-capitan：酋长岩，从谷底看。方幅。单位 km（示意）。
正中凸出的船首（The Nose）把左（西南壁）右（东南壁）两面巨壁分开；左壁上有心形凹坑；
右壁上一块“北美洲”形深色岩斑；长竖裂缝；顶部宽而近平；墙脚一排松树。"""
import sys, random
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull, conifer
cv = Canvas("方", seed=20)
rnd = random.Random(20)
sil = ridge([(-1.3, 0.0), (-1.18, 0.25), (-1.08, 0.42), (-0.95, 0.58), (-0.7, 0.72), (-0.4, 0.84), (-0.12, 0.93)], 0.02, 1) + \
      catmull([(-0.12, 0.93), (0.0, 0.97), (0.2, 0.985), (0.45, 0.975), (0.75, 0.93)], 6)[1:] + \
      ridge([(0.75, 0.93), (0.95, 0.82), (1.07, 0.6), (1.15, 0.38), (1.3, 0.18), (1.45, 0.0)], 0.025, 2)[1:]
SKY = sky(sil)
# 墙脚松林（最前）
trees = []
x = -1.32
while x < 1.47:
    h = rnd.uniform(0.07, 0.15)
    trees.append(conifer(x, 0.0, h, h * 0.28, tiers=3))
    x += rnd.uniform(0.035, 0.07)
cv.line(sil, OUTER, hide=trees)
cv.line([(-1.4, 0), (1.55, 0)], OUTER)
# 船首：从顶部向下的凸棱
nose = catmull([(0.0, 0.97), (-0.07, 0.72), (-0.06, 0.45), (0.0, 0.2), (0.04, 0.0)], 8)
cv.line(nose, OUTER, hide=trees)
# 心形凹坑（左壁）
hx, hz, hs = -0.55, 0.4, 0.1
hx, hz, hs = -0.55, 0.42, 0.13
heart = catmull([(hx + 0.02, hz - hs * 1.1), (hx - hs * 0.55, hz - hs * 0.2), (hx - hs * 0.95, hz + hs * 0.45),
                 (hx - hs * 0.7, hz + hs * 0.95), (hx - hs * 0.2, hz + hs * 0.8), (hx + hs * 0.05, hz + hs * 0.5),
                 (hx + hs * 0.35, hz + hs * 0.9), (hx + hs * 0.85, hz + hs * 0.7), (hx + hs * 0.8, hz + hs * 0.1),
                 (hx + 0.02, hz - hs * 1.1)], 5)
cv.line(heart, INNER)
# 北美洲岩斑（右壁）
na = catmull([(0.3, 0.72), (0.5, 0.78), (0.62, 0.7), (0.58, 0.55), (0.48, 0.48), (0.44, 0.36), (0.38, 0.42),
              (0.33, 0.52), (0.26, 0.6), (0.3, 0.72)], 6)
cv.line(na, INNER)
# 长竖裂缝：两面墙上，长短不一
for x in [-1.0, -0.85, -0.72, -0.36, -0.25, -0.16, 0.12, 0.2, 0.7, 0.8, 0.92, 1.02]:
    zt = next((z for xx, z in sil if xx >= x), 0.9) - rnd.uniform(0.02, 0.1)
    zb = rnd.uniform(0.05, 0.4)
    if -0.68 < x < -0.42:
        continue
    cv.line(ridge([(x, zt), (x + rnd.uniform(-0.02, 0.02), (zt + zb) / 2), (x + rnd.uniform(-0.02, 0.02), zb)], 0.02, int(x * 100) + 200),
            INNER, hide=[SKY] + trees)
# 顶部边缘下的一道平行线（顶部圆润的岩檐）
cv.line([(x, z - 0.035) for x, z in sil if -0.9 < x < 0.85], INNER, hide=[SKY])
for t in trees:
    cv.line(t, INNER, closed=True)
cv.save(sys.argv[1])
