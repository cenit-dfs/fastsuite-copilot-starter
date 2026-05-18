from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Tesla(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.MagneticField
        self._isDefault = True

class Weberpersquaremillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 100000
        self._unitGroup = UnitGroups.MagneticField

class Weberpersquareinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1550.003
        self._unitGroup = UnitGroups.MagneticField