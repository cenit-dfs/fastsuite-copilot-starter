from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Newton(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Force
        self._isDefault = True

class Millinewton(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Force

class Poundal(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.138255
        self._unitGroup = UnitGroups.Force

class Poundforce(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 4.4484
        self._unitGroup = UnitGroups.Force