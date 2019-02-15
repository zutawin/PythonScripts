import os, sys, re, datetime, argparse, time, ntpath
from shutil import copyfile, copytree, rmtree


class sharedResourcesClass():
    def __init__(self, logfile = ''):
        self.debug = True
        self.logfile = ''
        self.printToConsole = True
        self.writeToLogfile = False
        self.scriptDescription = ''
        self.currentFunc = __name__
        # self.getPresentWorkingDir()
        # self.defineLogfile(logfile)

    def getPresentWorkingDir(self):
        self.pwd = os.getcwd()
        self.logInfo('Current Working Directory: ' + str(self.pwd))
        return self.pwd

    def enableDebug(self):
        self.debug = True
        self.printToConsole = True

    def disbleDebug(self):
        self.debug = False

    def defineLogfile(self, logfile):
        if logfile:
            self.logfile = logfile
            self.enableWriteToLogfile()
            self.clearLogfile()
            self.logInfo('logfile defined: ' +str(self.logfile))
        else:
            self.disableWriteToLogfile()
            self.logWarning('No Logging to file is made.')

    def enableWriteToLogfile(self):
        self.writeToLogfile = True
        self.logDebug('Enabled WriteToLogFile.')

    def disableWriteToLogfile(self):
        self.writeToLogfile = False
        self.logDebug('Disabled WriteToLogFile.')

    def enableLogToConsole(self):
        self.printToConsole = True
        self.logDebug('Enabled PrintToConsole.')

    def disableLogToConsole(self):
        self.printToConsole = False
        self.logDebug('Disabled PrintToConsole.')

    def appendCurrentFuncName(self, funcName):
        self.currentFunc = self.currentFunc + '::' + funcName
        self.logDebug('Appended funcName.New CurrentFunc: ' + self.currentFunc)

    def removeLastFuncName(self, funcName):
        currentFunc = self.currentFunc
        temp = currentFunc.rsplit('::')
        # print('temp[-1] = ' + str(temp[-1]))
        if temp[-1] == funcName:
            self.currentFunc = '::'.join(temp[:-1])
            self.logDebug('Removed last FuncName. funcName.New CurrentFunc: ' + self.currentFunc)
        else:
            print('Exception ERROR: FULLcurrentFunc: ' + currentFunc)
            print('Exception ERROR: expectedFunc: ' + funcName)
            print('Exception ERROR: currentFunc: ' + temp[-1])
            raise Exception("function name mismatch.")



    def printCow(self):
        print("        0")
        print("            0           ^__^")
        print("                o       (oo)\_______")
        print("                        (__)\       )\/\\")
        print("                            ||----W |")
        print("                            ||     ||")
        print("")

    def printSeparationLine(self):
        for lopp in range(110):
            sys.stdout.write("=")
        print("")

    def printDescription(self):
        decc = "Hello.\n" \
               "I'm Moo. I am a Cow.\n" \
               "I eat grass.\n" \
               "I also produces tasty milk!\n"
        if self.scriptDescription:
            description = self.scriptDescription
        else:
            description = decc
        filteredDescription = description.replace("\r", "")
        listDes = filteredDescription.split("\n")
        longestText = 0
        for eachLine in listDes:
            tempLength = len(eachLine)
            if tempLength > longestText:
                longestText = tempLength
        sys.stdout.write("  ")
        for i in range(longestText):
            sys.stdout.write("_")
        sys.stdout.write("\n")
        sys.stdout.write(" /")
        for i in range(longestText):
            sys.stdout.write(" ")
        sys.stdout.write("\\")
        sys.stdout.write("\n")
        for eachLine in listDes:
            sys.stdout.write("| ")
            lineLength = 0
            while lineLength < len(eachLine):
                sys.stdout.write(eachLine[lineLength])
                lineLength = lineLength + 1
            if lineLength <= longestText:
                while lineLength <= longestText:
                    sys.stdout.write(" ")
                    lineLength = lineLength + 1
            sys.stdout.write("|")
            sys.stdout.write("\n")
        sys.stdout.write(" \\")
        for i in range(longestText):
            sys.stdout.write("_")
        sys.stdout.write("/")
        sys.stdout.write("\n")
        self.printCow()
        self.printSeparationLine()
        time.sleep(2)

    def getCurrentTime(self):
        return datetime.datetime.now()

    def appendToFile(self, msg):
        try:
            openfile = open(self.logfile, 'a+')
            openfile.write(msg + '\n')
            openfile.close()
        except:
            print("unable to open logfile.")
            exit()

    def log_msgType(self, msgtype, msg):
        timeFormat = "[" + str(self.getCurrentTime()) + "]"
        msgFormat = ">"+ str(msgtype) +": " + str(msg)
        if self.printToConsole:
            if self.debug:
                print(timeFormat + '{' + self.currentFunc + '}' + msgFormat)
                # print(timeFormat + msgFormat)
            else:
                print(timeFormat + msgFormat)
        else:
            if not msgtype == 'ERROR' and not msgtype == 'WARNING':
                sys.stdout.write("=")
            else:
                print(timeFormat + msgFormat)

        if self.writeToLogfile:
            self.appendToFile(timeFormat + msgFormat)

    def logFunctionStart(self, msg):
        msgType = "FUNCTION_START"
        self.log_msgType(msgType, msg)


    def logFunctionEnd(self, msg):
        msgType = "FUNCTION_END"
        self.log_msgType(msgType, msg)


    def logInfo(self, msg):
        msgType = "INFO"
        self.log_msgType(msgType, msg)


    def logError(self, msg):
        msgType = "ERROR"
        self.log_msgType(msgType, msg)


    def logWarning(self, msg):
        msgType = "WARNING"
        self.log_msgType(msgType, msg)

    def logDebug(self, msg):
        msgType = "DEBUG"
        self.log_msgType(msgType, msg)

    def clearLogfile(self):
        if self.writeToLogfile:
            self.logDebug("clearing logfile...")
            try:
                openfile = open(self.logfile, 'w')
                openfile.close()
                self.logDebug("logfile cleared.")
            except:
                print("unable to open logfile.")
                exit()

    def getFullPathFromFileName(self, _fileName):
        return os.path.abspath(_fileName)

    def GetDirectoryPathFromFileName(self, _fileName):
        return os.path.dirname(self.getFullPathFromFileName(_fileName))

    def GetFileNameFromPath(self, _filePath):
        return ntpath.basename(self.getFullPathFromFileName(_filePath))

    def IsFileExist(self, _file):
        x = os.path.exists(_file)
        if not x:
            self.logWarning(str(_file) + " does not exist.")
        return x

    def IsFile(self, _file):
        x = os.path.isfile(_file)
        if not x:
            self.logWarning(str(_file) + " is not a file.")
        return x

    def IsDirectory(self, _path):
        x = os.path.isdir(_path)
        if not x:
            self.logWarning(str(_path) + " is not a directory.")
        return x

    def IsExtension(self, _file, _extension):
        if (not _extension.replace(".", "") == ntpath.basename(_file).split(".")[-1]):
            self.logWarning(str(ntpath.basename(_file)) + ' does not have ".' + str(_extension) + '" extension.')
            return False
        return True

    def getPythonVersion(self):
        systemPythonVersion = sys.version_info[0]  # Major version number
        self.logInfo("Currently running on Python Version: " + str(systemPythonVersion))
        return systemPythonVersion

    def Argparse_Generic(self, _argList):
        # each argList entry has a list of size 3:
        #   - argName (type = string)
        #   - required (True/False)
        #   - help (type = string)
        _description = self.scriptDescription
        if not _description:
            _description = "no description"
        parser = argparse.ArgumentParser(description=_description, formatter_class=argparse.RawTextHelpFormatter)
        for eachArgs in _argList:
            if not isinstance(eachArgs[1], bool):
                raise Exception("variable 'required' is not boolean dataType.")
            if eachArgs[1] == True:
                parser.add_argument("-" + str(eachArgs[0]), required=True, help=str(eachArgs[2]))
            else:
                parser.add_argument("-" + str(eachArgs[0]), required=False, help=str(eachArgs[2]))
        parser.add_argument('-d', action='store_true', help='Enable debug console logging.')
        parser.add_argument('-p', action='store_true', help='Enable detailed console logging')
        # parser.add_argument('-', action='store_true')
        args = parser.parse_args()

        print('args.d >>' + str(args.d))
        print('args.p >>' + str(args.p))
        if args.p:
            self.printToConsole = True
        else:
            self.printToConsole = False
        if args.d:
            self.printToConsole = True
            self.debug = True
        else:
            self.printToConsole = False
            self.debug = False
        return args
