"""把若干 PNG 拼成一张预览，便于整体检查。python sheet.py out.png 02 06 ..."""
import sys, glob, os
from PIL import Image, ImageDraw
out, ids = sys.argv[1], sys.argv[2:]
here = os.path.dirname(os.path.abspath(__file__))
files = []
for i in ids:
    files += sorted(glob.glob(os.path.join(here, "..", i + "-*.png")))
cell = 420
cols = min(len(files), int(sys.argv[0] and 5))
rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cell, rows * cell), "#dddddd")
d = ImageDraw.Draw(sheet)
for k, f in enumerate(files):
    im = Image.open(f); im.thumbnail((cell - 10, cell - 10))
    x, y = (k % cols) * cell + 5, (k // cols) * cell + 5
    sheet.paste(im, (x, y)); d.text((x + 3, y + 3), os.path.basename(f)[:-4], fill="red")
sheet.save(out)
