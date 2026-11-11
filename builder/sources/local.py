import json
import os


class JsonFileWaypointSource:
    def __init__(self, path):
        self.path = path

    def get_waypoints(self, sol_min, sol_max):
        with open(self.path) as f:
            data = json.load(f)
        return [w for w in data if sol_min <= w["sol"] <= sol_max]


class JsonFileWeatherSource:
    """Reads data/rems_temps.json, made by rems_stats.py from NASA REMS data."""

    def __init__(self, path):
        self.path = path

    def get_temp_c(self, sol):
        with open(self.path) as f:
            data = json.load(f)
        return data[str(sol)]["ambient_mean_c"]


class LocalPhotoSource:
    """Photos already chosen and copied to <mission_dir>/assets/stopN.jpg."""

    def __init__(self, mission_dir):
        self.mission_dir = mission_dir

    def get_photo(self, stop_id):
        rel = f"assets/stop{stop_id}.jpg"
        if not os.path.exists(os.path.join(self.mission_dir, rel)):
            raise FileNotFoundError(rel)
        return rel


class LocalMineralSource:
    """CRISM strip converted by convert_crism.py; corners from NASA's metadata."""

    # [[south, west], [north, east]] from Mars Trek FGDC metadata
    BOUNDS = [[-5.2957424, 137.3382088], [-5.0790896, 137.571304]]

    def __init__(self, mission_dir):
        self.mission_dir = mission_dir

    def get_layer(self):
        rel = "assets/crism.png"
        if not os.path.exists(os.path.join(self.mission_dir, rel)):
            raise FileNotFoundError(rel)
        return {
            "id": "minerals",
            "name": "Minerals (CRISM strip, about 16 km south of the route)",
            "mission": "MRO",
            "instrument": "CRISM",
            "kind": "spectral",
            "image": rel,
            "bounds": self.BOUNDS,
        }