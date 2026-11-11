import json
import os
import re
import sys

import geo
from sources.local import (JsonFileWaypointSource, JsonFileWeatherSource,
                           LocalPhotoSource, LocalMineralSource)
# from sources.nasa import NasaWaypointSource   # real NASA download plug
from stops_seed import STOPS
from stop_cards import CARDS

# ---- CHOOSE THE DATA SOURCES HERE (change one line to swap a source) ----
MISSION_DIR = "../web/mission"
WAYPOINTS = JsonFileWaypointSource("data/waypoints.json")  # or NasaWaypointSource()
WEATHER = JsonFileWeatherSource("data/rems_temps.json")
PHOTOS = LocalPhotoSource(MISSION_DIR)
MINERALS = LocalMineralSource(MISSION_DIR)
# --------------------------------------------------------------------------

SOL_MIN, SOL_MAX = 4596, 4820
RAD_USV_H = 28        # Curiosity RAD average, same for every stop (see sources)
SLOPE_LIMIT = 12      # OUR team's safety rule, not a NASA number
OUT = os.path.join(MISSION_DIR, "mission.json")

HIRISE = {
    "id": "hirise", "name": "Photo", "mission": "MRO", "instrument": "HiRISE",
    "kind": "optical",
    "tiles": "https://trek.nasa.gov/tiles/Mars/EQ/curiosity_hirise_mosaic/"
             "1.0.0/default/default028mm/{z}/{y}/{x}.png",
}


def nearest(points, lat, lon):
    best = min(points, key=lambda w: geo.dist_m(lat, lon, w["lat"], w["lon"]))
    return best, geo.dist_m(lat, lon, best["lat"], best["lon"])


def build():
    pts = WAYPOINTS.get_waypoints(SOL_MIN, SOL_MAX)
    route = [{"lat": w["lat"], "lon": w["lon"], "elev": w["elev"],
              "slope": w["slope"]} for w in pts]
    stops = []
    for s in STOPS:
        card = CARDS[s["id"]]
        wp, _ = nearest(pts, s["mars"][0], s["mars"][1])
        stops.append({
            "id": s["id"], "name": s["name"], "mars": s["mars"], "field": None,
            "sol": s["sol"], "slope_deg": wp["slope"],
            "hazard": card["hazard"], "task": card["task"],
            "science": card["science"],
            "temp_c": WEATHER.get_temp_c(s["sol"]), "rad_uSv_h": RAD_USV_H,
            "photos": [PHOTOS.get_photo(s["id"])],
            "sources": card["sources"],
        })
    return {
        "mission_id": "boxwork-01",
        "site": "Mount Sharp boxwork, Gale Crater, Mars",
        "anchor": {"mars": [-4.803606, 137.380074], "field": [0, 0],
                   "rotation_deg": 0, "scale": 1.0},
        "route": route,
        "layers": [HIRISE, MINERALS.get_layer()],
        "stops": stops,
        "suit": {"o2_start_pct": 100, "o2_pct_per_min": 0.25,
                 "walk_speed_mps": 0.8},
    }


def validate(path):
    problems = []
    m = json.load(open(path, encoding="utf-8"))
    route, stops = m["route"], m["stops"]
    if [s["id"] for s in stops] != [0, 1, 2, 3, 4, 5]:
        problems.append("stops are not ids 0-5")
    need = ["id", "name", "mars", "field", "sol", "slope_deg", "hazard", "task",
            "science", "temp_c", "rad_uSv_h", "photos", "sources"]
    for s in stops:
        for k in need:
            if k not in s:
                problems.append(f"stop {s['id']}: missing {k}")
            elif k != "field" and s[k] in (None, "", []):
                problems.append(f"stop {s['id']}: empty {k}")
        for rel in s["photos"]:
            if not os.path.exists(os.path.join(MISSION_DIR, rel)):
                problems.append(f"stop {s['id']}: file missing {rel}")
        wp, d = nearest(route, s["mars"][0], s["mars"][1])
        if d > 1:
            problems.append(f"stop {s['id']}: nearest waypoint {d:.1f} m away")
        if abs(wp["slope"] - s["slope_deg"]) > 0.001:
            problems.append(f"stop {s['id']}: slope differs from waypoint")
        num = re.search(r"(\d+(?:\.\d+)?) degrees", s["hazard"])
        if not num or abs(float(num.group(1)) - s["slope_deg"]) > 0.1:
            problems.append(f"stop {s['id']}: hazard text slope does not match "
                            f"{s['slope_deg']}")
        says_over = "above the 12" in s["hazard"]
        if says_over != (s["slope_deg"] > SLOPE_LIMIT):
            problems.append(f"stop {s['id']}: hazard text vs 12 degree limit")
    for lay in m["layers"]:
        img = lay.get("image")
        if img and not os.path.exists(os.path.join(MISSION_DIR, img)):
            problems.append(f"layer {lay['id']}: file missing {img}")
    kinds = {l["kind"] for l in m["layers"]} | {"topographic", "atmospheric"}
    missions = {l["mission"] for l in m["layers"]} | {"MSL Curiosity"}
    if len(kinds) < 3 or len(missions) < 2:
        problems.append("fewer than 3 data kinds or 2 missions")
    return m, problems, kinds, missions


if __name__ == "__main__":
    mission = build()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(mission, f, indent=2, ensure_ascii=False)
    print("wrote", OUT, "|", os.path.getsize(OUT), "bytes")
    m, problems, kinds, missions = validate(OUT)
    print("route points:", len(m["route"]), "| stops:", len(m["stops"]))
    print("data kinds:", sorted(kinds), "| missions:", sorted(missions))
    for s in m["stops"]:
        print(f"  stop {s['id']}: slope {s['slope_deg']} temp {s['temp_c']} "
              f"photo {s['photos'][0]}")
    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("\nALL CHECKS PASSED")