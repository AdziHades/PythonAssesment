#-------------------------------------------------------------------------------
# Name:        Network Maintenance Toolkit.
# Purpose:     Class file containing the functions used in the Network Maintenance Toolkit.
# Author(s):   Adam Jacobs, Ben Walton & Will Brown.
# Created:     11/12/2018.

#-------------------------------------------------------------------------------

#Organise imports
import hashlib
import easygui

class networkToolkitFunctions:
    #Created by Adam Jacobs. 12/12/2018
    #Takes a file path as a string and returns the hash value of the file.
    def hashFile(filePath):
        hashLib = hashlib.md5()

        with open(fileName, 'rb') as filePath:
            buffer = filePath.read();
            hash.update(buffer)

        return hashLib.hexdigest()

    #Create by **Add author information and date
    #**Add function description
    def compareFile(currentFile, compareList):
        print("Throw new nonImplementedMethod exception")

