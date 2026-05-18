from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Degree(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Angle
        self._isDefault = True

class Radian(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 57.29578
        self._unitGroup = UnitGroups.Angle