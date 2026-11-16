import sys, resvg_py
svg = open(sys.argv[1]).read()
svg = svg.replace('<g fill="none"', '<rect width="100%" height="100%" fill="#FFFFFF"/><g fill="none"', 1)
png = resvg_py.svg_to_bytes(svg_string=svg, zoom=int(sys.argv[3]) if len(sys.argv) > 3 else 1)
open(sys.argv[2], "wb").write(bytes(png))
