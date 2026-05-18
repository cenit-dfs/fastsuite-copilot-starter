import os
from os.path import exists

def OpenFile(filePath):
    dirPath = os.path.dirname(filePath)
    if not exists(dirPath):
        return None
    return open(filePath, "r")


def UploadProgramFromFile(operator):
    logger = operator.GetLogOperator()
    logger.LogDebug("Starting Uploader")

    #### Get the class name of the uploader from globals and instantiate
    uploaderClass = "no_name"
    try:
        uploaderClass = globals()[UPLOAD_CLASS_NAME]
    except:
        logger.LogError("Uploader class name is not set! Aborting upload.")
        return
    
    uploader = uploaderClass()
    if uploader is None:
        logger.LogError("Could not initialize uploader class. Aborting upload.")
        return
    
    uploader.Initialize(operator)
    
    for sourceFile in operator.GetSourceFiles():
        logger.LogDebug("Opening file " + sourceFile)
        try:
            fileObject = OpenFile(sourceFile)
            if fileObject is None:
                logger.LogError("Unable to open file at " + sourceFile)
                continue
                
            uploader.ParseFile(operator, fileObject)
            fileObject.close()
        except Exception as Argument:
            logger.LogError("Error while parsing file " + sourceFile)
            logger.LogError(str(Argument))
        
    uploader.Finalize(operator)