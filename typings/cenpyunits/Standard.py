from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Standard(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Standard
        self._isDefault = True
