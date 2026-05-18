"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpAttribute import *

class CENPyOlpAttributeTable(CENPyOlpAttribute):
   def ClearTable(self):
      """Empty and delete content of the table.
      """
      ...
   
   def AddColumn(self, name: str, type: int, valueType: int) -> int:
      """Add a new column to the table.
      
      Args:
         name: Column name.
         type: Column type.
         valueType: Column attribute type.
      
      Returns:
         Number of columns (inclusive new one).
      """
      ...
   
   def AddRow(self) -> int:
      """Add a row. Cell values are filled with default values (int: 0; double: 0.0; bool: false; string: ("")
      
      Returns:
         Size of created row array.
      """
      ...
   
   def GetColumnType(self, columnNumber: int) -> int:
      """Get type of given column.
      
      Args:
         columnNumber: Number of column to get the type of (numbers start with 0).
      
      Returns:
         Column type.
      """
      ...
   
   def GetColumnName(self, columnNumber: int) -> str:
      """Get name of given column.
      
      Args:
         columnNumber: Number of column to get the name of (numbers start with 0).
      
      Returns:
         Column name.
      """
      ...
   
   def GetColumnSize(self) -> int:
      """Get number of columns.
      
      Returns:
         Columns number.
      """
      ...
   
   def GetRowSize(self) -> int:
      """Get number of rows.
      
      Returns:
         Rows number.
      """
      ...
   
   def GetCell(self, columnNumber: int, rowNumber: int) -> object:
      """Get cells of a row.
      
      Args:
         columnNumber: number of the column.
         rowNumber: Number of the row.
      
      Returns:
         Cell object.
      """
      ...
   
   def SetCell(self, columnNumber: int, rowNumber: int, pyValue: object):
      """Set the cell with a value.
      
      Args:
         columnNumber: Number of the column.
         rowNumber: Number of the row.
         pyValue: Desired value.
      """
      ...
   
   def GetCellType(self, columnNumber: int, rowNumber: int) -> int:
      """Get the cell types of a row.
      
      Args:
         columnNumber: Number of the column.
         rowNumber: Number of the row.
      
      Returns:
         Type of the cell, int corresponding to ColumnType.
      """
      ...
   
   def SetImportScriptName(self, importScriptName: str):
      """Searches path to the import script and sets it.
      
      Args:
         importScriptName: Filename of import script (python file, e.g. table.py).
      """
      ...
   
   def SetExportScriptName(self, exportScriptName: str):
      """Searches path to the export script and sets it.
      
      Args:
         exportScriptName: Filename of export script (python file, e.g. table.py).
      """
      ...
   
   def SetImportFilePath(self, importFilePath: str):
      """Sets path to the file which should be imported.
      
      Args:
         importFilePath: Full path of the import file.
      """
      ...
   
   def GetImportFilePath(self) -> str:
      """Get full path of the import file.
      
      Returns:
         Full path of the import file.
      """
      ...
   
   def GetRowNumberById(self, id: str) -> int:
      """Get row number of the row with specified ID (REQUIRES: First column has to be an ID).
      
      Args:
         id: Row ID.
      
      Returns:
         Row number, -1 if row not found.
      """
      ...
   
   def GetRowValuesById(self, id: str) -> list:
      """Get row values of the row with specified ID (REQUIRES: First column has to be an ID).
      
      Args:
         id: Row ID.
      
      Returns:
         Value objects of the desired row.
      """
      ...
   
   def GetRowValues(self, row: int) -> list:
      """Get row values of the row with specified index.
      
      Args:
         row: Row index.
      
      Returns:
         Value objects of the desired row.
      """
      ...
   
   def DeleteRow(self, index: int):
      """Delete a row in this table by index.
      
      Args:
         index: Index of the row to delete.
      """
      ...
   
   def DeleteAllRows(self):
      """Delete all existing rows of this table. So that there are only columns.
      """
      ...
   
   def SetTableIconName(self, tableIconName: str):
      """Set the table icon name for this table. 
      Attention: This icon is provisioned for the table representation. Use SetIconName for the attribute icon.
      
      Args:
         tableIconName: Icon name to be used for this table.
      """
      ...
   
   def GetTableIconName(self) -> str:
      """Get the icon name for this table.
      Attention: This method returns the table icon. Use GetIconName if you need the attribute icon.
      
      Returns:
         Icon name for this table.
      """
      ...
   
   def GetColumnValueType(self, columnNumber: int) -> int:
      """Get attribute type of the column.
      
      Args:
         columnNumber: Column to get attribute type of.
      
      Returns:
         Attribute type of the column.
      """
      ...
   
   def GetCellValueType(self, columnNumber: int, rowNumber: int) -> int:
      """Get attribute type of the cell.
      
      Args:
         columnNumber: Column number of the cell.
         rowNumber: Row number of the cell.
      
      Returns:
         Attribute type of the cell.
      """
      ...
   
