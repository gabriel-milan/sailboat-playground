__all__ = ["Manager"]

import numpy as np
from numpy.linalg.linalg import norm
from sailboat_playground.engine.utils import *
from sailboat_playground.engine.Boat import Boat
from sailboat_playground.constants import constants
from sailboat_playground.engine.Environment import Environment


class Manager:
    def __init__(self, boat_config: str, env_config: str, foils_dir: str = "foils/", debug: bool = False, boat_heading: float = 90):
        self._boat = Boat(boat_config, foils_dir)
        self._boat.set_heading(boat_heading)
        self._env = Environment(env_config)
        self._apparent_wind_speed = 0
        self._apparent_wind_direction = 0
        self._debug = debug

    def log(self, *args, **kwargs):
        if self._debug:
            print(*args, **kwargs)

    @property
    def boat(self):
        return self._boat

    @property
    def environment(self):
        return self._env

    @property
    def state(self):
        return {
            "wind_speed": self._env.wind_speed,
            "water_speed": self._env.water_speed,
            "boat_heading": self._boat.heading,
            "boat_speed": self._boat.speed,
            "boat_speed_direction": compute_angle(self._boat.speed),
            "boat_position": self._boat.position,
            "sail_angle": self._boat.alpha,
            "rudder_angle": self._boat.rudder_angle
        }

    @property
    def agent_state(self):
        return {
            "heading": self._boat.heading,
            "wind_speed": self._apparent_wind_speed,
            "wind_direction": self._apparent_wind_direction,
            "position": self._boat.position,
        }

    @classmethod
    def compute_force(cls, rho, velocity, area, coeff):
        return 1 / 2 * rho * (velocity ** 2) * area * coeff

    def print_current_state(self):
        self.log("*" * 15)
        self.log("*** Current Manager state:")
        self.log("True wind speed: {}".format(self._env.wind_speed))
        self.log("True water speed: {}".format(self._env.water_speed))
        self.log("Boat heading: {}".format(self._boat.heading))
        self.log("Boat speed: {}".format(self._boat.speed))
        self.log("Boat speed direction: {}".format(
            compute_angle(self._boat.speed) * 180 / np.pi))
        self.log("Boat position: {}".format(self._boat.position))
        self.log("Sail angle of attack: {}".format(self._boat.alpha))
        self.log("Rudder angle of attack: {}".format(self._boat.rudder_angle))
        self.log("*" * 15)

    def step(self, ans: list):
        if type(ans) != list or len(ans) != 2:
            raise Exception(
                "Argument \"ans\" for Manager.step() must be a list with two values: [alpha, rudder_angle]")
        self.apply_agent(ans[0], ans[1])
        self.print_current_state()
        total_force = np.array([0., 0.])
        # 1 - Wind forces on sail
        # 1.1 - Compute apparent wind
        self.log("----------- Wind forces on sail")
        Va = self._env.wind_speed - self._boat.speed
        self.log(f"Va={Va}")
        Va_angle = compute_angle(Va) * 180 / np.pi
        self._apparent_wind_direction = Va_angle - self._boat.heading
        global_sail_angle = self._boat.heading + self._boat.alpha
        while global_sail_angle < 0:
            global_sail_angle += 360
        while global_sail_angle > 360:
            global_sail_angle -= 360
        self.log(f"global_sail_angle={global_sail_angle}")
        alpha = Va_angle - global_sail_angle + 180
        while alpha < -180:
            alpha += 360
        while alpha > 180:
            alpha -= 360
        self.log(f"Va_angle={Va_angle}")
        self.log(f"alpha={alpha}")
        Va_norm = np.linalg.norm(Va)
        self._apparent_wind_speed = Va_norm
        self.log(f"Va_norm={Va_norm}")
        # 1.2 - Compute total force (in order to check driving force direction)
        D_norm = abs(self.compute_force(
            constants.wind_rho, Va_norm, self._boat.config["sail_area"], self._boat.sail_df[self._boat.sail_df["alpha"] == round(alpha)]["cd"].values[0]))
        self.log(f"D_norm={D_norm}")
        D_angle = Va_angle
        self.log(f"D_angle={D_angle}")
        D = norm_to_vector(D_norm, D_angle * np.pi / 180)
        self.log(f"D={D}")
        L_norm = abs(self.compute_force(
            constants.wind_rho, Va_norm, self._boat.config["sail_area"], self._boat.sail_df[self._boat.sail_df["alpha"] == round(alpha)]["cl"].values[0]))
        self.log(f"L_norm={L_norm}")
        if self._boat.alpha > 0:
            L_angle = D_angle + 90
        else:
            L_angle = D_angle - 90
        while L_angle > 360:
            L_angle -= 360
        while L_angle < 0:
            L_angle += 360
        self.log(f"L_angle={L_angle}")
        L = norm_to_vector(L_norm, L_angle * np.pi / 180)
        self.log(f"L={L}")
        F_T = L + D
        self.log(f"F_T={F_T}")
        # 1.3 - Compute driving force (project total force into unit vector on boat heading)
        unit_vector = norm_to_vector(1, self._boat.heading * np.pi / 180)
        F_R = np.dot(F_T, unit_vector) * unit_vector
        self.log(f"F_R={F_R}")
        self.log(f"* Adding {F_R}")
        total_force += F_R

        # # 2 - Water forces on hull
        # # 2.1 - Compute apparent water current
        self.log("----------- Water forces on hull")
        Wa = self._env.water_speed - self._boat.speed
        self.log(f"Wa={Wa}")
        Wa_angle = compute_angle(Wa) * 180 / np.pi
        while Wa_angle < 0:
            Wa_angle += 360
        while Wa_angle > 360:
            Wa_angle -= 360
        self.log(f"Wa_angle={Wa_angle}")
        Wa_norm = np.linalg.norm(Wa)
        self.log(f"Wa_norm={Wa_norm}")
        # 2.2 - Compute water resistance on hull
        F_WR_norm = abs(self.compute_force(
            constants.sea_water_rho, Wa_norm, self._boat.config["hull_area"], self._boat.config["hull_friction_coefficient"]))
        self.log(f"F_WR_norm={F_WR_norm}")
        F_WR = norm_to_vector(F_WR_norm, Wa_angle * np.pi / 180)
        self.log(f"F_WR={F_WR}")
        self.log(f"* Adding {F_WR}")
        # 2.3 - Apply forces
        total_force += F_WR

        # 3 - Water forces on rudder
        # 3.1 - Compute water force on rudder
        self.log("----------- Water forces on rudder")
        global_rudder_angle = self._boat.heading + self._boat.rudder_angle
        while global_rudder_angle < 0:
            global_rudder_angle += 360
        while global_rudder_angle > 360:
            global_rudder_angle -= 360
        rudder_angle = Wa_angle - global_rudder_angle + 180
        while rudder_angle < -180:
            rudder_angle += 360
        while rudder_angle > 180:
            rudder_angle -= 360
        D_norm = abs(self.compute_force(
            constants.sea_water_rho, Wa_norm, self._boat.config["rudder_area"], self._boat.rudder_df[self._boat.rudder_df["alpha"] == round(rudder_angle)]["cd"].values[0]))
        self.log(f"D_norm={D_norm}")
        D_angle = Va_angle
        self.log(f"D_angle={D_angle}")
        D = norm_to_vector(D_norm, D_angle * np.pi / 180)
        self.log(f"D={D}")
        L_norm = abs(self.compute_force(
            constants.sea_water_rho, Wa_norm, self._boat.config["rudder_area"], self._boat.rudder_df[self._boat.rudder_df["alpha"] == round(rudder_angle)]["cl"].values[0]))
        self.log(f"L_norm={L_norm}")
        if self._boat.rudder_angle > 0:
            L_angle = D_angle - 90
        else:
            L_angle = D_angle + 90
        while L_angle > 360:
            L_angle -= 360
        while L_angle < 0:
            L_angle += 360
        self.log(f"L_angle={L_angle}")
        L = norm_to_vector(L_norm, L_angle * np.pi / 180)
        self.log(f"L={L}")
        F_T = L + D
        self.log(f"F_T={F_T}")
        F_T_norm = np.linalg.norm(F_T)
        self.log(f"F_T_norm={F_T_norm}")
        # 3.2 - Compute hull rotation resistance
        F_WR_norm = abs(self.compute_force(
            constants.sea_water_rho, self._boat.angular_speed, self._boat.config["hull_area"], self._boat.config["hull_rotation_resistance"]))
        self.log(f"F_WR_norm={F_WR_norm}")
        # 3.3 - Compute torque and angular acceleration
        angular_acceleration_signal = 1 if self._boat.rudder_angle < 0 else -1
        self.log(f"angular_acceleration_signal={angular_acceleration_signal}")
        torque = (F_T_norm - F_WR_norm) * \
            (self._boat.config["length"] - self._boat.config["com_length"])
        self.log(f"torque={torque}")
        angular_acceleration = torque / \
            self._boat.config["moment_of_inertia"] * \
            angular_acceleration_signal
        self.log(f"angular_acceleration={angular_acceleration}")
        # 3.4 - Apply angular acceleration
        self._boat.apply_angular_acceleration(angular_acceleration)

        # 4 - Apply all forces
        self.log(f"--> Applying total_force={total_force}")
        self._boat.apply_force(total_force)

        # 4 - Execute boat and environment
        self._boat.execute()
        self._env.execute()

    def apply_agent(self, alpha: int, rudder_angle: int):
        self._boat.set_alpha(alpha)
        self._boat.set_rudder_angle(rudder_angle)
