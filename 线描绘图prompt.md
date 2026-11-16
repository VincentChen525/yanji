# 绳迹 · 登顶册线描绘图 prompt

## 怎么用

- **对话式绘图模型**（能一次读长文、逐张出图的）：把下面「一、总要求」和「二、清单」整段贴过去，让它按编号一张一张画。
- **一次一张的模型**：每次贴「一、总要求」里的英文风格段，再加清单里对应那一行的英文描述。
- **建议先试 3 张**：`08-eiffel`、`05-liberty`、`23-fuji`（一座镂空建筑、一个人像、一座山）。风格满意后，把这 3 张作为风格参考图，再画剩下的，整套才统一。
- **画完交回**：全部放进 `攀岩/art/` 文件夹，文件名按清单里的写（如 `08-eiffel.png`）。去白底、裁边、缩放、上色都由我来处理，不用管。

---

## 一、总要求

### 中文版

为一款攀岩记录 App 画一套 29 张的地标与山峰线描插画。整套必须风格完全一致，像同一个人用同一支笔在同一本速写本上画的。

**风格**
- 手绘钢笔线描，单色：纯黑线条（#1F1D19 或纯黑），纯白背景（#FFFFFF）。
- 只有线，没有任何填色、灰度、渐变、阴影、排线、水彩、纹理、纸张质感。
- 线条略带手绘的轻微不规则，但干净、肯定、不毛糙、不重复描线。
- 外轮廓线稍粗，内部结构线稍细。以 1024 像素短边计，外轮廓约 6 像素，内部线约 3–4 像素。
- 细节适度：只画最能让人一眼认出它的结构特征，不堆砌细节。缩小到 48 像素时，仅凭轮廓也要认得出是什么。
- 气质：安静、克制，像旅行速写本或建筑立面手稿。不要卡通、不要 Q 版、不要 logo 化、不要写实照片感。

**构图**
- 每张只画一个主体，完整入画，不裁切。
- 正面或最经典的识别角度，接近立面图，不要强烈透视、不要仰视俯视。
- **保持真实的高宽比例**，不要为了填满画面而拉伸或压扁。
- 主体水平居中，底部落在同一条水平线上（可画一条很短的地面线，或不画）。
- 例外：按真实比例画完后，若主体高度明显不足画面高度（富士山、乞力马扎罗、桌山等宽矮的山），则整体在画面里**垂直居中**，不贴底。
- 主体尽量占满画面：最高点距上边约 6%，最低点距下边约 6%，左右留白不少于 6%。
- 不要：文字、标题、签名、水印、边框、天空、太阳、飞鸟、人物、车辆、周围的其他建筑。
- 山可以带极少量点缀（清单里写明的才画，例如一缕云、一棵树），其余一律不加。

**输出格式**
- 首选 SVG 矢量（只用描边 stroke，不用填充 fill）。不支持矢量就出 PNG。
- PNG：纯白不透明背景、黑色线条，短边不小于 1024 像素（能出 2048 更好）。不需要做透明背景。
- 画幅按清单里标的三种之一：竖幅 2:3（1024×1536）、方幅 1:1（1024×1024）、横幅 3:2（1536×1024）。
- 一个主体一个文件，文件名按清单。

### English style block（每张图都带上这一段）

```
Minimalist hand-drawn ink line illustration, part of a consistent 29-piece set for a climbing logbook app. Pure black lines (#1F1D19) on a pure white (#FFFFFF) background. Line art only: no fill, no grey tones, no gradients, no shading, no hatching, no texture, no paper grain. Confident, clean pen lines with only a slight hand-drawn irregularity; no sketchy overlapping strokes. Outer silhouette contour slightly heavier (about 6 px at 1024 px short side), interior structural lines thinner (3–4 px). Moderate detail: only the features that make the subject instantly recognisable; the silhouette alone must still read at 48 px thumbnail size. Mood: quiet, restrained, like a travel sketchbook or an architect's elevation drawing. Not cartoon, not cute, not a logo, not photorealistic.

Composition: one single subject, complete and uncropped, shown in its most iconic, near-elevation view with no dramatic perspective. Keep true real-world proportions; never stretch or squash to fill the canvas. Subject horizontally centred, resting on one horizontal baseline, filling the canvas with about 6% margin on every side. No text, no title, no signature, no watermark, no frame, no sky, no sun, no birds, no people, no vehicles, no surrounding buildings.

Output: SVG with strokes only if possible; otherwise PNG, opaque pure white background, black lines, short side at least 1024 px.

Subject:
```

---

## 二、清单（29 张）

画幅：**竖** = 2:3（1024×1536）　**方** = 1:1（1024×1024）　**横** = 3:2（1536×1024）

### 建筑 15 座

| 文件名 | 名称 | 画幅 | Subject（接在英文风格段后面） |
|---|---|---|---|
| `01-tiantan.png` | 天坛祈年殿（中国） | 方 | Hall of Prayer for Good Harvests, Temple of Heaven, Beijing. Front elevation. Circular wooden hall with three tiers of conical tiled eaves that get smaller toward the top, crowned by a round gilded finial; standing on a wide three-tier circular white marble terrace with balustrades and a central stairway. |
| `02-pisa.png` | 比萨斜塔（意大利） | 竖 | Leaning Tower of Pisa. Cylindrical bell tower leaning about 4 degrees to the right. Tall blind-arcade ground storey, six stacked rings of open arcaded galleries with small columns, and a narrower bell chamber on top. |
| `03-sydney-opera.png` | 悉尼歌剧院（澳大利亚） | 横 | Sydney Opera House, side view from the harbour. Clusters of overlapping sail-shaped concrete shells of different heights rising from a long, low stepped podium; faint rib lines on the shells. |
| `04-taj-mahal.png` | 泰姬陵（印度） | 横 | Taj Mahal, symmetrical front elevation. Large central onion dome with finial, four small domed chhatris around it, tall pointed-arch iwan portal in the facade, four slender minarets at the corners of a square raised plinth. |
| `05-liberty.png` | 自由女神像（美国） | 竖 | Statue of Liberty, full figure including the granite pedestal and the star-shaped fort base. Right arm raised high holding a torch with flame, crown with seven rays, tablet held in the left arm, long draped robe with vertical folds. |
| `06-big-ben.png` | 大本钟（英国） | 竖 | Elizabeth Tower (Big Ben), London, front elevation of the tower only. Tall slender Gothic Revival clock tower with vertical tracery, a large round clock face in a square frame, belfry openings above, and a steep ornate pyramidal spire with small pinnacles. |
| `07-giza.png` | 吉萨金字塔（埃及） | 横 | Great Pyramid of Giza, a single pyramid seen slightly off one corner so two faces show. Visible horizontal courses of stone blocks, slightly worn blunt apex, a thin line of desert ground. |
| `08-eiffel.png` | 埃菲尔铁塔（法国） | 竖 | Eiffel Tower, front elevation. Four curved iron-lattice legs sweeping inward, large decorative arch between the legs at the base, three platforms (first, second, summit), cross-braced lattice pattern, small cupola and antenna at the top. |
| `09-tokyo-tower.png` | 东京塔（日本） | 竖 | Tokyo Tower, front elevation. Slender steel lattice tower with nearly straight, gently flaring legs (clearly slimmer and more angular than the Eiffel Tower), a box-shaped two-storey main observation deck about one third of the way up, a small top deck high above, and a very long thin antenna mast. A low building sits between the legs at the base. |
| `10-empire-state.png` | 帝国大厦（美国） | 竖 | Empire State Building, front elevation. Art Deco skyscraper with strong vertical window strips, symmetrical stepped setbacks narrowing toward the top, a rounded mooring-mast crown, and a tall thin antenna spire. |
| `11-oriental-pearl.png` | 东方明珠（中国） | 竖 | Oriental Pearl Tower, Shanghai. Three splayed diagonal legs supporting a large lower sphere, three vertical columns rising to a second large upper sphere, a row of small spheres stacked between the columns, a small top sphere, and a long antenna. |
| `12-taipei-101.png` | 台北 101（中国台湾） | 竖 | Taipei 101, front elevation. Tapering trapezoid base section, then eight identical outward-flaring segments stacked like bamboo joints or pagoda tiers, small circular coin ornaments on the facade, a stepped crown and a spire. |
| `13-cn-tower.png` | 多伦多电视塔（加拿大） | 竖 | CN Tower, Toronto. Very tall slim tapering concrete shaft with a gently flaring three-fin base, a doughnut-shaped main observation pod about two thirds of the way up, a small SkyPod ring above it, and a long antenna mast. |
| `14-canton-tower.png` | 广州塔（中国） | 竖 | Canton Tower, Guangzhou. Twisted hyperboloid lattice tower made of slanted columns and rings, wide at the base and top with a narrow tight waist above the middle, slanted elliptical top, and a tall antenna mast. |
| `15-burj-khalifa.png` | 哈利法塔（阿联酋） | 竖 | Burj Khalifa, Dubai. Extremely tall, slender tower with a stepped silhouette: staggered setbacks on alternating sides spiralling upward, narrowing into a long needle spire. Fine vertical lines on the shaft. |

### 山 14 座

| 文件名 | 名称 | 画幅 | Subject（接在英文风格段后面） |
|---|---|---|---|
| `16-table-mountain.png` | 桌山（南非） | 横 | Table Mountain, Cape Town, seen from across Table Bay. A long, perfectly flat-topped sandstone plateau with sheer cliff bands below the rim, the pointed Devil's Peak on the left and the conical Lion's Head on the right. One thin "tablecloth" cloud line draped over the plateau edge. |
| `17-taishan.png` | 泰山（中国） | 横 | Mount Tai (Taishan), China. A massive, broad, heavy mountain with a rounded (not pointed) summit. A steep stone stairway — the Eighteen Bends — climbs up a gully to a small Chinese gate tower (South Heavenly Gate) on the saddle near the top, with tiny temple roofs on the summit. A few pine trees. |
| `18-huangshan.png` | 黄山（中国） | 横 | Huangshan (Yellow Mountain), China. A cluster of tall vertical granite spires and pillars of different heights, a twisted Welcoming Guest Pine with flat horizontal branches growing from a rock ledge in the foreground, and two or three thin horizontal lines of a sea of clouds around the bases of the peaks. |
| `19-huashan.png` | 华山（中国） | 方 | Mount Hua (Huashan), West Peak. A giant bare white granite monolith with a sheer vertical cliff face cut as if by a blade, smooth rock with long vertical cracks, a narrow knife-edge ridge leading to the top, and a few tiny pines and a small temple on the summit. |
| `20-el-capitan.png` | 酋长岩（美国） | 方 | El Capitan, Yosemite, seen from the valley floor. A huge sheer granite monolith with a prominent central prow (The Nose) dividing two vast walls, a heart-shaped recess on the left-hand wall, long vertical crack lines, a broad nearly flat top, and a strip of small pine trees at the base for scale. |
| `21-half-dome.png` | 半穹顶（美国） | 横 | Half Dome, Yosemite, classic profile view. A granite dome that looks sliced in half: a sheer vertical flat face on the left, a smooth rounded curved back sloping down to the right, with faint curved exfoliation lines on the rounded side and forested ridges below. |
| `22-emeishan.png` | 峨眉山（中国） | 横 | Mount Emei, Golden Summit, China. An asymmetric mountain: a long gentle forested slope rising from the left to a summit that ends abruptly in a tremendous sheer vertical cliff dropping away on the right. A small temple and a tiny multi-headed Buddha statue stand at the cliff edge; a few thin horizontal sea-of-clouds lines below the cliff. |
| `23-fuji.png` | 富士山（日本） | 横 | Mount Fuji. A wide, perfectly symmetrical volcanic cone with long, gently concave slopes, a small flat notched crater rim at the top, and a jagged zigzag snow-cap line a short way below the summit. |
| `24-matterhorn.png` | 马特洪峰（瑞士/意大利） | 方 | The Matterhorn seen from Zermatt. An isolated, steep four-sided rock pyramid with a sharp central ridge facing the viewer dividing two faces, a characteristic slightly crooked hooked summit, snow patches and rock strata lines on the faces. |
| `25-mont-blanc.png` | 勃朗峰（法国/意大利） | 横 | Mont Blanc seen from Chamonix. A broad, rounded, snow-covered dome summit (soft and massive, not a sharp peak) rising above subsidiary shoulders, with crevassed glacier tongues flowing down and a row of sharp rock needles (aiguilles) lower on the left. |
| `26-yulong.png` | 玉龙雪山（中国） | 横 | Jade Dragon Snow Mountain (Yulong), Lijiang, China. A long serrated ridge of many sharp snow peaks in a row like a dragon's spine, with the highest fan-shaped main peak (Shanzidou) near the centre, steep fluted rock and ice faces, and a small glacier below. |
| `27-kilimanjaro.png` | 乞力马扎罗（坦桑尼亚） | 横 | Mount Kilimanjaro seen from the savanna. A very wide, low-angled volcanic massif with a broad flat-topped summit (Kibo), a few patches of glacier ice along the summit rim, long gentle slopes on both sides, and one or two flat-topped acacia trees on the ground line in front. |
| `28-k2.png` | 乔戈里峰（中国/巴基斯坦） | 方 | K2 seen from Concordia. A steep, sharp, nearly symmetrical rock-and-ice pyramid, much steeper and more pointed than Everest, with a distinct shoulder on the right-hand ridge, fluted ice faces, rock ribs, and a glacier at its foot. |
| `29-everest.png` | 珠穆朗玛峰（中国/尼泊尔） | 横 | Mount Everest north face seen from Rongbuk, Tibet. A massive, broad-shouldered pyramid with long ridges descending left and right, distinct horizontal rock strata bands across the upper face (the Yellow Band), a couple of snow couloirs, and a small plume of wind-blown snow trailing from the summit to the right. |

---

## 三、出图后自查（给绘图模型，也给你自己看）

1. 背景是不是纯白，线条是不是纯黑，有没有混进灰色、阴影或填色。
2. 主体有没有被裁掉，上下左右留白是否大致一致。
3. 有没有多余的东西：文字、签名、边框、云、鸟、人、别的建筑。
4. 比例有没有被拉伸：富士山、乞力马扎罗、桌山应该又宽又矮；哈利法塔、多伦多电视塔应该极细极高。
5. 容易画混的几对能不能分清：埃菲尔铁塔 / 东京塔；珠峰 / 乔戈里峰 / 马特洪峰；酋长岩 / 半穹顶 / 华山。
6. 29 张摆在一起，线条粗细和细节密度是不是一致。
