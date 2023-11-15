#!/usr/bin/env python2.7

# ADOBE CONFIDENTIAL
#
# Copyright 2010-2021 Adobe
# All Rights Reserved.
#
# NOTICE:  Adobe permits you to use, modify, and distribute this file in
# accordance with the terms of the Adobe license agreement accompanying it.
# If you have received this file from a source other than Adobe,
# then your use, modification, or distribution of it requires the prior
# written permission of Adobe.
#

import os, sys, subprocess, platform, time

# -----------------------------------------------------------------------------
# Editable variables
cPerforceP4AbsPath = os.path.abspath("c:/Program Files/Perforce/p4.exe")
cVerbose = True

# -----------------------------------------------------------------------------
# Application Constants
cStatusUndefined = 0
cStatusNotInDepot = 1
cStatusPreviousRevision = 2
cStatusLastRevision = 3
cStatusCheckedOut = 4
cStatusMarkedForAdd = 5

# -----------------------------------------------------------------------------
if cVerbose:
    print("Python Version: "+str(sys.version_info))

def getStatusLabel(aStatus):
    if aStatus == cStatusNotInDepot: return "Not in depot"
    if aStatus == cStatusPreviousRevision: return "Previous Revision"
    if aStatus == cStatusLastRevision: return "Last Revision"
    if aStatus == cStatusCheckedOut: return "Checked Out"
    if aStatus == cStatusMarkedForAdd: return "Marked For Add"
    return "unknown"

# -----------------------------------------------------------------------------
def getCurrentScriptPath(file = __file__):
    return os.path.abspath(os.path.dirname(os.path.realpath(file)))

def getTempFileAbsPath(fileName):
    return os.path.join(getCurrentScriptPath(), "__tmp_" + fileName)

# -----------------------------------------------------------------------------
class RunResult:
    def __init__(self, aExitCode = 0, aLines = []):
        self.mExitCode = aExitCode
        if self.mExitCode is None:
            self.mExitCode = 0

        self.mOutputLines = []

        for l in aLines:
            lineStr = l.decode().rstrip('\n').rstrip('\r')
            self.mOutputLines.append(lineStr)

    def printInfo(self):
        if not cVerbose:
            return

        for l in self.mOutputLines:
            print(l)
        print("Exit Code:" + str(self.mExitCode))

    def getExitCode(self):
        return self.mExitCode

    def getOutputLines(self):
        return self.mOutputLines

# return a RunResult instance
def runCommand(cmd, environment = os.environ, aInputContent = None):
    if cVerbose:
        # print(str(environment))
        print(cmd)
        print("aInputContent = {}".format(aInputContent))

    cTimeOut = 10
    result = [1,[""]]

    argStdIn = None
    if aInputContent:
        aInputContent = aInputContent.encode('utf-8')
        argStdIn = subprocess.PIPE

    try:
        proc = subprocess.Popen(cmd,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  stdin=argStdIn,
                                  env=environment)
    except OSError:
        return RunResult(1)

    output = []
    startTime = time.process_time()
    stdoutAccum = []
    stderrAccum = []

    if aInputContent:
        lines = proc.communicate(aInputContent)
        for l in lines:
            if l and len(str(l)) > 0:
                stdoutAccum.append(l)
    print("stdoutAccum = {}".format(stdoutAccum))

    while True:
        ret = proc.poll()
        proc.stdout.flush()
        newStdout = proc.stdout.readlines()
        newStderr = proc.stderr.readlines()

        if len(newStdout) > 0:
            stdoutAccum += newStdout
        if len(newStderr) > 0:
            stderrAccum += newStderr

        # if the proc has terminated, deal with returning appropriate data
        if ret is not None:
            output = stdoutAccum + stderrAccum
            break

        # if there has been new output, the proc is still alive so reset counters
        if newStderr or newStdout:
            startTime = time.process_time()

        # Make sure we haven't timed out
        curTime = time.process_time()
        if curTime - startTime > cTimeOut:
            break

    if cVerbose:
        print("Output:")
        print(str(output))
    return RunResult(proc.returncode, output)

# -----------------------------------------------------------------------------
class Context:
    def __init__(self):
        self.mWorkspaceName = ""
        self.mWorkspacePath = ""
        self.mAction = ""
        self.mDescription = ""
        self.mFiles = []

    def isValid(self):
        return len(self.mAction) > 0

    def printInfo(self):
        if not cVerbose:
            return
        print("WorkSpaceName:"+self.mWorkspaceName)
        print("WorkSpacePath:"+self.mWorkspacePath)
        print("Action       :"+self.mAction)
        print("Description  :"+self.mDescription)
        print("Files        :"+str(self.mFiles))
        for f in self.mFiles:
            print("   "+str(f))

    def getAction(self):
        return self.mAction

    def getDescription(self):
        return self.mDescription

    def parseArgs(self, aArgs):
        def _parseFilesList(aFileAbsPath):
            if not os.path.isfile(aFileAbsPath):
                return []

            f = open(aFileAbsPath, "rt")
            if f == None:
                print("Unable to open file : " + aFileAbsPath)
                return []

            fileLines = f.readlines()
            f.close()

            return fileLines;
        #---------------------------------------------------
        i = 0
        if (i < len(aArgs)):
            if cVerbose:
                print("arg[" + str(i) + "]=" + str(aArgs[i]))
            self.mWorkspaceName = aArgs[i]
            i += 1

        if (i < len(aArgs)):
            if cVerbose:
                print("arg[" + str(i) + "]=" + str(aArgs[i]))
            self.mWorkspacePath = os.path.abspath(aArgs[i])
            i += 1

        if (i < len(aArgs)):
            if cVerbose:
                print("arg[" + str(i) + "]=" + str(aArgs[i]))
            self.mAction = aArgs[i]
            i += 1

        delimiterDesc = "-desc:"
        delimiterFiles = "-files:"
        delimiterFilesList = "-files_list:"
        delimiters = [delimiterDesc, delimiterFiles, delimiterFilesList]
        while i < len(aArgs):
            if cVerbose:
                print("arg[" + str(i) + "]=" + str(aArgs[i]))
            arg = aArgs[i]
            i += 1

            if arg == delimiterDesc:
                if i < len(aArgs):
                    self.mDescription = aArgs[i]
                    i += 1
            elif arg == delimiterFiles:
                while i < len(aArgs) and (not aArgs[i] in delimiters):
                    self.mFiles.append(os.path.abspath(os.path.join(self.mWorkspacePath, aArgs[i])))
                    i += 1
            elif arg == delimiterFilesList:
                if i < len(aArgs):
                    fileList = aArgs[i]
                    i += 1

                    # parse file
                    for file in _parseFilesList(fileList):
                        self.mFiles.append(os.path.abspath(os.path.join(self.mWorkspacePath, file.rstrip('\n').rstrip('\r'))))

    def getP4AbsPath(self):
        return cPerforceP4AbsPath

    def runP4(self, aArgs, aInputContent = None):
        newEnv = os.environ.copy()
        newEnv["P4CLIENT"] = self.mWorkspaceName
        newArgs = []
        newArgs.append(self.getP4AbsPath())
        newArgs += aArgs
        return runCommand(newArgs, newEnv, aInputContent)

# -----------------------------------------------------------------------------
class P4FileStatus:
    def __init__(self, aLines):
        self.mValues = {}
        self.parse(aLines)

    def parse(self, aLines):
        for line in aLines:
            tokens = line.split(" ")
            if len(tokens) < 2:
                continue

            fieldName = tokens[1]
            value = " ".join(tokens[2:])
            self.mValues[fieldName] = value

    def get(self, fieldName):
        if fieldName in self.mValues:
            return self.mValues[fieldName]
        return None

    def getDepotFile(self):
        return self.get("depotFile")
    def getAction(self):
        return self.get("action")
    def getHeadRev(self):
        return self.get("headRev")
    def getRev(self):
        return self.get("haveRev")

    # return Status constant value
    def getStatus(self):
        p4depotFile = self.getDepotFile()
        p4action = self.getAction()
        p4headRev = self.getHeadRev()
        p4haveRev = self.getRev()

        if cVerbose:
            print("p4depotFile: "+str(p4depotFile))
            print("p4action   : "+str(p4action))
            print("p4headRev  : "+str(p4headRev))
            print("p4haveRev  : "+str(p4haveRev))

        if not p4depotFile:
            return cStatusNotInDepot

        if not p4action:
            if not p4haveRev:
                return cStatusLastRevision
            if p4haveRev==p4headRev:
                return cStatusLastRevision
            return cStatusPreviousRevision

        if p4action=="edit":
            return cStatusCheckedOut

        if p4action=="add":
            return cStatusMarkedForAdd

        return cStatusUndefined

# -----------------------------------------------------------------------------
class P4File:
    def __init__(self, aContext, aPath):
        self.mContext = aContext
        self.mPath = aPath
        self.mStatusExitCode = 0

    def getPath(self):
        return self.mPath

    def getStatus(self):
        runResult = self.runP4Action("fstat", ['-c', str(self.mContext.mWorkspaceName)])
        self.mStatusExitCode = runResult.getExitCode()
        if self.mStatusExitCode != 0:
            return None
        return P4FileStatus(runResult.getOutputLines())

    def getStatusExitCode(self):
        return self.mStatusExitCode

    def runP4Action(self, aP4Action, aOptions = []):
        return self.mContext.runP4(aOptions + [aP4Action, self.mPath])

# -----------------------------------------------------------------------------
class P4Info:
    def __init__(self, aContext, aLines):
        self.mContext = aContext
        self.mValues = {}
        self.parse(aLines)

    def parse(self, aLines):
        for line in aLines:
            index = line.find(':')
            if index < 0:
                continue

            fieldName = line[0:index]
            value = line[index+1:]
            self.mValues[fieldName] = value

    def get(self, fieldName):
        if fieldName in self.mValues:
            return self.mValues[fieldName]
        return None

    def getClientName(self):
        return self.get("Client name")

    def getUserName(self):
        return self.get("User name")

# -----------------------------------------------------------------------------
sIntance = None
def getP4Info(aContext):
    global sIntance
    if not sIntance:
        runResult = aContext.runP4(["info"])
        if runResult.getExitCode() == 0:
            sIntance = P4Info(aContext, runResult.getOutputLines())
    return sIntance

# -----------------------------------------------------------------------------
class P4ChangeList:
    def __init__(self, aContext):
        self.mContext = aContext
        self.mID = None
        self.mDescription = ""

    # return new changelist ID or None if error
    def create(self, aDescription = ""):
        p4Info = getP4Info(context)
        inputContent = '''Change:\tnew\n\nClient:\t%s\n\nUser:\t%s\n\nStatus:\tnew\n\nDescription:\n\t%s\n''' % (p4Info.getClientName(), p4Info.getUserName(), str(aDescription))

        runResult = self.mContext.runP4(["change", "-i"], inputContent)
        runResult.printInfo()
        if runResult.getExitCode() != 0:
            return None

        if len(runResult.getOutputLines()) <= 0:
            return None

        tokens = runResult.getOutputLines()[0].split(" ")
        if len(tokens) < 3:
            return None

        if tokens[0] != "Change":
            return None

        changeListID = None
        try:
            changeListID = int(tokens[1])
        except:
            return None

        self.mID = changeListID
        self.mDescription = aDescription
        return self.mID

    def addFile(self, aP4File):
        return self.mContext.runP4(["reopen", "-c", str(self.mID), aP4File.getPath()])

    def submit(self):
        return self.mContext.runP4(["submit", "-c", str(self.mID)])

    def removeFile(self, aP4File):
        return self.mContext.runP4(["reopen", "-c", "default", aP4File.getPath()])

    def delete(self):
        return self.mContext.runP4(["change", "-d", str(self.mID)])

# -----------------------------------------------------------------------------
def executeP4Action(aContext, aP4Action):
    if len(aContext.mFiles) < 0:
        return 1
    for f in aContext.mFiles:
        runResult = P4File(aContext, f).runP4Action(aP4Action)
        if runResult.getExitCode() != 0:
            return runResult.getExitCode()
    return 0

# -----------------------------------------------------------------------------
def executeAdd(aContext):
    return executeP4Action(aContext, "add")

def executeCheckOut(aContext):
    return executeP4Action(aContext, "edit")

def executeSubmit(aContext):
    if len(aContext.mFiles) < 0:
        return 1

    # Create new change set
    p4ChangeList = P4ChangeList(aContext)
    changeListID = p4ChangeList.create(aContext.getDescription())
    if not changeListID:
        return 1

    exitCode = 0
    for f in aContext.mFiles:
        runResult = p4ChangeList.addFile(P4File(aContext, f))
        if runResult.getExitCode() != 0:
            exitCode = runResult.getExitCode()
            break

    if exitCode == 0:
        # Submit changelist
        runResult = p4ChangeList.submit()
        if runResult.getExitCode() == 0:
            return 0
        exitCode = runResult.getExitCode()

    # Error occured whe add file in Changelist
    # move files Back to the default changeset
    for f in aContext.mFiles:
        p4ChangeList.removeFile(P4File(aContext, f))
    p4ChangeList.delete()
    return exitCode

def executeRevert(aContext):
    return executeP4Action(aContext, "revert")

def executeGetLastVersion(aContext):
    return executeP4Action(aContext, "sync")

# -----------------------------------------------------------------------------
def executeGetStatus(aContext):
    if len(aContext.mFiles) < 0:
        return 1

    p4File = P4File(aContext, aContext.mFiles[0])
    p4FileStatus = p4File.getStatus()
    if not p4FileStatus:
        return p4File.getStatusExitCode()

    status = p4FileStatus.getStatus()
    if cVerbose:
        print("Status: " + getStatusLabel(status) + " (" + str(status) + ")")
    return status

# -----------------------------------------------------------------------------
def execute(aContext):
    if aContext.getAction() == "add":
        printHelp()
        return executeAdd(aContext)
    if aContext.getAction() == "checkout":
        return executeCheckOut(aContext)
    if aContext.getAction() == "submit":
        return executeSubmit(aContext)
    if aContext.getAction() == "revert":
        return executeRevert(aContext)
    if aContext.getAction() == "get_last_version":
        return executeGetLastVersion(aContext)
    if aContext.getAction() == "get_status":
        return executeGetStatus(aContext)
    elif len(aContext.getAction()) > 0:
        print("Not implemented Custom action '" + aContext.getAction() + "'")
    return 100 # error

def printHelp():
    print("Syntax: perforce.py WorkspaceName WorkspacePath Action [ActionParams]")

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    context = Context()
    # C:/Python37/python.exe D:/toolset/SubstanceDesigner/Tools/ManageLibrary/ManageLibrary/perforce.py qinjiaxin_01YXHY1235_Assets D:/Dev/Assets/ get_status -files: D:/Dev/Assets/SD/Content/SD_Filis/Common/Surfaces/SurfaceTest/Wood/X_SD_Wood_001_ParamGraph/SD_Files/P4SubmitTest.sbs

    context.parseArgs(sys.argv[1:])
    context.printInfo()

    exitCode = 1
    if not context.isValid():
        print("Error: Invalid Arguments")
        printHelp()
    else:
        exitCode = execute(context)
    sys.exit(exitCode)
