"""重建全部或指定的图：python build.py [编号...]。每个 NN_name.py 输出 ../NN-name.svg 和 .png。"""
import glob, os, subprocess, sys
import resvg_py
here = os.path.dirname(os.path.abspath(__file__))
want = set(sys.argv[1:])
for src in sorted(glob.glob(os.path.join(here, "[0-9][0-9]_*.py"))):
    name = os.path.basename(src)[:-3].replace("_", "-")
    if want and name[:2] not in want:
        continue
    if name.startswith("08-"):
        continue  # 埃菲尔铁塔为独立脚本，单独生成
    svg = os.path.join(here, "..", name + ".svg")
    subprocess.run([sys.executable, src, svg], check=True, cwd=here)
    s = open(svg).read().replace('<g fill="none"', '<rect width="100%" height="100%" fill="#FFFFFF"/><g fill="none"', 1)
    open(svg[:-4] + ".png", "wb").write(bytes(resvg_py.svg_to_bytes(svg_string=s)))
