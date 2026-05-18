"""
COPYRIGHT Cenit AG Q1/2023
    Class "ArcReportUtility" for PDF Reports
    can be called from AuxiliaryCommands
    
    AutoExecute :
       def createAuxCommandArcWeldReport(self, Operator):
    
    
    possible Call from PostProgramDownload::ModifyActiveProgram()
       arc = ArcReportUtility()
       arc.createAuxCommandArcWeldReport(Operator, "")
"""

# import libraries
from datetime import datetime
from os.path import exists
from centypes import *
from .file import *
from .nls import *
from .ui import *
import os, locale
import math
import tkinter as tk

# import custom libraries
from fpdf import FPDF

from tkinter import *
from tkinter import filedialog


class ArcReportUtility(FPDF):
   '''
   Class "ArcReportUtility" for ArcWelding PDF Reports
   '''
   
   AW_OPERATION_WORKMETHOD_NAME = "ArcWeldingOperationWorkMethodName"
   AW_STITCHWELDING_WORKMETHOD = "StitchWeldingWorkMethod";
   AW_ARC_PRGNR_DEF = "ProgNumberDefine"
   AW_SPEED_WELDING = "Speed"
   AW_ARC_ON_EVENT_NAME = "ArcOnEvent"
   AW_ARC_OFF_EVENT_NAME = "ArcOffEvent"
   
   # ==        ==========================================================================================
   def __init__(self):
      '''
      Initialization
      '''
      super().__init__()
      self.__appPath = FileUtility().CENIT_LANGUAGE_FOLDER + "\\"
      self.__NLS = NLSUtility()
      self.__language = ""
      self.__downloadFolder = ""
      self.__maxTCPFeedrate = 1.6
      self.__unit = 0
      self.__systemUnit = ""
      self.__systemSizeUnit = ""
      self.__systemFeedUnit = ""
      self.__systemTimeUnit = ""
      self.__returnState = 0
      
   # ==               ==========================================================================================
   def createAuxCommandArcWeldReport(self, Operator, apppath):
      '''
      Pass Command from AutoExecute, e.g. after Download
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         apppath: the Location of the customer NLS Files.
      '''
      # get logger (global)
      self.__logging = Operator.GetLoggerOperator()
      # if no Path given take default
      forNLSPath = ""
      if apppath == "":
         apppath = self.__appPath
      else:
         self.__appPath = apppath
         forNLSPath = apppath
      
      # defines the NLS Translation : FileUtility().defineNLS(self, language = "", project = "", altpath = ""):
      if self.__language == "":
         self.__language = self.__NLS.getETwoNLS(Operator)
      if self.__language == "None":
         self.__language = ""
      self.__NLS.defineNLS(self.__language, "arcreport", forNLSPath)
      
      #self.__unit = Operator.GetSystemUnit() # metric/imperial
      if self.__unit == 1:
         self.__systemUnit = " " + self.__NLS.getNLS("unitImperial", "inch*")
         self.__systemSizeUnit = " " + self.__NLS.getNLS("unitFeet", "ft.*")
      else:
         self.__systemUnit = " " + self.__NLS.getNLS("unitMetric", "mm*")
         self.__systemSizeUnit = " " + self.__NLS.getNLS("unitMeter", "m*")
      self.__systemFeedUnit = self.__systemUnit + "/" + self.__NLS.getNLS("unitTime", "sec*")
      self.__systemTimeUnit = " " + self.__NLS.getNLS("unitTime", "sec*")
      
      # build the Report Name
      defaultFileName = self.buildReportName(Operator.GetActiveProgram().GetName(), Operator.GetController().GetName())
      # build Report's Path/File
      if self.__downloadFolder == "":
         self.__downloadFolder = Operator.GetController().GetOutputDirectory()
      repfilepath =  self.__downloadFolder + "\\" + defaultFileName
      
      # set the desired Font&Size
      self.defineFont()
      
      self.createPDFReport(Operator, repfilepath)
      
      return self.__returnState

   # ==               ==========================================================================================
   def createPDFReport(self, Operator, repfilepath):
      '''
      Main Method to create the PDF Report
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         repfilepath: the Location of the where the PDF Report should be written.
      '''
      
      self.__logging.LogInfo("ArcWeld PDF-Report : " + self.__NLS.getNLS("pdfbegin", "PDF Report creation is going to start...*") + " : " + str(repfilepath))
      
      # check for existing Target Folder
      dlPath = os.path.dirname(repfilepath)
      dlPathExist = os.path.exists(dlPath)
      # self.__logging.LogInfo("................................repfilepath=" + str(dlPath) + " = " + str(dlPathExist))
      if dlPathExist == False:
         self.__returnState = 2
         return
      
      # define desired Range and Order of Columns. Technology Table
      # [1],     [2],        [3],           [4],              [5],            [6],           [7],                [8],           [9],       [10],         [11],      [12],         [13]
      #"Id", "Material", "SeamSize", "WeldingPosition", "WeldingSpeed", "WireDiameter", "WireFeedSpeed", "WireConsumption", "Voltage", "Current", "GasFlow", "GasFlowRate", "TotalWeldingTime"
      # get the Columns (seperate Method for easier inheritance)
      columns = self.techColumnSelection()
      headLineTech, colWidthsTech, orderTech, totalWidthTech = self.defineColumnTitleWidth(columns)
      totalWidth = totalWidthTech
      
      # define desired Range and Order of Columns. Welding Operations Table
      #    [1],       [2],      [3],           [4],              [5],         [6]
      # "WeldSeam", "WPSID", "SeamSize", "WeldingPosition", "SeamLength", "WeldingTime"
      # get the Columns (seperate Method for easier inheritance)
      columns = self.weldColumnSelection()
      headLineOps, colWidthsOps, orderOps, totalWidthOps = self.defineOpsColumnTitleWidth(columns)
      if totalWidthOps > totalWidthTech:
         totalWidth = totalWidthOps
      
      # Portrait or Landscape Format
      global portrLands
      portrLands = "P"
      if (totalWidth > 180):
         portrLands = "L"
      
      # Resource´s max. TCP Feedrate to calc. correct Speed
      self.__maxTCPFeedrate = Operator.GetController().GetMainResourcesMaxTCPFeedrate()
      
      #-----------------------------------------------------------------------------
      # Common Header
      self.add_page(portrLands)
      # Related Header
      self.cenheader(Operator, portrLands)
      #-----------------------------------------------------------------------------
      self.techTable(Operator, headLineTech, colWidthsTech, orderTech)
      self.weldTable(Operator, headLineOps, colWidthsOps, orderOps)
      #-----------------------------------------------------------------------------
      # Related Footer
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.0))
      self.cenfooter(portrLands)
      # Common Footer
      self.output(repfilepath)
      #-----------------------------------------------------------------------------
      self.__logging.LogInfo("ArcWeld PDF-Report : " + self.__NLS.getNLS("pdfsuccess", "PDF Report successfully created*.") + " : " + str(repfilepath))

   # ==               ==========================================================================================
   def techColumnSelection(self):
      '''
      Get the desired Set of Columns and its Order.
      
      Returns:
         str: the List of Columns
      '''
      #          [1],     [2],        [3],           [4],              [5],            [6],           [7],                [8],           [9],       [10],         [11],      [12],         [13]
      columns = ["Id", "Material", "SeamSize", "WeldingPosition", "WeldingSpeed", "WireDiameter", "WireFeedSpeed", "WireConsumption", "Voltage", "Current", "GasFlow", "GasFlowRate", "TotalWeldingTime"]
      return columns
   # ==               ==========================================================================================
   def weldColumnSelection(self):
      '''
      Get the desired Set of Columns and its Order.
      
      Returns:
         str: the List of Columns
      '''
      #             [1],       [2],      [3],           [4],              [5],         [6]
      columns = ["WeldSeam", "WPSID", "SeamSize", "WeldingPosition", "SeamLength", "WeldingTime"]
      return columns
   # ==               ==========================================================================================
   def buildReportName(self, programName, controllerName):
      '''
      Build Report File Name, to be inheritate if customizing desired.
      
      Args:
         programName: the Process Program Name
         controllerName: the Name of the Controller
      
      Returns:
         str: fileName: the desired File Name
      '''
      reportName = self.__NLS.getNLS("defaultreportname","ArcWeldReport_++_##")
      reportName = reportName.replace("++", str(controllerName))
      reportName = reportName.replace("##", str(programName))
      fileName = reportName + ".pdf"
      return fileName
   
   def defineFont(self):
      '''
      Defines the desired Font Type and size to Globals.
      Note : CN & JP are only supported by one unique Font, Size can be adjusted
      '''
      self.__fontStyle = "B"
      if self.__language == "CN":
         self.__fontType = "Simsun"
         fu = FileUtility()
         filepath = fu.CENIT_LANGUAGE_FOLDER + "\\font\\unifont\\SIMSUN.ttf"
         self.add_font(self.__fontType, "", filepath, uni=True)
         self.__fontStyle = ""
      elif self.__language == "JP":
         self.__fontType = "rounded-mgenplus-1c-light"
         fu = FileUtility()
         filepath = fu.CENIT_LANGUAGE_FOLDER + "\\font\\unifont\\rounded-mgenplus-1c-light.ttf"
         self.add_font(self.__fontType, "", filepath, uni=True)
         self.__fontStyle = ""
      else:
         self.__fontType = self.__NLS.getNLS("setfontname","Arial")
      
      self.__fontSize = int(self.__NLS.getNLS("setfontsize","10"))
      
   # ==               ==========================================================================================
   def setLanguage(self, language):
      '''
      Sets the desired Language
      
      Args:
         language : the desired NLS Language 
         english "EN",  german "DE",  french "FR",  chinese "CN",  japanese "JP"
      '''
      range = ["EN", "DE", "FR", "CN", "JP"]
      if not range.count(language.upper()):
         language = "EN"
      self.__language = language.upper()
   
   def setReportUnit(self, unit):
      '''
      Sets the desired Unit mm/inch
      
      Args:
         unit : the desired unit mm or inch
      '''
      if unit == "inch" or unit == "INCH" or unit == "imperial":
         self.__systemUnit = " " + self.__NLS.getNLS("unitImperial", "inch*")
         self.__systemSizeUnit = " " + self.__NLS.getNLS("unitFeet", "ft.*")
         self.__unit = 1
      else:
         self.__systemUnit = " " + self.__NLS.getNLS("unitMetric", "mm*")
         self.__systemSizeUnit = " " + self.__NLS.getNLS("unitMeter", "m*")
         self.__unit = 0
   
   def setDownloadFolder(self, folder):
      '''
      Sets the desired Report Download Folder, vary from standard DL-Folder
      
      Args:
         folder : the desired Folder 
      '''
      dbl = chr(92) + chr(92)
      sgl = chr(92)
      folder = folder.replace(dbl, sgl)
      if folder[-1:] == sgl:
         folder = folder[:-1]
      folder = folder.replace(sgl, dbl)
      # should be "C:\\..\\..\\blablabla"
      self.__downloadFolder = folder

   # ==               ==========================================================================================
   def defineColumnTitleWidth(self, columns):
      '''
      Defines the Order of the desired Table Columns.
      Note: internal Column Name and its Place in the Order must be fix
      
      Args:
         columns : the desired List of Columns in desired Order
      Possible Items : "Id", "Material", "SeamSize", "WeldingPosition", "WireDiameter", "GasFlowRate", "WireFeedSpeed", "WeldingSpeed", "Current", "Voltage", "WireConsumption", "GasFlow", "TotalWeldingTime"
      
      Returns:
         strList: headLine   : the List of the Columns Header Names in desired Order
         strList: colWidth   : the List of the Columns Width in desired Order
         intList: order      : the List of the ordered Column Numbers
         int :    totalWidth : the total Width of all Columns to define Portrait or Landscape Format
      '''
      # define the Columns Titel & Width
      headLine = []
      colWidth = []
      order = []
      totalWidth = 0
      for name in columns:
         if(name == "Id"):
            title, width = self.defineColId()
            order.append(1)
         if(name == "Material"):
            title, width = self.defineColMaterial()
            order.append(2)
         if(name == "SeamSize"):
            title, width = self.defineColSeamSize()
            order.append(3)
         if(name == "WeldingPosition"):
            title, width = self.defineColWeldingPosition()
            order.append(4)
         if(name == "WeldingSpeed"):
            title, width = self.defineColWeldingSpeed()
            order.append(5)
         if(name == "WireDiameter"):
            title, width = self.defineColWireDiameter()
            order.append(6)
         if(name == "WireFeedSpeed"):
            title, width = self.defineColWireFeedSpeed()
            order.append(7)
         if(name == "WireConsumption"):
            title, width = self.defineColWireConsumption()
            order.append(8)
         if(name == "Voltage"):
            title, width = self.defineColVoltage()
            order.append(9)
         if(name == "Current"):
            title, width = self.defineColCurrent()
            order.append(10)
         if(name == "GasFlow"):
            title, width = self.defineColGasFlow()
            order.append(11)
         if(name == "GasFlowRate"):
            title, width = self.defineColGasFlowRate()
            order.append(12)
         if(name == "TotalWeldingTime"):
            title, width = self.defineColTotalWeldingTime()
            order.append(13)
            
         headLine.append(title)
         colWidth.append(width)
         totalWidth += width

      return headLine, colWidth, order, totalWidth

   # ==               ==========================================================================================
   def defineOpsColumnTitleWidth(self, columns):
      '''
      Defines the Order of the desired Table Columns.
      Note: internal Column Name and its Place in the Order must be fix
      
      Args:
         columns : the desired List of Columns in desired Order
      Possible Items : "WeldSeam", "WPSID", "SeamSize", "WeldingPosition", "SeamLength", "WeldingTime"
      
      Returns:
         strList: headLine   : the List of the Columns Header Names in desired Order
         strList: colWidth   : the List of the Columns Width in desired Order
         intList: order      : the List of the ordered Column Numbers
         int :    totalWidth : the total Width of all Columns to define Portrait or Landscape Format
      '''
      # define the Columns Titel & Width
      headLine = []
      colWidth = []
      order = []
      totalWidth = 0
      for name in columns:
         if(name == "WeldSeam"):
            title, width = self.defineColOpsWeldSeam()
            order.append(1)
         if(name == "WPSID"):
            title, width = self.defineColOpsWPSID()
            order.append(2)
         if(name == "SeamSize"):
            title, width = self.defineColOpsSeamSize()
            order.append(3)
         if(name == "WeldingPosition"):
            title, width = self.defineColOpsWeldingPosition()
            order.append(4)
         if(name == "SeamLength"):
            title, width = self.defineColOpsSeamLength()
            order.append(5)
         if(name == "WeldingTime"):
            title, width = self.defineColOpsWeldingTime()
            order.append(6)
            
         headLine.append(title)
         colWidth.append(width)
         totalWidth += width

      return headLine, colWidth, order, totalWidth

   # ==============================================================================================================
   '''
   Defines the Table Header Name and Width of the Items
   Each Item must have its own Method
   Possible Items : "Id", "Material", "SeamSize", "WeldingPosition", "WireDiameter", "GasFlowRate", "WireFeedSpeed", "WeldingSpeed", "Current", "Voltage", "WireConsumption", "GasFlow", "TotalWeldingTime"
      
   Returns:
      str: the Header Name of the Column 
      int: the Column Width
   '''
   def defineColId(self):
      return self.__NLS.getNLS("Id","Id*"), int(self.__NLS.getNLS("IdWidth","21"))
   def defineColMaterial(self):
      return self.__NLS.getNLS("Material","Material*"),  int(self.__NLS.getNLS("MaterialWidth","21"))
   def defineColSeamSize(self):
      return self.__NLS.getNLS("SeamSize","Seam Size*") + self.__systemUnit,  int(self.__NLS.getNLS("SeamSizeWidth","21"))
   def defineColWeldingPosition(self):
      return self.__NLS.getNLS("WeldingPosition","Welding Position*"),  int(self.__NLS.getNLS("WeldingPositionWidth","21"))
   def defineColWeldingSpeed(self):
      return self.__NLS.getNLS("WeldingSpeed","Welding Speed*") + self.__systemFeedUnit,  int(self.__NLS.getNLS("WeldingSpeedWidth","21"))
   def defineColWireDiameter(self):
      return self.__NLS.getNLS("WireDiameter","Wire Diameter*") + self.__systemUnit,  int(self.__NLS.getNLS("WireDiameterWidth","21"))
   def defineColWireFeedSpeed(self):
      return self.__NLS.getNLS("WireFeedSpeed","Wire Feed Speed*") + self.__systemFeedUnit,  int(self.__NLS.getNLS("WireFeedSpeedWidth","21"))
   def defineColWireConsumption(self):
      return self.__NLS.getNLS("WireConsumption","Wire Consumption*"),  int(self.__NLS.getNLS("WireConsumptionWidth","21"))
   def defineColVoltage(self):
      return self.__NLS.getNLS("Voltage","Voltage*"),  int(self.__NLS.getNLS("VoltageWidth","21"))
   def defineColCurrent(self):
      return self.__NLS.getNLS("Current","Current*"),  int(self.__NLS.getNLS("CurrentWidth","21"))
   def defineColGasFlow(self):
      return self.__NLS.getNLS("GasFlow","Gas Flow*"),  int(self.__NLS.getNLS("GasFlowWidth","21"))
   def defineColGasFlowRate(self):
      return self.__NLS.getNLS("GasFlowRate","Gas Flow Rate*"),  int(self.__NLS.getNLS("GasFlowRateWidth","21"))
   def defineColTotalWeldingTime(self):
      return self.__NLS.getNLS("TotalWeldingTime","Total Welding Time*") + self.__systemTimeUnit,  int(self.__NLS.getNLS("TotalWeldingTimeWidth","21"))
   '''
   Possible Items : "WeldSeam", "WPSID", "SeamSize", "WeldingPosition", "SeamLength", "WeldingTime"
   '''
   def defineColOpsWeldSeam(self):
      return self.__NLS.getNLS("WeldSeamOps","Weld Seam*"), int(self.__NLS.getNLS("WeldSeamOpsWidth","35"))
   def defineColOpsWPSID(self):
      return self.__NLS.getNLS("WPSIDOps","WPS ID*"),  int(self.__NLS.getNLS("WPSIDOpsWidth","35"))
   def defineColOpsSeamSize(self):
      return self.__NLS.getNLS("SeamSizeOps","Seam Size*") + self.__systemUnit,  int(self.__NLS.getNLS("SeamSizeOpsWidth","35"))
   def defineColOpsWeldingPosition(self):
      return self.__NLS.getNLS("WeldingPositionOps","Welding Position*"),  int(self.__NLS.getNLS("WeldingPositionOpsWidth","35"))
   def defineColOpsSeamLength(self):
      return self.__NLS.getNLS("SeamLengthOps","Seam Length*") + self.__systemSizeUnit,  int(self.__NLS.getNLS("SeamLengthOpsWidth","35"))
   def defineColOpsWeldingTime(self):
      return self.__NLS.getNLS("WeldingTimeOps","Welding Time*") + self.__systemTimeUnit,  int(self.__NLS.getNLS("WeldingTimeOpsWidth","35"))
      
   # ===========================================================================================================
   # ==               ==========================================================================================
   def header(self):
      '''
      Defines the common Header of the PDF Report, called from FPDF Base Class
      '''
      # Setting font
      # self.defineFont()
      # ...done in cenheader, Table and Header collides from 2nd Page

   def cenheader(self, Operator, portrLands):
      '''
      Defines the customized Header of the PDF Report, underneath common Header
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         portrLands : if Report is created in Portrait or Landscape Mode
      '''
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.5))
      self.set_font(style=self.__fontStyle)
      self.cell(80, 10, self.__NLS.getNLS("title","Arc Welding Report*"), border=0, align="L")
      # Performing a line break:
      self.ln(2)
      self.header_table(Operator)
      
   def cenfooter(self, portrLands):
      '''
      Defines the customized Footer of the PDF Report, underneath common Header
      
      Args:
         portrLands : if Report is created in Portrait or Landscape Mode
      '''
      self.ln(2)
      # Comment "The calculated lengths, speeds and times use a direct connection of the tool path elements. Accuracy, acceleration and deceleration behavior of the robot/machine are not taken into account."
      self.ln(8)
      self.set_font(self.__fontType, size=int(self.__fontSize))
      wid = 200
      if portrLands == "L":
         wid = 280
      # self.multi_cell(wid, 8, self.__NLS.getNLS("consideration","Calculated without accuracy, acceleration and deceleration*"), border=0, align="L")
      # footer line
      self.ln(8)
      self.set_font(self.__fontType, size=int(self.__fontSize))
      self.cell(80, 10, self.__NLS.getNLS("title","Arc Welding Report*") + " " + self.__NLS.getNLS("finished","finished*"), border=0, align="L")

   def footer(self):
      '''
      Defines the common Footer of the PDF Report, called from FPDF Base Class
      '''
      # Position cursor at 1.5 cm from bottom:
      self.set_y(-20)
      # Setting font: arial 10
      self.set_font(self.__fontType, size=int(self.__fontSize))
      # Printing page number:
      self.cell(0, 10, self.__NLS.getNLS("page","Page*") + f"{self.page_no()}/{{nb}}", align="R")


   # ==               ==========================================================================================
   # ==               ==========================================================================================
   def techTable(self, Operator, headLine, colWidths, order):
      '''
      Defines the customized Body of the PDF Report.
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         headLine : the List of the Columns Header Names
         colWidths : the List of the Columns Width
         order : the List of the ordered Column Numbers
      '''
      self.ln(8)
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.2))
      self.cell(180, 10, self.__NLS.getNLS("techTablePrelude","Welding procedure data sets*"), border=0, align="L")
      self.ln(2)
      # ----------- get all information from the Program ------
      controller = Operator.GetController()
      techTableList = controller.GetWeldingDataSetsFromDataBase()
      techList = []
      if len(techTableList) < 1:
         row = [self.__NLS.getNLS("tableNo","No"),self.__NLS.getNLS("tableTechnology","Technology"),self.__NLS.getNLS("tableTable","Table"),self.__NLS.getNLS("tableLoaded","loaded"),"-","-","-","-","-","-","-","-","-"]
         techList.append(row)
      else:
         for tableRow in techTableList:
            #self.__logging.LogInfo("....................tableRow:" + str(tableRow))
            #get the List and Order from : CENPyOlpController::GetWeldingDataSetsFromDataBase()
            row = []
            if len(tableRow) > 13:  
               # NEW EXTENDED FORMAT (24 Items)
               iP = 1
               row.append(str(tableRow[0]) + "/" + str(tableRow[1]) )                # Id/SubId
               row.append(str(tableRow[2+iP]))                # Material
               row.append(str(round(self.unitConvert(tableRow[4+iP]*1000),2)))  # SeamSize
               row.append(str(self.weldPosition(tableRow[8+iP]))) # WeldingPosition
               row.append(str(round(self.unitConvert(tableRow[9+iP]*1000),2)))  # WeldingSpeed
               row.append(str(round(self.unitConvert(tableRow[10+iP]*1000),2)))  # WireDiameter
               row.append(str(round(self.unitConvert(tableRow[17+iP]*1000),2)))  # WireFeedSpeed
               row.append(str(round(tableRow[18+iP],2)))       # WireConsumption
               row.append(str(round(tableRow[19+iP],0)))       # Voltage
               row.append(str(round(tableRow[20+iP],2)))       # Current
               row.append(str(round(tableRow[21+iP]*0.06,3)))      # GasFlow
               row.append(str(round(tableRow[22+iP],2)))      # GasConsumption
               row.append(str(round(tableRow[23+iP],2)))      # TotalWeldingTime
            else:
               # OLD FORMAT (13 Items)
               row.append(str(tableRow[0]))                # Id
               row.append(str(tableRow[1]))                # Material
               row.append(str(round(self.unitConvert(tableRow[2]*1000),2)))  # SeamSize
               row.append(str(self.weldPosition(tableRow[3]))) # WeldingPosition
               row.append(str(round(self.unitConvert(tableRow[4]*1000),2)))  # WeldingSpeed
               row.append(str(round(self.unitConvert(tableRow[5]*1000),2)))  # WireDiameter
               row.append(str(round(self.unitConvert(tableRow[6]*1000),2)))  # WireFeedSpeed
               row.append(str(round(tableRow[7],2)))       # WireConsumption
               row.append(str(round(tableRow[8],0)))       # Voltage
               row.append(str(round(tableRow[9],2)))       # Current
               row.append(str(round(tableRow[10]*0.06,3)))      # GasFlow
               row.append(str(round(tableRow[11],2)))      # GasConsumption
               row.append(str(round(tableRow[12],2)))      # TotalWeldingTime
            rowOrdered = self.columnOrder(order, row)
            techList.append(rowOrdered)
      
      # -------- write the Techno Tables ---------------
      self.colored_table(headLine, techList, colWidths)
      self.ln(2)
      # -------------------------------------------------------
   # ==               ==========================================================================================
   def weldTable(self, Operator, headLine, colWidths, order):
      '''
      Defines the customized Body of the PDF Report.
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         headLine : the List of the Columns Header Names
         colWidths : the List of the Columns Width
         order : the List of the ordered Column Numbers
      '''
      self.ln(8)
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.2))
      self.cell(180, 10, self.__NLS.getNLS("weldTablePrelude","Welding report*"), border=0, align="L")
      self.ln(2)
      
      
      # get active program
      program = Operator.GetActiveProgram()
      # get all operations
      operations = program.GetOperations()
      # ----------- get all Operations in Program ------
      opList = []
      for op in operations:
         pgmnr = 0
         feed = 0.01
         attribGetter = op.GetAttribGetter()
         
         # ONLY STITCHWELDING OPERATIONS !
         wmAttrib = attribGetter.GetAttributeByName(self.AW_OPERATION_WORKMETHOD_NAME)
         wmName = ""
         if wmAttrib.IsValid():
            wmName = attribGetter.GetString(self.AW_OPERATION_WORKMETHOD_NAME)
         if wmName != self.AW_STITCHWELDING_WORKMETHOD:
            continue
         
         opAttrib = attribGetter.GetAttributeByName(self.AW_ARC_PRGNR_DEF)
         if opAttrib.IsValid():
            pgmnr = attribGetter.GetInteger(self.AW_ARC_PRGNR_DEF)
         opAttrib = attribGetter.GetAttributeByName(self.AW_SPEED_WELDING)
         if opAttrib.IsValid():
            feed = attribGetter.GetDouble(self.AW_SPEED_WELDING)
         if feed < 0.00001:
            feed = 0.001
         # self.__logging.LogInfo("....................ProgNumberDefine:" + str(pgmnr))
         # self.__logging.LogInfo("...............................Speed:" + str(feed))
         # ----------------------- getting Contour Data and DataSet -----------------------
         weldingLength = self.collectOperation(Operator, op)
         dataSet = self.getRelatedDataSet(Operator, pgmnr)
         # ----------------------- getting Contour Data and DataSet -----------------------
         row = []
         row.append(str(op.GetName()))
         row.append(str(pgmnr))                     # Id
         if dataSet[6] == -999:
            row.append(str(dataSet[0]))      # Error
            row.append("-")                  # didnot found DataSet
            weldingTime = weldingLength / feed
         else:
            #get DB-Items List and Order from : CENPyOlpController::GetWeldingDataSetsFromDataBase()
            item = [2,3,12] # DataSet holds 13 Items (Legacy)
            if len(dataSet) > 13:
               item = [5,9,24] # DataSet holds 24 Items (>~2024.2)
            row.append(str(round(self.unitConvert(dataSet[item[0]]*1000),2)))      # SeamSize
            row.append(str(self.weldPosition(dataSet[item[1]]))) # WeldingPosition
            if dataSet[item[2]] > 0:
               weldingTime = weldingLength * dataSet[item[2]]   # ContourLength * WeldingTime
            else:
               weldingTime = weldingLength / feed
         
         row.append(str(round(self.unitConvert(weldingLength,1),3)))
         row.append(str(round(weldingTime,1)))
         rowOrdered = self.columnOrder(order, row)
         opList.append(rowOrdered)
      # -------- write the Toolpath Information ---------------
      self.colored_table(headLine, opList, colWidths)
      # -------------------------------------------------------   
      
   # ==               ==========================================================================================
   def unitConvert(self, value, var=0):
      '''
      Converts a Value to the set Unit.
      '''
      if self.__unit == 0:
         return value
      if var == 1:
         ret = value*3.281 # meter to feet
      else:
         ret = value/25.4 # mm to inch
      return ret
   
   # ==               ==========================================================================================
   def getRelatedDataSet(self, Operator, pgmnr):
      '''
      Check and returns if there is a related DataSet where the Program number fits.
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         pgmnr : the Welding Program Number
         
      Returns:
         list: the List of the related DataSet or default
      '''
      controller = Operator.GetController()
      techTableList = controller.GetWeldingDataSetsFromDataBase()
      
      row = [self.__NLS.getNLS("tableDataSet","No Dataset found.*"),"-","-","-","-","-",-999]
      if len(techTableList) > 0:
         for tableRow in techTableList:
            #self.__logging.LogInfo("....................tableRow:" + str(tableRow))
            if pgmnr == tableRow[0]:
               return tableRow
      return row
   # ==               ==========================================================================================
   def weldPosition(self, index):
      '''
      Check and returns if there is a related DataSet where the Program number fits.
      
      Args:
         index : the Integer Index for the Welding Position
         
      Returns:
         string: the Name of the Welding Position
      '''
      if index == 0:
         return "PA"
      if index == 1:
         return "PB"
      if index == 2:
         return "PC"
      if index == 3:
         return "PD"
      if index == 4:
         return "PE"
      if index == 5:
         return "PF"
      if index == 6:
         return "PG"
      if index == 7:
         return "PH"
      if index == 8:
         return "PJ"
         
      return self.__NLS.getNLS("tableWeldPosition","unknown*")
   
   # ==               ==========================================================================================
   
   def collectOperation(self, Operator, operation):
      '''
      Looping through the requested Operation and getting the welded Length.
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         operation : the Adress of the requested Operation
         
      Returns:
         length: the welded Length of the Operation
      '''
      contourLength = 0.0
      tpeCount = 0
      nrTpes = 0
      technoFlag = 0
      lastTpE = None
      
      teachHandler = Operator.GetTeachHandler()
      eventHandler = Operator.GetEventHandler()
      opTpes = operation.GetTpElements()
      nrTpes = len(opTpes)
      
      # ----------------------- loop TPEs --------------------------
      for opTpe in opTpes:
         tpeCount +=1
         
         # check TPE for ArcOn/Off Events
         arcOnEvent, arcOnInsPos = self.getAnyEvent(eventHandler, opTpe, self.AW_ARC_ON_EVENT_NAME)
         if arcOnEvent == True and arcOnInsPos == TPINSERTPOS_INSERTBEFORE :
            technoFlag = 1
         arcOffEvent, arcOffInsPos = self.getAnyEvent(eventHandler, opTpe, self.AW_ARC_OFF_EVENT_NAME)
         if arcOffEvent == True and arcOffInsPos == TPINSERTPOS_INSERTBEFORE :
            technoFlag = 0
         
         if technoFlag == 1 and lastTpE != None:
            # calculate Weld Length
            if (opTpe.GetMotionType() == MOTIONTYPE_CIR):
               # path is cicle -> calc circle length
               tpeLength = self.calcCircLength(teachHandler, lastTpE, opTpe)
               contourLength += tpeLength
            elif (opTpe.GetMotionType() == MOTIONTYPE_LIN):
               # path is linear -> calc line length
               tpeLength = self.calcLinLength(teachHandler, lastTpE, opTpe)
               contourLength += tpeLength
         
         if arcOnEvent == True and arcOnInsPos == TPINSERTPOS_INSERTAFTER :
            technoFlag = 1
         if arcOffEvent == True and arcOffInsPos == TPINSERTPOS_INSERTAFTER :
            technoFlag = 0
         
         # save Tpe for Length Calculation
         lastTpE = opTpe
      
      return contourLength
   
   # ==               ==========================================================================================
   def columnOrder(self, order, unsorted):
      '''
      Sorts the complete Range of Columns to the desired Order of the single Columns
      
      Args:
         order    : the numeric List of the desired Order
         unsorted : the complete Range of Information per TPE
      
      Returns:
         strList: sorted: the List of the sorted and desired Columns per TPE
      '''
      # bring Values into correct Column
      iC = 0
      sorted = []
      for nr in order:
         sorted.append(unsorted[nr-1])
      return sorted

   # ==               ==========================================================================================
   def header_table(self, Operator):
      '''
      Write a Table with common Program Information
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
      '''
      program = Operator.GetActiveProgram()
      # Colors, line width and bold font:
      self.ln(8)
      self.set_fill_color(255, 255, 255)
      self.set_text_color(0, 0, 0)
      self.set_draw_color(0, 0, 0)
      self.set_line_width(0.3)
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.0))
      # -----------------------------------------------------------------------
      frame = 0
      lineHeight = 6
      self.cell(40, lineHeight, self.__NLS.getNLS("programname","Program name*:"), border=frame, align="L", fill=False)
      self.cell(80, lineHeight, str(program.GetName()), border=frame, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      self.cell(40, lineHeight, self.__NLS.getNLS("controller","Controller*:"), border=frame, align="L", fill=False)
      self.cell(80, lineHeight, str(Operator.GetController().GetName()), border=frame, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      # today = datetime.now()
      today = datetime.datetime.now()
      date = str(today.day).zfill(2) + "." + str(today.month).zfill(2) + "." + str(today.year).zfill(2)
      date += "   " + str(today.hour).zfill(2) + ":" + str(today.minute).zfill(2) + ":" + str(today.second).zfill(2)
      self.cell(40, lineHeight, self.__NLS.getNLS("date","Date*:"), border=frame, align="L", fill=False)
      self.cell(80, lineHeight, date , border=frame, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      self.cell(40, lineHeight, self.__NLS.getNLS("operator","Operator*:"), border=frame, align="L", fill=False)
      self.cell(80, lineHeight, str(os.getlogin()), border=frame, align="L", fill=False)
      self.ln()
   
   # ==                       =================================================================================
   def getRGBColours(self, item):
      '''
      Get the RGB Colours for the Table Header Row.
      Can be set in the Report NLS File by "headerrowcolor=176.195.52" (Cenit green)
      
      Args:
         item : the desired Item from NLS File
      Returns:
         red   : the Portion of RED
         green : the Portion of GREEN
         blue  : the Portion of BLUE
      '''
      colour = self.__NLS.getNLS(item,"176.176.176")
      rgbList = str(colour).split(".")
      if len(rgbList) < 3:
         rgbList = ["176","176","176"]
      red = int(rgbList[0])
      green = int(rgbList[1])
      blue = int(rgbList[2])
      return red, green, blue
      
   # ==               ==========================================================================================
   def colored_table(self, headings, rows, colWidths):
      '''
      Write the Program TPEs Information to the Table
      
      Args:
         headings : the List of the Table Header
         rows : the List of the TPE Information
         colWidths : the List of the Column Width
      '''
      # Colors, line width and bold font:
      self.ln(8)
      #self.set_fill_color(176, 195, 52)
      red, green, blue = self.getRGBColours("headerrowcolorrgb")
      self.set_fill_color(red, green, blue)
      self.set_text_color(0)
      self.set_draw_color(0, 0, 0)
      self.set_line_width(0.3)
      self.set_font(self.__fontType, size=int(self.__fontSize))
      self.set_font(style=self.__fontStyle)
      
      # ---------- Header Line Creation Start (multi line) --------------
      nrColumns = len(headings)
      totalWidth = 0
      lineHeight = 5
      headLines = []
      maxLineCount = 1
      # get nr. of max HeaderLines (depends on the neccessary LineFeeds)
      for col_width, heading in zip(colWidths, headings):
         # newHead gets the List of splitted Column Header, * will force a LineFeed
         newHead = self.multi_cell(col_width, lineHeight, self.stringLF(heading), border=0, align="J", fill=True, split_only=True)
         if maxLineCount < len(newHead):
            maxLineCount = len(newHead)
         totalWidth +=col_width
      # fill up whole table (line x columns)
      dummyItem = " "
      for l in range(maxLineCount):
         curLine = []
         for c in range(nrColumns):
            curLine.append(dummyItem)
         headLines.append(curLine)
      # fill the requested Cells
      c = 0
      for col_width, heading in zip(colWidths, headings):
         # newHead gets the List of splitted Column Header, * will force a LineFeed
         newHead = self.multi_cell(col_width, lineHeight, self.stringLF(heading), border=0, align="J", fill=True, split_only=True)
         # replace Dummy in Cells with certain String
         for l in range(len(newHead)):
            headLines[l][c] = newHead[l]
         c +=1
      # output to Table
      l = 0
      for line in headLines:
         l +=1
         frame = "LRT"
         if l > 1:
            frame = "LR"
         if l == maxLineCount:
            frame = "LRB"
         for col_width, heading in zip(colWidths, line):
            self.cell(col_width, lineHeight, heading, border=frame, align="C", fill=True)
         self.ln()
      # ---------- Header Line Creation End --------------
      
      # Color and font restoration:
      self.set_fill_color(233, 233, 233)
      self.set_text_color(0)
      self.set_font()
      fill = False
      for row in rows:
         rowCols = len(row)
         if rowCols == 1:
            # new OP
            fill = False
            self.cell(totalWidth, 6, "", border="LR", align="L", fill=fill)
            self.ln()
            self.cell(totalWidth, 6, row[0], border="LR", align="L", fill=fill)
         else:
            iC = 0
            for item in row:
               align = "C"
               border = "L"
               if(iC == 0):
                  align = "L"
               if(iC == nrColumns-1):
                  border = "LR"
               self.cell(colWidths[iC], 6, item, border=border, align=align, fill=fill)
               iC += 1
         self.ln()
         fill = not fill
      self.cell(sum(colWidths), 0, "", "T")
      
   # --             -------------------------------------------------------------------------------------
   def stringLF(self, thisText):
      """
      Converts an Asteriks * in a String into an Linefeed chr(10)
      """
      nl = chr(10)
      return thisText.replace("*", nl)
      
   # ==               ==========================================================================================
   def getAnyEvent(self, eventHandler, opTpe, eventName):
   
      """
      Calculates linear tool path length
      
      Args:
         eventHandler: The event handler 
         opTpE: the current tool path element
      
      Returns:
         bool: requestedEvent : Bool True/False if Event found
         int:  insPos : the InsertPosition of the req. Event before/after
      """
      technoEvent = False
      evtInsPos = TPINSERTPOS_INSERTNONE
      
      allOlpEvents  = eventHandler.GetAllRuleBasedEvents(opTpe)
      if any(allOlpEvents):
         for olpEvent in allOlpEvents:
            olpEvtName =  olpEvent.GetOlpEventName()
            if olpEvtName == eventName:
               evtInsPos =  olpEvent.GetOlpEventInsertPosition()
               return True, evtInsPos
      
      allOlpEvents  = eventHandler.GetAllNonRuleBasedEvents(opTpe)
      if any(allOlpEvents):
         for olpEvent in allOlpEvents:
            olpEvtName =  olpEvent.GetOlpEventName()
            if olpEvtName == eventName:
               evtInsPos =  olpEvent.GetOlpEventInsertPosition()
               return True, evtInsPos

      return False, evtInsPos
      
   # ==               ==========================================================================================
   def calcLinLength(self, teachHandler, lastTpE, opTpe):
      """
      Calculates linear tool path length
      
      Args:
         teachHandler: the teach handler
         lastTpE: the last tool path element
         opTpe: the current tool path element
      
      Returns:
         double: length : the linear Length between the last and current TPE
      """
      lastTpeCoordinates = teachHandler.GetTpElementPosition(lastTpE, POSRELATION_WORKPIECEROOT).GetCoordinates()
      currentTpeCoordinates = teachHandler.GetTpElementPosition(opTpe, POSRELATION_WORKPIECEROOT).GetCoordinates()
      length = abs(math.sqrt((lastTpeCoordinates[0]-currentTpeCoordinates[0])**2 + (lastTpeCoordinates[1]-currentTpeCoordinates[1])**2 + (lastTpeCoordinates[2]-currentTpeCoordinates[2])**2))
      return length
   
   # ==               ==========================================================================================
   def calcCircLength(self, teachHandler, lastTpE, opTpe):
      """
      Calculates circular tool path length
      
      Args:
         teachHandler: the teach handler
         lastTpE: the last tool path element
         opTpe: the current tool path element
      
      Returns:
         double: length : the circular Length between the last and current TPE
      """
      # get arc end points and via point coordinates
      lastTpeCoordinates = teachHandler.GetTpElementPosition(lastTpE, POSRELATION_BASEFRAME).GetCoordinates()
      viaPointCoords = teachHandler.GetTpElementPosition(opTpe, POSRELATION_BASEFRAME).GetViaPointCoordinates()
      currentTpeCoordinates = teachHandler.GetTpElementPosition(opTpe, POSRELATION_BASEFRAME).GetCoordinates()

      # calculates chord of the circle throught arc end points
      chord = abs(math.sqrt((lastTpeCoordinates[0]-currentTpeCoordinates[0])**2 + (lastTpeCoordinates[1]-currentTpeCoordinates[1])**2 + (lastTpeCoordinates[2]-currentTpeCoordinates[2])**2))
      
      # calculates vectors a (through first end point and via point) and b (through via point and second end point):
      vec1 = self.getVector(lastTpeCoordinates, viaPointCoords)
      vec2 = self.getVector(viaPointCoords, currentTpeCoordinates)

      # calculates vector length: |a|, |b|
      vec1Length = self.getVectorLength(vec1)
      vec2Length = self.getVectorLength(vec2)

      # calculates vector scalar : a*b
      vecScalar = self.getVectorScalar(vec1, vec2)

      # calculates angle in via point between vectors a and b : 2*acos(a*b/|a|*|b|) in radians
      gamma = 2 * math.acos(vecScalar/(vec1Length * vec2Length))

      # calculates circle radius
      radius = chord/(2 * math.sin(gamma/2))

      # calculates arc length = alfa*r 
      return gamma * radius

   def getVector(self, point1, point2):
      """
      Gets vector through two points
      
      Args:
         point1: First point
         point2: Second point
      
      Returns:
         double: the Vector between the two Points
      """
      return [(point2[0]-point1[0]), (point2[1]-point1[1]), (point2[2]-point1[2])]

   def getVectorLength(self, vector):
      """
      Calculates vector length
      
      Args:
         vector: The vector to calculate the length for
      
      Returns:
         double: the Vector Length
      """
      return math.sqrt( vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])

   def getVectorScalar(self, vector1, vector2):
      """
      Calculates vector scalar
      
      Args:
         vector1: The first vector 
         vector2: The second vector 
      
      Returns:
         double: the scalar Product of the two given Vectors
      """
      return vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]
      
# ========================= END OF FILE =============================================================================
   
