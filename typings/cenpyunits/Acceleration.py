from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class FootSecondSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.3047999902464
        self._unitGroup = UnitGroups.Acceleration

class InchSecondSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0254
        self._unitGroup = UnitGroups.Acceleration

class MeterSecondSecond(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Acceleration
        self._isDefault = True

class MillimeterSecondSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Acceleration