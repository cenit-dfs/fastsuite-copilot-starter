from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class DegreeSecondSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.01745329
        self._unitGroup = UnitGroups.AngularAcceleration

class RadianSecondSecond(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.AngularAcceleration
        self._isDefault = True