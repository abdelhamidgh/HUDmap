from typing import Protocol


class WaypointSource(Protocol):
    def get_waypoints(self, sol_min: int, sol_max: int) -> list[dict]:
        """Return [{'sol','lat','lon','elev','slope'}, ...] sorted by sol."""
        ...


class WeatherSource(Protocol):
    def get_temp_c(self, sol: int) -> float:
        """Daily mean air temperature for one sol, in degrees Celsius."""
        ...


class PhotoSource(Protocol):
    def get_photo(self, stop_id: int) -> str:
        """Path of the photo for a stop, relative to web/mission/, e.g. 'assets/stop2.jpg'."""
        ...


class MineralSource(Protocol):
    def get_layer(self) -> dict:
        """Return the 'minerals' layer: id, name, mission, instrument, kind, image, bounds."""
        ...