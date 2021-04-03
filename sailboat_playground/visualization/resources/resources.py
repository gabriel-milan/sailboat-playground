__all__ = [
    "sailboat_image",
    "sail_image",
    "rudder_image",
    "wind_image",
    "speed_image",
    "buoy_image",
]

import pyglet
from os import path
import sailboat_playground


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


base_path = path.dirname(sailboat_playground.__file__)
pyglet.resource.path = [path.join(base_path, 'visualization/resources')]
pyglet.resource.reindex()

sailboat_image = pyglet.resource.image("sailboat.png")
center_image(sailboat_image)

sail_image = pyglet.resource.image("foil.png")
center_image(sail_image)

rudder_image = pyglet.resource.image("foil_rudder.png")
rudder_image.anchor_x = rudder_image.width / 2
rudder_image.anchor_y = rudder_image.height * 1.5

wind_image = pyglet.resource.image("arrow.png")
center_image(wind_image)

speed_image = pyglet.resource.image("speed.png")
center_image(speed_image)

buoy_image = pyglet.resource.image("buoy.png")
center_image(buoy_image)
