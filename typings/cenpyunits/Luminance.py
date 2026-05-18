from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Candelapersquaremeter(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Luminance
        self._isDefault = True

class Candelapersquaremillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000000.0
        self._unitGroup = UnitGroups.Luminance

class Candelapersquareinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1550.003
        self._unitGroup = UnitGroups.Luminance

class Candelapersquarefoot(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 10.76391
        self._unitGroup = UnitGroups.Luminance