from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class CubicMillimeterSecond(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.FlowRate
        self._isDefault = True

class CubicCentimeterMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 16.666666667
        self._unitGroup = UnitGroups.FlowRate

class CubicInchMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 273.117733333
        self._unitGroup = UnitGroups.FlowRate