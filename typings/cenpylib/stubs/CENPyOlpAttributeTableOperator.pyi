"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""

from .CENPyOlpLogOperator import *

class CENPyOlpAttributeTableOperator:
   def GetLoggerOperator(self) -> CENPyOlpLogOperator:
      """Get logger operator.
      
      Returns:
         Logger operator.
      """
      ...
   
   def GetTableName(self) -> str:
      """Get name of the table.
      
      Returns:
         Table name.
      """
      ...
   
   def AddRow(self) -> int:
      """Add a row. Cell values are filled with default values (int: 0; double: 0.0; bool: false; string: "").
      
      Returns:
         Size of created row array.
      """
      ...
   
   def GetColumnType(self, columnNumber: int) -> int:
      """Get type of the given column.
      
      Args:
         columnNumber: Number of the column to get the type of (numbers start with 0).
      
      Returns:
         Column type.
      """
      ...
   
   def GetColumnName(self, columnNumber: int) -> str:
      """Get name of the given column.
      
      Args:
         columnNumber: Number of the column to get the name of (numbers start with 0).
      
      Returns:
         Column name.
      """
      ...
   
   def GetColumnSize(self) -> int:
      """Get number of the columns.
      
      Returns:
         Columns number.
      """
      ...
   
   def GetRowSize(self) -> int:
      """Get number of the rows.
      
      Returns:
         Rows number.
      """
      ...
   
   def GetCell(self, columnNumber: int, rowNumber: int) -> object:
      """Get cell by the column and row number.
      
      Args:
         columnNumber: Number of the column.
         rowNumber: Number of the row.
      
      Returns:
         Cell object.
      """
      ...
   
   def GetCellType(self, columnNumber: int, rowNumber: int) -> int:
      """Get the cell type by the column and row number.
      
      Args:
         columnNumber: Number of the column.
         rowNumber: Number of the row.
      
      Returns:
         None
      """
      ...
   
   def GetImportFilePath(self) -> str:
      """Get full path of the import file.
      
      Returns:
         Full path of the import file.
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
         Values object of the desired row.
      """
      ...
   
   def GetRowValues(self, row: int) -> list:
      """Get row values of the row with specified index.
      
      Args:
         row: Row index.
      
      Returns:
         Values object of the desired row.
      """
      ...
   
   def DeleteRow(self, index: int):
      """Delete a row in this table.
      
      Args:
         index: Index of the row to delete.
      """
      ...
   
   def DeleteAllRows(self):
      """Delete all existing rows of this table. So that there are only columns.
      """
      ...
   
   def GetColumnValueType(self, columnNumber: int) -> int:
      """Get attribute type of column.
      
      Args:
         columnNumber: Column number to get attribute type of.
      
      Returns:
         Attribute type of column.
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
   
