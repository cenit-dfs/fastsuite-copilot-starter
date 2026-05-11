# E2 Python API: ArcWelding Report Utility

## Table of Contents

- [Overview](#overview)
- [ReportUtility Class](#reportutility-class)
- [Report Settings](#report-settings)
  - [Method Calls](#method-calls)
  - [Language Files](#language-files)
- [Column Configuration](#column-configuration)
- [NLS Translation](#nls-translation)
- [Inheritance](#inheritance)
- [Example Usage](#example-usage)

---

## Overview

The ArcWelding Report Utility provides PDF report generation for offline programs with customizable columns, language support, and branding.

---

## ReportUtility Class

**Import:**
```python
from cenpylib.report import ReportUtility
```

### Main Methods

#### createAutoExecutePDFReport

Creates report from AutoExecute command (after download).

**Signature:**
```python
def createAutoExecutePDFReport(self, Operator, apppath, selection=""):
```

**Parameters:**
- `Operator` - CENPyOlpProgramModifyOperator
- `apppath` - Location of caller script (for images)
- `selection` - Optional list of columns (default: predefined columns)

**Available columns:**
- `"Name"` - TPE name
- `"MotionType"` - Motion type (PTP/LIN/CIR)
- `"Length"` - Path length (mm)
- `"Speed"` - Motion speed
- `"Time"` - Cycle time
- `"Costs"` - Calculated costs
- `"CollReach"` - Collision/reachability status
- `"Events"` - Events on TPE
- `"Various"` - Custom column

**Usage:**
```python
def PostProgramDownload(Operator):
    pdf = ReportUtility()
    pdf.setLanguage("EN")
    pdf.createAutoExecutePDFReport(Operator, "")
```

#### createAuxCommandsPDFReport

Creates report from Auxiliary Commands in program dashboard.

**Signature:**
```python
def createAuxCommandsPDFReport(self, Operator, apppath, selection=""):
```

**Parameters:** Same as `createAutoExecutePDFReport`

**Usage:**
```python
def ModifyActiveProgram(Operator):
    pdf = ReportUtility()
    pdf.setLanguage("DE")
    
    # Custom column selection
    columns = ["Name", "MotionType", "Length", "Time"]
    pdf.createAuxCommandsPDFReport(Operator, "", columns)
```

#### createPDFReport

Main method for custom report generation.

**Signature:**
```python
def createPDFReport(self, Operator, apppath, repfilepath, selection=""):
```

**Parameters:**
- `Operator` - CENPyOlpProgramModifyOperator
- `apppath` - Location of caller script
- `repfilepath` - Output path for PDF file
- `selection` - Optional column list

---

## Report Settings

### Method Calls

#### setLanguage

Sets report language.

**Signature:**
```python
def setLanguage(self, language):
```

**Parameters:**
- `language` - Language code: `"EN"`, `"DE"`, `"FR"`, `"CN"`, `"JP"`

**Usage:**
```python
pdf = ReportUtility()
pdf.setLanguage("CN")  # Chinese
```

#### setHeaderLogo

Sets custom header logo.

**Signature:**
```python
def setHeaderLogo(self, filename):
```

**Parameters:**
- `filename` - Image filename (jpg, png)

**Usage:**
```python
myPath = "C:\\Technologies\\TechnologyCommon\\Standard\\AuxiliaryCommands\\Logos\\"
pdf.setHeaderLogo("MyCustomerHeader.jpg")
pdf.createAutoExecutePDFReport(Operator, myPath)
```

#### setFooterLogo

Sets custom footer logo.

**Signature:**
```python
def setFooterLogo(self, filename):
```

**Parameters:**
- `filename` - Image filename (jpg, png)

#### setCosts

Sets cost per meter for calculation.

**Signature:**
```python
def setCosts(self, value):
```

**Parameters:**
- `value` - Cost per meter (float)

**Usage:**
```python
pdf.setCosts(2.56)
```

#### setCurrency

Sets currency symbol for costs.

**Signature:**
```python
def setCurrency(self, currency):
```

**Parameters:**
- `currency` - Currency code: `"E"` (Euro), `"D"` (Dollar), `"P"` (Pound), `"Y"` (Yen/Yuan)

**Default:** Euro (€)

**Usage:**
```python
pdf.setCurrency("D")  # Dollar
```

---

### Language Files

#### Location

**Default:** `\Lib\site-packages\cenpylib\languages`

**Custom:** Copy entire `languages` folder to custom path, pass to `createPDFReport`

#### Available Settings

**defaultreportname**
Default PDF filename (## replaced by program name).

```
defaultreportname=Report_##.pdf
```

**setfontname**
Font type (not applicable for CN/JP).

```
setfontname=Arial
```

**setfontsize**
Font size (applies to all languages).

```
setfontsize=10
```

**commandname**
Command name in auxiliary commands menu.

```
commandname=Generate Report
```

**operationheader**
Operation header style:
- `0` - None, but divider
- `1` - Only operation name (default)
- `2` - Group & operation name
- `3` - Absolutely none

```
operationheader=1
```

**operationsummary**
Summary row after each operation (0 = no summary).

```
operationsummary=0
```

**nologouse**
Use header/footer images (True = no images).

```
nologouse=False
```

**headerrowcolorrgb**
Table header background color (RGB format: xxx.yyy.zzz).

```
headerrowcolorrgb=176.176.176
```

**Column widths**
Naming: `[columnName]colwidth`

```
Namecolwidth=40
MotionTypecolwidth=15
Lengthcolwidth=20
```

---

## Column Configuration

### Default Columns

By default, 6 columns are displayed:
1. Name
2. MotionType
3. Length
4. Speed
5. Time
6. Costs

### Custom Column Selection

**Specify exact column order:**
```python
pdf = ReportUtility()
columns = ["Name", "MotionType", "Speed", "Time", "Events"]
pdf.createAuxCommandsPDFReport(Operator, "", columns)
```

**Note:** Column names must match exactly.

### Column Details

| Column | Description | Unit |
|--------|-------------|------|
| Name | TPE name | - |
| MotionType | PTP/LIN/CIR | - |
| Length | Path length | mm |
| Speed | Motion speed | mm/s or % |
| Time | Cycle time | seconds |
| Costs | Calculated costs | Currency |
| CollReach | Collision/unreachable status | - |
| Events | Events on TPE | - |
| Various | Custom data | - |

---

## NLS Translation

### NLS Files

**Location:** `\Lib\site-packages\cenpylib\languages\*.lng`

**Supported languages:** English, German, French, Chinese, Japanese

### Using NLS in Scripts

```python
from cenpylib.nlsUtility import NLSUtility

nls = NLSUtility()
nls.defineNLS(project="report")

# Get translated item
cmdname = nls.getNLS("commandname", "Report")  # Default: "Report"
```

### Available Report Items

**Program info:**
- `programname` - Program
- `controllername` - Controller
- `totalcycletime` - Total cycle time
- `totalpathlenght` - Total path length

**Table headers:**
- `name` - Name
- `motiontype` - Motion type
- `length` - Length [mm]
- `speed` - Speed [mm/s]
- `time` - Time [s]
- `costs` - Costs [##]  (## replaced by currency)
- `collreach` - Coll/Reach
- `events` - Events
- `various` - Various

**Motion types:**
- `ptp` - PTP
- `lin` - LIN
- `cir` - CIR

---

## Inheritance

### Custom Report Class

Override methods for deep customization.

```python
class ReportUtility(ReportUtility):
    '''
    Inherited class for customized PDF reports.
    '''
    
    def cenheader(self, Operator, path, portrLands):
        '''
        Customized header section.
        '''
        # General info table
        self.ln(4)
        self.header_table(Operator)
        self.ln(20)
        
        # Custom logo placement
        filepath = path + self.__headerLogo
        if exists(filepath):
            hpos = 140 if portrLands == "P" else 200
            self.image(filepath, 10, 60, 100)
```

### Inheritable Methods

**cenheader(Operator, path, portrLands)**
Customizes header section below common header.

**cenfooter(path, portrLands)**
Customizes footer section below common footer.

**body(Operator, headLine, colWidths, order)**
Customizes report body/table.

**calculateCosts(costPerMeter, length, technoState, motionType)**
Custom cost calculation logic.

**getVariousField(operator, opTpe)**
Custom data for "Various" column.

---

## Example Usage

### Basic Report

```python
def PostProgramDownload(Operator):
    pdf = ReportUtility()
    pdf.setLanguage("EN")
    pdf.createAutoExecutePDFReport(Operator, "")
```

### Custom Branding

```python
def ModifyActiveProgram(Operator):
    pdf = ReportUtility()
    
    logoPath = "C:\\MyCompany\\Logos\\"
    pdf.setHeaderLogo("CompanyLogo.png")
    pdf.setFooterLogo("CompanyFooter.png")
    pdf.setLanguage("FR")
    
    pdf.createAuxCommandsPDFReport(Operator, logoPath)
```

### Cost Calculation

```python
def PostProgramDownload(Operator):
    pdf = ReportUtility()
    
    pdf.setCosts(2.56)  # €2.56 per meter
    pdf.setCurrency("E")  # Euro
    pdf.setLanguage("DE")
    
    # Include costs column
    columns = ["Name", "Length", "Time", "Costs"]
    pdf.createAutoExecutePDFReport(Operator, "", columns)
```

### Multi-Language Support

```python
def CreateReport(Operator, language):
    pdf = ReportUtility()
    pdf.setLanguage(language)  # "EN", "DE", "FR", "CN", "JP"
    
    logoPath = "C:\\Technologies\\Logos\\"
    pdf.setHeaderLogo("Logo.jpg")
    
    # Language-specific settings handled automatically
    pdf.createAuxCommandsPDFReport(Operator, logoPath)
```

### Custom Columns

```python
def ModifyActiveProgram(Operator):
    pdf = ReportUtility()
    pdf.setLanguage("EN")
    
    # Minimal report: only name, type, and time
    columns = ["Name", "MotionType", "Time"]
    
    # Detailed report: all available columns
    # columns = ["Name", "MotionType", "Length", "Speed", 
    #            "Time", "Costs", "CollReach", "Events", "Various"]
    
    pdf.createAuxCommandsPDFReport(Operator, "", columns)
```

### Inherited Custom Report

```python
def ModifyActiveProgram(Operator):
    pdf = MyCustomReport()
    pdf.setLanguage("fr")
    pdf.createAuxCommandsPDFReport(Operator, "")

class MyCustomReport(ReportUtility):
    '''Custom report with modified header.'''
    
    def cenheader(self, Operator, path, portrLands):
        '''Reordered header section.'''
        self.ln(4)
        self.header_table(Operator)
        self.ln(20)
        
        # Logo placement
        filepath = path + self.__headerLogo
        if not exists(filepath):
            fu = FileUtility()
            filepath = fu.CENIT_LOGO_FOLDER + "\\" + self.__headerLogo
            
        if exists(filepath):
            hpos = 140 if portrLands == "L" else 200
            self.image(filepath, 10, 60, 100)
    
    def calculateCosts(self, costPerMeter, length, technoState, motionType):
        '''Custom cost calculation - only charge for welding.'''
        if technoState == 1:  # Tool ON
            return costPerMeter * length / 1000.0
        else:
            return 0.0
```

---

## Complete Example

```python
from cenpylib.report import ReportUtility
from cenpylib.fileUtility import FileUtility

def PostProgramDownload(Operator: CENPyOlpProgramModifyOperator):
    '''
    Generate comprehensive PDF report after download.
    '''
    pdf = ReportUtility()
    
    # Configure branding
    fu = FileUtility()
    logoPath = fu.CENIT_LOGO_FOLDER
    pdf.setHeaderLogo("CustomerLogo.jpg")
    pdf.setFooterLogo("CustomerFooter.png")
    
    # Configure language and costs
    pdf.setLanguage("EN")
    pdf.setCosts(2.50)  # €2.50 per meter
    pdf.setCurrency("E")  # Euro
    
    # Select columns to display
    columns = [
        "Name",
        "MotionType",
        "Length",
        "Speed",
        "Time",
        "Costs",
        "Events"
    ]
    
    # Generate report
    pdf.createAutoExecutePDFReport(Operator, logoPath, columns)
    
    # Log completion
    logger = Operator.GetLoggerOperator()
    logger.Info("PDF report generated successfully")
```

---

*For Offline Programming callbacks, see E2_API_Offline_Programming.md*  
*For Download API, see E2_API_Download.md*  
*For OlpCore objects, see E2_API_OlpCore.md*
