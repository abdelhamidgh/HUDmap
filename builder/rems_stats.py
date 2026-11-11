import csv
import json
import os
import re
import requests

ROOT = "https://pds-atmospheres.nmsu.edu/PDS/data/mslrem_1001/DATA/"
FOLDERS = {
    4596: "SOL_04489_04612",
    4618: "SOL_04613_04709",
    4639: "SOL_04613_04709",
    4655: "SOL_04613_04709",
    4711: "SOL_04710_04843",
    4820: "SOL_04710_04843",
}
os.makedirs("cache/rems_raw", exist_ok=True)


def find_tab_url(sol, folder):
    base = f"{ROOT}{folder}/SOL{sol:05d}/"
    r = requests.get(base, timeout=60)
    r.raise_for_status()
    links = re.findall(r'href="([^"]+)"', r.text)
    hits = [l for l in links if "RMD" in l and l.upper().endswith(".TAB")]
    if len(hits) != 1:
        raise SystemExit(f"sol {sol}: expected 1 RMD .TAB file, found {hits}")
    return base + hits[0]


def get_rows(sol):
    path = f"cache/rems_raw/rems_{sol}_rmd.tab"
    old = "cache/rems_4639_rmd.tab"
    if sol == 4639 and os.path.exists(old):
        path = old
    if not os.path.exists(path):
        url = find_tab_url(sol, FOLDERS[sol])
        print(f"sol {sol}: downloading {url.split('/')[-1]} ...", flush=True)
        r = requests.get(url, timeout=600)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    return list(csv.reader(open(path, encoding="utf-8"), skipinitialspace=True))


results = {}
for sol in FOLDERS:
    rows = get_rows(sol)
    bins = {}
    valid = []
    for r in rows:
        v = float(r[15])  # column 16 = AMBIENT_TEMP (Kelvin)
        if v > -900:
            valid.append(v)
            hour = int(r[1].split("M")[1][:2])
            bins.setdefault(hour // 3, []).append(v)
    bin_means = [sum(b) / len(b) for b in bins.values()]
    day_mean_k = sum(bin_means) / len(bin_means)
    results[sol] = {
        "ambient_mean_c": round(day_mean_k - 273.15, 1),
        "ambient_min_c": round(min(valid) - 273.15, 1),
        "ambient_max_c": round(max(valid) - 273.15, 1),
        "bins_with_data_of_8": len(bins),
        "valid_rows": len(valid),
        "total_rows": len(rows),
    }
    print(f"sol {sol}: {results[sol]}", flush=True)

with open("cache/rems_temps.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nsaved cache/rems_temps.json")