# E2 Python API: OlpCore Objects

## Table of Contents

- [Core Objects](#core-objects)
  - [OlpCorePythonAttributeProvider](#olpcorepythonattributeprovider)
  - [OlpCorePythonItem](#olpcorepythonitem)
  - [OlpCorePythonProgramComponent](#olpcorepythonprogramcomponent)
  - [OlpCorePythonController](#olpcorepythoncontroller)
  - [OlpCorePythonEvent](#olpcorepythonevent)
  - [OlpCorePythonOperation](#olpcorepythonoperation)
  - [OlpCorePythonOperationGroup](#olpcorepythonoperationgroup)
  - [OlpCorePythonProgram](#olpcorepythonprogram)
  - [OlpCorePythonSubprogram](#olpcorepythonsubprogram)
  - [OlpCorePythonResource](#olpcorepythonresource)
  - [OlpCorePythonTechnology](#olpcorepythontechnology)
- [Attributes](#attributes)
  - [Setter Classes](#setter-classes)
  - [Getter Classes](#getter-classes)
- [Operators](#operators)
  - [OlpCorePythonLogOperator](#olpcorepythonlogoperator)
  - [OlpCorePythonBaseOperator](#olpcorepythonbaseoperator)
  - [OlpCorePythonAttributeSetterOperator](#olpcorepythonattributesetteroperator)
- [Enumerations](#enumerations)
  - [AttributeProperties](#attributeproperties)
  - [AttributeValueUnitType](#attributevalueunittype)
  - [ControllerTypes](#controllertypes)
  - [OperationType](#operationtype)
  - [InsertPosition](#insertposition)
  - [ItemType](#itemtype)
  - [ItemSubtype](#itemsubtype)

---

## Core Objects

### OlpCorePythonAttributeProvider

Base class providing attribute access functionality.

#### Methods

**GetAttribute(name: str) → Attribute**
Gets attribute by name.

**GetAttributeValue(name: str) → object**
Gets attribute value by name.

**SetAttributeValue(name: str, value: object)**
Sets attribute value by name.

**HasAttribute(name: str) → bool**
Checks if attribute exists.

**GetAttributeNames() → list[str]**
Returns list of all attribute names.

---

### OlpCorePythonItem

Base class for all OLP items.

#### Methods

**GetName() → str**
Returns item name.

**SetName(name: str)**
Sets item name.

**GetUuid() → str**
Returns item UUID.

**GetType() → ItemType**
Returns item type.

**GetSubtype() → ItemSubtype**
Returns item subtype.

**GetParent() → Item**
Returns parent item.

**GetChildren() → list[Item]**
Returns child items.

**IsValid() → bool**
Checks if item is valid.

---

### OlpCorePythonProgramComponent

Represents program components (operations, groups, subprograms).

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetComponentType() → int**
Returns component type constant.

**GetProgram() → OlpCorePythonProgram**
Returns parent program.

**GetTechnology() → OlpCorePythonTechnology**
Returns associated technology.

**IsEnabled() → bool**
Returns enabled state.

**SetEnabled(enabled: bool)**
Sets enabled state.

---

### OlpCorePythonController

Represents robot controller.

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetControllerType() → ControllerTypes**
Returns controller type enum.

**GetManufacturer() → str**
Returns manufacturer name.

**GetSeries() → str**
Returns controller series.

**GetVersion() → str**
Returns controller version.

**GetRobots() → list[Robot]**
Returns associated robots.

**GetExternalAxes() → list[ExternalAxis]**
Returns external axes.

**GetPrograms() → list[Program]**
Returns controller programs.

---

### OlpCorePythonEvent

Represents technology event.

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetEventName() → str**
Returns event name.

**GetEventType() → str**
Returns event type.

**GetEventUuid() → str**
Returns event UUID.

**GetInsertPosition() → InsertPosition**
Returns insert position (before/after).

**SetInsertPosition(pos: InsertPosition)**
Sets insert position.

**GetReferenceTpElement() → TpElement**
Returns reference TPE.

**GetOperation() → OlpCorePythonOperation**
Returns parent operation.

---

### OlpCorePythonOperation

Represents operation.

**Inherits from:** `OlpCorePythonProgramComponent`

#### Methods

**GetOperationType() → OperationType**
Returns operation type.

**GetTpElements() → list[TpElement]**
Returns toolpath elements.

**GetEvents() → list[Event]**
Returns operation events.

**GetProcessGeometry() → ProcessGeometry**
Returns associated process geometry.

**GetWorkMethod() → WorkMethod**
Returns workmethod.

**Compute() → bool**
Computes operation.

**IsComputed() → bool**
Returns compute state.

**GetCycleTime() → float**
Returns cycle time in seconds.

**GetPathLength() → float**
Returns path length in mm.

---

### OlpCorePythonOperationGroup

Represents operation group.

**Inherits from:** `OlpCorePythonProgramComponent`

#### Methods

**GetOperations() → list[Operation]**
Returns child operations.

**AddOperation(op: Operation)**
Adds operation to group.

**RemoveOperation(op: Operation)**
Removes operation from group.

**GetSubgroups() → list[OperationGroup]**
Returns child operation groups.

---

### OlpCorePythonProgram

Represents OLP program.

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetController() → OlpCorePythonController**
Returns associated controller.

**GetTechnology() → OlpCorePythonTechnology**
Returns program technology.

**GetChildComponents() → list[ProgramComponent]**
Returns all child components.

**GetOperations() → list[Operation]**
Returns all operations.

**GetOperationGroups() → list[OperationGroup]**
Returns all operation groups.

**GetSubprograms() → list[Subprogram]**
Returns all subprograms.

**Compute() → bool**
Computes entire program.

**IsComputed() → bool**
Returns compute state.

**GetCycleTime() → float**
Returns total cycle time.

**GetPathLength() → float**
Returns total path length.

---

### OlpCorePythonSubprogram

Represents subprogram.

**Inherits from:** `OlpCorePythonProgramComponent`

#### Methods

**GetCalledProgram() → OlpCorePythonProgram**
Returns referenced program.

**SetCalledProgram(prog: Program)**
Sets referenced program.

---

### OlpCorePythonResource

Represents manufacturing resource (robot, tool, fixture).

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetResourceType() → str**
Returns resource type.

**GetFrame() → Matrix**
Returns resource frame.

**SetFrame(frame: Matrix)**
Sets resource frame.

**GetParentResource() → Resource**
Returns parent resource.

**GetChildResources() → list[Resource]**
Returns child resources.

---

### OlpCorePythonTechnology

Represents technology package.

**Inherits from:** `OlpCorePythonItem`

#### Methods

**GetTechnologyName() → str**
Returns technology name.

**GetManufacturer() → str**
Returns manufacturer.

**GetVersion() → str**
Returns technology version.

**GetWorkMethods() → list[WorkMethod]**
Returns available workmethods.

**GetEvents() → list[Event]**
Returns available events.

**GetEventByName(name: str) → Event**
Returns event by name.

**GetEventByUuid(uuid: str) → Event**
Returns event by UUID.

---

## Attributes

### Setter Classes

Used to set attribute values.

#### OlpCorePythonSetBoolAttribute

**SetValue(value: bool)**
Sets boolean value.

#### OlpCorePythonSetIntegerAttribute

**SetValue(value: int)**
Sets integer value.

**SetMinValue(min: int)**
Sets minimum constraint.

**SetMaxValue(max: int)**
Sets maximum constraint.

#### OlpCorePythonSetDoubleAttribute

**SetValue(value: float)**
Sets double value.

**SetMinValue(min: float)**
Sets minimum constraint.

**SetMaxValue(max: float)**
Sets maximum constraint.

**SetUnit(unit: str)**
Sets unit type.

#### OlpCorePythonSetStringAttribute

**SetValue(value: str)**
Sets string value.

#### OlpCorePythonSetEnumAttribute

**SetValue(value: int)**
Sets enum index.

**SetOptions(options: list[str])**
Sets enum options list.

**SetOptionByName(name: str)**
Sets enum by option name.

---

### Getter Classes

Used to read attribute values.

#### OlpCorePythonBoolAttribute

**GetValue() → bool**
Gets boolean value.

**GetDefaultValue() → bool**
Gets default boolean value.

#### OlpCorePythonIntegerAttribute

**GetValue() → int**
Gets integer value.

**GetDefaultValue() → int**
Gets default integer value.

**GetMinValue() → int**
Gets minimum value.

**GetMaxValue() → int**
Gets maximum value.

**HasMin() → bool**
Checks if minimum is set.

**HasMax() → bool**
Checks if maximum is set.

#### OlpCorePythonDoubleAttribute

**GetValue() → float**
Gets double value.

**GetDefaultValue() → float**
Gets default double value.

**GetMinValue() → float**
Gets minimum value.

**GetMaxValue() → float**
Gets maximum value.

**GetUnit() → str**
Gets unit type.

**HasMin() → bool**
Checks if minimum is set.

**HasMax() → bool**
Checks if maximum is set.

#### OlpCorePythonStringAttribute

**GetValue() → str**
Gets string value.

**GetDefaultValue() → str**
Gets default string value.

#### OlpCorePythonEnumAttribute

**GetValue() → int**
Gets enum index.

**GetValueName() → str**
Gets enum option name.

**GetOptions() → list[str]**
Gets all enum options.

**GetDefaultValue() → int**
Gets default enum index.

---

## Operators

### OlpCorePythonLogOperator

Provides logging functionality.

#### Methods

**Info(message: str)**
Logs info message.

**Warning(message: str)**
Logs warning message.

**Error(message: str)**
Logs error message.

**Debug(message: str)**
Logs debug message.

#### Usage

```python
logger = Operator.GetLoggerOperator()
logger.Info("Processing started")
logger.Warning("Non-critical issue detected")
logger.Error("Critical error occurred")
```

---

### OlpCorePythonBaseOperator

Base operator class providing common functionality.

#### Methods

**GetLoggerOperator() → OlpCorePythonLogOperator**
Returns logger operator.

**GetProgram() → OlpCorePythonProgram**
Returns current program.

**GetController() → OlpCorePythonController**
Returns controller.

**GetTechnology() → OlpCorePythonTechnology**
Returns technology.

---

### OlpCorePythonAttributeSetterOperator

Provides batch attribute setting capabilities.

**Inherits from:** `OlpCorePythonBaseOperator`

#### Methods

**SetInteger(name: str, value: int)**
Sets integer attribute.

**SetDouble(name: str, value: float)**
Sets double attribute.

**SetString(name: str, value: str)**
Sets string attribute.

**SetBool(name: str, value: bool)**
Sets boolean attribute.

**SetEnum(name: str, value: int)**
Sets enum attribute by index.

**SetEnumByName(name: str, valueName: str)**
Sets enum attribute by name.

#### Usage

```python
attribSetter = Operator.GetAttribSetter()
attribSetter.SetInteger("Speed", 500)
attribSetter.SetDouble("Voltage", 25.5)
attribSetter.SetString("ProcessName", "Welding")
attribSetter.SetBool("Enabled", True)
attribSetter.SetEnumByName("WeldType", "MIG")
```

---

## Enumerations

### AttributeProperties

Attribute property flags.

**Values:**
- `ATTRIBUTEPROPERTY_NONE` - No properties
- `ATTRIBUTEPROPERTY_READONLY` - Read-only attribute
- `ATTRIBUTEPROPERTY_HIDDEN` - Hidden from UI
- `ATTRIBUTEPROPERTY_DOWNLOADABLE` - Available for download
- `ATTRIBUTEPROPERTY_REQUIRED` - Required attribute

---

### AttributeValueUnitType

Unit types for numeric attributes.

**Values:**
- `UNIT_NONE` - No unit
- `UNIT_MM` - Millimeters
- `UNIT_CM` - Centimeters
- `UNIT_M` - Meters
- `UNIT_INCH` - Inches
- `UNIT_DEG` - Degrees
- `UNIT_RAD` - Radians
- `UNIT_MM_S` - Millimeters per second
- `UNIT_CM_S` - Centimeters per second
- `UNIT_M_S` - Meters per second
- `UNIT_DEG_S` - Degrees per second
- `UNIT_RAD_S` - Radians per second
- `UNIT_PERCENT` - Percentage
- `UNIT_VOLT` - Volts
- `UNIT_AMPERE` - Amperes
- `UNIT_SECOND` - Seconds
- `UNIT_MILLISECOND` - Milliseconds

---

### ControllerTypes

Robot controller types.

**Values:**
- `CONTROLLER_ABB` - ABB IRC5/S4
- `CONTROLLER_FANUC` - FANUC R-30iB
- `CONTROLLER_KUKA` - KUKA KRC4
- `CONTROLLER_MOTOMAN` - Yaskawa Motoman
- `CONTROLLER_KAWASAKI` - Kawasaki E-series
- `CONTROLLER_PANASONIC` - Panasonic
- `CONTROLLER_UNIVERSAL` - Universal Robots
- `CONTROLLER_DAIHEN` - Daihen FD-series

---

### OperationType

Operation type constants.

**Values:**
- `OPERATIONTYPE_STANDARD` - Standard operation
- `OPERATIONTYPE_HOME` - Home position
- `OPERATIONTYPE_APPROACH` - Approach motion
- `OPERATIONTYPE_RETRACT` - Retract motion
- `OPERATIONTYPE_TRANSFER` - Transfer motion

---

### InsertPosition

Event insert position.

**Values:**
- `INSERTPOSITION_BEFORE` - Insert before motion
- `INSERTPOSITION_AFTER` - Insert after motion

---

### ItemType

Item type enumeration.

**Values:**
- `ITEMTYPE_PROGRAM` - Program
- `ITEMTYPE_OPERATION` - Operation
- `ITEMTYPE_OPERATIONGROUP` - Operation group
- `ITEMTYPE_SUBPROGRAM` - Subprogram
- `ITEMTYPE_EVENT` - Event
- `ITEMTYPE_TPELEMENT` - Toolpath element
- `ITEMTYPE_CONTROLLER` - Controller
- `ITEMTYPE_ROBOT` - Robot
- `ITEMTYPE_TOOL` - Tool
- `ITEMTYPE_FIXTURE` - Fixture

---

### ItemSubtype

Item subtype enumeration.

**Values:**
- `ITEMSUBTYPE_NONE` - No subtype
- `ITEMSUBTYPE_ARCWELDING` - Arc welding
- `ITEMSUBTYPE_SPOTWELDING` - Spot welding
- `ITEMSUBTYPE_PAINTING` - Painting
- `ITEMSUBTYPE_HANDLING` - Material handling
- `ITEMSUBTYPE_CUTTING` - Cutting/laser
- `ITEMSUBTYPE_GLUING` - Gluing/sealing

---

## Additional Objects

### Matrix

4x4 transformation matrix.

#### Methods

**GetX() → float**
Gets X translation.

**GetY() → float**
Gets Y translation.

**GetZ() → float**
Gets Z translation.

**SetX(x: float)**
Sets X translation.

**SetY(y: float)**
Sets Y translation.

**SetZ(z: float)**
Sets Z translation.

**GetRX() → float**
Gets rotation around X (degrees).

**GetRY() → float**
Gets rotation around Y (degrees).

**GetRZ() → float**
Gets rotation around Z (degrees).

**Multiply(other: Matrix) → Matrix**
Matrix multiplication.

**Invert() → Matrix**
Returns inverted matrix.

**Copy() → Matrix**
Creates matrix copy.

---

### Vector

3D vector.

#### Methods

**X() → float**
Returns X component.

**Y() → float**
Returns Y component.

**Z() → float**
Returns Z component.

**Length() → float**
Returns vector length.

**Normalize() → Vector**
Returns normalized vector.

**Dot(other: Vector) → float**
Dot product.

**Cross(other: Vector) → Vector**
Cross product.

---

### TpElement

Toolpath element.

#### Methods

**GetName() → str**
Returns TPE name.

**GetMotionType() → int**
Returns motion type (PTP/LIN/CIR).

**GetPosition() → Matrix**
Returns target position.

**GetSpeed() → float**
Returns speed value.

**GetAccuracy() → float**
Returns accuracy value.

**IsReachable() → bool**
Returns reachability state.

**HasCollision() → bool**
Returns collision state.

---

*For Offline Programming callbacks and operators, see E2_API_Offline_Programming.md*  
*For Download and Upload APIs, see E2_API_Download.md and E2_API_Upload.md*  
*For ArcWelding Report utility, see E2_API_ArcWelding_Report.md*
