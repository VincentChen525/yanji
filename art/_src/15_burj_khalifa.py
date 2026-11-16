"""15-burj-khalifa：哈利法塔。竖幅。单位米。总高 828m。
Y 形平面三翼逐级退台、螺旋上升，立面上表现为左右交替的台阶；翼的边缘作为细竖线一直延伸上去。"""
import sys
from lineart import Canvas, OUTER, INNER
cv = Canvas("竖", seed=15)
L = cv.line
# 退台序列：(高度, 收进的一侧, 收进后该侧的半宽)
steps = [(0, None, None)]
left, right = 33.0, 33.0
seq = [(155, 'L', 29.5), (205, 'R', 29.0), (250, 'L', 26.0), (300, 'R', 25.0), (345, 'L', 22.5), (390, 'R', 21.0),
       (430, 'L', 19.0), (470, 'R', 17.0), (505, 'L', 15.0), (540, 'R', 13.0), (570, 'L', 11.0), (598, 'R', 9.5)]
lp, rp = [(-left, 0)], [(right, 0)]
edges = []
z_prev = 0
for z, side, w in seq:
    if side == 'L':
        lp += [(-left, z), (-w, z)]
        edges.append((-left + 2.0, z))
        left = w
    else:
        rp += [(right, z), (w, z)]
        edges.append((right - 2.0, z))
        right = w
TOPZ = 640
lp.append((-left, TOPZ)); rp.append((right, TOPZ))
L(lp, OUTER); L(rp, OUTER)
# 每个退台留下的翼边线：从退台处向上延续一小段
for x, z in edges:
    L([(x if x < 0 else x, z - 40), (x, z)])
# 主体中轴两侧的竖线（三翼交接处）
for x in (-5.5, 5.5):
    L([(x, 4), (x, TOPZ)])
for x in (-18, 18):
    L([(x, 4), (x, 245 if x < 0 else 300)])
# 底部裙楼
L([(-48, 0), (-48, 12), (-33, 12)], OUTER); L([(48, 0), (48, 12), (33, 12)], OUTER)
L([(-58, 0), (58, 0)], OUTER)
# 塔冠与塔尖
L([(-left, TOPZ), (-6.5, 700), (-4.0, 700), (-1.2, 790), (0, 828), (1.2, 790), (4.0, 700), (6.5, 700), (right, TOPZ)], OUTER)
L([(-6.5, 700), (6.5, 700)])
for z in (660, 680):
    w = left + (6.5 - left) * (z - TOPZ) / 60
    L([(-w, z), (w, z)])
L([(0, TOPZ), (0, 790)])
cv.save(sys.argv[1])
