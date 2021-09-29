from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
Ui_MainWindow, _ = uic.loadUiType('mainwindow.ui')
from threading import Thread
import sys
#
import apkmaker


class TextEditStream:
	def __init__(self, text_edit):
		self.textEdit = text_edit

	def write(self, text):
		self.textEdit.append(text)
		self.textEdit.verticalScrollBar().setValue(self.textEdit.verticalScrollBar().maximum())

	def flush(self):
		pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	showDialog_pyqtSignal = QtCore.pyqtSignal(str, str, str, str)

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.connect_handlers()
		self.custom_stream = TextEditStream(self.log_textEdit)
		sys.stdout = self.custom_stream
		sys.stderr = self.custom_stream

	def connect_handlers(self):
		self.generateApk_pushButton.clicked.connect(self.generateApk_pushButton__onClick)
		self.browseProjectFolder_pushButton.clicked.connect(self.browseProjectFolder_pushButton__onClick)
		self.browseApkDestinationFolder_pushButton.clicked.connect(self.browseApkDestinationFolder_pushButton__onClick)
		self.browseKeystoreFile_pushButton.clicked.connect(self.browseKeystoreFile_pushButton__onClick)
		self.showDialog_pyqtSignal.connect(self.showDialog)

	def generateApk_pushButton__onClick(self):
		self.generateApk_pushButton.setEnabled(False)
		self.bot_starting_thread = Thread(target=self.__build_apk)
		self.bot_starting_thread.start()

	def browseProjectFolder_pushButton__onClick(self):
		folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Android Project Folder')
		self.projectFolder_lineEdit.setText(folderpath)

	def browseApkDestinationFolder_pushButton__onClick(self):
		folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Destination Folder for Apk')
		self.destinationFolder_lineEdit.setText(folderpath)

	def browseKeystoreFile_pushButton__onClick(self):
		file_path = QtWidgets.QFileDialog.getOpenFileName(self,
															'Select Keystore File',
															'.',
															'Keystore (*.jks *.keystore)')[0]
		self.keystoreFile_lineEdit.setText(file_path)

	def __build_apk(self):
		self.process = QtCore.QProcess(self)
		self.process.readyReadStandardOutput.connect(lambda: print(str(self.process.readAllStandardOutput())))
		self.process.readyReadStandardError.connect(lambda: print(str(self.process.readAllStandardError())))
		self.process.started.connect(lambda: print('- Started!'))
		self.process.finished.connect(lambda: print('- Finished!'))
		try:
			apkmaker.make_apk(project_path=self.projectFolder_lineEdit.text(),
								apk_destination_path=self.destinationFolder_lineEdit.text(),
								keystore_path=self.keystoreFile_lineEdit.text(),
								key_alias=self.keyAlias_lineEdit.text(),
								key_password=self.keyPassword_lineEdit.text(),
								store_password=self.storePassword_lineEdit.text())
			self.showDialog_pyqtSignal.emit('Build completed!', 'Apk generated successfully!', '', '')
		except Exception as e:
			print(e)
			self.showDialog_pyqtSignal.emit('Something went wrong!',
											'An error occured while building Apk.',
											'', str(e))
		self.generateApk_pushButton.setEnabled(True)

	def showDialog(self, title='', text='', info_text='', detail_text=''):
		msg = QMessageBox(self)
		#msg = QMessageBox()
		msg.setWindowTitle(title)
		msg.setText(text)
		msg.setInformativeText(info_text)
		msg.setDetailedText(detail_text)
		msg.setStandardButtons(QMessageBox.Ok)
		retval = msg.exec_()



######
######
######

def main():
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()
