__all__ = ["constants"]


def const(cls):
    def is_special(name): return (
        name.startswith("__") and name.endswith("__"))
    class_contents = {n: getattr(cls, n)
                      for n in vars(cls) if not is_special(n)}

    def unbind(value):
        return lambda self: value
    propertified_contents = {
        name: property(unbind(value)) for (name, value) in class_contents.items()
    }
    receptor = type(cls.__name__, (object,), propertified_contents)
    return receptor()


@const
class constants (object):
    epsilon = 1e-7
    time_delta = 0.1  # second
    sea_water_rho = 1029  # kg / m^3
    wind_rho = 1.225  # kg / m^3
