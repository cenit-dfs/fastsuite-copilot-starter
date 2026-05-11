# E2 Python API: Offline Programming

## Table of Contents

- [Introduction](#introduction)
  - [Tips for Beginners](#tips-for-beginners)
  - [Debugging with Visual Studio Code](#debugging-with-visual-studio-code)
  - [Python Code Style Guide](#python-code-style-guide)
  - [Python Libraries](#python-libraries)
  - [Recommendations](#recommendations)
- [Callbacks](#callbacks)
  - [IOlpTechnology](#iolptechnology)
  - [IOlpWorkMethod](#iolpworkmethod)
  - [IOlpSeries](#iolpseries)
  - [IOlpEvent](#iolpevent)
  - [IOlpEventRule](#iolpeventrule)
- [Operators](#operators)
  - [AuxiliaryCommands](#auxiliarycommands)
  - [Attribute Table Operator](#attribute-table-operator)
  - [Program Modify Operator](#program-modify-operator)
  - [Process Geometry Operator](#process-geometry-operator)

---

## Introduction

This document covers the E2 Python API for offline programming, including technology, workmethod, and event callbacks, as well as programming operators.

### Tips for Beginners

#### Python Basics

**Dynamic typing:**
- Variables don't require explicit type declaration
- Type is determined at runtime

**Operators:**
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division
- `%` : Modulo
- `**` : Exponentiation

**String concatenation:**
```python
text = "Hello " + "World"
```

**The `__init__` method:**
- Constructor method called when creating class instances
- Used for initialization

**Modules:**
- Import with `import module_name`
- Use `from module_name import function_name` for specific imports

**Lists and Tuples:**
- Lists: Mutable sequences `[1, 2, 3]`
- Tuples: Immutable sequences `(1, 2, 3)`

### Debugging with Visual Studio Code

#### Setup with ptvsd/debugpy

1. Install debugpy: `pip install debugpy`
2. Add debugging code to your script:

```python
import debugpy
debugpy.listen(5678)
print("Waiting for debugger attach...")
debugpy.wait_for_client()
```

3. Configure launch.json:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

#### IntelliSense Configuration

Create a `.vscode/settings.json` file:

```json
{
    "python.autoComplete.extraPaths": [
        "C:\\Program Files\\CENIT\\FASTSUITE Edition 2\\Lib\\site-packages"
    ],
    "python.analysis.extraPaths": [
        "C:\\Program Files\\CENIT\\FASTSUITE Edition 2\\Lib\\site-packages"
    ]
}
```

### Python Code Style Guide

Follow PEP 8 conventions:
- Use **CapWords** for class names
- Use **lowercase_with_underscores** for functions and variables
- Indent with 4 spaces

### Python Libraries

#### cenpylib

Provides utility functions for E2 integration:

**FileUtility:**
```python
from cenpylib.fileUtility import FileUtility

fu = FileUtility()
path = fu.CENIT_LOGO_FOLDER
```

**ReportUtility:**
```python
from cenpylib.report import ReportUtility

pdf = ReportUtility()
pdf.setLanguage("EN")
pdf.createAutoExecutePDFReport(Operator, appPath)
```

#### tkinter

For GUI creation:

```python
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
messagebox.showinfo("Title", "Message")
```

#### fpdf2

For PDF generation:

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="Hello World", ln=1, align='C')
pdf.output("output.pdf")
```

### Recommendations

#### Attribute Naming Conventions

**User attributes:**
```python
USER_ATTRIBUTE = "MyCustomAttribute"
```

**Download attributes:**
```python
DOWNLOAD_ATTRIBUTE = "ExportSetting"
```

#### NLS Translation Dictionaries

Use dictionaries for multi-language support:

```python
translations = {
    "EN": "English Text",
    "DE": "Deutscher Text",
    "FR": "Texte français"
}
```

---

## Callbacks

### IOlpTechnology

Technology-level callbacks for initialization and event handling.

#### PostTechInitAttributes

Creates technology attributes.

**Signature:**
```python
def PostTechInitAttributes(Operator: CENPyOlpTech_InitAtributeOperator) -> bool:
```

**Usage:**
```python
def PostTechInitAttributes(Operator):
    attribCreator = Operator.GetAttribCreator()
    
    # Create integer attribute
    attribCreator.AddInteger("WeldSpeed", 500)
    
    # Create double attribute
    attribCreator.AddDouble("Voltage", 25.0)
    
    # Create string attribute
    attribCreator.AddString("ProcessName", "ArcWelding")
    
    # Create boolean attribute
    attribCreator.AddBool("UseShielding", True)
    
    # Create enum attribute
    attribCreator.AddEnum("WeldType", ["MIG", "TIG", "Laser"], 0)
    
    return True
```

**Accessing attributes:**
```python
attribGetter = Operator.GetAttribGetter()
speed = attribGetter.GetInteger("WeldSpeed")

attribSetter = Operator.GetAttribSetter()
attribSetter.SetInteger("WeldSpeed", 600)
```

**System attributes:**
```python
sysAttribCreator = Operator.GetSysAttribCreator()
sysAttribCreator.AddMinRadius(5.0)
sysAttribCreator.AddMaxRadius(100.0)
```

#### PostTechInitEvents

Registers custom technology events.

**Signature:**
```python
def PostTechInitEvents(Operator: CENPyOlpTech_InitEventOperator) -> bool:
```

**Usage:**
```python
def PostTechInitEvents(Operator):
    # Register custom event
    Operator.RegisterPyTechnologyEvent("GasEvent.py")
    return True
```

**Custom event file (GasEvent.py):**
```python
class GasEvent:
    def GetEventName(self):
        return "Gas On/Off"
    
    def GetEventUuId(self):
        return "{12345678-1234-1234-1234-123456789012}"
    
    def GetIconName(self):
        return "gas_icon.png"
    
    def GetExplodeCycle(self):
        return False  # True if event should be expanded in cycle view
```

#### PostTechInitRules

Initializes event rules for automatic event placement.

**Signature:**
```python
def PostTechInitRules(Operator: CENPyOlpTech_InitRuleOperator) -> bool:
```

**Usage:**
```python
def PostTechInitRules(Operator):
    # Add rule to insert event after retract
    Operator.AddPyEvent(
        "GasEvent.py",
        EVENTPROCESS_RETRACT,
        TPINSERTPOS_INSERTAFTER
    )
    return True
```

**Constants:**
- `EVENTPROCESS_RETRACT` - After retract motion
- `EVENTPROCESS_APPROACH` - After approach motion
- `TPINSERTPOS_INSERTAFTER` - Insert after motion
- `TPINSERTPOS_INSERTBEFORE` - Insert before motion

#### PostInitManufacturingGeometry

Called after manufacturing geometry is initialized.

**Signature:**
```python
def PostInitManufacturingGeometry(Operator: CENPyOlpTech_InitMfGeoOperator) -> bool:
```

**Usage:**
```python
def PostInitManufacturingGeometry(Operator):
    pgOperator = Operator.GetProcessGeometryOperator()
    
    # Get regshape center
    if pgOperator.IsRegshape():
        centerMatrix = pgOperator.GetRegshapeCenter()
        x = centerMatrix.GetX()
        y = centerMatrix.GetY()
        z = centerMatrix.GetZ()
    
    return True
```

#### PrevExecuteRecipe

Called before recipe execution, allows override.

**Signature:**
```python
def PrevExecuteRecipe(Operator: CENPyOlpTech_ExecuteRecipeOperator) -> bool:
```

**Usage:**
```python
def PrevExecuteRecipe(Operator):
    # Get selected geometries
    pgList = Operator.GetSelectedProcessGeometries()
    
    # Create custom operation
    for pg in pgList:
        operation = Operator.CreateOperation("CustomOp")
        # Configure operation
        
    return True  # True = override default recipe
                 # False = use default recipe
```

#### PostTechOnAttribChanged

Called when technology attributes change.

**Signature:**
```python
def PostTechOnAttribChanged(Operator: CENPyOlpTech_OnAttribChangedOperator) -> bool:
```

**Usage:**
```python
def PostTechOnAttribChanged(Operator):
    changedAttr = Operator.GetChangedAttributeName()
    
    if changedAttr == "WeldSpeed":
        speed = Operator.GetAttribGetter().GetInteger("WeldSpeed")
        # React to speed change
        
    return True
```

#### PostProcessOperationGroupAttributes

Processes operation group attributes.

**Signature:**
```python
def PostProcessOperationGroupAttributes(
    Operator: CENPyOlpTech_ProcessOperationGroupAttribOperator) -> bool:
```

#### PostTechOnFrameChanged

Called when frames are modified.

**Signature:**
```python
def PostTechOnFrameChanged(Operator: CENPyOlpTech_OnFrameChangedOperator) -> bool:
```

**Usage:**
```python
def PostTechOnFrameChanged(Operator):
    frameName = Operator.GetChangedFrameName()
    frameIndex = Operator.GetChangedFrameIndex()
    frameType = Operator.GetChangedFrameType()
    
    # Get frame matrices
    frameMatrix = Operator.GetChangedFrameMatrix()
    worldMatrix = Operator.GetChangedFrameWorldMatrix()
    
    # Return True to request recompute
    return True
```

#### PostTechUpdate

Handles technology version updates.

**Signature:**
```python
def PostTechUpdate(Operator: CENPyOlpTech_UpdateOperator) -> bool:
```

**Usage:**
```python
def PostTechUpdate(Operator):
    currentVersion = Operator.GetPythonTechnologyVersion()
    lastSavedVersion = Operator.GetLastSavedPythonTechnologyVersion()
    
    if lastSavedVersion < currentVersion:
        # Perform migration
        program = Operator.GetOlpProgram()
        
        # Iterate components
        for component in program.GetChildComponents():
            if component.GetType() == OLPPROGRAMCOMPONENTTYPE_OPERATION:
                # Update operation
                pass
                
        # Update event rules
        techRuleOp = Operator.GetTechEventRuleUpdateOperator()
        wmRuleOp = Operator.GetWmEventRuleUpdateOperator()
        
    return True
```

---

### IOlpWorkMethod

Workmethod-level callbacks with similar patterns to technology callbacks.

#### PostWmInitAttributes

Creates workmethod attributes (identical pattern to `PostTechInitAttributes`).

**Signature:**
```python
def PostWmInitAttributes(Operator: CENPyOlpWm_InitAtributeOperator) -> bool:
```

#### PostWmInitEvents

Registers workmethod events.

**Signature:**
```python
def PostWmInitEvents(Operator: CENPyOlpWm_InitEventOperator) -> bool:
```

**Usage:**
```python
def PostWmInitEvents(Operator):
    Operator.RegisterPyTechnologyEvent("ZAxisEvent.py")
    return True
```

#### PostWmInitRules

Initializes workmethod event rules.

**Signature:**
```python
def PostWmInitRules(Operator: CENPyOlpWm_InitRuleOperator) -> bool:
```

#### PostWmOnAttribChanged

Called when workmethod attributes change.

**Signature:**
```python
def PostWmOnAttribChanged(Operator: CENPyOlpWm_OnAttribChangedOperator) -> bool:
```

#### PostWmSyncPgAttributes

Synchronizes process geometry attributes. Called only on compute, not recompute.

**Signature:**
```python
def PostWmSyncPgAttributes(Operator: CENPyOlpWm_SyncPgAttribOperator) -> bool:
```

**Usage:**
```python
def PostWmSyncPgAttributes(Operator):
    pgOperator = Operator.GetCurrentProcessGeometryOperator()
    
    # Get geometry info
    pgName = pgOperator.GetProcessGeometryName()
    isRegshape = pgOperator.IsRegshape()
    
    if isRegshape:
        center = pgOperator.GetRegshapeCenter()
        length = pgOperator.GetRegshapeLength()
        height = pgOperator.GetRegshapeHeight()
        radius = pgOperator.GetRegshapeRadius()
        cornerRadius = pgOperator.GetRegshapeCornerRadius()
        geoType = pgOperator.GetGeoType()
        shapeType = pgOperator.GetRegshapeType()
    
    # Access event attributes for specific events
    eventAttribGetter = pgOperator.GetEventAttribGetter("EventName")
    eventAttribSetter = pgOperator.GetEventAttribSetter("EventName")
    
    return True
```

#### PostProcessOperationAttributes

Processes operation attributes with CSV parsing support.

**Signature:**
```python
def PostProcessOperationAttributes(
    Operator: CENPyOlpWm_ProcessOperationAttribOperator) -> bool:
```

**Usage:**
```python
def PostProcessOperationAttributes(Operator):
    # Get geometry operator
    geoOp = Operator.GetGeometryOperator()
    
    # Vector operations
    vec1 = geoOp.CreateVector(0, 0, 1)
    vec2 = geoOp.CreateVector(1, 0, 0)
    angle = geoOp.GetIncludedAngle(vec1, vec2)
    radians = geoOp.ToRadian(90.0)
    degrees = geoOp.ToDegrees(1.5708)
    
    # CSV parsing
    from cenpylib.csvParser import CsvParser
    csv = CsvParser.LoadCsvFile("data.csv")
    
    rows = csv.GetNumberOfRows()
    cols = csv.GetNumberOfColumns()
    cell = csv.GetCell(row=0, col=0)
    rowData = csv.GetRow(row=0)
    
    return True
```

#### PostWmOnFrameChanged

Called when frames change (identical to tech version).

**Signature:**
```python
def PostWmOnFrameChanged(Operator: CENPyOlpWm_OnFrameChangedOperator) -> bool:
```

---

### IOlpSeries

Controller series-specific callbacks.

#### PostSeriesInitAttributes

Creates series-level attributes.

**Signature:**
```python
def PostSeriesInitAttributes(Operator: CENPyOlpSeries_InitAtributeOperator) -> bool:
```

#### PostSeriesInitEvents

Registers series-specific events.

**Signature:**
```python
def PostSeriesInitEvents(Operator: CENPyOlpSeries_InitEventOperator) -> bool:
```

#### PostSeriesOnAttribChanged

Called when series attributes change.

**Signature:**
```python
def PostSeriesOnAttribChanged(Operator: CENPyOlpSeries_OnAttribChangedOperator) -> bool:
```

---

### IOlpEvent

Event-specific callbacks for custom events.

#### PostInitAttributes

Initializes event attributes.

**Signature:**
```python
def PostInitAttributes(Operator: CENPyOlpEvent_InitAtributeOperator) -> bool:
```

#### PostProcessAttributes

Processes event attributes after creation.

**Signature:**
```python
def PostProcessAttributes(Operator: CENPyOlpEvent_ProcessAttribOperator) -> bool:
```

**Usage:**
```python
def PostProcessAttributes(Operator):
    # CSV reading
    from cenpylib.csvParser import CsvParser
    csv = CsvParser.LoadCsvFile("params.csv")
    
    attribSetter = Operator.GetAttribSetter()
    value = csv.GetCell(0, 0)
    attribSetter.SetString("Parameter", value)
    
    return True
```

#### PostProcessAttributesUpload

Processes attributes for uploaded events.

**Signature:**
```python
def PostProcessAttributesUpload(Operator: CENPyOlpEvent_ProcessAttribOperator) -> bool:
```

#### PostCompute

Computes event behavior during program compute.

**Signature:**
```python
def PostCompute(Operator: CENPyOlpEvent_ComputeOperator) -> bool:
```

**Usage:**
```python
def PostCompute(Operator):
    logger = Operator.GetLoggerOperator()
    attribGetter = Operator.GetAttribGetter()
    controller = Operator.GetController()
    actors = Operator.GetActors()
    sensors = Operator.GetSensors()
    
    # Get initial path matrix
    pathMatrix = Operator.GetInitialPathMatrixByLength(0.0)
    
    # Get reference TPE
    refTpe = Operator.GetRefTpElement()
    
    # Event operations
    eventOp = Operator.GetEventOperator()
    eventOp.AddSpeed(500)
    eventOp.SkipPath()
    
    # Matrix operations
    matrix = Operator.CreateMatrix()
    
    # Circular motion
    eventOp.MoveCir(centerMatrix, targetMatrix)
    
    return True
```

#### PostOnAttribChanged

Called when event attributes change.

**Signature:**
```python
def PostOnAttribChanged(Operator: CENPyOlpEvent_OnAttribChangedOperator) -> bool:
```

---

### IOlpEventRule

Event rule callbacks for automatic placement.

#### PostExecute

Executes event rule logic.

**Signature:**
```python
def PostExecute(Operator: CENPyOlpEventRule_ExecuteOperator) -> bool:
```

**Usage:**
```python
def PostExecute(Operator):
    # Find TPEs by type
    tpeList = Operator.FindTpElementsByType(TP_TYPE_LIN)
    
    # Add TPE to rule
    for tpe in tpeList:
        Operator.AddTpe(tpe)
    
    return True
```

---

## Operators

### AuxiliaryCommands

Scripts automatically executed at specific points.

#### AutoExecute Script Entries

**Location:** `Standard\AuxiliaryCommands\OlpProgram\AutoExecute.py`

**Available callbacks:**
- `PostProgramProcessGeometries` - After process geometries created
- `PostProgramReCompute` - After program recompute
- `PostProgramDownload` - After successful download
- `PostProgramUpload` - After successful upload
- `PrevProgramDownload` - Before download starts
- `PrevProgramUpload` - Before upload starts
- `PostProgramDownloadOnsite` - After onsite download
- `PostProgramUploadOnsite` - After onsite upload
- `PrevProgramDownloadOnsite` - Before onsite download
- `PrevProgramUploadOnsite` - Before onsite upload

**CycleTimeDelayCalculation:**
Custom cycle time calculation scripts.

#### OlpProgram Commands

**Location:** `Standard\AuxiliaryCommands\OlpProgram\`

Auxiliary commands available in program dashboard.

#### ProcessGeometry Commands

**Callback:** `ProgramProcessGeometries`

Called during process geometry processing.

---

### Attribute Table Operator

**Class:** `CENPyOlpAttributeTableOperator`

Manages attribute tables.

#### Methods

**GetTableName() → str**
Returns table name.

**GetLoggerOperator() → LoggerOperator**
Gets logger for messages.

**AddRow() → int**
Adds new row, returns row ID.

**GetColumnType(col: int) → str**
Returns column type.

**GetColumnName(col: int) → str**
Returns column name.

**GetColumnSize() → int**
Returns number of columns.

**GetRowSize() → int**
Returns number of rows.

**GetCell(row: int, col: int) → object**
Returns cell value.

**SetCell(row: int, col: int, value: object)**
Sets cell value.

**GetCellType(row: int, col: int) → str**
Returns cell type.

**GetImportFilePath() → str**
Returns import file path.

**GetRowNumberById(id: int) → int**
Gets row number by ID.

**GetRowValuesById(id: int) → list**
Gets row values by ID.

**GetRowValues(row: int) → list**
Gets row values by index.

**DeleteRow(row: int)**
Deletes row.

**DeleteAllRows()**
Clears all rows.

**GetColumnValueType(col: int) → str**
Returns column value type.

**GetCellValueType(row: int, col: int) → str**
Returns cell value type.

---

### Program Modify Operator

**Class:** `CENPyOlpProgramModifyOperator`

Provides program modification capabilities.

#### Methods

**GetAttribGetter() → AttribGetter**
Gets attribute getter.

**GetAttribSetter() → AttribSetter**
Gets attribute setter.

**GetLoggerOperator() → LoggerOperator**
Gets logger.

**GetController() → Controller**
Gets controller object.

**GetCsvParserOperator() → CsvParser**
Gets CSV parser.

**GetActiveProgram() → Program**
Gets active program.

**GetComputeHandler() → ComputeHandler**
Gets compute handler.

**GetInterpolationHandler() → InterpolationHandler**
Gets interpolation handler.

**GetTeachHandler() → TeachHandler**
Gets teach handler.

**GetEventHandler() → EventHandler**
Gets event handler.

**GetProgramTpElementsByName(name: str) → list[TpElement]**
Finds TPEs by name.

**CreateMatrix() → Matrix**
Creates new matrix.

---

### Process Geometry Operator

**Class:** `CENPyOlpProgramProcessGeometryOperator**

Handles process geometry operations.

---

## Constants

### Event Processing Types
- `EVENTPROCESS_RETRACT` - Retract motion
- `EVENTPROCESS_APPROACH` - Approach motion

### Insert Positions
- `TPINSERTPOS_INSERTAFTER` - Insert after motion
- `TPINSERTPOS_INSERTBEFORE` - Insert before motion

### Component Types
- `OLPPROGRAMCOMPONENTTYPE_OPERATION` - Operation component
- `OLPPROGRAMCOMPONENTTYPE_OPERATIONGROUP` - Operation group
- `OLPPROGRAMCOMPONENTTYPE_SUBPROGRAM` - Subprogram

### TP Types
- `TP_TYPE_LIN` - Linear motion
- `TP_TYPE_PTP` - Point-to-point motion
- `TP_TYPE_CIR` - Circular motion

---

*For OlpCore objects, Download, Upload, and Report APIs, see the dedicated API documents.*
