"""21-half-dome：半穹顶，经典侧影。横幅。单位 km（示意）。
左侧刀切般的垂直平面（顶部略有外悬的“帽檐”），右侧圆润的穹背缓缓下滑；穹背上有同心的剥离层纹；下方是长着树的山脊。"""
import sys, random, math
from lineart import Canvas, OUTER, INNER, ridge, sky, catmull, conifer
cv = Canvas("横", seed=21)
rnd = random.Random(21)
face_x = -0.7
back = catmull([(face_x - 0.02, 1.42), (-0.45, 1.5), (-0.15, 1.5), (0.15, 1.42), (0.45, 1.25), (0.72, 1.02), (0.95, 0.8)], 8)
sil = ridge([(-1.7, 0.1), (-1.4, 0.3), (-1.15, 0.44), (-0.9, 0.56)], 0.04, 1) + \
      [(-0.78, 0.6), (face_x, 0.66), (face_x + 0.01, 1.0), (face_x - 0.005, 1.3), (face_x - 0.03, 1.4)] + back + \
      ridge([(0.95, 0.8), (1.25, 0.62), (1.6, 0.48), (1.95, 0.3), (2.2, 0.1)], 0.04, 2)[1:]
SKY = sky(sil)
# 前景树脊（最前）：一条低山脊，脊上一排小针叶树
fr = ridge([(-1.8, 0.12), (-1.2, 0.3), (-0.6, 0.36), (0.4, 0.3), (1.4, 0.34), (2.0, 0.2), (2.3, 0.1)], 0.03, 3)
trees = []
for i in range(0, len(fr) - 1, 3):
    x, z = fr[i]
    h = rnd.uniform(0.07, 0.13)
    trees.append(conifer(x, z - 0.01, h, h * 0.3, tiers=3))
FRONT_POLY = fr + [(2.3, -1), (-1.8, -1)]
cv.line(sil, OUTER, hide=[FRONT_POLY] + trees)
cv.line(fr, OUTER, hide=trees)
for t in trees:
    cv.line(t, INNER, closed=True)
# 平面：第二条边（平面略斜着看到）+ 竖向水痕
cv.line(ridge([(face_x + 0.08, 1.46), (face_x + 0.1, 1.1), (face_x + 0.12, 0.75), (face_x + 0.16, 0.6)], 0.01, 4), INNER, hide=[SKY])
for x in (face_x + 0.03, face_x + 0.055):
    cv.line([(x, 1.35), (x + 0.01, 0.8)], INNER)
# 剥离层纹：与穹背平行的几道弧
for k, f in enumerate((0.12, 0.24, 0.37, 0.5)):
    arc = [(x - f * 0.15, z - f * (0.35 + 0.15 * (x + 0.5))) for x, z in back[4:]]
    cv.line(arc[: int(len(arc) * (0.9 - 0.12 * k))], INNER, hide=[SKY])
# 下方山体：几道下落的脊线
for pts, sd in [([(-0.75, 0.62), (-0.95, 0.45), (-1.2, 0.33)], 5), ([(0.9, 0.78), (0.8, 0.55), (0.9, 0.35)], 6),
                ([(0.2, 0.9), (0.15, 0.65), (0.25, 0.4)], 7), ([(-0.35, 0.9), (-0.4, 0.65), (-0.3, 0.42)], 8),
                ([(1.45, 0.5), (1.4, 0.38)], 9)]:
    cv.line(ridge(pts, 0.05, sd), INNER, hide=[SKY, FRONT_POLY] + trees)
cv.save(sys.argv[1])
