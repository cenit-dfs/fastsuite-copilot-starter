from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Weber(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.MagneticFlux
        self._isDefault = True

class Milliweber(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.MagneticFlux

class Teslasquaremeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.MagneticFlux

class Teslasquaremillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000001
        self._unitGroup = UnitGroups.MagneticFlux