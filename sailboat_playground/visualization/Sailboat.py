import pyglet
import numpy as np
from sailboat_playground.visualization.resources.resources import sailboat_image, sail_image, rudder_image


class Sailboat (pyglet.sprite.Sprite):

    def __init__(self, map_size: int = 800, *args, **kwargs):
        super(Sailboat, self).__init__(img=sailboat_image, *args, **kwargs)
        self._map_size = map_size
        self._position = np.array(
            [400, 400])

        # Child sprite for sail
        self.sail_sprite = pyglet.sprite.Sprite(
            img=sail_image, *args, **kwargs)
        self.sail_sprite.visible = True

        # Child sprite for rudder
        self.rudder_sprite = pyglet.sprite.Sprite(
            img=rudder_image, *args, **kwargs)

        self.event_handlers = [self]

    def set_alpha(self, alpha):
        self.sail_sprite.rotation = self.rotation - alpha

    def set_rudder_angle(self, rudder_angle):
        self.rudder_sprite.rotation = self.rotation - rudder_angle

    def set_position(self, position):
        self._position = position

    def set_rotation(self, rotation):
        self.rotation = 90 - rotation

    def update(self, dt):
        super(Sailboat, self).update(dt)
        self.x = self._position[0]
        self.sail_sprite.x = self._position[0]
        self.rudder_sprite.x = self._position[0]
        self.y = self._position[1]
        self.sail_sprite.y = self._position[1]
        self.rudder_sprite.y = self._position[1]

    def delete(self):
        self.sail_sprite.delete()
        self.rudder_sprite.delete()
        super(Sailboat, self).delete()
