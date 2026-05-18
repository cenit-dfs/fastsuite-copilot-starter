from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Micrometer(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000001
        self._unitGroup = UnitGroups.Length

class Millimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Length

class Centimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.01
        self._unitGroup = UnitGroups.Length
        
class Decimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.1
        self._unitGroup = UnitGroups.Length

class Meter(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Length
        self._isDefault = True

class Kilometer(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.Length
        
class Milliinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0000254
        self._unitGroup = UnitGroups.Length

class Inch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0254
        self._unitGroup = UnitGroups.Length
        
class Feet(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.3047999902464
        self._unitGroup = UnitGroups.Length

class Yard(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.9144
        self._unitGroup = UnitGroups.Length

class Mile(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1609.344
        self._unitGroup = UnitGroups.Length