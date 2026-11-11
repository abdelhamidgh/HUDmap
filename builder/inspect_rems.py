import csv
import os
import requests

URL = ("https://pds-atmospheres.nmsu.edu/PDS/data/mslrem_1001/DATA/"
       "SOL_04613_04709/SOL04639/RME_809270943RMD46390000000_______P1.TAB")
CACHE = "cache/rems_4639_rmd.tab"

if not os.path.exists(CACHE):
    print("downloading (about 11.5 MB)...")
    r = requests.get(URL, timeout=300)
    r.raise_for_status()
    with open(CACHE, "wb") as f:
        f.write(r.content)
print("file size:", os.path.getsize(CACHE))

rows = list(csv.reader(open(CACHE, encoding="utf-8"), skipinitialspace=True))
print("rows:", len(rows), "| columns in first row:", len(rows[0]))

COLS = {"BRIGHTNESS_TEMP(8)": 8, "BOOM1_AIR(12)": 12,
        "BOOM2_AIR(14)": 14, "AMBIENT(16)": 16}

for name, c in COLS.items():
    vals = [float(r[c - 1]) for r in rows if float(r[c - 1]) > -900]
    if vals:
        print(f"{name}: valid={len(vals)} of {len(rows)} | "
              f"min={min(vals):.1f} K ({min(vals)-273.15:.1f} C) | "
              f"max={max(vals):.1f} K ({max(vals)-273.15:.1f} C) | "
              f"mean={sum(vals)/len(vals):.1f} K ({sum(vals)/len(vals)-273.15:.1f} C)")
    else:
        print(name, ": no valid values")

print("\nAMBIENT mean by local Mars hour (3-hour bins):")
bins = {}
for r in rows:
    v = float(r[15])
    if v > -900:
        hour = int(r[1].split("M")[1][:2])
        bins.setdefault(hour // 3 * 3, []).append(v)
for h in sorted(bins):
    b = bins[h]
    print(f"  hour {h:02d}-{h+3:02d}: n={len(b)} mean={sum(b)/len(b)-273.15:.1f} C")