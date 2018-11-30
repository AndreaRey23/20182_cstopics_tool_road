import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QWidget, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QPixmap, QImage, QRegExpValidator
import numpy as np
import cv2

import os


class mainwindow(QMainWindow):
	def __init__(self):
		super(mainwindow,self).__init__(None)
		loadUi('./Interface/mainwindow.ui',self)
		#self.cap = cv2.VideoCapture(0)
		#self.Peaje.clicked.connect(self.capture)

	#def capture(self):
		#ret, frame = self.cap.read()
		#self.cap.release()
		#self.show_capture_peaje(frame,frame)
		#self.show_capture_placa(frame,frame)
		#self.show_capture_placar(frame)
		#self.write_txt("56dfdsf","56465")

	def show_capture_peaje(self, img_rgb, window=1):
		img = cv2.resize(img_rgb,(int(360),int(280)))
		frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.Image_peaje.setPixmap(pix)

	def show_capture_placa(self, img_d, window=1):
		img = cv2.resize(img_d,(int(360),int(280)))
		frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.Image_placa.setPixmap(pix)

	def show_capture_placar(self, img_placa, window=1):
		img = cv2.resize(img_placa,(int(180),int(90)))
		frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.Placa_Recortada.setPixmap(pix)

	def write_txtCiudad(self,msg_Ciudad="Error"):
		self.Ciudad.setText(msg_Ciudad)
	def write_txtPlaca(self,msg_Placa="Error"):
		self.Placa.setText(msg_Placa)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	ui = mainwindow()
	ui.setWindowTitle('Detector Placas')
	ui.show()
	sys.exit(app.exec_())
