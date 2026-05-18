from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Candela(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.LuminousIntensity
        self._isDefault = True