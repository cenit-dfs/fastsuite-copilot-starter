from cenpyunits.Unit import Unit
    
def ConvertDefaultToUnit(value, targetUnit : Unit):
    if targetUnit is None or value is None:
        raise ValueError("Value and target unit must not be None")
    
    return (value / targetUnit.GetScale()) + targetUnit.GetShift()

def ConvertUnitToDefault(value, currentUnit : Unit):
    if currentUnit is None or value is None:
        raise ValueError("Value and current unit must not be None")

    return (value - currentUnit.GetShift()) * currentUnit.GetScale()

def ConvertUnitToUnit(value, currentUnit : Unit, targetUnit : Unit):
    if currentUnit is None or targetUnit is None or value is None:
        raise ValueError("Value and units must not be None")
    
    if targetUnit.GetUnitGroup() != currentUnit.GetUnitGroup():
        raise TypeError("Units must be of the same UnitGroup!")
    
    default = ConvertUnitToDefault(value, currentUnit)
    return ConvertDefaultToUnit(default, targetUnit)