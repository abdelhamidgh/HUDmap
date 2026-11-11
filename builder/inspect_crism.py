import re
import shutil
import requests
from pathlib import Path
from PIL import Image

NAME = "frt0000a091_07_brpfmj_mtr3_ll"
SRC = Path.home() / "Downloads" / f"{NAME}.tif"
DST = Path("data") / f"{NAME}.tif"

# 1) keep a copy inside our project
DST.parent.mkdir(exist_ok=True)
shutil.copy(SRC, DST)
print("copied to:", DST)

# 2) what is inside the picture?
img = Image.open(DST)
print("size (pixels):", img.size, "| mode:", img.mode)
print("TIFF tag numbers:", sorted(img.tag_v2.keys()))
print("has geo tags (33550/33922/34264):",
      [t for t in (33550, 33922, 34264) if t in img.tag_v2])

# 3) ask NASA's Trek site for this scene's corner numbers
URL = ("https://trek.nasa.gov/mars/TrekWS/rest/cat/metadata/fgdc/html?label="
       + NAME)
r = requests.get(URL, timeout=60)
print("\nmetadata status:", r.status_code)
text = re.sub(r"<[^>]+>", " ", r.text)
for side in ("West", "East", "North", "South"):
    m = re.search(side + r"_Bounding_Coordinate:\s*(-?[0-9.]+)", text)
    print(side, m.group(1) if m else "NOT FOUND")