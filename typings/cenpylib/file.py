"""COPYRIGHT Cenit AG 2022"""

import os
import csv
import shutil
import inspect
import pathlib
import datetime
import subprocess
from os.path import exists
from pathlib import Path


class FileUtility:
   """Utility functions for the file system."""
   
   # ----------------------------------------------------------------------
   #   GLOBAL ENCODING SUPPORT (automatic detection for worldwide files)
   # ----------------------------------------------------------------------
   # Order matters: strict / unambiguous encodings must come first, because
   # cp1252 and similar single-byte encodings accept *any* byte sequence and
   # would silently mis-decode CJK files into mojibake otherwise.
   ENCODINGS_TO_TRY = [
      "utf-8-sig",     # BOM is unambiguous
      "utf-8",         # strict: invalid bytes raise
      "gb18030",       # Chinese (superset of GBK / GB2312)
      "shift_jis",     # Japanese
      "euc_jp",
      "iso2022_jp",
      "cp1250",        # Central European
      "cp1252",        # Western European — decodes almost anything, keep last
   ]

   def DetectEncoding(self, filePath):
      """Try multiple encodings to detect which one is correct."""
      for enc in self.ENCODINGS_TO_TRY:
         try:
            with open(filePath, "r", encoding=enc) as f:
               f.read()
            return enc
         except Exception:
            continue
      return None

   def SmartOpen(self, filePath, mode="r"):
      """
      Open file with automatic encoding detection for reading.
      For writing, always use UTF‑8‑SIG (Excel/Windows friendly).
      """
      if "r" in mode and "b" not in mode and exists(filePath):
         # Note: open() does not actually decode bytes, so a try/except around
         # open() can never catch a UnicodeDecodeError. We must read the file
         # to validate the encoding before returning the handle.
         for enc in self.ENCODINGS_TO_TRY:
            try:
               with open(filePath, mode, encoding=enc) as probe:
                  probe.read()
               return open(filePath, mode, encoding=enc)
            except UnicodeDecodeError:
               continue
            except Exception:
               continue
         # Last resort: open with latin-1 (never raises) so callers still get
         # a usable handle instead of crashing.
         return open(filePath, mode, encoding="latin-1", errors="replace")

      return open(filePath, mode, encoding="utf-8")

   # Default variables shared by all instances
   __currentFilePath = Path(os.path.abspath(inspect.getfile(inspect.currentframe())))
   CENIT_LOGO_FOLDER = os.path.join(__currentFilePath.parent, "images")
   CENIT_LANGUAGE_FOLDER = os.path.join(__currentFilePath.parent, "languages")
   CENIT_LOGO_BLACK = os.path.join(__currentFilePath.parent, "images", "CENIT_Logo_black.png")
   CENIT_LOGO_GREEN = os.path.join(__currentFilePath.parent, "images", "CENIT_Logo_green.png")
   FASTSUITE_E2_ICON = os.path.join(__currentFilePath.parent, "images", "Fastsuite_E2_Icon.ico")
   FASTSUITE_E2_LOGO = os.path.join(__currentFilePath.parent, "images", "Fastsuite_E2_Logo.png")

   def GetWindowsUserName(self):
      """Get a name of the windows user.

      Returns:
          str: windows user name.
      """
      return os.getlogin()

   def GetCurrentDateAndTime(self, format="%d.%m.%Y %H:%M:%S"):
      """Get a date and time in the specified format.

      Args:
          format (str, optional): the format of the string time. Defaults to "%d.%m.%Y %H:%M:%S".

      Returns:
          str: current datetime string.
      """
      return datetime.datetime.now().strftime(format)

   def GetFilenameWithoutExtension(self, filePath):
      """"Get the name of the file without extension from the given file path.

      Args:
          filePath (str): path to the file.

      Returns:
          str: name of the file without extension.
      """
      if not os.path.isdir(filePath) and exists(filePath):
         return pathlib.Path(filePath).stem
      return None

   def CopyDirectoryRecursively(self, sourceDirectory, destinationDirectory):
      """Recursively copy an entire directory tree to the given location.
      Create the destination directory if it does not exist.
      Replace the destination directory if it exists.

      Args:
          sourceDirectory (str): path to the dictionary to copy.
          destinationDirectory (str): path to the destination directory.

      Returns:
          bool: True if successful, otherwise False.
      """
      if exists(destinationDirectory):
         if not self.RemoveDirectory(destinationDirectory):
            return False
      if os.path.isdir(sourceDirectory) and not exists(destinationDirectory):
         shutil.copytree(sourceDirectory, destinationDirectory)
         return True
      return False

   def CopyFileToDirectory(self, sourceFile, destinationDirectory):
      """Copy a source file to the destination directory.
      Create the destination directory if it does not exist.
      Replace the destination file if it exists.

      Args:
          sourceFile (str): path to the file to copy.
          destinationDirectory (str): path to the destination directory.

      Returns:
          bool: True if successful, otherwise False.
      """
      if not exists(destinationDirectory):
         os.makedirs(destinationDirectory)
      if exists(sourceFile) and os.path.isdir(destinationDirectory):
         shutil.copy2(sourceFile, destinationDirectory)
         return True
      return False

   def CopyMultipleFilesToDirectory(self, sourceFiles, destinationDirectory):
      """Copy a multiple source files to the destination directory.
      Create the destination directory if it does not exist.
      Replace the destination files if they exist.

      Args:
          sourceFiles (list): list of file paths to copy.
          destinationDirectory (str): path to the destination directory.

      Returns:
          bool: True if successful, otherwise False.
      """
      if not exists(destinationDirectory):
         os.makedirs(destinationDirectory)
      if os.path.isdir(destinationDirectory):
         for sourceFile in sourceFiles:
            if exists(sourceFile):
               shutil.copy2(sourceFile, destinationDirectory)
         return True
      return False

   def CutAndPaste(self, source, destinationDirectory):
      """Recursively move a file or an entire directory tree to the given location.
      Create the destination directory if it does not exist.
      Replace the destination directory if it exists.

      Args:
          source (str): path to the file or dictionary to move.
          destinationDirectory (str): path to the destination directory.

      Returns:
          bool: True if successful, otherwise False.
      """
      if exists(destinationDirectory):
         if not self.RemoveDirectory(destinationDirectory):
            return False
      if exists(source) and not exists(destinationDirectory):
         shutil.move(source, destinationDirectory)
         return True
      return False

   def RemoveDirectory(self, directoryPath, ignoreErrors=True):
      """Delete an entire directory tree, path must point to a directory.

      Args:
          directoryPath (str): path to the directory to delete.
          ignoreErrors (bool, optional): ignore errors. Defaults to True.

      Returns:
          bool: True if successful, otherwise False.
      """
      if os.path.isdir(directoryPath):
         shutil.rmtree(directoryPath, ignore_errors=ignoreErrors)
         return True
      return False

   def AppendTextToFile(self, filePath, text):
      """Open a text file, append the given text and close it. Create a new file if it does not exist.

      Args:
          filePath (str): path to the text file.
          text (str): new text to append.

      Returns:
          bool: True if successful, otherwise False.
      """
      dirPath = os.path.dirname(filePath)
      if not exists(dirPath):
         os.makedirs(dirPath)
      with self.SmartOpen(filePath, "a") as file_object:
         file_object.write(text)
         file_object.write("\n")
         return True
      return False
   
   def AppendTextArrayToFile(self,filePath, block):
      """Open a text file, append the given text array and close it. Create a new file if it does not exist.

      Args:
          filePath (str): path to the text file.
          block (str):  text array to append.

      Returns:
          bool: True if successful, otherwise False.
      """
      dirPath = os.path.dirname(filePath)
      if not exists(dirPath):
         os.makedirs(dirPath)
      with self.SmartOpen(filePath, "a") as file_object:
         for line in block:
            file_object.write(line)
            file_object.write("\n")
         return True
      return False

   def ReadCSVColumnIntoList(self, filePath, columnName):
      """Read the CSV file and return the specified column as a list.

      Args:
          filePath (str): path to the SCV file
          columnName (str): name of the column to search.

      Returns:
          list: column values.
      """
      returnList = []
      if exists(filePath):
         with self.SmartOpen(filePath, "r") as csvFile:
            reader = csv.DictReader(csvFile)
            for col in reader:
                returnList.append(col[columnName])
      return returnList

   def GetFilesAndDirectoriesRecursively(self, directoryPath):
      """Recursively gets all files and all directories inside the given directory.

      Args:
          directoryPath (str): path of the directory to explore.

      Returns:
          list, list: found directories, found files.
      """
      if os.path.isdir(directoryPath):
         _, directories, files = next(os.walk(directoryPath), (None, [], []))
         return directories, files
      return [], []

   def RunWinMerge(self, winMergePath, leftFilePath, rightFilePath, 
                   reportFilePath=None, readonly=True, inBackground=False, useDefaultSettings=False):
      """Call the WinMerge to compare original and modified files.

      Args:
          winMergePath (str): path to WinMerge executable.
          leftFilePath (str): path to the first file or directory to compare.
          rightFilePath (str): path to the second file or directory to compare.
          reportFilePath (str, optional): path to the report file. Defaults to None.
          readonly (bool, optional): readonly mode. Defaults to True.
          inBackground (bool, optional): run in background. Defaults to False.

      Returns:
          bool: True if successful, otherwise False.
      """
      if exists(winMergePath) and exists(leftFilePath) and exists(rightFilePath):
         args = [winMergePath, leftFilePath, rightFilePath]
         if useDefaultSettings:
            args.append("-noprefs")  # Do not read / write setting information from registry (use the default settings)
         args.append("-r")  # Compares all files in all subfolders (recursive compare)
         args.append("-u")  # Do not save the paths to the Most Recently Used list
         if readonly:
            args.extend(["-wl", "-wr"])  # Prohibit editing of compared files
         if inBackground:
            args.append("-minimize")  # Starts WinMerge as a minimized window
            args.append("-noninteractive")  # Exit WinMerge after compare / report generation
         if reportFilePath:
            args.extend(["-cfg", "Settings/DirViewExpandSubdirs=1"])  # Expand folder tree after comparison; 0: do not expand
            args.extend(["-cfg", "ReportFiles/ReportType=2"])  # Generate HTML-format report
            args.extend(["-cfg", "ReportFiles/IncludeFileCmpReport=1"])  # Include file comparison report; 0: do not include
            args.extend(["-or", reportFilePath])  # Generate report file
         result = subprocess.run(args=args, universal_newlines=True, stdout=subprocess.PIPE)
         if result.returncode == 0:
            return True
      return False
