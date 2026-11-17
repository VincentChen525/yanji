# 岩迹 · 标志文件

标志叫 **一条线路**：一条柔和的 S 形线路，线上有两个镂空的岩点/螺栓孔，起点在左下、到顶一颗橙点。

## 颜色

| 名称 | HEX | 用途 |
|---|---|---|
| 墨 | `#1F1D19` | 线路、文字、岩点孔外圈 |
| 纸 | `#F4F0E6` | 背景（镂空处透出底色） |
| 橙 | `#E2552B` | 只给到顶点这一颗 |

单色用时全部转墨；深色底用 `yanji-symbol-dark.svg`（纸色线 + 橙点，孔仍镂空）。

## 文件

| 文件 | 用途 |
|---|---|
| `yanji-symbol.svg` | 主标志（透明底，两个岩点真正镂空） |
| `yanji-symbol-small.svg` | 小尺寸主标志（无孔、粗线，16–24px） |
| `yanji-symbol-dark.svg` / `yanji-symbol-mono.svg` | 深色底 / 单色墨 |
| `variants/` | 黑 / 白 / 单色 / 方形（SVG + 256 PNG） |
| `yanji-favicon.svg` / `favicon.ico` / `favicon-16/32/48.png` | 浏览器标签（16 网格单独画的粗线版） |
| `apple-touch-icon.png` | iOS 主屏（180） |
| `yanji-app-icon.svg` / `-1024.png` / `-512.png` / `-192.png` | app icon（纸底 + 主标志） |
| `maskable-512.png` | Android maskable（内容在安全区内） |
| `yanji-lockup-horizontal.svg` / `.png` | 横版组合（透明底） |
| `yanji-lockup-horizontal-paper.png` | 纸色底横版（README/浅底用） |
| `yanji-lockup-stacked.svg` / `.png` | 竖版组合 |
| `yanji-lockup-horizontal-dark.svg` / `-dark.png` | 深色底横版 |
| `yanji-lockup-horizontal-mono.svg` | 单色横版 |
| `site.webmanifest` | PWA / 主屏图标清单 |
| `head-snippet.html` | 页面 `<head>` 里要加的图标链接 |

## 用法

- **留白**：标志四周至少留一根线宽（≈ 标志高度的 1/10）。
- **最小尺寸**：主标志 ≥ 32px；16–24px 用 `yanji-symbol-small.svg`；横版组合 ≥ 160px 宽。
- **不要**：改曲线走向、把橙点放到线中间、把岩点孔做成实心白点、加投影/渐变/描边、拉伸压扁。
- **字标**：中文「岩迹」用霞鹜文楷（OFL，和 app 一致），英文 YANJI 字距略大。当前 lockup SVG 里的字是**活字**，正式印刷/对外物料需要转曲；网页里用 HTML 文字 + 标志即可。
- **动效**：可以逐段画出这条线，橙点最后落下；不要弹跳。
