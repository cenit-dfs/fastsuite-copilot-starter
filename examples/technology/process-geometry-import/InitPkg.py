import clr

clr.AddReference("Cenit.FastSuite.Customization")

import Cenit.FastSuite.Customization as Customization
import GenericPoint.PGImport as PGImport


def InitializeWorkpiecePackage():
    package = Customization.ProcessGeometryPackage()
    package.ProcessGeometryImportTypes.Add(
        "AtolPointImport", PGImport.AtolPointImport
    )
    return package
