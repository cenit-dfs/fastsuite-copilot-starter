from cenpydownload import DULPythonDownloadOperator
from cenpydownload import DULPythonProgram
from cenpydownload import DULPythonSubprogram
from cenpydownload import DULPythonOperationGroup
from cenpydownload import DULPythonOperation
from cenpydownload import DULPythonEvent
from cenpydownload import DULPythonMotion
from cenpydownload import DULPythonPosition
from cenpydownload import DULPythonController

DOWNLOAD_CLASS_NAME = "Downloader"

class Downloader():

    def __init__(self) -> None:
        pass

    def HandleSubprogramInLoop(self):
        return False
    
    def OutputSubprogramInSeparateFiles(self):
        return True

    def Initialize(self, operator : DULPythonDownloadOperator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default Initialize called")

    def ProgramStart(self, operator : DULPythonDownloadOperator, program : DULPythonProgram):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default ProgramStart called")

    def ProgramEnd(self, operator : DULPythonDownloadOperator, program : DULPythonProgram):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default ProgramEnd called")

    def SubprogramStart(self, operator : DULPythonDownloadOperator, subprogram : DULPythonSubprogram):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default SubProgramStart called")

    def SubprogramEnd(self, operator : DULPythonDownloadOperator, subprogram : DULPythonSubprogram):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default SubProgramEnd called")

    def OperationGroupStart(self, operator : DULPythonDownloadOperator, operationGroup : DULPythonOperationGroup):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OperationGroupStart called")

    def OperationGroupEnd(self, operator : DULPythonDownloadOperator, operationGroup : DULPythonOperationGroup):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OperationGroupEnd called")

    def OperationStart(self, operator : DULPythonDownloadOperator, operation : DULPythonOperation):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OperationStart called")

    def OperationEnd(self, operator : DULPythonDownloadOperator, operation : DULPythonOperation):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OperationEnd called")
        
    def HandleEvent(self, operator : DULPythonDownloadOperator, event : DULPythonEvent):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default HandleEvent called")

    def HandleMotion(self, operator : DULPythonDownloadOperator, motion : DULPythonMotion):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default HandleMotion called")
    
    def OutputPtp(self, operator : DULPythonDownloadOperator, position : DULPythonPosition):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OutputPtp called")

    def OutputLin(self, operator : DULPythonDownloadOperator, position : DULPythonPosition):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OutputLin called")

    def OutputCirc(self, operator : DULPythonDownloadOperator, viaPoint : DULPythonPosition, endPoint : DULPythonPosition):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OutputCirc called")

    def OutputEvent(self, operator : DULPythonDownloadOperator, event : DULPythonEvent):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OutputEvent called")

    def OutputHeader(self, operator : DULPythonDownloadOperator, controller : DULPythonController):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default OutputHeader called")

    def CreateOutputFile(self, operator : DULPythonDownloadOperator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default CreateOutputFile called")

    def CloseOutputFile(self, operator : DULPythonDownloadOperator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default CloseOutputFile called")

    def WriteOutputFile(self, operator : DULPythonDownloadOperator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default WriteOutputFile called")
