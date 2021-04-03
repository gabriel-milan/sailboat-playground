from sailboat_playground.engine import Manager
from sailboat_playground.visualization import Viewer


def get_rudder_angle(current_heading, target_heading):
    diff = current_heading - target_heading
    return diff


if __name__ == "__main__":
    print("**** Sailboat Playground example: sailing_downwind.py")
    print("- Generating simulation data...", end="")
    state_list = []
    stop = False
    steps = 0
    m = Manager(
        "boats/sample_boat.json",
        "environments/playground.json",
        boat_heading=270
    )
    while not stop and steps < 3000:
        state = m.agent_state
        if state["position"][1] <= -410:
            stop = True
        m.step([70, get_rudder_angle(state["heading"], 270)])
        state = m.state
        state_list.append(state)
        steps += 1
    print(" done.")
    print("- Showing simulation...", end="")
    buoys = [
        (-200, -400),
        (200, -400),
    ]
    v = Viewer(buoy_list=buoys, map_size=1000)
    v.run(state_list=state_list, simulation_speed=100)
    print(" done.")
