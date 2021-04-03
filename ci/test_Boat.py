import numpy as np
from sailboat_playground.engine import Boat


def test_boat():
    try:
        boat = Boat("boats/this-file-doesnt-exist.json")
        raise Exception("This shouldn't happen")
    except:
        pass
    boat = Boat("boats/sample_boat.json")
    assert boat.mass == 20
    sail_cols = boat.sail_df.columns
    rudder_cols = boat.rudder_df.columns
    for col in ["alpha", "cl", "cd", "cr", "clat"]:
        assert col in sail_cols
        assert col in rudder_cols
    assert boat.speed[0] == 0
    assert boat.speed[1] == 0
    assert boat.config["name"] == "Example boat"
    boat.apply_force(np.array([20, 20]))
    assert boat.speed[0] == 0.1
    assert boat.speed[1] == 0.1
    assert boat.position[0] == 0
    assert boat.position[1] == 0
    boat.execute()
    assert round(boat.position[0], 1) == 0
    assert round(boat.position[1], 1) == 0
    assert boat.alpha == 0
    boat.set_alpha(2)
    assert boat.alpha == 2
    assert boat.rudder_angle == 0
    boat.set_rudder_angle(2)
    assert boat.rudder_angle == 2
