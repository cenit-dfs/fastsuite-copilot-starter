"""
Automatically generated module. COPYRIGHT CENIT AG 2026.
"""


class CENPyOlpCsvParserOperator:
   def LoadCsvFile(self, filepath: str) -> int:
      """This functions loads the csv-File. After that, you can access the different cells.
      
      Args:
         filepath: File path with ending '.csv'.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def GetNumberOfRows(self) -> int:
      """Get the number of rows of the csv file, if a file was loaded successfully.
      If called after an unsuccessful load, returns an unspecified value.
      
      Returns:
         The number of rows of the file.
      """
      ...
   
   def GetNumberOfColumns(self) -> int:
      """Get the number of columns of the loaded csv file.
      If called after an unsuccessful load, returns an unspecified value.
      
      Returns:
         The number of columns of the file.
      """
      ...
   
   def GetCell(self, columnIndex: int, rowIndex: int) -> str:
      """Accessing a cell by an integer.
      Remark: Accessing the first cell by column = row = 1.
      
      Args:
         columnIndex: The column-index.
         rowIndex: The row-index.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def GetCellByColumnName(self, columnName: str, rowIndex: int) -> str:
      """Accessing a cell by column-name(e.g. A, B, .., AA, AB,..) and a row-index.
      Remark: Accessing the first cell by column = A, row = 1.
      
      Args:
         columnName: The column-name.
         rowIndex: The row-index.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
   def SetSeparator(self, separator: str):
      """Setting the separator-character in the csv-file.
      Remark: The default separator is ';'.
      
      Args:
         separator: The separator-character.
      """
      ...
   
   def GetRow(self, rowIndex: int) -> list:
      """Gets the row at the given, zero-based index.
      
      Args:
         rowIndex: Row index.
      
      Returns:
         ERR_NO_ERROR (0) on success, an error code otherwise.
      """
      ...
   
