from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Celsius(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Temperature
        self._isDefault = True

class Kelvin(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 273.15
        self._scale = 1.0
        self._unitGroup = UnitGroups.Temperature

class Fahrenheit(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 32.0
        self._scale = 0.5555555556
        self._unitGroup = UnitGroups.Temperature
