import csv
import math

import clr

clr.AddReference("Cenit.FastSuite.Customization")
clr.AddReference("System.Windows.Forms")

import Cenit.FastSuite.Customization.FileSelectionDialog as FileSelectionDialog
import Cenit.FastSuite.Customization.ProcessGeometryImport as ProcessGeometryImport
from System.Windows.Forms import *


class AtolPointImport(ProcessGeometryImport):

    def __init__(self):
        ProcessGeometryImport.__init__(self)

    @staticmethod
    def _normalize(x, y, z):
        length = math.sqrt(x * x + y * y + z * z)
        if length == 0.0:
            raise ValueError("Zero-length orientation vector.")
        return x / length, y / length, z / length

    @classmethod
    def _axes_from_rxyz(cls, rx_deg, ry_deg, rz_deg):
        rx = math.radians(rx_deg)
        ry = math.radians(ry_deg)
        rz = math.radians(rz_deg)
        cx, sx = math.cos(rx), math.sin(rx)
        cy, sy = math.cos(ry), math.sin(ry)
        cz, sz = math.cos(rz), math.sin(rz)

        # R = Rx * Ry * Rz. Local X is tangent; local Y is normal.
        tangent = cls._normalize(
            cy * cz,
            sx * sy * cz + cx * sz,
            -cx * sy * cz + sx * sz
        )
        normal = cls._normalize(
            -cy * sz,
            -sx * sy * sz + cx * cz,
            cx * sy * sz + sx * cz
        )
        return tangent, normal

    @staticmethod
    def _number(text):
        return float(text.strip().replace(",", "."))

    @staticmethod
    def _add_optional_value(process_geometry, name, value):
        process_geometry.AddBool("Has_" + name, value is not None)
        if value is not None:
            process_geometry.AddDouble(name, value)

    def Import(self, workpiece):
        self.Workpiece = workpiece
        selected_file = FileSelectionDialog.Select("CSV files", "*.csv")
        if not selected_file:
            return

        try:
            group = self.CreateProcessGeometryGroup()
            if not group:
                raise RuntimeError("Could not create a process-geometry group.")
            self.ImportedProcessGeometryGroups.Add(group)

            pending_speed = None
            pending_wait = None
            with open(selected_file, "r") as csv_file:
                rows = csv.reader(
                    csv_file, delimiter=";", quotechar="#",
                    quoting=csv.QUOTE_NONE
                )
                for line_number, row in enumerate(rows, 1):
                    if not row or len(row) < 2:
                        continue

                    row_type = row[1].strip()
                    if row_type == "Speed":
                        if len(row) < 3:
                            raise ValueError("Speed value missing at line %d." % line_number)
                        pending_speed = self._number(row[2])
                        continue
                    if row_type == "Wait":
                        if len(row) < 3:
                            raise ValueError("Wait value missing at line %d." % line_number)
                        pending_wait = self._number(row[2])
                        continue
                    if row_type != "Move":
                        continue
                    if len(row) < 8:
                        raise ValueError("Move fields missing at line %d." % line_number)

                    x = self._number(row[2]) / 1000.0
                    y = self._number(row[3]) / 1000.0
                    z = self._number(row[4]) / 1000.0
                    tangent, normal = self._axes_from_rxyz(
                        self._number(row[5]),
                        self._number(row[6]),
                        self._number(row[7])
                    )

                    process_geometry = self.CreatePointProcessGeometry(group)
                    if not process_geometry:
                        raise RuntimeError(
                            "Could not create process geometry at line %d." % line_number
                        )
                    process_geometry.AssignTargetData(
                        x, y, z,
                        normal[0], normal[1], normal[2],
                        tangent[0], tangent[1], tangent[2]
                    )
                    self._add_optional_value(
                        process_geometry, "Speed", pending_speed
                    )
                    self._add_optional_value(
                        process_geometry, "Wait", pending_wait
                    )
                    pending_speed = None
                    pending_wait = None
        except Exception as error:
            MessageBox.Show(
                "Import failed.\n\n" + str(error),
                "ATOL point import",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error
            )
