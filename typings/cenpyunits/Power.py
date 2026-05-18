from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Footpoundforcepersecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1.35575
        self._unitGroup = UnitGroups.Power

class Britishthermalunitpersecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1055.075
        self._unitGroup = UnitGroups.Power

class Watt(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Power
        self._isDefault = True

class Kilowatt(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.Power