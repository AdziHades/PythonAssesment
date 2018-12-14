#Organise imports
import hashlib
import easygui
import collections

class networkToolkitFunctions:

	dict_FileHashed = {["File Path" : "File Hash"]}
	l_DuplicateFiles = []
	msg_ErrorMessage = ""
	

    #Created by Adam Jacobs. 12/12/2018
    #Takes a file path as a string and returns the hash value of the file.
    def hashFile(filePath):
        hashLib = hashlib.md5()

        with open(fileName, 'rb') as filePath:
            buffer = filePath.read();
            hash.update(buffer)

        return hashLib.hexdigest()

    #Created by Adam Jacobs. 14/12/2018
	#Takes a file path as a parameter and adds the hash value to the global list l_FileHashes
    def recordFileHash(par_CurrentFile):
		global l_FileHashes
		global msg_ErrorMessage
	
		try:
			l_FileHashes.append(hashFile(par_CurrentFile))
			dict_FileHashed[par_CurrentFile] = hashFile(par_CurrentFile)
		except:
			msg_ErrorMessage = "Unable to compare file path", par_CurrentFile);
		
	#Created by Adam Jacobs. 14/12/2018
	#Detect duplicates from the dict_FileHashed dictionary and add the duplicates to the l_DuplicateFiles list object.
	def detectDuplicates():
		global l_DuplicateFiles
		
		#Get the values from the dictionary.
		fileValues = dict_FileHashed.values()
		
		#Get the files from the dictionary where the file hash value exists more than once.
		for fileName, fileHashValue in dict_FileHashed.items():
			if fileValues.count(fileHashValue) > 1:
				l_DuplicateFiles.append(fileName)
