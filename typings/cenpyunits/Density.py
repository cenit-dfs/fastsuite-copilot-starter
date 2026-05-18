from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Kilogramcubicmeter(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Density
        self._isDefault = True
        
class Gramcubicmeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Density
        
class Kilogramcubicmillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000000000
        self._unitGroup = UnitGroups.Density
        
class Milligramcubicmeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000001
        self._unitGroup = UnitGroups.Density
        
class Ouncecubicinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1730.104
        self._unitGroup = UnitGroups.Density
        
class Poundcubicinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 27677.83
        self._unitGroup = UnitGroups.Density
        
class Tonnecubicmeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000
        self._unitGroup = UnitGroups.Density