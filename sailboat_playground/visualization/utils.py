__all__ = ["map_position"]


def map_position(pos, map_size):
    return pos / map_size * 800 + 400
