# 岩迹 · 标志文件

标志叫 **刻痕**：四道竖刻痕 + 一道橙色斜杠。
每一次攀爬是一道刻痕；橙色斜杠是「今天这一下」。

## 颜色

| 名称 | HEX | 用途 |
|---|---|---|
| 墨 | `#1F1D19` | 竖刻痕、文字 |
| 纸 | `#F4F0E6` | 背景 |
| 橙 | `#E2552B` | 斜杠这一笔（唯一的彩色） |

单色用时全部换成墨色；深色底用 `yanji-symbol-dark.svg`（纸色刻痕 + 橙斜杠）。

## 文件

| 文件 | 用途 |
|---|---|
| `yanji-symbol.svg` | 主标志（四竖一斜，透明底） |
| `yanji-symbol-small.svg` | 小尺寸主标志（三竖一斜，用于 16–24px） |
| `yanji-symbol-black.svg` / `-white.svg` / `-mono-1f1d19.svg` | 单色版（在 `variants/`） |
| `yanji-symbol-dark.svg` | 深色底版本 |
| `yanji-app-icon.svg` / `-1024.png` / `-512.png` / `-192.png` | app icon（纸底） |
| `apple-touch-icon.png` | iOS 主屏图标（180） |
| `favicon.ico` / `favicon-16.png` / `favicon-32.png` | 浏览器标签（用三竖一斜的极简版） |
| `yanji-lockup-horizontal.svg` / `.png` | 横版组合（标志 + 岩迹 + YANJI） |
| `yanji-lockup-stacked.svg` / `.png` | 竖版组合 |
| `yanji-lockup-horizontal-dark.svg` / `-dark.png` | 深色底横版 |
| `yanji-lockup-horizontal-mono.svg` | 单色横版 |
| `site.webmanifest` | PWA / 主屏图标清单 |
| `head-snippet.html` | 页面 `<head>` 里要加的图标链接 |

## 用法

- **留白**：标志四周至少留一根刻痕的宽度（≈ 标志高度的 1/8）。
- **最小尺寸**：主标志 ≥ 32px；16–24px 用 `yanji-symbol-small.svg`；横版组合 ≥ 160px 宽。
- **不要**：拉伸、加投影/渐变、改斜杠角度、把橙色用在竖刻痕上、在花背景上直接放透明底标志。
- **字标**：中文「岩迹」用霞鹜文楷（OFL，和 app 一致），英文 YANJI 字距略大。当前 lockup SVG 里的字是**活字**，正式印刷/对外物料需要转曲；网页里直接用 HTML 文字 + 标志即可。
- **刻痕的含义**：可以拿它当「记了多少次」的符号——分享卡角落盖一组，就是“这个月 23 次”。

## 生成方式

`yanji-symbol.svg` 为母版：刻痕是实心胶囊（非描边），斜杠 `rotate(-25.46°)`；小尺寸版把 4 竖减到 3 竖、线宽加到 30，保证 16px 还能读。所有 PNG 由 SVG 渲染，见 `logo-design` skill 的 `render_png.py` / `export_variants.py`。
