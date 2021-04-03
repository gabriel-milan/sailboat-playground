import pyglet
import numpy as np
from sailboat_playground.engine.utils import compute_angle
from sailboat_playground.visualization.Sailboat import Sailboat
from sailboat_playground.visualization.utils import map_position
from sailboat_playground.visualization.resources.resources import wind_image, speed_image, buoy_image


class Viewer ():

    def __init__(self, map_size: int = 800, buoy_list: list = None):
        self._map_size = map_size
        self._buoy_list = buoy_list if buoy_list is not None else []
        self._window = pyglet.window.Window(800, 800)
        self._window.event(self.on_draw)
        pyglet.gl.glClearColor(0.1, 0.4, 0.8, 0.4)
        self._step = 0
        self._main_batch = pyglet.graphics.Batch()

        self._end_label = pyglet.text.Label(text="End of simulation", x=400,
                                            y=-400, anchor_x="center", batch=self._main_batch, font_size=48)

        WIND_X = 40
        self._wind_arrow = pyglet.sprite.Sprite(
            img=wind_image, x=WIND_X, y=40, batch=self._main_batch)
        self._wind_text = pyglet.text.Label(
            text="N/A m/s", x=WIND_X, y=10, anchor_x="center", anchor_y="center", batch=self._main_batch, font_size=15)

        SPEED_X = 140
        self._speed_icon = pyglet.sprite.Sprite(
            img=speed_image, x=SPEED_X, y=40, batch=self._main_batch)
        self._speed_text = pyglet.text.Label(
            text="N/A m/s", x=SPEED_X, y=10, anchor_x="center", anchor_y="center", batch=self._main_batch, font_size=15)

        self._sailboat = None
        self._objects = []

    def init(self):
        self._sailboat = Sailboat(
            x=400, y=400, batch=self._main_batch, map_size=self._map_size)
        self._objects = [self._sailboat]

        for obj in self._objects:
            for handler in obj.event_handlers:
                self._window.push_handlers(handler)

        for (x, y) in self._buoy_list:
            pos = map_position(np.array([x, y]), self._map_size)
            x_map = pos[0]
            y_map = pos[1]
            self._objects.append(pyglet.sprite.Sprite(
                img=buoy_image, x=x_map, y=y_map, batch=self._main_batch))

    def on_draw(self):
        self._window.clear()
        self._main_batch.draw()

    def update(self, dt, state_list=None):
        if self._step >= len(state_list):
            self._end_label.y = 400
        else:
            state = state_list[self._step]
            self._wind_arrow.rotation = 90 - \
                compute_angle(state["wind_speed"]) * 180 / np.pi
            self._sailboat.set_position(map_position(
                state["boat_position"], self._map_size))
            self._sailboat.set_rotation(state["boat_heading"])
            self._sailboat.set_alpha(state["sail_angle"])
            self._sailboat.set_rudder_angle(state["rudder_angle"])
            self._sailboat.update(dt)
            self._wind_text.text = "{:.1f}m/s".format(
                np.linalg.norm(state["wind_speed"]))
            self._speed_text.text = "{:.1f}m/s".format(
                np.linalg.norm(state["boat_speed"]))
            self._step += 1

    def run(self, state_list, simulation_speed=100):

        # Init
        self.init()

        # Set update interval
        pyglet.clock.schedule_interval(
            self.update, 1 / simulation_speed, state_list=state_list)

        # Run
        pyglet.app.run()
