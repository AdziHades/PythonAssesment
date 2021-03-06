from PyQt5 import QtWidgets, QtCore, QtGui
from mainWindowUIFinal import Ui_mainWindow  # importing our generated file
import networkToolkitFunctions
import os
import time
import sys
import datetime

# Default variable parameters. These are used to allow main thread GUI updates from
# worker processes
monitorServer = False;
searchFiles = False;
serverToMonitor = ""
searchText = ""
mainThreadUI = ""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Define mainThreadUI as global variable
        global mainThreadUI

        # Setup and open window
        super(MainWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Connect event handler to the buttons on screen
        self.ui.btnFindText.clicked.connect(self.btnFindTextClicked)
        self.ui.btnDirectory.clicked.connect(self.btnCleanDirectoryClicked)
        self.ui.btnMonitorServer.clicked.connect(self.btnMonitorServerClicked)

        # Set a mainThreadUI variable so that it can be used in different threads.
        if mainThreadUI == "":
            mainThreadUI = self

        # First update of the time upon load
        self.ui.label.setText(datetime.datetime.now().strftime('%H:%M'))

        # Define the update time thread and start it.
        self.UpdateTimeThread = UpdateTime()
        self.UpdateTimeThread.start()

        # Define the worker threads
        self.MonitorServerThread = MonitorServer()
        self.SearchFilesThread = FileSearch()

    def close(self):
        self.UpdateTimeThread.terminate()
        self.SearchFilesThread.terminate()
        self.MonitorServerThread.terminate()

    def updateTimeGUI(self):
        # Update the time on the top right of the GUI
        mainThreadUI.ui.label.setText(datetime.datetime.now().strftime('%H:%M'))

    def updateServerMonitorText(self, boolActive):
        # Main thread handler, accessed from the MonitorServer class thread
        if boolActive:
            mainThreadUI.ui.txtServerMonitorResults.append(str(datetime.datetime.now()) + "     Server is online")
        else:
            mainThreadUI.ui.txtServerMonitorResults.append(str(datetime.datetime.now()) + "     Server is offline")

        # Keep cursor at the bottom of the textbox.
        mainThreadUI.ui.txtServerMonitorResults.moveCursor(QtGui.QTextCursor.End)

    def updateFileSearchResults(self, txtResults):
        global searchFiles

        # Main thread handler, access by the SearchFile class thread
        textResultsMainThread = txtResults.split("\\r\\n")
        textResultsFormatted = ""

        iterationCounter = 0
        while(iterationCounter < len(textResultsMainThread)):
            textResultsFormatted += textResultsMainThread[iterationCounter] + "\n"
            iterationCounter += 1

        mainThreadUI.ui.btnFindText.setText("Search Files")

        # Only populate the text file if the search files boolean is true.
        if searchFiles:
            mainThreadUI.ui.txtFindResults.append(textResultsFormatted)

        searchFiles = False


    # Server monitor clicked event
    def btnMonitorServerClicked(self):
        # Define the below variables as global
        global monitorServer
        global serverToMonitor

        # Set the server to monitor globally to use in worker threads
        serverToMonitor = self.ui.txtServerToMonitor.text()

        if monitorServer:
            monitorServer = False
            self.ui.btnMonitorServer.setText("Monitor Server")
            self.MonitorServerThread.terminate()
        else:
            monitorServer = True
            self.ui.txtServerMonitorResults.setText("")
            self.ui.btnMonitorServer.setText("Stop Monitoring")
            self.MonitorServerThread.start()

    # Find text clicked event
    def btnFindTextClicked(self):
        global searchFiles
        global searchText

        searchText = self.ui.txtTextToFind.text()

        if searchFiles:
            searchFiles = False
            self.ui.btnFindText.setText("Search Files")
            self.ui.txtFindResults.setText("Cancelled")
            self.SearchFilesThread.terminate()
        else:
            searchFiles = True
            self.ui.txtFindResults.setText("")
            self.ui.btnFindText.setText("Stop Search")
            self.SearchFilesThread.start()

    # Clean directory button clicked
    def btnCleanDirectoryClicked(self):
        # loop through each file and pass into the hashFile function from the networkToolkitFunctions class
        iterationNumber = 0

        if os.path.exists(self.ui.txtDirectory.text()):
            pass
        else:
            self.ui.txtDirectoryResults.setText("That directory could not be found. Please check the directory and try again")
            return

        # Set the directory to run
        txtDirectory = self.ui.txtDirectory.text()

        # Create list of files in the directory.
        # Bug in Pycharm which forced me to create the list separately to populating it
        listFiles = []
        listFiles = os.listdir(txtDirectory)

        # Get number of files in the directory
        maxIterationNumber = len(listFiles)

        # Output a message to screen
        self.ui.txtDirectoryResults.append("Checking " + str(maxIterationNumber) + " files.\n")

        # Iteration through the files using the networkToolkitFunctions class.
        while iterationNumber < maxIterationNumber:
            networkToolkitFunctions.recordFileHash(txtDirectory + "\\" + listFiles[iterationNumber])
            if networkToolkitFunctions.msg_ErrorMessage != "":
                self.ui.txtDirectoryResults.append(networkToolkitFunctions.msg_ErrorMessage)
            iterationNumber += 1

        # Call the detect duplicates function from the networkToolkitFunctions class.
        # This will store the duplicates in the l_DuplicateFiles object.
        networkToolkitFunctions.detectDuplicates()

        # Get the list of duplicates from the networkToolkitFunctions class
        if len(networkToolkitFunctions.l_DuplicateFiles) == 0:
            self.ui.txtDirectoryResults.append("\nNo duplicate files detected")
        else:
            self.ui.txtDirectoryResults.append("\n".join(networkToolkitFunctions.l_DuplicateFiles))


# Separate class of MonitorServer which utilises a worker thread to keep the GUI active.
class MonitorServer(QtCore.QThread):

    def __init__(self):
        QtCore.QThread.__init__(self, mainThreadUI)

    def __del__(self):
        self.wait()

    def run(self):
        global monitorServer
        # Create an instanced version of the MainWindow class to use in this class
        mainWindow = MainWindow()

        # Use while true to keep monitoring the monitorServer boolean for change
        while True:
            # Check if the monitorServer boolean is true.
            # This is controlled by the "Monitor Server"/"Stop Monitoring" button on the GUI
            while monitorServer:
                # Return of 0 means a response was received. Server is active.
                # Pass a boolean value to the updateServerMonitorText method from the mainWindow class.
                if networkToolkitFunctions.pingServer(serverToMonitor) == 0:
                    mainWindow.updateServerMonitorText(True)
                else:
                    mainWindow.updateServerMonitorText(False)

                # Sleep for 1 second and re-run.
                time.sleep(1)


class FileSearch(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self, mainThreadUI)

    def __del__(self):
        self.wait()

    def run(self):
        global searchFiles

        # Create an instanced version of the MainWindow class to use in this class
        mainWindow = MainWindow()

        # Use while true to keep monitoring the searchFiles boolean for change
        while True:
            # Check if the searchFiles boolean is true.
            # This is controlled by the Search Files button on the GUI and is set to False at the end of the function
            # inside the updateFileSearchResults function
            while searchFiles:
                stringFunction = networkToolkitFunctions.checkFile(searchText)
                mainWindow.updateFileSearchResults(stringFunction)


class UpdateTime(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self, mainThreadUI)

    def __del__(self):
        self.wait()

    def run(self):
        # Create an instanced version of the MainWindow class to use in this class
        mainWindow = MainWindow()

        # Use while true to keep updating the time
        while True:
            mainWindow.updateTimeGUI()
            time.sleep(1)

def main():
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

