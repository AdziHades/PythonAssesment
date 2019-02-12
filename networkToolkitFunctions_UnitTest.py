#-------------------------------------------------------------------------------
# Name:        networkToolkitFunctions_UnitTests
# Purpose:     Unit test file for networkToolkitFunctions class
#-------------------------------------------------------------------------------

#Add test cases for each function of the networkToolkitFunctions
import networkToolkitFunctions as fn

#Setup
file = ""
masterFileHash = ""

#Assert and test
if fn.hashFile(file) == masterFileHash:
    print("hashFile function working correctly")
else:
    print("hashFile function failed.", fn.hashFile(file), "and", masterFileHash, "comparison")