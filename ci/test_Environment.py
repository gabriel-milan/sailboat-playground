import numpy as np
from sailboat_playground.engine import Environment


def test_environment():
    try:
        env = Environment("environments/this-file-doesnt-exist.json")
        raise Exception("This shouldn't happen")
    except:
        pass
    env = Environment("environments/sample_environment.json")
    assert env.config["name"] == "Example environment"
    assert env.wind_direction_rad == 90 * np.pi / 180
    env.execute()
    assert env.wind_speed[0] != 0
    assert env.wind_speed[1] != 0
    for _ in range(20):
        env.execute()
    assert env.water_speed[0] == 0
    assert env.water_speed[1] == 0
