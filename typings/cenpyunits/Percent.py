from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Percentage(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Percent
        self._isDefault = True

class PercentageDecimal(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 100.0
        self._unitGroup = UnitGroups.Percent