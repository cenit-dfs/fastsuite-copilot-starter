# -------------------------------------------------------------------------------------------
# Name: MultiLayerDiagnostics
# Description: Controller-neutral Multilayer diagnostic codes, severities, and fallback scoping.
#              Shared by technology scripts and the KUKA downloader so both sides raise the
#              same structured warnings instead of duplicating prose.
#              See docs/ctrl-specific/KUKA/spec/multilayer.md section 14.
# Debug info: E2@localhost:5254
# Author: Cenit AG
# Changelog:
#     Version: 1.0
#        Changed by:
#        Date:
#
# -------------------------------------------------------------------------------------------
import sys, inspect, os
sys.dont_write_bytecode = True
sys.path.append(str(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


# code -> (severity, short description); mirrors spec section 14 table exactly.
CODES = {
    "ML001": (Severity.WARNING, "WPS not from process table"),
    "ML002": (Severity.WARNING, "Selected WPS is not Multilayer"),
    "ML003": (Severity.WARNING, "Stable WPS row cannot be resolved"),
    "ML004": (Severity.WARNING, "Duplicate WPS name/main-ID ambiguity"),
    "ML005": (Severity.WARNING, "Duplicate layer/bead coordinate"),
    "ML006": (Severity.WARNING, "Seam UUID missing"),
    "ML007": (Severity.WARNING, "AML option pack not configured"),
    "ML008": (Severity.WARNING, "Unsupported controller/KSS/AML version"),
    "ML009": (Severity.WARNING, "More than 99 AML fillers"),
    "ML010": (Severity.WARNING, "Closed-contour start shift required"),
    "ML011": (Severity.WARNING, "Unsupported spline/motion construct"),
    "ML012": (Severity.WARNING, "Unsupported TTS X offset"),
    "ML013": (Severity.WARNING, "Recipe snapshot changed"),
    "ML014": (Severity.WARNING, "Recipe source missing"),
    "ML015": (Severity.WARNING, "Cross-seam sequencing feature not enabled"),
    "ML016": (Severity.WARNING, "AML/E2 simulation may differ"),
    "ML017": (Severity.WARNING, "Reverse correction mapping unverified"),
    "ML018": (Severity.WARNING, "Automatic CAD-driven WPS matching not supported"),
}


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: Severity
    message: str
    program: Optional[str] = None
    seam_uuid: Optional[str] = None
    operation_name: Optional[str] = None
    wps_main_id: Optional[int] = None
    wps_sub_id: Optional[int] = None
    layer: Optional[int] = None
    bead: Optional[int] = None
    selected_mode: Optional[str] = None
    fallback_mode: Optional[str] = None


def make_diagnostic(code: str, message: Optional[str] = None, **fields) -> Diagnostic:
    """Build a Diagnostic for a known ML0xx code.

    An unknown code is a programming error and must fail loudly, not be
    swallowed into a generic warning (spec section 14: "An unexpected
    exception is not a fallback policy").
    """
    if code not in CODES:
        raise ValueError("Unknown Multilayer diagnostic code: " + str(code))
    severity, description = CODES[code]
    return Diagnostic(code=code, severity=severity, message=message or description, **fields)


def seams_with_code(diagnostics, code: str):
    """Seam UUIDs carrying a given diagnostic code.

    Used to scope per-seam AML fallback so one seam's problem never disables
    another valid seam in the same program (spec section 13.6).
    """
    return {d.seam_uuid for d in diagnostics if d.code == code and d.seam_uuid is not None}
