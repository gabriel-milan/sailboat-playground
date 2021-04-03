__all__ = ["Boat"]

import json
import numpy as np
from os import path
import pandas as pd
from sailboat_playground.constants import constants


class Boat:
    def __init__(self, config_file: str, foils_dir: str = "foils/"):
        try:
            with open(config_file, "r") as f:
                self._config = json.loads(f.read())
                f.close()
        except Exception as e:
            raise Exception(f"Failed to load configuration file: {e}")
        self._sail_foil_df = pd.read_csv(
            path.join(foils_dir, f"{self._config['sail_foil']}.csv"))
        self._rudder_foil_df = pd.read_csv(
            path.join(foils_dir, f"{self._config['rudder_foil']}.csv"))

        self._sail_foil_df["alpha_rad"] = self._sail_foil_df["alpha"] * np.pi / 180
        self._sail_foil_df["cr"] = np.sin(self._sail_foil_df["alpha_rad"]) * self._sail_foil_df["cl"] - np.cos(
            self._sail_foil_df["alpha_rad"]) * self._sail_foil_df["cd"]
        self._sail_foil_df["clat"] = np.cos(self._sail_foil_df["alpha_rad"]) * self._sail_foil_df["cl"] + np.cos(
            self._sail_foil_df["alpha_rad"]) * self._sail_foil_df["cd"]

        self._rudder_foil_df["alpha_rad"] = self._rudder_foil_df["alpha"] * np.pi / 180
        self._rudder_foil_df["cr"] = np.sin(self._rudder_foil_df["alpha_rad"]) * self._rudder_foil_df["cl"] - np.cos(
            self._rudder_foil_df["alpha_rad"]) * self._rudder_foil_df["cd"]
        self._rudder_foil_df["clat"] = np.cos(self._rudder_foil_df["alpha_rad"]) * self._rudder_foil_df["cl"] + np.cos(
            self._rudder_foil_df["alpha_rad"]) * self._rudder_foil_df["cd"]

        self._speed = np.array([0, 0])
        self._angular_speed = 0
        self._position = np.array([0, 0])
        self._currentTime = 0
        self._alpha = 0
        self._rudder_angle = 0
        self._heading = 270

    @property
    def alpha(self):
        return self._alpha

    @property
    def rudder_angle(self):
        return self._rudder_angle

    @property
    def heading(self):
        return self._heading

    @property
    def sail_df(self):
        return self._sail_foil_df

    @property
    def rudder_df(self):
        return self._rudder_foil_df

    @property
    def config(self):
        return self._config

    @property
    def mass(self):
        return self._config["mass"]

    @property
    def speed(self):
        return self._speed

    @property
    def angular_speed(self):
        return self._angular_speed

    @property
    def position(self):
        return self._position

    def apply_force(self, force: np.ndarray):
        self._speed = self._speed + (force / self.mass * constants.time_delta)

    def apply_angular_acceleration(self, accel: float):
        self._angular_speed += accel * constants.time_delta

    def execute(self):
        self._currentTime += constants.time_delta
        self._position = self._position + (self._speed * constants.time_delta)
        self._heading += self._angular_speed * constants.time_delta
        while self._heading >= 360:
            self._heading -= 360

    def set_alpha(self, alpha):
        self._alpha = alpha

    def set_rudder_angle(self, rudder_angle):
        self._rudder_angle = rudder_angle

    def set_heading(self, heading):
        self._heading = heading
