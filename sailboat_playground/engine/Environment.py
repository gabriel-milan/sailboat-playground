__all__ = ["Environment"]

import json
import random
import numpy as np
from sailboat_playground.constants import constants


class Environment:
    def __init__(self, config_file: str):
        try:
            with open(config_file, "r") as f:
                self._config = json.loads(f.read())
                f.close()
        except Exception as e:
            raise Exception(f"Failed to load configuration file: {e}")
        self._currentWindSpeed = (
            self.config["wind_min_speed"] + self.config["wind_max_speed"])/2
        self._isWindGust = False
        self._currentWindGustStart = 0
        self._currentWindGustDuration = 0
        self._currentTime = 0

    @property
    def config(self):
        return self._config

    @property
    def wind_direction_rad(self):
        return self.config["wind_direction"] * np.pi / 180

    @property
    def current_direction_rad(self):
        return self.config["current_direction"] * np.pi / 180

    @property
    def wind_speed(self):
        return np.array([np.cos(self.wind_direction_rad), np.sin(self.wind_direction_rad)]) * self._currentWindSpeed

    @property
    def water_speed(self):
        return np.array([np.cos(self.current_direction_rad), np.sin(self.current_direction_rad)]) * self.config["current_speed"]

    @classmethod
    def get_delta_range(cls, current_speed, min_speed, max_speed, max_delta):
        delta_range = np.arange(
            min_speed, max_speed, 0.1)
        return list(delta_range[(delta_range > current_speed * (1 - max_delta / 100))
                                & (delta_range < current_speed * (1 + max_delta / 100))])

    def execute(self):
        self._currentTime += constants.time_delta
        self.change_wind_speed()

    def change_wind_speed(self):
        if self._isWindGust:
            delta_range = self.get_delta_range(
                self._currentWindSpeed, self.config["wind_gust_min_speed"], self.config["wind_gust_max_speed"], self.config["wind_gust_max_delta_percent"])
            try:
                self._currentWindSpeed = random.choice(delta_range)
            except IndexError:
                pass
            except Exception as e:
                raise e
            self._isWindGust = (
                self._currentTime - self._currentWindGustStart) < self._currentWindGustDuration
        else:
            delta_range = self.get_delta_range(
                self._currentWindSpeed, self.config["wind_min_speed"], self.config["wind_max_speed"], self.config["wind_max_delta_percent"])
            try:
                self._currentWindSpeed = random.choice(delta_range)
            except IndexError:
                pass
            except Exception as e:
                raise e
            self._isWindGust = random.random(
            ) < self.config["wind_gust_probability"]
            if self._isWindGust:
                self._currentWindGustDuration = random.choice(np.arange(
                    self.config["wind_gust_min_duration"], self.config["wind_gust_max_duration"], constants.time_delta))
