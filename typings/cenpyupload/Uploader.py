UPLOAD_CLASS_NAME = "Uploader"

class Uploader():

    def __init__(self) -> None:
        pass

    def Initialize(self, operator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default Initialize called")

    def ParseFile(self, operator, fileObject):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default ParseFile called")
        
    def Finalize(self, operator):
        logger = operator.GetLogOperator()
        logger.LogDebug("Default Finalize called")