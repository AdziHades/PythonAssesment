# Organise imports
import hashlib
from platform import system
from subprocess import call
from pathlib import Path
import subprocess

## Global variables
dict_FileHashed = {}
l_DuplicateFiles = []
msg_ErrorMessage = ""

# Created by Adam Jacobs. 12/12/2018
# Takes a file path as a string and returns the hash value of the file.
def hashFile(filePath):
    global dict_FileHashed

    with open(filePath, 'rb') as fileName:
        buffer = fileName.read()

    strBuffer = str(buffer)
    strBuffer = strBuffer.encode()
    strBuffer = hashlib.md5(strBuffer)
    strBuffer = strBuffer.digest()

    return str(strBuffer)

# Created by Adam Jacobs. 14/12/2018
# Takes a file path as a parameter and adds the hash value to the global list l_FileHashes
def recordFileHash(par_CurrentFile):
    global msg_ErrorMessage
    global dict_FileHashed

    #try:
    dict_FileHashed.update({par_CurrentFile:hashFile(par_CurrentFile)})
    dict_FileHashed[par_CurrentFile] = hashFile(par_CurrentFile)
    msg_ErrorMessage = ""
    #except:
        #msg_ErrorMessage = "Unable to compare file path " + par_CurrentFile

# Created by Adam Jacobs. 14/12/2018
# Detect duplicates from the dict_FileHashed dictionary and add the duplicates to the l_DuplicateFiles list object.
def detectDuplicates():
    global l_DuplicateFiles

    #Create a duplicate dictionary
    dict_FileDuplicate = dict_FileHashed

    # Get the files from the dictionary where the file hash value exists more than once.
    for fileName, fileHashValue in dict_FileHashed.items():
        for fileNameDupe, fileHashDupe in dict_FileDuplicate.items():
            if fileHashValue == fileHashDupe and fileName != fileNameDupe:
                l_DuplicateFiles.append(fileName + " is a duplicate of " + fileNameDupe)

# Created by Adam Jacobs. 05/01/2018
# Ping the server requested and return the command (0 if online)
def pingServer(serverHost):
    # Ping the server. This function is capable of handling both windows and unix systems

    # If the system is a window system then use -n, else use -c.
    # This is the count of how many requests to send, This will be 1 in the command.
    param = '-n' if system().lower() == 'windows' else '-c'

    # Generate the command field using the param generated above
    command = ['ping', param, '1', serverHost]

    return call(command)


# Created by Will Brown. 14/1/2018
# Detect duplicates from the dict_FileHashed dictionary and add the duplicates to the l_DuplicateFiles list object.
def checkFile(txtToSearch):
    # Generate a command to find the string needed.
    windowsSearch = "findStr /s /i /n /m /M /p /P /C:" + txtToSearch + " /D:" + str(Path.home()).replace("/", "//") + " *"
    unixSearch = "grep -r --include='*.*' " + txtToSearch

    # Use either the windowsSearch or the unixSearch command string
    command = windowsSearch if system().lower() == 'windows' else unixSearch

    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    return str(output.communicate())
