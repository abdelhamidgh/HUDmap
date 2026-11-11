from pathlib import Path
from PIL import Image

SRC = Path("data/frt0000a091_07_brpfmj_mtr3_ll.tif")
OUT = Path("../web/mission/assets/crism.png")

img = Image.open(SRC).convert("RGB")
w, h = img.size
px = list(img.getdata())
white = sum(1 for p in px if p == (255, 255, 255))
black = sum(1 for p in px if p == (0, 0, 0))
print("size:", w, "x", h)
print("pure white: %.1f%%" % (100 * white / len(px)))
print("pure black: %.1f%%" % (100 * black / len(px)))

# white = outside the CRISM strip -> make it see-through
rgba = Image.new("RGBA", img.size)
rgba.putdata([(0,0,0,0) if (p == (255,255,255) or max(p) < 25) else (p[0],p[1],p[2],255) for p in px])
OUT.parent.mkdir(parents=True, exist_ok=True)
rgba.save(OUT)
print("saved:", OUT, "| bytes:", OUT.stat().st_size)
print("bounds [[south, west], [north, east]] =",
      [[-5.2957424, 137.3382088], [-5.0790896, 137.571304]])