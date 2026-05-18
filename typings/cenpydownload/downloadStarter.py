from cenpydownload import DULPythonDownloadOperator
from cenpydownload import DULPythonProgram
from cenpydownload import DULPythonController
from cenpydownload import DULPythonOperationGroup
from cenpydownload import DULPythonSubprogram

def CastToOperationGroup(object) -> DULPythonOperationGroup:
    """ Cast the given object to DULPythonOperationGroup.
        if the cast fails None is returned.

        object: object to cast
        Returns: returns object as DULPythonOperationGroup if cast is successful, None otherwise    
    """
    if type( object).__name__ in DULPythonOperationGroup.__name__:
        return object
    
    return None

def CastToSubprogram(object) -> DULPythonSubprogram:
    """ Cast the given object to DULPythonSubprogram.
        if the cast fails None is returned.

        object: object to cast
        Returns: returns object as DULPythonSubprogram if cast is successful, None otherwise    
    """
    if type( object).__name__ in DULPythonSubprogram.__name__:
        return object
    
    return None

def HandleProgram(downloader, operator : DULPythonDownloadOperator, controller : DULPythonController, program : DULPythonProgram):
    """ Handles the given program by calling the header output, looping over the program and 
        calling the write to file methods.

        downloader: downloader class instance
        operator: download operator providing all necessary data for the download
        program: program to loop over    
    """
    downloader.OutputHeader(operator, controller)
    #### Traverser the programs and call handlers
    LoopProgram(downloader, operator, program)

    # Handle Subprograms within same program file
    if not downloader.OutputSubprogramInSeparateFiles() and not downloader.HandleSubprogramInLoop():
        subprogramList = []
        for subprogram in program.GetSubprograms():
            calledProgram = subprogram.GetCalledProgram()
            # do not handle a subprogram twice
            if calledProgram.GetName() not in subprogramList:
                subprogramList.append(calledProgram.GetName())
                LoopProgram(downloader, operator, calledProgram)

    #### Handle Output file creation here ####
    downloader.CreateOutputFile(operator) 
    #### Write Output file creation here ####
    downloader.WriteOutputFile(operator) 
    #### Handle output file closing ####
    downloader.CloseOutputFile(operator)    

def LoopProgram(downloader, operator : DULPythonDownloadOperator, program : DULPythonProgram):
    """ Loops over the given progam and calls the handler methods on the given 
        downloader class instance.

        downloader: downloader class instance
        operator: download operator providing all necessary data for the download
        program: program to loop over
    """
    downloader.ProgramStart(operator, program)
    for programCompenent in program.GetGroupsAndSubprograms():

        logger = operator.GetLogOperator()
        logger.LogDebug( DULPythonOperationGroup.__name__ )
        logger.LogDebug(str(type( programCompenent)))
        logger.LogDebug(type( programCompenent).__name__)
        operationGroup = CastToOperationGroup(programCompenent)
        if operationGroup is not None:
            downloader.OperationGroupStart(operator, operationGroup)
            for operation in operationGroup.GetOperations():
                downloader.OperationStart(operator, operation)
                for motion in operation.GetMotions():
                    downloader.HandleMotion(operator, motion)
                downloader.OperationEnd(operator, operation)
            downloader.OperationGroupEnd(operator, operationGroup)
        subprogram = CastToSubprogram(programCompenent)
        if subprogram is not None:
            downloader.SubprogramStart(operator, subprogram)
            if not downloader.OutputSubprogramInSeparateFiles() and downloader.HandleSubprogramInLoop():
                LoopProgram(downloader, operator, subprogram.GetCalledProgram())
            downloader.SubprogramEnd(operator, subprogram)
        
    downloader.ProgramEnd(operator, program)

def DownloadActiveProgram(operator : DULPythonDownloadOperator):
    """ This method is the entry point in to the download process. It will be called
        by the E2 embedded python interpreter.
        The method will try to initialize the loaded Downloader and loop through the program.

        operator: download operator providing all necessary data for the download
    """
    logger = operator.GetLogOperator()
    logger.LogDebug("Starting Downloader")

    #### Get the class name of the downloader from globals and instantiate
    downloaderClass = "no_name"
    try:
        downloaderClass = globals()[DOWNLOAD_CLASS_NAME]
    except:
        logger.LogError("Downloader class name is not set! Aborting download.")
        return
    
    downloader = downloaderClass()
    if downloader is None:
        logger.LogError("Could not initialize downloader class. Aborting download.")
        return
    
    downloader.Initialize(operator)
    
    controller = operator.GetController()
    program = controller.GetActiveProgram()

    #### Output a general header in file(s) if needed
    HandleProgram(downloader, operator, controller, program)

    # Handle Subprograms in separate program file
    if downloader.OutputSubprogramInSeparateFiles():
        subprogramList = []
        for subprogram in program.GetSubprograms():
            calledProgram = subprogram.GetCalledProgram()
            # do not handle a subprogram twice
            if calledProgram.GetName() not in subprogramList:
                subprogramList.append(calledProgram.GetName())
                HandleProgram(downloader, operator, controller, calledProgram)