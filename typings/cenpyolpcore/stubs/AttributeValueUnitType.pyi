from enum import Enum

class AttributeValueUnitType(Enum):
    """Defines the unit the value of an attribute is given in"""
    Standard : int = 0 #measured in nothing

    Length : int = 1 #measured in meter (float/double)
    Mass : int = 2 #measured in kilogram (float/double)
    Time : int = 3 #measured in seconds (float/double)
    Area : int = 4 #measured in m^2 (float/double)
    Volume : int = 5 #measured in m^3 (float/double)
    Density : int = 6 #measured in kg/m^3 (float/double)
    Speed : int = 7 #measured in m/s (float/double)
    Power : int = 8 #measured in Watt=kg*m^2/s^3 (float/double)
    Energy : int = 9 #measured in Joule=Newton-meter=kg*m^2/s^2 (float/double)
    Force : int = 10 #measured in Newton=kg*m/s^2 (float/double)
    Pressure : int = 11 #measured in Pascal=kg/(m*s^2) (float/double)
    Frequency : int = 12 #measured in Hertz=1/s (float/double)
    Temperature : int = 13 #measured in Kelvin (float/double)
    LuminousIntensity : int = 14 #measured in Candela (float/double)
    Luminance : int = 15 #measured in cd/m^2 (float/double)
    Angle : int = 16 #measured in degree (float/double)
    Acceleration : int = 17 #measured in m/s^2 (float/double)
    ElectricCurrent : int = 18 #measured in Ampere (float/double)
    ElectricCharge : int = 19 #measured in Coulomb=A*s (float/double)
    ElectricResistance : int = 20 #measured in Ohm=kg*m^2/(A^2*s^3) (float/double)
    ElectricCapacity : int = 21 #measured in Farad=s^4*A^2/(m^2*kg) (float/double)
    Voltage : int = 22 #measured in Volt=kg*m^2/(A*s^3) (float/double)
    MagneticFlux : int = 23 #measured in Weber=kg*m^2/(A*s^2) (float/double)
    MagneticField : int = 24 #measured in Tesla=kg/(A*s^2) (float/double)
    Induction : int = 25 #measured in Henry=kg*m^2/(A^2*s^2) (float/double)
    AngularSpeed : int = 26 #measured in rad/s (float/double)
    AngularAcceleration : int = 27 #measured in rad/s^2 (float/double)
    Percent : int = 28 #measured in percent
    FlowRate : int = 29 #measured in  cubic meters per second (m3/s)

    Color : int = 30 # Possible sub-type of int array attribute (where R = G and B values are stored in the int array)