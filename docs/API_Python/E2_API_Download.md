# E2 Python API: Download

## Table of Contents

- [Overview](#overview)
- [Download Callbacks](#download-callbacks)
- [Download Objects](#download-objects)
  - [DULPythonAccuracyProfile](#dulpythonaccuracyprofile)
  - [DULPythonController](#dulpythoncontroller)
  - [DULPythonEvent](#dulpythonevent)
  - [DULPythonJoint](#dulpythonjoint)
  - [DULPythonMotion](#dulpythonmotion)
  - [DULPythonPosition](#dulpythonposition)
  - [DULPythonProgram](#dulpythonprogram)
  - [DULPythonSpeedProfile](#dulpythonspeedprofile)
- [Download Operators](#download-operators)
  - [DULPythonDownloadOperator](#dulpythondownloadoperator)
- [Download Enums](#download-enums)
- [Download Scripts](#download-scripts)
  - [downloadStarter.py](#downloadstarterpy)
  - [downloader.py](#downloaderpy)

---

## Overview

The Download API provides classes and methods for generating robot controller code from E2 offline programs.

---

## Download Callbacks

Download callbacks are defined in the downloader script to customize code generation.

### Available Callbacks

**PreDownload**
Called before download starts.

**PostDownload**
Called after download completes.

**PreProgram**
Called before program download.

**PostProgram**
Called after program download.

**PreOperation**
Called before operation download.

**PostOperation**
Called after operation download.

**PreMotion**
Called before motion download.

**PostMotion**
Called after motion download.

**PreEvent**
Called before event download.

**PostEvent**
Called after event download.

---

## Download Objects

### DULPythonAccuracyProfile

Represents accuracy/approximation settings.

#### Methods

**GetType() → int**
Returns accuracy type.

**GetValue() → float**
Returns accuracy value.

**IsActive() → bool**
Returns active state.

**GetDistance() → float**
Returns distance accuracy (mm).

**GetOrientation() → float**
Returns orientation accuracy (degrees).

**GetVelocity() → float**
Returns velocity accuracy (%).

#### Usage

```python
def PreMotion(motion):
    accuracy = motion.GetAccuracyProfile()
    if accuracy.IsActive():
        acType = accuracy.GetType()
        value = accuracy.GetValue()
```

---

### DULPythonController

Provides controller information during download.

#### Methods

**GetName() → str**
Returns controller name.

**GetManufacturer() → str**
Returns manufacturer.

**GetSeries() → str**
Returns controller series.

**GetVersion() → str**
Returns controller version.

**GetIP() → str**
Returns IP address.

**GetPort() → int**
Returns port number.

**GetOutputPath() → str**
Returns download output path.

**GetAttribute(name: str) → object**
Gets controller attribute value.

#### Usage

```python
def PreDownload(controller):
    name = controller.GetName()
    series = controller.GetSeries()
    outputPath = controller.GetOutputPath()
```

---

### DULPythonEvent

Represents technology event during download.

#### Methods

**GetName() → str**
Returns event name.

**GetType() → str**
Returns event type.

**GetUuid() → str**
Returns event UUID.

**GetInsertPosition() → int**
Returns insert position (before/after).

**GetAttribute(name: str) → object**
Gets event attribute value.

**GetBoolAttribute(name: str) → bool**
Gets boolean attribute.

**GetIntegerAttribute(name: str) → int**
Gets integer attribute.

**GetDoubleAttribute(name: str) → float**
Gets double attribute.

**GetStringAttribute(name: str) → str**
Gets string attribute.

**GetEnumAttribute(name: str) → int**
Gets enum attribute index.

**GetEnumAttributeName(name: str) → str**
Gets enum attribute option name.

#### Usage

```python
def PreEvent(event):
    eventName = event.GetName()
    insertPos = event.GetInsertPosition()
    
    # Get event attributes
    speed = event.GetDoubleAttribute("Speed")
    enabled = event.GetBoolAttribute("Enabled")
    mode = event.GetEnumAttributeName("Mode")
```

---

### DULPythonJoint

Represents joint configuration.

#### Methods

**GetNumberOfAxes() → int**
Returns number of axes.

**GetJointValue(index: int) → float**
Returns joint value by index (degrees).

**GetJointValues() → list[float]**
Returns all joint values.

**IsValid() → bool**
Returns validity state.

**GetExternalAxisValues() → list[float]**
Returns external axis values.

**GetTurns() → list[int]**
Returns axis turn values.

#### Usage

```python
def PreMotion(motion):
    joint = motion.GetJoint()
    if joint.IsValid():
        numAxes = joint.GetNumberOfAxes()
        values = joint.GetJointValues()
        
        for i, val in enumerate(values):
            print(f"Axis {i+1}: {val:.2f} degrees")
```

---

### DULPythonMotion

Represents robot motion.

#### Methods

**GetName() → str**
Returns motion name.

**GetMotionType() → int**
Returns motion type (PTP/LIN/CIR).

**GetPosition() → DULPythonPosition**
Returns target position.

**GetJoint() → DULPythonJoint**
Returns joint configuration.

**GetSpeed() → DULPythonSpeedProfile**
Returns speed profile.

**GetAccuracyProfile() → DULPythonAccuracyProfile**
Returns accuracy profile.

**IsReachable() → bool**
Returns reachability state.

**HasCollision() → bool**
Returns collision state.

**GetPathLength() → float**
Returns path length (mm).

**GetCycleTime() → float**
Returns cycle time (seconds).

**GetAttribute(name: str) → object**
Gets motion attribute.

#### Motion Types

- `MOTIONTYPE_PTP` - Point-to-point
- `MOTIONTYPE_LIN` - Linear
- `MOTIONTYPE_CIR` - Circular

#### Usage

```python
def PreMotion(motion):
    motionType = motion.GetMotionType()
    position = motion.GetPosition()
    speed = motion.GetSpeed()
    
    if motionType == MOTIONTYPE_LIN:
        # Handle linear motion
        pass
    elif motionType == MOTIONTYPE_CIR:
        # Handle circular motion
        pass
```

---

### DULPythonPosition

Represents Cartesian position.

#### Methods

**GetX() → float**
Returns X coordinate (mm).

**GetY() → float**
Returns Y coordinate (mm).

**GetZ() → float**
Returns Z coordinate (mm).

**GetRX() → float**
Returns rotation around X (degrees).

**GetRY() → float**
Returns rotation around Y (degrees).

**GetRZ() → float**
Returns rotation around Z (degrees).

**GetMatrix() → list[list[float]]**
Returns 4x4 transformation matrix.

**GetFrameName() → str**
Returns reference frame name.

**IsValid() → bool**
Returns validity state.

#### Usage

```python
def PreMotion(motion):
    pos = motion.GetPosition()
    x = pos.GetX()
    y = pos.GetY()
    z = pos.GetZ()
    rx = pos.GetRX()
    ry = pos.GetRY()
    rz = pos.GetRZ()
    
    print(f"Position: X={x:.2f}, Y={y:.2f}, Z={z:.2f}")
    print(f"Rotation: RX={rx:.2f}, RY={ry:.2f}, RZ={rz:.2f}")
```

---

### DULPythonProgram

Represents program being downloaded.

#### Methods

**GetName() → str**
Returns program name.

**GetProgramType() → int**
Returns program type.

**GetOperationCount() → int**
Returns number of operations.

**GetMotionCount() → int**
Returns total motion count.

**GetEventCount() → int**
Returns total event count.

**GetCycleTime() → float**
Returns total cycle time (seconds).

**GetPathLength() → float**
Returns total path length (mm).

**GetAttribute(name: str) → object**
Gets program attribute.

#### Usage

```python
def PreProgram(program):
    progName = program.GetName()
    opCount = program.GetOperationCount()
    cycleTime = program.GetCycleTime()
    
    print(f"Downloading program: {progName}")
    print(f"Operations: {opCount}")
    print(f"Cycle time: {cycleTime:.2f}s")
```

---

### DULPythonSpeedProfile

Represents speed settings.

#### Methods

**GetType() → int**
Returns speed type.

**GetValue() → float**
Returns speed value.

**GetUnit() → str**
Returns speed unit.

**IsPercentage() → bool**
Returns True if speed is percentage.

**IsAbsolute() → bool**
Returns True if speed is absolute value.

**GetLinearSpeed() → float**
Returns linear speed (mm/s).

**GetAngularSpeed() → float**
Returns angular speed (deg/s).

**GetAcceleration() → float**
Returns acceleration value.

#### Usage

```python
def PreMotion(motion):
    speed = motion.GetSpeed()
    
    if speed.IsPercentage():
        value = speed.GetValue()
        print(f"Speed: {value}%")
    else:
        linSpeed = speed.GetLinearSpeed()
        print(f"Speed: {linSpeed} mm/s")
```

---

## Download Operators

### DULPythonDownloadOperator

Main operator providing download functionality.

#### Methods

**GetController() → DULPythonController**
Returns controller object.

**GetProgram() → DULPythonProgram**
Returns program being downloaded.

**WriteFile(filename: str, content: str)**
Writes file to output directory.

**WriteLine(line: str)**
Writes line to current file.

**GetLogger() → Logger**
Returns logger for messages.

**LogInfo(message: str)**
Logs info message.

**LogWarning(message: str)**
Logs warning message.

**LogError(message: str)**
Logs error message.

**GetOutputPath() → str**
Returns download output path.

**CreateDirectory(path: str)**
Creates output directory.

**FileExists(filename: str) → bool**
Checks if file exists in output.

**ReadFile(filename: str) → str**
Reads file from output directory.

**GetAttribute(name: str) → object**
Gets download setting attribute.

#### Usage

```python
def PostDownload(operator):
    controller = operator.GetController()
    program = operator.GetProgram()
    
    # Write summary file
    content = f"Program: {program.GetName()}\n"
    content += f"Controller: {controller.GetName()}\n"
    content += f"Cycle time: {program.GetCycleTime():.2f}s\n"
    
    operator.WriteFile("summary.txt", content)
    operator.LogInfo("Summary file created")
```

---

## Download Enums

### Motion Type Constants

- `MOTIONTYPE_PTP` - Point-to-point motion
- `MOTIONTYPE_LIN` - Linear motion
- `MOTIONTYPE_CIR` - Circular motion
- `MOTIONTYPE_SPLINE` - Spline motion

### Insert Position Constants

- `INSERTPOSITION_BEFORE` - Before motion
- `INSERTPOSITION_AFTER` - After motion

### Accuracy Type Constants

- `ACCURACY_OFF` - No accuracy
- `ACCURACY_ON` - Accuracy enabled
- `ACCURACY_DISTANCE` - Distance-based
- `ACCURACY_ORIENTATION` - Orientation-based
- `ACCURACY_VELOCITY` - Velocity-based

---

## Download Scripts

### downloadStarter.py

Entry point for download process.

**Location:** `OLPTranslators/<VENDOR>/`

**Structure:**
```python
def StartDownload(Operator):
    """
    Main entry point called by E2.
    
    Args:
        Operator: DULPythonDownloadOperator
    
    Returns:
        bool: True if download successful
    """
    # Initialize downloader
    from downloader import Downloader
    
    downloader = Downloader()
    result = downloader.Execute(Operator)
    
    return result
```

---

### downloader.py

Main download implementation.

**Location:** `OLPTranslators/<VENDOR>/`

**Structure:**
```python
class Downloader:
    def __init__(self):
        self.operator = None
        
    def Execute(self, operator):
        """Main download method."""
        self.operator = operator
        
        # Get objects
        controller = operator.GetController()
        program = operator.GetProgram()
        
        # Pre-download
        if not self.PreDownload(controller):
            return False
            
        # Process program
        if not self.ProcessProgram(program):
            return False
            
        # Post-download
        return self.PostDownload()
        
    def PreDownload(self, controller):
        """Called before download."""
        return True
        
    def PostDownload(self):
        """Called after download."""
        return True
        
    def ProcessProgram(self, program):
        """Process program download."""
        return True
```

---

## Example: Complete Downloader

```python
# downloader.py
class Downloader:
    def __init__(self):
        self.operator = None
        self.outputLines = []
        
    def Execute(self, operator):
        self.operator = operator
        controller = operator.GetController()
        program = operator.GetProgram()
        
        # Generate program file
        self.GenerateProgram(program)
        
        # Write output
        filename = f"{program.GetName()}.prg"
        content = "\n".join(self.outputLines)
        operator.WriteFile(filename, content)
        
        operator.LogInfo(f"Downloaded {filename}")
        return True
        
    def GenerateProgram(self, program):
        self.outputLines.append(f"PROGRAM {program.GetName()}")
        self.outputLines.append("")
        
        # Process operations would go here
        
        self.outputLines.append("END_PROGRAM")
        
    def PreMotion(self, motion):
        motionType = motion.GetMotionType()
        pos = motion.GetPosition()
        speed = motion.GetSpeed()
        
        if motionType == MOTIONTYPE_LIN:
            line = f"  LIN {{X {pos.GetX():.2f}, Y {pos.GetY():.2f}, Z {pos.GetZ():.2f}}}"
            line += f" V={speed.GetLinearSpeed():.0f}"
            self.outputLines.append(line)
            
        return True
        
    def PreEvent(self, event):
        line = f"  {event.GetName()}"
        self.outputLines.append(line)
        return True
```

---

*For OlpCore objects, see E2_API_OlpCore.md*  
*For Upload API, see E2_API_Upload.md*  
*For Offline Programming callbacks, see E2_API_Offline_Programming.md*
