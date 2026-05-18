from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Kilovolt(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.Voltage

class Millivolt(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Voltage

class Volt(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Voltage
        self._isDefault = True