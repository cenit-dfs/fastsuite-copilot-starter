# E2 Python API: Upload

## Table of Contents

- [Overview](#overview)
- [Upload Callbacks](#upload-callbacks)
- [Upload Objects](#upload-objects)
  - [ULPythonBaseProfile](#ulpythonbaseprofile)
  - [ULPythonController](#ulpythoncontroller)
  - [ULPythonEvent](#ulpythonevent)
  - [ULPythonMotion](#ulpythonmotion)
  - [ULPythonPosition](#ulpythonposition)
  - [ULPythonProgram](#ulpythonprogram)
- [Upload Operators](#upload-operators)
  - [ULPythonUploadOperator](#ulpythonuploadoperator)
- [Upload Scripts](#upload-scripts)
  - [uploadStarter.py](#uploadstarterpy)
  - [uploader.py](#uploaderpy)

---

## Overview

The Upload API provides classes and methods for importing robot controller programs into E2 offline environment.

---

## Upload Callbacks

Upload callbacks are defined in the uploader script to customize program import.

### Available Callbacks

**PreUpload**
Called before upload starts.

**PostUpload**
Called after upload completes.

**PreParseFile**
Called before file parsing.

**PostParseFile**
Called after file parsing.

**PreCreateProgram**
Called before program creation.

**PostCreateProgram**
Called after program creation.

**PreCreateOperation**
Called before operation creation.

**PostCreateOperation**
Called after operation creation.

---

## Upload Objects

### ULPythonBaseProfile

Base profile information.

#### Methods

**GetName() → str**
Returns profile name.

**GetType() → str**
Returns profile type.

**GetValue() → float**
Returns profile value.

---

### ULPythonController

Provides controller information during upload.

#### Methods

**GetName() → str**
Returns controller name.

**GetManufacturer() → str**
Returns manufacturer.

**GetSeries() → str**
Returns controller series.

**GetVersion() → str**
Returns controller version.

**GetSourcePath() → str**
Returns upload source path.

**SetAttribute(name: str, value: object)**
Sets controller attribute.

#### Usage

```python
def PreUpload(controller):
    name = controller.GetName()
    series = controller.GetSeries()
    sourcePath = controller.GetSourcePath()
    
    print(f"Uploading from: {sourcePath}")
```

---

### ULPythonEvent

Represents event during upload.

#### Methods

**GetName() → str**
Returns event name.

**GetType() → str**
Returns event type.

**SetName(name: str)**
Sets event name.

**SetType(eventType: str)**
Sets event type.

**SetUuid(uuid: str)**
Sets event UUID.

**SetInsertPosition(pos: int)**
Sets insert position (before/after).

**SetAttribute(name: str, value: object)**
Sets event attribute.

**SetBoolAttribute(name: str, value: bool)**
Sets boolean attribute.

**SetIntegerAttribute(name: str, value: int)**
Sets integer attribute.

**SetDoubleAttribute(name: str, value: float)**
Sets double attribute.

**SetStringAttribute(name: str, value: str)**
Sets string attribute.

**SetEnumAttribute(name: str, value: int)**
Sets enum attribute by index.

**SetEnumAttributeByName(name: str, valueName: str)**
Sets enum attribute by name.

#### Usage

```python
def CreateArcOnEvent(operator):
    event = operator.CreateEvent("ArcOn")
    event.SetType("TechEvent")
    event.SetUuid("{ARCON-UUID}")
    event.SetInsertPosition(INSERTPOSITION_BEFORE)
    
    # Set event attributes
    event.SetDoubleAttribute("Voltage", 25.5)
    event.SetDoubleAttribute("Current", 180.0)
    event.SetBoolAttribute("GasOn", True)
    
    return event
```

---

### ULPythonMotion

Represents motion during upload.

#### Methods

**GetName() → str**
Returns motion name.

**GetMotionType() → int**
Returns motion type.

**SetName(name: str)**
Sets motion name.

**SetMotionType(motionType: int)**
Sets motion type (PTP/LIN/CIR).

**SetPosition(pos: ULPythonPosition)**
Sets target position.

**SetSpeed(speed: float)**
Sets speed value.

**SetAccuracy(accuracy: float)**
Sets accuracy value.

**SetAttribute(name: str, value: object)**
Sets motion attribute.

#### Motion Types

- `MOTIONTYPE_PTP` - Point-to-point
- `MOTIONTYPE_LIN` - Linear
- `MOTIONTYPE_CIR` - Circular

#### Usage

```python
def CreateLinearMotion(operator, x, y, z):
    motion = operator.CreateMotion("P001")
    motion.SetMotionType(MOTIONTYPE_LIN)
    
    pos = operator.CreatePosition()
    pos.SetX(x)
    pos.SetY(y)
    pos.SetZ(z)
    pos.SetRX(180.0)
    pos.SetRY(0.0)
    pos.SetRZ(0.0)
    
    motion.SetPosition(pos)
    motion.SetSpeed(500.0)
    motion.SetAccuracy(1.0)
    
    return motion
```

---

### ULPythonPosition

Represents Cartesian position during upload.

#### Methods

**GetX() → float**
Returns X coordinate.

**GetY() → float**
Returns Y coordinate.

**GetZ() → float**
Returns Z coordinate.

**GetRX() → float**
Returns rotation around X.

**GetRY() → float**
Returns rotation around Y.

**GetRZ() → float**
Returns rotation around Z.

**SetX(x: float)**
Sets X coordinate (mm).

**SetY(y: float)**
Sets Y coordinate (mm).

**SetZ(z: float)**
Sets Z coordinate (mm).

**SetRX(rx: float)**
Sets rotation around X (degrees).

**SetRY(ry: float)**
Sets rotation around Y (degrees).

**SetRZ(rz: float)**
Sets rotation around Z (degrees).

**SetFromMatrix(matrix: list[list[float]])**
Sets position from 4x4 matrix.

**SetFrameName(name: str)**
Sets reference frame name.

#### Usage

```python
def CreatePosition(operator, x, y, z, rx, ry, rz):
    pos = operator.CreatePosition()
    pos.SetX(x)
    pos.SetY(y)
    pos.SetZ(z)
    pos.SetRX(rx)
    pos.SetRY(ry)
    pos.SetRZ(rz)
    pos.SetFrameName("World")
    return pos
```

---

### ULPythonProgram

Represents program during upload.

#### Methods

**GetName() → str**
Returns program name.

**SetName(name: str)**
Sets program name.

**SetProgramType(progType: int)**
Sets program type.

**SetAttribute(name: str, value: object)**
Sets program attribute.

**AddOperation(operation: Operation)**
Adds operation to program.

**GetOperationCount() → int**
Returns operation count.

#### Usage

```python
def PreCreateProgram(program):
    program.SetName("UploadedProgram")
    program.SetAttribute("Description", "Uploaded from controller")
```

---

## Upload Operators

### ULPythonUploadOperator

Main operator providing upload functionality.

#### Methods

**GetController() → ULPythonController**
Returns controller object.

**GetProgram() → ULPythonProgram**
Returns program being uploaded.

**CreateProgram(name: str) → ULPythonProgram**
Creates new program.

**CreateOperation(name: str) → Operation**
Creates new operation.

**CreateMotion(name: str) → ULPythonMotion**
Creates new motion.

**CreatePosition() → ULPythonPosition**
Creates new position.

**CreateEvent(name: str) → ULPythonEvent**
Creates new event.

**ReadFile(filename: str) → str**
Reads file from source directory.

**FileExists(filename: str) → bool**
Checks if file exists.

**GetFileList(pattern: str) → list[str]**
Gets list of files matching pattern.

**GetLogger() → Logger**
Returns logger.

**LogInfo(message: str)**
Logs info message.

**LogWarning(message: str)**
Logs warning message.

**LogError(message: str)**
Logs error message.

**GetSourcePath() → str**
Returns upload source path.

**GetAttribute(name: str) → object**
Gets upload setting attribute.

#### Usage

```python
def StartUpload(operator):
    controller = operator.GetController()
    
    # Read program file
    filename = "robot_program.prg"
    if operator.FileExists(filename):
        content = operator.ReadFile(filename)
        
        # Parse and create program
        program = ParseProgram(operator, content)
        
        operator.LogInfo(f"Uploaded {filename}")
        return True
    else:
        operator.LogError(f"File not found: {filename}")
        return False
```

---

## Upload Scripts

### uploadStarter.py

Entry point for upload process.

**Location:** `OLPTranslators/<VENDOR>/`

**Structure:**
```python
def StartUpload(Operator):
    """
    Main entry point called by E2.
    
    Args:
        Operator: ULPythonUploadOperator
    
    Returns:
        bool: True if upload successful
    """
    # Initialize uploader
    from uploader import Uploader
    
    uploader = Uploader()
    result = uploader.Execute(Operator)
    
    return result
```

---

### uploader.py

Main upload implementation.

**Location:** `OLPTranslators/<VENDOR>/`

**Structure:**
```python
class Uploader:
    def __init__(self):
        self.operator = None
        
    def Execute(self, operator):
        """Main upload method."""
        self.operator = operator
        
        # Get objects
        controller = operator.GetController()
        
        # Pre-upload
        if not self.PreUpload(controller):
            return False
            
        # Process files
        files = operator.GetFileList("*.prg")
        for filename in files:
            if not self.ProcessFile(filename):
                return False
                
        # Post-upload
        return self.PostUpload()
        
    def PreUpload(self, controller):
        """Called before upload."""
        return True
        
    def PostUpload(self):
        """Called after upload."""
        return True
        
    def ProcessFile(self, filename):
        """Process single file."""
        content = self.operator.ReadFile(filename)
        # Parse and create program
        return True
```

---

## Example: Complete Uploader

```python
# uploader.py
import re

class Uploader:
    def __init__(self):
        self.operator = None
        
    def Execute(self, operator):
        self.operator = operator
        controller = operator.GetController()
        
        # Get program files
        files = operator.GetFileList("*.prg")
        if not files:
            operator.LogError("No program files found")
            return False
            
        # Process each file
        for filename in files:
            self.ProcessFile(filename)
            
        operator.LogInfo(f"Uploaded {len(files)} programs")
        return True
        
    def ProcessFile(self, filename):
        """Parse and create program from file."""
        content = self.operator.ReadFile(filename)
        lines = content.split('\n')
        
        # Create program
        progName = filename.replace('.prg', '')
        program = self.operator.CreateProgram(progName)
        
        # Create operation
        operation = self.operator.CreateOperation("Main")
        
        # Parse motions
        for line in lines:
            line = line.strip()
            
            # Parse LIN motion
            if line.startswith('LIN'):
                motion = self.ParseLinMotion(line)
                if motion:
                    operation.AddMotion(motion)
                    
            # Parse event
            elif line.startswith('ARC'):
                event = self.ParseArcEvent(line)
                if event:
                    operation.AddEvent(event)
                    
        program.AddOperation(operation)
        return True
        
    def ParseLinMotion(self, line):
        """Parse linear motion line."""
        # Example: LIN {X 100.0, Y 200.0, Z 300.0} V=500
        match = re.search(r'X\s+([\d.]+),\s*Y\s+([\d.]+),\s*Z\s+([\d.]+)', line)
        if not match:
            return None
            
        x = float(match.group(1))
        y = float(match.group(2))
        z = float(match.group(3))
        
        # Create motion
        motion = self.operator.CreateMotion("P")
        motion.SetMotionType(MOTIONTYPE_LIN)
        
        # Create position
        pos = self.operator.CreatePosition()
        pos.SetX(x)
        pos.SetY(y)
        pos.SetZ(z)
        pos.SetRX(180.0)
        pos.SetRY(0.0)
        pos.SetRZ(0.0)
        
        motion.SetPosition(pos)
        
        # Parse speed
        speedMatch = re.search(r'V=([\d.]+)', line)
        if speedMatch:
            speed = float(speedMatch.group(1))
            motion.SetSpeed(speed)
            
        return motion
        
    def ParseArcEvent(self, line):
        """Parse arc event line."""
        # Example: ARCON V=25.5 I=180.0
        event = self.operator.CreateEvent("ArcOn")
        event.SetType("TechEvent")
        event.SetInsertPosition(INSERTPOSITION_BEFORE)
        
        # Parse voltage
        voltageMatch = re.search(r'V=([\d.]+)', line)
        if voltageMatch:
            voltage = float(voltageMatch.group(1))
            event.SetDoubleAttribute("Voltage", voltage)
            
        # Parse current
        currentMatch = re.search(r'I=([\d.]+)', line)
        if currentMatch:
            current = float(currentMatch.group(1))
            event.SetDoubleAttribute("Current", current)
            
        return event
```

---

## Best Practices

### File Parsing

1. **Read all files first:**
```python
files = operator.GetFileList("*.prg")
for filename in files:
    content = operator.ReadFile(filename)
```

2. **Handle missing files gracefully:**
```python
if not operator.FileExists(filename):
    operator.LogWarning(f"File not found: {filename}")
    return True  # Continue with other files
```

3. **Use regex for parsing:**
```python
import re
pattern = r'LIN\s+\{X\s+([\d.]+)'
match = re.search(pattern, line)
```

### Program Structure

1. **Create program hierarchy:**
```python
program = operator.CreateProgram("MainProgram")
operation = operator.CreateOperation("Op1")
motion = operator.CreateMotion("P001")
operation.AddMotion(motion)
program.AddOperation(operation)
```

2. **Set attributes early:**
```python
program.SetName("UploadedProgram")
program.SetAttribute("Description", "From controller")
```

3. **Log progress:**
```python
operator.LogInfo(f"Processing file: {filename}")
operator.LogInfo(f"Created {motionCount} motions")
```

---

*For Download API, see E2_API_Download.md*  
*For OlpCore objects, see E2_API_OlpCore.md*  
*For Offline Programming callbacks, see E2_API_Offline_Programming.md*
