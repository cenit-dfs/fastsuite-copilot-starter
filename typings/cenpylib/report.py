"""
COPYRIGHT Cenit AG Q1/2023
    Class "ReportUtility" for PDF Reports
    can be called from AutoExecute or AuxiliaryCommands
    
    AutoExecute :
       def createAutoExecutePDFReport(self, Operator, apppath, selection = ""):
    
    AuxiliaryCommands :
       def createAuxCommandsPDFReport(self, Operator, apppath, selection = ""):
       
    Args:
       Operator: the CENPyOlpProgramModifyOperator
       apppath: the Location of the Caller Script. Needed to find the Images. if kept empty, E2-lib Folder taken
       selection (optional): desired Selection of Columns (and its Order). Otherwise the pre-defined Columns are taken.
             Possible Items : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
             
    other usefull settings (pre to "createAuxCommandsPDFReport"/"createAutoExecutePDFReport" Command:
        setCosts(cost per meter): Sets the Costs per Meter
        setCurrency(currency): Sets the desired Currency for Costs [E,D,P,Y]
        setLanguage(language): Sets the desired NLS Language [EN,DE,FR,CN,JP]
        setHeaderLogo(logo): the Name of the Logo File (Format approx. 1:3), must be located in "apppath"
        setFooterLogo(logo): the Name of the Logo File (Format approx. 1:3), must be located in "apppath"
   
    possible Call from PostProgramDownload::ModifyActiveProgram()
       pdf = ReportUtility()
       variant = "AutoExecute"
       path = str(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))) + '\\' + variant + '\\')
       path = "C:\\Temp\\Pictures\\"
       pdf.setCosts(9.11)                                                               optional, default 8.2
       pdf.setCurrency("P")                                                             optional, default E [E,D,P,Y]
       pdf.setLanguage("DE")                                                            optional, default EN [EN,DE,FR,CN,JP]
       pdf.setHeaderLogo("Headline.png")                                                optional, default Fastsuite_E2_focus_on_effiency_RGB_100%.png"
       pdf.setFooterLogo("Footprint.png")                                               optional, default CENIT_Logo_2022_green.png
       
       table = ["Name", "MotionType", "Length", "Speed", "Time", "Costs"]
       pdf.createAuxCommandsPDFReport(Operator, path, table)                            table optional, default like shown above
       or
       pdf.createAutoExecutePDFReport(Operator, path)
       or
       pdf.createAutoExecutePDFReport(Operator, "")
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


class ReportUtility(FPDF):
   '''
   Class "ReportUtility" for PDF Reports
   '''
   # ==        ==========================================================================================
   def __init__(self):
      '''
      Initialization
      '''
      super().__init__()
      self.__appPath = FileUtility().CENIT_LOGO_FOLDER + "\\"
      self.__NLS = NLSUtility()
      self.__language = ""
      self.__headerLogo = "Fastsuite_E2_Logo2023.jpg"
      self.__footerLogo = "CENIT_Logo_green.png"
      self.__currency = "E"
      self.__costsPerMeter = 8.90
      self.__maxTCPFeedrate = 1.6
      self.__returnState = 0
      
   # ==               ==========================================================================================
   def createAutoExecutePDFReport(self, Operator, apppath, selection = ""):
      '''
      Pass Command from AutoExecute, e.g. after Download
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         apppath: the Location of the Caller Script. Needed to find the Images
         selection (optional): desired List of Selection of Columns (and its Order). Otherwise the pre-defined Columns are taken.
            Possible Items : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
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
      self.__NLS.defineNLS(self.__language, "report", forNLSPath)
      
      # get active program
      program = Operator.GetActiveProgram()
      # set Report Name
      defaultFileName = self.buildReportName(program.GetName())
      
      # set the desired Font&Size
      self.defineFont()
      
      dlpath = Operator.GetController().GetOutputDirectory()
      repfilepath =  dlpath + "\\" + defaultFileName
      
      # no selection applied, this is the default
      if len(selection) < 1:
         selection = ["Name", "MotionType", "Length", "Speed", "Time", "Costs"]
      
      self.createPDFReport(Operator, apppath, repfilepath, selection)
      
      return self.__returnState

   # ==               ==========================================================================================
   def createAuxCommandsPDFReport(self, Operator, apppath, selection = ""):
      '''
      Pass Command from Program Dashboard's "Auxiliary Commands"
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         apppath: the Location of the Caller Script. Needed to find the Images
         selection (optional): desired List of Selection of Columns (and its Order). Otherwise the pre-defined Columns are taken.
            Possible Items : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
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
      self.__NLS.defineNLS(self.__language, "report", forNLSPath)
      
      # get active program
      program = Operator.GetActiveProgram()
      # set Report Name
      defaultFileName = self.buildReportName(program.GetName())
      
      # set the desired Font&Size
      self.defineFont()
      
      dlpath = Operator.GetController().GetOutputDirectory()
      repfilepath =  dlpath + "\\" + defaultFileName
      
      # no selection applied, this is the default
      if len(selection) < 1:
         selection = ["Name", "MotionType", "Length", "Speed", "Time", "Costs"]
      
      if(selection.count("Costs")):
         # if "Costs" selected, provide own extended SaveFile-Dlg
         repfilepath, execute = self.extendedSaveUI(Operator, defaultFileName, apppath)
         if execute == False:
            return
      else:
         # Users confirm with saveReportAs Dialogue
         repfilepath = self.saveReportAs(defaultFileName, apppath)
         # check path is NONE, empty, blank
         if(not (repfilepath and repfilepath.strip)):
            # file would not be set -> build default target in OutputDirectory
            dlpath = Operator.GetController().GetOutputDirectory()
            repfilepath =  dlpath + "\\" + defaultFileName

      self.createPDFReport(Operator, apppath, repfilepath, selection)
      
      return self.__returnState

   # ==               ==========================================================================================
   def createPDFReport(self, Operator, apppath, repfilepath, selection = ""):
      '''
      Main Method to create the PDF Report
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         apppath: the Location of the Caller Script. Needed to find the Images
         repfilepath: the Location of the where the PDF Report should be written.
         selection (optional): desired Selection of Columns (and its Order). Otherwise the pre-defined Columns are taken.
            Possible Items : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
      '''
      
      self.__logging.LogInfo("PDF-Report : " + self.__NLS.getNLS("pdfbegin", "PDF Report creation is going to start...*") + " : " + str(repfilepath))
      
      # check for existing Target Folder
      dlPath = os.path.dirname(repfilepath)
      dlPathExist = os.path.exists(dlPath)
      # self.__logging.LogInfo("................................repfilepath=" + str(dlPath) + " = " + str(dlPathExist))
      if dlPathExist == False:
         self.__returnState = 2
         return
      
      # get active program
      program = Operator.GetActiveProgram()
      
      # define desired Range and Order of Columns. Adding new Items defineColumnTitleWidth() has to be extended
      # by Default : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
      #                [1],       [2],        [3],      [4],    [5],    [6],       [7],        [8],       [9]
      #  define desired Range :
      if(len(selection) < 1):
         columns = ["Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"]
      else:
         columns = selection
      
      totalWidth = 180
      # Build Lists
      headLine, colWidths, order, totalWidth = self.defineColumnTitleWidth(columns)
      
      # Portrait or Landscape Format
      global portrLands
      portrLands = "P"
      if (totalWidth > 180):
         portrLands = "L"
      # prevent using any Logo (OEM)
      noLogoUse = self.__NLS.getNLS("nologouse", "True")
      if noLogoUse == "True":
         self.__headerLogo="WhiteHeader.jpg"
         self.__footerLogo="WhiteFooter.png"
      
      # Resource´s max. TCP Feedrate to calc. correct Speed
      self.__maxTCPFeedrate = Operator.GetController().GetMainResourcesMaxTCPFeedrate()
      
      #-----------------------------------------------------------------------------
      # Common Header
      self.add_page(portrLands)
      # Related Header
      self.cenheader(Operator, apppath, portrLands)
      #-----------------------------------------------------------------------------
      self.body(Operator, headLine, colWidths, order)
      #-----------------------------------------------------------------------------
      # Related Footer
      self.cenfooter(apppath, portrLands)
      # Common Footer
      self.output(repfilepath)
      #-----------------------------------------------------------------------------
      self.__logging.LogInfo("PDF-Report : " + self.__NLS.getNLS("pdfsuccess", "PDF Report successfully created*.") + " : " + str(repfilepath))

   # ==               ==========================================================================================
   def buildReportName(self, programName):
      '''
      Build Report File Name, to be inheritate if customizing desired.
      
      Args:
         programName: the Process Program Name
      
      Returns:
         str: fileName: the desired File Name
      '''
      reportName = self.__NLS.getNLS("defaultreportname","FastsuiteE2_Report_##")
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
   def defineColumnTitleWidth(self, columns):
      '''
      Defines the Order of the desired Table Columns.
      Note: internal Column Name and its Place in the Order must be fix
      
      Args:
         columns : the desired List of Columns in desired Order
      Possible Items : "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events"
      
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
         if(name == "Name"):
            title, width = self.defineColName()
            order.append(1)
         if(name == "MotionType"):
            title, width = self.defineColMotionType()
            order.append(2)
         if(name == "Length"):
            title, width = self.defineColLength()
            order.append(3)
         if(name == "Speed"):
            title, width = self.defineColSpeed()
            order.append(4)
         if(name == "Time"):
            title, width = self.defineColTime()
            order.append(5)
         if(name == "Costs"):
            title, width = self.defineColCosts()
            order.append(6)
         if(name == "CollReach"):
            title, width = self.defineColCollReach()
            order.append(7)
         if(name == "Events"):
            title, width = self.defineColEvents()
            order.append(8)
         if(name == "Various"):
            title, width = self.defineColVarious()
            order.append(9)
         # ------- add here more columns if necessary -------
         # if(name == "__newItem_"):
         #    title, width = self.defineCol__defMethod__()
         #    order.append(__orderNr__)

         headLine.append(title)
         colWidth.append(width)
         totalWidth += width

      return headLine, colWidth, order, totalWidth

   # ==               ==========================================================================================
   '''
   Defines the Table Header Name and Width of the Items
   Each Item must have its own Method
   
   Returns:
      str: the Header Name of the Column 
      int: the Column Width
   '''
   def defineColName(self):
      return self.__NLS.getNLS("tpename","Name*"), int(self.__NLS.getNLS("tpenamecolwidth","40"))
   def defineColMotionType(self):
      return self.__NLS.getNLS("motiontype","Motion-Type*"),  int(self.__NLS.getNLS("motiontypecolwidth","25"))
   def defineColLength(self):
      return self.__NLS.getNLS("length","Path-Length [mm]*"),  int(self.__NLS.getNLS("lengthcolwidth","35"))
   def defineColSpeed(self):
      return self.__NLS.getNLS("speed","Speed [mm/s]*"),  int(self.__NLS.getNLS("speedcolwidth","30"))
   def defineColTime(self):
      return self.__NLS.getNLS("time","Time [s]*"),  int(self.__NLS.getNLS("timecolwidth","20"))
   def defineColCosts(self):
      tmpStr = self.__NLS.getNLS("costs","Costs [##]")
      tmpStr = tmpStr.replace("##", chr(self.getCurrencyCode()) )
      return tmpStr,  int(self.__NLS.getNLS("costscolwidth","25"))
   def defineColCollReach(self):
      return self.__NLS.getNLS("collreach","Collision/Reach*"),  int(self.__NLS.getNLS("collreachcolwidth","30"))
   def defineColEvents(self):
      return self.__NLS.getNLS("events","Events*"),  int(self.__NLS.getNLS("eventscolwidth","30"))
   def defineColVarious(self):
      return self.__NLS.getNLS("various","Various*"),  int(self.__NLS.getNLS("variouscolwidth","30"))
   # ------- add here more columns if necessary -------
   # def defineCol__defMethod__(self):
   #    return "__itemName__", 30

   # ==               ==========================================================================================
   def header(self):
      '''
      Defines the common Header of the PDF Report, called from FPDF Base Class
      '''
      # Setting font
      # self.defineFont()
      # ...done in cenheader, Table and Header collides from 2nd Page

   def cenheader(self, Operator, path, portrLands):
      '''
      Defines the customized Header of the PDF Report, underneath common Header
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         path : the Location of the Caller Script. Needed to find the Images
         portrLands : if Report is created in Portrait or Landscape Mode
      '''
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.5))
      self.set_font(style=self.__fontStyle)
      self.cell(80, 10, self.__NLS.getNLS("title","Fastsuite E2 Report*"), border=0, align="L")
      # Performing a line break:
      self.ln(2)
	  # Rendering logo:
      filepath =  path + self.__headerLogo
      if not exists(filepath):
         fu = FileUtility()
         self.__logging.LogInfo("PDF-Report : Header Logo not found. Search here :" + fu.CENIT_LOGO_FOLDER + "\\" + self.__headerLogo )
         filepath = fu.CENIT_LOGO_FOLDER + "\\" + self.__headerLogo
      if exists(filepath):
         hpos = 140
         if portrLands == "L":
            hpos = 200
         self.image(filepath, hpos, 8, 60)
      # general Info Table
      self.ln(4)
      self.header_table(Operator)
      
   def cenfooter(self, path, portrLands):
      '''
      Defines the customized Footer of the PDF Report, underneath common Header
      
      Args:
         path : the Location of the Caller Script. Needed to find the Images
         portrLands : if Report is created in Portrait or Landscape Mode
      '''
      self.ln(2)
      # Comment "The calculated lengths, speeds and times use a direct connection of the tool path elements. Accuracy, acceleration and deceleration behavior of the robot/machine are not taken into account."
      self.ln(8)
      self.set_font(self.__fontType, size=int(self.__fontSize))
      wid = 200
      if portrLands == "L":
         wid = 280
      self.multi_cell(wid, 8, self.__NLS.getNLS("consideration","Calculated without accuracy, acceleration and deceleration*"), border=0, align="L")
      # Rendering logo:
      filepath =  path + self.__footerLogo
      if not exists(filepath):
         fu = FileUtility()
         self.__logging.LogInfo("PDF-Report : Header Logo not found. Search here :" + fu.CENIT_LOGO_FOLDER + "\\" + self.__footerLogo )
         filepath = fu.CENIT_LOGO_FOLDER + "\\" + self.__footerLogo
      if exists(filepath):
         vpos = 285
         if portrLands == "L":
            vpos = 200
         self.image(filepath, 10, vpos, 25)
      # no footer line, PM decision 
      #self.ln(8)
      #self.set_font(self.__fontType, size=int(self.__fontSize))
      #self.cell(80, 10, self.__NLS.getNLS("title","Fastsuite E2 Report*") + " " + self.__NLS.getNLS("finished","finished*"), border=0, align="L")

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

   def setCosts(self, cost):
      '''
      Sets the Costs per Meter
      
      Args:
         cost : Value of the Costs per Meter
      '''
      self.__costsPerMeter = cost

   def setCurrency(self, currency):
      '''
      Sets the desired Currency
      
      Args:
         currency : the desired Currency 
         Euro "E"
         Dollar "D"
         Pound "P"
         Yen/Yuan "Y"
      '''
      self.__currency = currency

   def getCurrencyCode(self):
      '''
      Returns the Ascii Code of the desired Currency
         Euro "E", Dollar "D", Pound "P", Yen/Yuan "Y"
      
      Returns:
         int: currency: Ascii Value of the Currency
      '''
      euroCode = 128
      dllrCode = 36
      poundCode = 163
      yenCode = 165
      currency = euroCode
      
      if self.__currency == "D":
         currency = dllrCode
      if self.__currency == "P":
         currency = poundCode
      if self.__currency == "Y":
         currency = yenCode
      return currency

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

   def setHeaderLogo(self, logo):
      '''
      Sets the Logo shown on Reports top/right
      
      Args:
         logo : Name of the Logo File ()
      '''
      self.__headerLogo = logo

   def setFooterLogo(self, logo):
      '''
      Sets the Logo shown on Reports bottom/left
      
      Args:
         logo : Name of the Logo File ()
      '''
      self.__footerLogo = logo

   # ==               ==========================================================================================
   # ==               ==========================================================================================
   def body(self, Operator, headLine, colWidths, order):
      '''
      Defines the customized Body of the PDF Report.
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         headLine : the List of the Columns Header Names
         colWidths : the List of the Columns Width
         order : the List of the ordered Column Numbers
      '''
      
      costPerMeter = self.__costsPerMeter
      currency = self.getCurrencyCode()
      totalLength = 0.0
      totalCosts = 0.0
      # ----------- get all information from the Program ------
      tpeList, totalLength, totalCosts = self.collectelements(Operator, order, costPerMeter)
      # -------------------------------------------------------
      # ----------- intermediate Block before TPE List --------
      paramList = []
      paramList.append(totalLength)
      paramList.append(totalCosts)
      paramList.append(costPerMeter)
      paramList.append(order.count(6))
      paramList.append(currency)
      self.intermediateBlockBefore(Operator, paramList)
      # -------------------------------------------------------
      # -------- write the Toolpath Information ---------------
      self.colored_table(headLine, tpeList, colWidths)
      # -------------------------------------------------------
      # ----------- intermediate Block after TPE List --------
      self.intermediateBlockAfter(Operator, [])
      # -------------------------------------------------------
   
   # ==               ==========================================================================================
   def collectelements(self, Operator, order, costPerMeter):
      '''
      Collect all the necessary Information from the Program and writes it to a List
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         order : the List of the ordered Column Numbers
         costPerMeter : the Value of the Costs per Meter
      
      Returns:
         strList: columns     : the List of all TPE Informations
         double:  totalLength : the Summary of all Path Length
         double:  totalCosts  : the Summary of all Path Costs
      '''
      # loop though the TPEs
      # get active program
      program = Operator.GetActiveProgram()
      # get all operations groups
      operationGroups = program.GetOperationGroups()
      # get all operations
      operations = program.GetOperations()
      # get teach handler
      teachHandler = Operator.GetTeachHandler()
      # get event handler
      eventHandler = Operator.GetEventHandler()
      
      if (program == None or operationGroups == None or operations == None or teachHandler == None or eventHandler == None):
         return
      
      # reset Variables
      columns = []
      technoState = 0
      lastTechnoState = 0
      lastTpE = None
      totalLength = 0.0
      totalCosts = 0.0
      totalTime = 0.0
      opLength = 0.0
      opCosts = 0.0
      opTime = 0.0
      length = 0.0
      cost = 0.0
      speed = 0.0
      lastSpeed = 0.0
      time = 0.0
      columnCount = 0

      # --------- loop operations groups ----------
      for operationGrp in operationGroups:
         
         # --------- loop operations ---------
         for operation in operationGrp.GetOperations():
            
            # empty List for Operation Infos
            opColumns = []
            # Header OperationGroup/Operation to Table (0:none but divider, 1:only OpName [dflt], 2:Group&OpName, 3:abs.None)
            operationHeader = self.__NLS.getNLS("operationheader","1")
            # Header for the current Operation (if requested)
            if (operationHeader == "0"):
               column = [""]
               opColumns.append(column)
            elif  (operationHeader == "2"):
               column = [str(operationGrp.GetName()) + ":" + str(operation.GetName())]
               opColumns.append(column)
            elif  (operationHeader == "3"):
               column = [str(operation.GetName())]
               # no divider between Ops : opColumns.append(column)
            else:
               column = [str(operation.GetName())]
               opColumns.append(column)
            
            opLength = 0
            opCosts = 0
            opTime = 0
            opUnreachable = 0

            opTpes = operation.GetTpElements()
            
            # check if TOOL BuildIn Events recognized (for Costs Calculation)
            withTechnoEvents = self.technoEventsExist(eventHandler, opTpes)
               
            if technoState == 0 or technoState == -1:
               # reset variables       
               lastTpE = None
               length = 0
               cost = 0
               speed = 0
         
            # --------- loop TPEs ---------
            for opTpe in opTpes:
               
               eventStr = ""
               # ------------------------ SPEED -----------------------
               # get any speed for tool path element (just for Comment)
               speedEvent, retSpeed, insPos = self.getSpeedEvent(eventHandler, opTpe)
               if speedEvent == True and retSpeed > 0.00001:
                  if abs(lastSpeed - retSpeed) > 0.00001:
                     # Speed has changed
                     eventStr += self.__NLS.getNLS("eventspeed","Speed*")
                     if insPos == TPINSERTPOS_INSERTBEFORE:
                        eventStr += "(b)"
                     if insPos == TPINSERTPOS_INSERTAFTER:
                        eventStr += "(a)"
               
               # get insert_before SpeedEvents : output immediately for TPE
               speedEvent, retSpeed, insPos = self.getSpeedEvent(eventHandler, opTpe, TPINSERTPOS_INSERTBEFORE)
               if speedEvent == True and insPos == TPINSERTPOS_INSERTBEFORE and retSpeed > 0.00001:
                  speed = retSpeed
                  lastSpeed = retSpeed
               
               
               # ------------------------ TECHNO -----------------------
               # get the Techno Event On/Off on the TPE (just for Comment)
               technoEvent, retTechnoState, insPos = self.getTechnoEvent(eventHandler, opTpe)
               if retTechnoState != 0:
                  if len(eventStr):
                     eventStr += ","
                  if retTechnoState == 1:
                     curTechnoState = self.__NLS.getNLS("eventtoolon","T-ON*")
                  if retTechnoState == -1:
                     curTechnoState = self.__NLS.getNLS("eventtooloff","T-OFF*")
                  eventStr += curTechnoState
                  if insPos == TPINSERTPOS_INSERTBEFORE:
                     eventStr += "(b)"
                  if insPos == TPINSERTPOS_INSERTAFTER:
                     eventStr += "(a)"
               
               # get insert_before Tool Events : output immediately for TPE
               technoEvent, retTechnoState, insPos = self.getTechnoEvent(eventHandler, opTpe, TPINSERTPOS_INSERTBEFORE)
               if retTechnoState != 0:
                  technoState = retTechnoState
                  lastTechnoState = retTechnoState
               
               # if no Tool Events recognized, always ON (for Costs)
               if withTechnoEvents == False:
                  technoState = 1
                  lastTechnoState = 1
               
               # ------------------------ ACCURACY -----------------------
               # get the Accuracy Event on the TPE
               accCriteria, accValue, insPos = self.getAccuracyEvent(eventHandler, opTpe)
               if accCriteria > -1:
                  curAccuracy = self.__NLS.getNLS("eventaccuracy","ACC*") + str(accCriteria)
                  if len(eventStr):
                     eventStr += ","
                  eventStr += curAccuracy
                  if insPos == TPINSERTPOS_INSERTBEFORE:
                     eventStr += "(b)"
                  if insPos == TPINSERTPOS_INSERTAFTER:
                     eventStr += "(a)"
               
               # ------------------------ COLLISION/REACHABILITY -----------------------
               # check Reachability and CollisionState of the TPE
               collReachStr, unreachableReturn = self.getCollisionReachabilityString(Operator, opTpe)
               if unreachableReturn == 1:
                  opUnreachable = 1
                  
               # ------------------------ MOTION TYPE -----------------------
               # get the Line Type
               motionTypeStr = self.getMotionTypeString(Operator, opTpe)
               
               # ------------------------ VARIOUS FIELD -----------------------
               # get a Various Filed
               variousStr = self.getVariousField(Operator, opTpe)
               
               # ------------------------ TPE LENGTH -----------------------
               # get path length
               if(lastTpE != None):
                  if (opTpe.GetMotionType() == MOTIONTYPE_CIR):
                     # path is cicle -> calc circle length
                     length = self.calcCircLength(teachHandler, lastTpE, opTpe)
                  else:
                     # path is line -> calc line length
                     length = self.calcLinLength(teachHandler, lastTpE, opTpe)
                  # calculate time & cost
                  if speed == 0 and lastSpeed == 0:
                     time = 0
                  elif speed == 0:
                     speed = lastSpeed
                     time = length / speed
                  else:
                     time = length / speed
                  
                  # calculate the Costs per TPE (Method can be inheritate)
                  cost = self.calculateCosts(costPerMeter, length, technoState, opTpe.GetMotionType())
                  
                  totalLength += length
                  totalCosts += cost
                  totalTime += time
                  opLength += length
                  opCosts += cost
                  opTime += time
               
               # save Tpe for Length Calculation
               lastTpE = opTpe

               # "Name", "MotionType", "Length", "Speed", "Time", "Costs", "CollReach", "Events", "Various"
               forOrder = []
               forOrder.append(str(opTpe.GetName()))
               forOrder.append(motionTypeStr)
               forOrder.append(str(round((length*1000), 2)))
               forOrder.append(str(round((speed*1000),2)))
               forOrder.append(str(round(time, 2)))
               forOrder.append(str(round(cost,2)).zfill(2))
               forOrder.append(str(collReachStr))
               forOrder.append(str(eventStr))
               forOrder.append(str(variousStr))
               # forOrder.append(..) - be aware to fill all available fields
               
               # re-order Items in desired Order
               column = self.columnOrder(order, forOrder)
               # column = [str(opTpe.GetName()), motionTypeStr, str(round((length*1000), 2)), str(round((speed*1000),2)), str(round(time, 2)), str(round(cost,2)), str(collReachStr), str(eventStr)]
               opColumns.append(column)
               
               # ------------------------ set Values for insert_after Events -----------------------
               # get insert_after SpeedEvents : pre-set for next TPE
               speedEvent, retSpeed, insPos = self.getSpeedEvent(eventHandler, opTpe, TPINSERTPOS_INSERTAFTER)
               if speedEvent == True and insPos == TPINSERTPOS_INSERTAFTER and retSpeed > 0.00001:
                  speed = retSpeed
                  lastSpeed = retSpeed
               
               # get insert_before Tool Events : output immediately for TPE
               technoEvent, retTechnoState, insPos = self.getTechnoEvent(eventHandler, opTpe, TPINSERTPOS_INSERTAFTER)
               if retTechnoState != 0:
                  technoState = retTechnoState
                  lastTechnoState = retTechnoState
            # TPE-Loop
            
            operationSummary = self.__NLS.getNLS("operationsummary","0")
            # Summary of the current Operation (if requested)
            if (operationSummary == "1"):
               summary = []
               summary.append(self.__NLS.getNLS("summary","Summary:") + str(operation.GetName()))
               summary.append("")
               summary.append(str(round((opLength*1000),2)))
               summary.append("")
               summary.append(str(round(opTime,2)))
               summary.append(str(round(opCosts,2)))
               summary.append("")
               summary.append("")
               summary.append("")
               # summary.append(..) - be aware to fill all available fields
               # re-order Items in desired Order
               column = self.columnOrder(order, summary)
               opColumns.append(column)

             # no List if Operation contains unreachable TPEs
            if opUnreachable == 1:
               # delete Operation List (except the Header)
               del opColumns[1:]
               column = [self.__NLS.getNLS("operationcancelled","Operation canceled due to unreachable TPEs.*")]
               opColumns.append(column)
               totalLength -= opLength
               totalCosts -= opCosts
               warnMessage = "PDF-Report : " + str(operation.GetName()) + "  " + self.__NLS.getNLS("operationcancelled","Operation canceled due to unreachable TPEs.*")
               self.__logging.LogWarn(warnMessage)
            # write Operation Items to Program List (or unreachable Message)
            for opCol in opColumns:
                columns.append(opCol)
         # Operation-Loop
      
      # OpGroup-Loop
      return columns, totalLength, totalCosts
   
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
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.2))
      # -----------------------------------------------------------------------
      self.cell(40, 8, self.__NLS.getNLS("programname","Program name*:"), border=1, align="L", fill=False)
      self.cell(80, 8, str(program.GetName()), border=1, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      self.cell(40, 8, self.__NLS.getNLS("controller","Controller*:"), border=1, align="L", fill=False)
      self.cell(80, 8, str(Operator.GetController().GetName()), border=1, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      # today = datetime.now()
      today = datetime.datetime.now()
      date = str(today.day).zfill(2) + "." + str(today.month).zfill(2) + "." + str(today.year).zfill(2)
      date += "   " + str(today.hour).zfill(2) + ":" + str(today.minute).zfill(2) + ":" + str(today.second).zfill(2)
      self.cell(40, 8, self.__NLS.getNLS("date","Date*:"), border=1, align="L", fill=False)
      self.cell(80, 8, date , border=1, align="L", fill=False)
      self.ln()
      # -----------------------------------------------------------------------
      self.cell(40, 8, self.__NLS.getNLS("operator","Operator*:"), border=1, align="L", fill=False)
      self.cell(80, 8, str(os.getlogin()), border=1, align="L", fill=False)
      self.ln()
   
   # ==                       =================================================================================
   def intermediateBlockBefore(self, Operator, paramList):
      '''
      Anything between CenHeader and TPE List (Template for Inheritance)
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         paramList : the List of used Parameters
      paramList = [(totalLength)(totalCosts)(costPerMeter)(order.count(6))(currency)
                        0            1            2             3              4
      '''
      # Outputs a Line with total Length and Costs (if required)
      # Setting font
      self.set_font(self.__fontType, size=int(int(self.__fontSize)*1.2))
      self.ln(8)
      lenghtCosts = self.__NLS.getNLS("overalllength","Overall length*: ") + str(round(paramList[0],2)) + "m"
      if(paramList[3]):
         lenghtCosts += "   /  " + self.__NLS.getNLS("overallcosts","Overall cost*: ") + str(round(paramList[1],2)).zfill(2) + " " + chr(paramList[4]) + "  (" + str(paramList[2]).zfill(2) + chr(paramList[4]) + "/m)" 
      self.cell(180, 10, lenghtCosts, border=0, align="L")
      self.ln(8)
      
   # ==                       =================================================================================
   def intermediateBlockAfter(self, Operator, paramList):
      '''
      Anything between TPE List and CenFooter (Template for Inheritance)
      
      Args:
         Operator : the CENPyOlpProgramModifyOperator
         paramList : the List of used Parameters
      '''
      # self.__logging.LogInfo("PDF-Report : intermediateBlockAfter(self, Operator, paramList)")
      # n.t.d.
      
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
      nrColumns = len(headings)
      totalWidth = 0
      for col_width, heading in zip(colWidths, headings):
         self.cell(col_width, 7, heading, border=1, align="C", fill=True)
         totalWidth +=col_width
      self.ln()
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

   # ==               ==========================================================================================
   def getSpeedEvent(self, eventHandler, opTpe, beforeAfter = -1):
      """
      Calculates linear tool path length
      
      Args:
         eventHandler: The event handler 
         opTpe: the current tool path element
         beforeAfter: get only desired Events (before/after/all)
      
      Returns:
         bool:   speedEvent : Bool True/False if a TPE contains a specific Event
         double:      speed : the Value of the Speed Event in mm/s
         int:        insPos : the InsertPosition of the Speed Event before/after
      """
      speed = 0
      speedEvent = False
      insPos = -1
      withSpeedEvents = eventHandler.GetBuiltInEventsByType(opTpe, EVENT_SPEED)
      if any(withSpeedEvents):
         for spdevt in withSpeedEvents:
            # only get desired (before, after, all)
            if spdevt.GetBuiltInEventInsertPosition() == beforeAfter or beforeAfter == -1:
               speed = spdevt.GetSpeed()
               insPos = spdevt.GetBuiltInEventInsertPosition()
               if spdevt.GetUnit() == ATTRIB_PERCENT:
                  # Speed as Percentage Value, re-calc. with maxTCPFeedrate
                  speed = self.__maxTCPFeedrate * (speed / 100)
               speedEvent = True
            continue   
      return speedEvent, speed, insPos
   
   # ==               ==========================================================================================
   def technoEventsExist(self, eventHandler, opTpes):
      """
      Calculates linear tool path length
      
      Args:
         eventHandler: The event handler 
         opTpes: array of the Ops TPEs
      
      Returns:
         bool : True/False if a Tool On/Off exists (for Cost Calculation)
      """
      for opTpe in opTpes:
         withTechEvents  = eventHandler.GetBuiltInEventsByType(opTpe, EVENT_TOOL)
         if any(withTechEvents):
            return True
      return False
      
   # ==               ==========================================================================================
   def getTechnoEvent(self, eventHandler, opTpe, beforeAfter = -1):
      """
      Calculates linear tool path length
      
      Args:
         eventHandler: The event handler 
         opTpE: the current tool path element
         beforeAfter: get only desired Events (before/after/all)
      
      Returns:
         bool: technoEvent : Bool True/False if a TPE contains a specific Event
         int:       retVal : an Integer 0=no Event  1=Tool ON  -1=Tool OFF
         int:       insPos : the InsertPosition of the Techno Event before/after
      """
      retVal = 0
      state = False
      technoEvent = False
      insPos = -1
      withTechEvents  = eventHandler.GetBuiltInEventsByType(opTpe, EVENT_TOOL)
      if any(withTechEvents):
         for techevt in withTechEvents:
            # only get desired (before, after, all)
            if techevt.GetBuiltInEventInsertPosition() == beforeAfter or beforeAfter == -1:
               state = techevt.GetState()
               if state == True:
                  retVal = 1
               else:
                  retVal = -1
               insPos = techevt.GetBuiltInEventInsertPosition()
               technoEvent = True
      return technoEvent, retVal, insPos
   
   # ==               ==========================================================================================
   def getAccuracyEvent(self, eventHandler, opTpe):
      """
      Calculates linear tool path length
      
      Args:
         eventHandler: The event handler 
         opTpE: the current tool path element
      
      Returns:
         int: criteria : an Criteria Integer  A_OFF=0 A_ON=1 A_JOINTDISTANCE=2 A_DISTANCE=3 A_ORIENTATION=4 A_VELOCITY=5
         double: value : the Value of the Accuracy
         int:   insPos : the InsertPosition of the Accuracy Event before/after
      """
      criteria = -1
      value = 0
      insPos = -1
      withAccuracyEvents  = eventHandler.GetBuiltInEventsByType(opTpe, EVENT_ACCURACY)
      if any(withAccuracyEvents):
         for accevt in withAccuracyEvents:
            criteria = accevt.GetCriteria()
            value = accevt.GetAccuracy
            insPos = accevt.GetBuiltInEventInsertPosition()
      return criteria, value, insPos
   
   # ==               ==========================================================================================
   def calculateCosts(self, costPerMeter, length, technoState, motionType):
      """
      Calculates Costs per TPE dependent to TechnoState, MotionType, etc. if desired
      Might be inheritate for own Calculation.
      
      Args:
         costPerMeter: the Costs per Meter moving 
         length: the length of the TPE
         technoState: 1=Tool ON  -1=Tool OFF
         motionType : the Motion Type  MOTIONTYPE_CIR _LIN _PTP
      
      Returns:
         double: costs : the Costs of the TPE
      """
      costs = 0.0
      if technoState == 1:
         costs = length * costPerMeter 
      
      return costs
   
   # ==               ==========================================================================================
   def getMotionTypeString(self, operator, opTpe):
      """
      Get the Motion Type of the TPE (PTP, LIN, CIR)
      ...might be inheritate for own desired Information in PlugIn Script
      
      Args:
         operator: the CENPyOlpProgramModifyOperator
         opTpe: the current tool path element
      
      Returns:
         str: motionTypeStr : the String of the Motion Type
      """
      motionTypeStr = ""
      if (opTpe.GetMotionType() == MOTIONTYPE_CIR):
         motionTypeStr = "CIR"
      if (opTpe.GetMotionType() == MOTIONTYPE_LIN):
         motionTypeStr = "LIN"
      if (opTpe.GetMotionType() == MOTIONTYPE_PTP):
         motionTypeStr = "PTP"
      return motionTypeStr
   
   # ==               ==========================================================================================
   def getCollisionReachabilityString(self, operator, opTpe):
      """
      Get the Colloision and/or Reachability of the TPE,
      ...might be inheritate for own desired Information in PlugIn Script
      
      Args:
         operator: the CENPyOlpProgramModifyOperator
         opTpe: the current tool path element
      
      Returns:
         str: collReachStr : the String of the CollisionReachability
      """
      collReachStr = ""
      unreachableRet = 0
      if (opTpe.GetCollisionStatus() == COLLISIONSTATUS_COLLISION):
         collReachStr = self.__NLS.getNLS("tpecollision","Collision*")
      if (opTpe.GetReachabilityStatus() == REACHABILITYSTATUS_NOTREACHABLE):
         collReachStr = self.__NLS.getNLS("tpeunreachable","Unreachable*")
         self.__returnState = 1
         unreachableRet = 1
      if (opTpe.GetCollisionStatus() == COLLISIONSTATUS_COLLISION and opTpe.GetReachabilityStatus() == REACHABILITYSTATUS_NOTREACHABLE):
         collReachStr = self.__NLS.getNLS("tpecollunreach","Coll. & Unrea.*")
         self.__returnState = 1
         unreachableRet = 1
      return collReachStr, unreachableRet
   
   # ==               ==========================================================================================
   def getVariousField(self, operator, opTpe):
      """
      Template, ...might be inheritate for own desired Information in PlugIn Script
      
      Args:
         operator: the CENPyOlpProgramModifyOperator
         opTpe: the current tool path element
      
      Returns:
         str: variousString : the String for Column "Various"
      """
      variousString = "- - - -"
      return variousString
   
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
      
   # ==               ==========================================================================================
   def saveReportAs(self, defaultFileName: str, apppath: str):
      """
      Calls the usual file save dialog
      
      Args:
         defaultFileName: default file name
         apppath: the Application Path for Pictures and Icons
      
      Returns:
         str: fullpath: the selected path and file name
      """
      root = tk.Tk(baseName="SaveReport")
      root.withdraw()
      # add E2 icon
      icoFile = apppath + "e2.ico"
      if exists(icoFile):
         root.iconbitmap(icoFile)
      icoFile = apppath + "Fastsuite_E2_Icon.ico"
      if exists(icoFile):
         root.iconbitmap(icoFile)
      files = [('PDF Files', '.pdf')]
      # call file save dialog
      fullpath = filedialog.asksaveasfilename(parent=root,filetypes=files, defaultextension=files, initialfile=defaultFileName, title=self.__NLS.getNLS("savedlgtitle","Save E2 PDF Report*"))
      root.destroy()

      return fullpath
      
   # ==               ==========================================================================================
   def getReportLocation(self, apppath: str):
      """
      Calls the Folder select dialog
      
      Args:
         apppath: the Application Path for Pictures and Icons
      
      Returns:
         str: path: the selected path
      """
      root = tk.Tk(baseName="SaveReport")
      root.withdraw()
      # add E2 icon
      icoFile = apppath + "e2.ico"
      if exists(icoFile):
         root.iconbitmap(icoFile)
      icoFile = apppath + "Fastsuite_E2_Icon.ico"
      if exists(icoFile):
         root.iconbitmap(icoFile)
      # call folder selection dialog
      path = filedialog.askdirectory(parent=root, title=self.__NLS.getNLS("savedlgpath","Report path*"))
      root.destroy()

      return path

   # ------------------------------------------------------------------------
   def extendedSaveUI(self, Operator, defaultFileName, apppath):
      """
      extended File Save dialogue with Costs Settings
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
         defaultFileName: the default Filename of the PDF Report
         apppath: the Location of the Caller Script. Needed to find the Images
      """

      # get logger
      logging = Operator.GetLoggerOperator()
      # get DownLoad Folder as Default
      defaultDlPath = Operator.GetController().GetOutputDirectory()

      app = UserInterface(self.__NLS.getNLS("savedlgtitle","Save E2 PDF Report*"), 640, 270)
      # add window content: label, dropdown, buttons
      self.uiexecutebutton = False
      self.createDialogueUI(app, defaultFileName, defaultDlPath)
      
      app.attributes('-topmost', True) # make window always on top of others
      app.focus_force() # make window active
      # run window, listen for events and wait for the window to close.
      # Code execution is stopped until window is closed!
      app.mainloop()

      # check if execute button was pressed
      if not self.uiexecutebutton:
         logging.LogWarn("PDF-Report : Command Create PDF Report canceled by Users request. ABORT.")
         return "", False
      else:
         logging.LogInfo("PDF-Report : Execute, on we go ....")
      
      dlgFile = app.pdffilename.get()
      dlgFolder = app.pdfpath.get()
      self.setCosts(app.costspermeter.get())
      range = ["E", "D", "P", "Y"]
      currency = app.currency.get().upper()
      if range.count(currency):
         self.setCurrency(currency)

      # if TickBox set, overwrite Path setting with Controller-DownLoadFolder (after save Values)
      useDownloadFolder = app.useDLFolder.get()

      # save [Folder, Currency, CostsValue] to INI File
      saveStuff = [dlgFolder, str(currency), str(app.costspermeter.get()), str(useDownloadFolder)]
      self.getsetValues(True, saveStuff)

      # overwrite Path setting with Controller-DownLoadFolder
      if useDownloadFolder == 1:
         dlgFolder = defaultDlPath

      repfilepath =  dlgFolder + "\\" + dlgFile
      return repfilepath, True

   # ------------------------------------------------------------------------
   def createDialogueUI(self, window: UserInterface, defaultFileName, defaultDlPath):
      """
      Create the window elements and functions.
      
      Args:
         window: UserInterface: the Window Handler
         defaultFileName: the default Filename of the PDF Report
         defaultDlPath: the default Location of the PDF Report
      """
      # Configure the main frame and grid
      mainFrame = window.AddFrame(window)
      # configure grid
      window.grid_rowconfigure(0, weight=1)
      window.grid_columnconfigure(0, weight=1)
      mainFrame.grid(row=0, column=0, sticky=E+W+N+S, **window.PADDINGS)
      rownr = 0
      
      # get List of stored [Folder, Currency, CostsValue] to INI File
      saveStuff = []
      saveStuff = self.getsetValues(False, "")
      # check Stored
      defaultCosts = 8.2
      defaultCurrency = "E"
      defaultUseDLFld = 0
      if len(saveStuff) > 0:
         # Path
         if exists(saveStuff[0]):
            defaultDlPath = saveStuff[0]
         # Currency
         if len(saveStuff) > 1:
            range = ["E", "D", "P", "Y"]
            if range.count(saveStuff[1]):
               defaultCurrency = saveStuff[1]
         # Costs
         if len(saveStuff) > 2 and saveStuff[2] != "":
            temp = float(saveStuff[2])
            if temp > 0.0 and temp < 999.0:
               defaultCosts = temp
         # use DLFolder
         if len(saveStuff) > 3 and saveStuff[3] != "":
            udlf = int(saveStuff[3])
            defaultUseDLFld = udlf

      # Textbox Filename
      rownr += 1
      lblFileName = window.AddLabel(mainFrame, self.__NLS.getNLS("savedlgfilename","Report file name*"), 120, 25, None)
      lblFileName.grid(row=rownr, column=0, sticky=E+W, **window.PADDINGS)
      window.pdffilename = StringVar(value=defaultFileName)
      dfltFileName = window.AddTextBox(mainFrame, window.pdffilename)
      dfltFileName.grid(row=rownr, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)

      # Textbox Path
      rownr += 1
      lblPathName = window.AddLabel(mainFrame, self.__NLS.getNLS("savedlgpath","Report path*"), 120, 25, None)
      lblPathName.grid(row=rownr, column=0, sticky=E+W, **window.PADDINGS)
      window.pdfpath = StringVar(value=defaultDlPath)
      dfltReportPath = window.AddTextBox(mainFrame, window.pdfpath, True)
      dfltReportPath.grid(row=rownr, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)
      # sub function to save "return" value from user interface
      def GetPath():
         """Define an action for on PathSearch button click."""
         path = self.getReportLocation(self.__appPath)
         if len(path):
            window.pdfpath.set(path)
      window.AddButton(mainFrame, "...", 50, 25, GetPath).grid(row=rownr, column=3, **window.PADDINGS)
      
      # Checkbox use DownloadFolder regardless
      rownr += 1
      window.useDLFolder = IntVar(value=defaultUseDLFld)
      Checkbutton(mainFrame, text="", variable=window.useDLFolder, fg="black", bg="black", selectcolor="#C1C1CD",activebackground="black", activeforeground="white").grid(row=rownr, column=0, sticky=E)
      lblDLPath = window.AddLabel(mainFrame, self.__NLS.getNLS("savedlgusedlfolder","use Download Folder*"), 240, 25, None)
      lblDLPath.grid(row=rownr, column=1, columnspan=2, sticky=W, **window.PADDINGS)
      
      # Textbox Cost per Meter
      rownr += 1
      lblCosts = window.AddLabel(mainFrame, self.__NLS.getNLS("savedlgcostspermeter","Costs per meter*"), 120, 25, None)
      lblCosts.grid(row=rownr, column=0, sticky=E+W, **window.PADDINGS)
      window.costspermeter = DoubleVar(value=defaultCosts)
      dfltCosts = window.AddTextBox(mainFrame, window.costspermeter)
      dfltCosts.grid(row=rownr, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)
      
      # Textbox Currency
      rownr += 1
      lblcurrency = window.AddLabel(mainFrame, self.__NLS.getNLS("savedlgcurrency","Currency [E,D,P,Y]*"), 120, 25, None)
      lblcurrency.grid(row=rownr, column=0, sticky=E+W, **window.PADDINGS)
      window.currency = StringVar(value=defaultCurrency)
      dfltcurrency = window.AddTextBox(mainFrame, window.currency)
      dfltcurrency.grid(row=rownr, column=1, columnspan=2, sticky=E+W+N+S, **window.PADDINGS)

      # sub function to save "return" value from user interface
      def AcceptClicked():
         """Define an action for on Accept button click."""
         self.uiexecutebutton = True
         window.destroy()
      def CancelClicked():
         """Define an action for on Accept button click."""
         self.uiexecutebutton = False
         window.destroy()

      # add buttons
      rownr += 1
      window.AddButton(mainFrame, self.__NLS.getNLS("execute","EXECUTE"), 180, 25, AcceptClicked).grid(row=rownr, column=1, **window.PADDINGS)
      window.AddButton(mainFrame, self.__NLS.getNLS("cancel","CANCEL"), 180, 25, CancelClicked).grid(row=rownr, column=2, **window.PADDINGS)

   def getsetValues(self, write, inList, myFileName="E2PDFReport.ini"):
      """
      read or write 
      
      Args:
         write : bool for writing = true, reading=false
         inList : List of Values in Case of writing = true
         myFileName : optional, default is "E2PDFReport.ini"
      
      Returns:
         strList: outList : List of Values in Case of reading=false
      """
      filepath = str(os.path.join(os.environ["HOMEDRIVE"],os.path.join(os.environ["HOMEPATH"], myFileName)))
      outList = []
      if write == False: # get the Values
         if exists(filepath):
            file = open(filepath,"r") #opens file for read
            ret = file.read()
            outList = str(ret).split("\n")
            file.close()
      else:  # set the Values
         file = open(filepath,"w") #opens file for write
         for item in inList:
            ret = file.write(item + "\n")
         file.close()
      return outList
