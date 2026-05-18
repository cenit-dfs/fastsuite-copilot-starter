COPYRIGHT: Cenit AG 2023

-----------------------------------------------------------------------------------------------------------------------------
How to add a new file/class to the cenpylib:
-----------------------------------------------------------------------------------------------------------------------------
1. Add the new file.py to the cenpylib folder.
2. Add the new import line to the __init__.py file, for example: 
   <from .file import method> where 'method' is a function that is present in a file called 'file.py'
   or
   <from .file import class> where 'class' is present in a file called 'file.py'
   or
   <from .file import *> import everything from 'file.py'
3. Update Cenit.API.PyLibrary Nuget package version by creating a new Tag -> the NuGet will be automatically released.
4. Update the NuGet package in the CenitViewer project.


-----------------------------------------------------------------------------------------------------------------------------
How to update the cenpylib:
-----------------------------------------------------------------------------------------------------------------------------
1. Do the nessesary modifications.
3. Update Cenit.API.PyLibrary Nuget package version by creating a new Tag -> the NuGet will be automatically released.
4. Update the NuGet package in the CenitViewer project.