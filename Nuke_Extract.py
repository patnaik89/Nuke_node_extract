# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dillip.patnaik/Documents/qt/Nuke_Node.ui'
#
# Created: Sat Jul 24 18:09:26 2021
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from PySide.QtGui import QFileDialog
import in_nuke_utils
import os
import shutil
#import nuke
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Nuke(object):
    def setupUi(self, Nuke):
        Nuke.setObjectName(_fromUtf8("Nuke"))
        Nuke.resize(507, 300)
        self.frame = QtGui.QFrame(Nuke)
        self.frame.setGeometry(QtCore.QRect(-10, 0, 521, 301))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.choose_dir_linedit = QtGui.QLineEdit(self.frame)
        self.choose_dir_linedit.setGeometry(QtCore.QRect(160, 120, 260, 32))
        self.choose_dir_linedit.setObjectName(_fromUtf8("choose_dir_linedit"))
        self.project_name_lineedit = QtGui.QLineEdit(self.frame)
        self.project_name_lineedit.setGeometry(QtCore.QRect(160, 75, 331, 32))
        self.project_name_lineedit.setObjectName(_fromUtf8("project_name_lineedit"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(40, 80, 91, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(30, 130, 130, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.extact_button = QtGui.QPushButton(self.frame)
        self.extact_button.setGeometry(QtCore.QRect(300, 230, 90, 28))
        self.extact_button.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.extact_button.setStyleSheet(_fromUtf8("background-color: rgb(176, 176, 176);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 11pt \"Cantarell\";"))
        self.extact_button.setObjectName(_fromUtf8("extact_button"))
        self.cancel_button = QtGui.QPushButton(self.frame)
        self.cancel_button.setGeometry(QtCore.QRect(400, 230, 90, 28))
        self.cancel_button.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.cancel_button.setStyleSheet(_fromUtf8("background-color: rgb(176, 176, 176);\n"
"color: rgb(0, 0, 0);\n"
"font: 75 11pt \"Cantarell\";"))
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.selection_comboBox = QtGui.QComboBox(self.frame)
        self.selection_comboBox.setGeometry(QtCore.QRect(30, 180, 461, 30))
        self.selection_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.selection_comboBox.setObjectName(_fromUtf8("selection_comboBox"))
        self.browse_button = QtGui.QPushButton(self.frame)
        self.browse_button.setGeometry(QtCore.QRect(430, 120, 61, 28))
        self.browse_button.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.browse_button.setStyleSheet(_fromUtf8("background-color: rgb(176, 176, 176);\n"
"color: rgb(0, 0, 0);"))
        self.browse_button.setObjectName(_fromUtf8("browse_button"))
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(30, 30, 481, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.browse_button.clicked.connect(self.openFileDialog)
        self.selection_comboBox.addItems(['ALL_NODES', 'SELECT_NODE'])
        # self.selection_comboBox.currentIndexChanged.connect(self.nodeType)
        self.extact_button.clicked.connect(self.nodeType)
        self.cancel_button.clicked.connect(self.clearFields)



        self.retranslateUi(Nuke)
        QtCore.QMetaObject.connectSlotsByName(Nuke)

    def nodeType(self):
        selection_type = self.selection_comboBox.currentText()
        print selection_type
        if selection_type == 'ALL_NODES':
            doNodes = nuke.allNodes("Read")
            nuke.selectAll()
            nuke.nodeCopy(outDir + inScriptName + '.nk')
            return inScriptName, outDir, doNodes
        else:
            if nuke.selectedNodes() == []:
                nuke.message('Please select the nodes you want to extract')
                return
            doNodes = nuke.selectedNodes("Read")
            nuke.nodeCopy(outDir + inScriptName + '.nk')
            return inScriptName, outDir, doNodes

        os.chdir(outDir)
        # Checking existing folder
        if not os.path.exists('Footage'):
            os.mkdir('Footage')

        # New script name
        newScriptName = (outDir + inScriptName + '.nk')

        # Progress Bar
        progTask = nuke.ProgressTask("Extracting...")

        # Scan Loop the extracted nodes
        for n in doNodes:
            # Get the file path and split it
            fullPath = n.knob('file').getValue()
            # Split Path
            splitPath = fullPath.split('/')
            # Get the file folder directory
            mediaPath = splitPath[-2]
            # Get the file name
            fileName = splitPath[-1]
            # Get the format
            fileFormat = fileName[-4:]

            # print mediaPath
            # print fileName
            # print fileFormat

            # Create a common path for project files (no file name)
            commonDir = fullPath[0:fullPath.find(fileName)]

            # For sequence of images
            print fileName
            # If this statement is FALSE
            if not fileName.find('%') == -1:
                print fileName + ' is a sequence'
                # Find padding for the sequence
                padding = int(fileName[fileName.find('%') + 2:fileName.find('%') + 3])

                # Get the start and end frame of the sequence
                startFrame = int(n.knob('first').getValue())
                endFrame = int(n.knob('last').getValue())

                # Get the sequence name with dot/dash mark also
                seName = fileName[0:fileName.find('%') - 1]
                seNameD = fileName[0:fileName.find('%')]
                # print seName, seNameD
                # print 'start', startFrame, 'end', endFrame

                # Change the Footage Directory
                os.chdir(outDir + 'Footage')

                # Creating a folder for image sequences
                if not os.path.exists(seName):
                    os.mkdir(seName)
                # Go to this dir
                os.chdir(seName)

                # Start Extracting sequence images
                for f in range(startFrame, endFrame + 1):  # make sure endFrame is int
                    # If progress bar is cancelled
                    if progTask.isCancelled():
                        nuke.message("Media files might not be complete")
                        break;
                    percent = int((f / endFrame) * 100)
                    # Set progress
                    progTask.setProgress(percent)

                    # Locate the current file location
                    curLoc = commonDir + seNameD + str(f).zfill(padding) + fileFormat

                    # new file in new destination/location
                    newLoc = seNameD + str(f).zfill(padding) + fileFormat

                    # Copy file from current to new location
                    shutil.copyfile(curLoc, newLoc)

                    # Show extracting process
                    progTask.setMessage("Copying: " + seNameD + str(f).zfill(padding) + fileFormat)

            # Else is a still image
            else:
                print fileName + ' is a still image'
                os.chdir(outDir + 'Footage')
                shutil.copyfile(fullPath, fileName)


    def clearFields(self):
        self.choose_dir_linedit.clear()
        self.project_name_lineedit.clear()
        # self.selection_comboBox.

    def openFileDialog(self):
        try:
            # browse_file_path = r'/home/dillip.patnaik/Documents/qt'
            directory_path = QFileDialog.getExistingDirectory()
            self.choose_dir_linedit.setText(directory_path)


            # fname, _ = QFileDialog.getOpenFileName(self, 'Choose file', r'/ASEX/share/dillip.patnaik/', "Files (*.jpg, *.tif)")
            print fname
        except Exception as e:
            print "open dialog errror {}".format(e)

    def retranslateUi(self, Nuke):
        Nuke.setWindowTitle(_translate("Nuke", "Node Reading", None))
        self.label_2.setText(_translate("Nuke", "<html><head/><body><p><span style=\" font-weight:600;\">Project Name</span></p></body></html>", None))
        self.label_3.setText(_translate("Nuke", "<html><head/><body><p><span style=\" font-weight:600;\">Choose  Project Dir</span></p></body></html>", None))
        self.extact_button.setText(_translate("Nuke", "Extract", None))
        self.cancel_button.setText(_translate("Nuke", "Cancel", None))
        self.browse_button.setText(_translate("Nuke", "Browser", None))
        self.label_4.setText(_translate("Nuke", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Read Node</span></p></body></html>", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Nuke = QtGui.QDialog()
    ui = Ui_Nuke()
    ui.setupUi(Nuke)
    Nuke.show()
    sys.exit(app.exec_())
