"""
COPYRIGHT Cenit AG Q1/2023
    Class "NLSUtility" for language Translation
    
    Set the desired Language in the certain Project and accesses to the translated Items.
    
    def defineNLS(self, language, project = "", altpath = "")
    
      Args:
         language : the desired NLS Language 
                    english "EN",  german "DE",  french "FR",  chinese "CN",  japanese "JP"
         project  : sets the requested NLS Project "common", "report", etc.(optional)
         altpath  : alternative Path for own customized PlugIn NLS Files (optional)
                    e.g. myPath = "C:\\PlugIn\\Technologies\\TechnologyCommon\\Standard\\AuxiliaryCommands\\Language"
    
    
    def getNLS(self, name, default = ""):
    
      Args:
         name: the NLS-Item
         default: the default Translation if NLS-Item not found
      
      Returns:
         str: nlsStr: the found NLS or the default
"""

# import libraries
from os.path import exists
from .file import *
import os, locale


class NLSUtility:
   '''
   Class "NLSUtility" for Language Translations
   '''
   # ==        ==========================================================================================
   def __init__(self):
      '''
      Initialization
      '''
      # super().__init__()
      self.__apppath = FileUtility().CENIT_LANGUAGE_FOLDER + "\\"
      self.__language = "EN"
      self.__nlsList = []
      
   # ==               ==========================================================================================
   def getETwoNLS(self, Operator):
      '''
      getting the set Language in E2
      
      Args:
         Operator: the CENPyOlpProgramModifyOperator
      
      Returns :
         str : language: the Language String in upper Case
      '''
      # getting from Controller
      logging = Operator.GetLoggerOperator()
      controller = Operator.GetController()
      if controller == None:
         return ""
      # getting de-"DE", en-"US", fr-"FR", ja-"JP", zh-"CN"
      language = (controller.GetEtwoLanguage())[3:]
      if language == "US":
         language = "EN"
      # check for existence
      range = ["EN", "DE", "FR", "CN", "JP"]
      if not range.count(language.upper()):
         language = "EN"
      return language.upper()
      
   # ==               ==========================================================================================
   def defineNLS(self, language = "", project = "", altpath = ""):
      '''
      Sets the desired Language, Project Name(optional) and PlugIn Path(optional)
      
      Args:
         language : the desired NLS Language, if empty determine the Systems Language
                    english "EN",  german "DE",  french "FR",  chinese "CN",  japanese "JP"
                    (optional, try to get OS Language if not set, default "EN")
         project  : sets the requested NLS Project "common", "report", etc.(optional, default "common" if not set)
         altpath  : alternative Path for own customized PlugIn NLS Files (optional)
      
      Note : following Conditions to call the defineNLS
             defineNLS() : no Args : get language from OS, Project "common", NLS in cenpylib\languages
             defineNLS(language) : only language Arg : desired language, Project "common", NLS in cenpylib\languages
             defineNLS(altpath="__yourpath") : only path Arg : get language from OS, Project "common", NLS in altpath & cenpylib\languages
             defineNLS(language, altpath="__yourpath") : language & path Arg : desired language, Project "common", NLS in altpath & cenpylib\languages
             defineNLS(language, project) : language & project Arg : desired language or empty ""=OS, Project with desired Name, NLS in cenpylib\languages
             defineNLS(language, project, altpath) : language & project Arg : desired language or empty ""=OS, Project with desired Name, NLS in altpath & cenpylib\languages
             defineNLS(project="__yourproject__", altpath="__yourpath") : language=OS, Project with desired Name, NLS in altpath & cenpylib\languages
             
      '''
      
      # get the checked Language String
      self.__language = self.setNLSLanguage(language)
      
      # which Project should be used ? common, report, etc.
      if project == "":
         project = "common"
      project = project.lower()
         
      # reads the NLS File to a List
      self.__nlsList = self.readInNLSFile(project, altpath)
      
   # ==               ==========================================================================================
   def setNLSLanguage(self, language):
      '''
      Checks and sets the desired Language
      
      Args:
         language : the desired NLS Language 
                    english "EN",  german "DE",  french "FR",  chinese "CN",  japanese "JP"
      
      Returns :
         str : language: the Language String in upper Case
      '''
      if language == "":
         # get the first to Chars of the first Item of getdefaultlocale : en_US, de_DE, fr_FR, etc.
         language = (locale.getdefaultlocale()[0])[0:2]
         
      range = ["EN", "DE", "FR", "CN", "JP"]
      if not range.count(language.upper()):
         language = "EN"
      return language.upper()
      
   # ==               ==========================================================================================
   def readInNLSFile(self, project, altpath):
      '''
      Reads the Language File and save it to a List.
      
      Args:
         project: sets the requested NLS Project "common", "report", etc.
         altpath: the alternative Location of the LanguageFiles (customized NLS)
      
      Returns:
         strList: nlsList: the List of the Columns Header Names in desired Order
      '''
      # reads the language File
      nlsList = []
      if altpath != "":
         # altpath given, check if NLS File exists and read in
         if altpath[-2:] != "\\":
            altpath += "\\"
         nlsFile = altpath +  project + "." + self.__language.lower() + ".lng"
         if exists(nlsFile):
            with open(nlsFile, encoding='utf-8') as file:
               for line in file:
                  thisLine = []
                  if line.find("[") == 0:
                     continue
                  if len(line) > 2:
                     thisLine = str(line).split("=")
                     nlsList.append(thisLine)
            file.close()
            
      # get the E2 Installation NLS File and read in if exists
      nlsFile = self.__apppath + project + "." + self.__language.lower() + ".lng"
      if exists(nlsFile):
         with open(nlsFile, encoding='utf-8') as file:
            for line in file:
               thisLine = []
               if line.find("[") == 0:
                  continue
               if len(line) > 2:
                  thisLine = str(line).split("=")
                  nlsList.append(thisLine)
         file.close()
      
      # return NLS List
      return nlsList
   
   # ==               ==========================================================================================
   def getNLS(self, name, default = ""):
      '''
      Returns the desired Item if translated, otherwise Default taken.
      
      Args:
         name: the NLS-Item
         default: the default Translation if NLS-Item not found
      
      Returns:
         str: nlsStr: the found NLS or the default
      '''
      if default == "":
         default = name
      if len(self.__nlsList) < 1:
         return default
      for nlsLine in self.__nlsList:
         if name == nlsLine[0]:
            if len(nlsLine) > 1:
               nlsStr = nlsLine[1].replace("\n", "")
               return nlsStr
      return default
      
   # ==               ==========================================================================================
   def replaceNLS(self, instring, searchstr, replacestr):
      '''
      Searches in a String for a chain of Characters and replace it, if found, with a desired String and returns this.
      
      Args:
         instring : the Base String with the to be replaced Item
         searchstr : the String to be searched and replaced
         replacestr : the String for replacing
      
      Returns:
         str: outstring: the String with the replaced Item
      '''
      outstring = instring.replace(searchstr, replacestr)
      return outstring