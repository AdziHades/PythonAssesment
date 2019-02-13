# Organise imports
import hashlib
from platform import system
from subprocess import call

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

    print("Buffer text: " + str(filePath) + ": " + str(strBuffer))
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

    print(dict_FileHashed, dict_FileDuplicate, sep="\n")

    # Get the files from the dictionary where the file hash value exists more than once.
    for fileName, fileHashValue in dict_FileHashed.items():
        for fileNameDupe, fileHashDupe in dict_FileDuplicate.items():
            if fileHashValue == fileHashDupe and fileName != fileNameDupe:
                l_DuplicateFiles.append(fileName + " is a duplicate of " + fileNameDupe)

def pingServer(serverHost):
    # Ping the server. This function is capable of handling both windows and unix systems
    param = '-n' if system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', serverHost]

    return call(command)

def checkFile(self):
    textSearchString = ui.textbox.text
    fileToSearch = self.ui.txtDirector.text

#Get the text to search for
for files in os.listdir(fileToSearch):
#Read Text and compare
    readText = fileToSearch.read()
if str(textSearchString) == str(fileToSearch):
    print "Match Found"
else:
    print "No Match Found"





#Loop through each directory
         #Loop through each file
                #Check if file contains the text
                #If yes, add it to a list

#Return the list