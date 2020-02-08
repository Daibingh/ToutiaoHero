from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui_roi import Ui_ROI
import sys
import numpy as np
# import cv2


class ROI(QWidget,Ui_ROI):
	"""docstring for Test"""
	def __init__(self, parent=None):
		super(ROI, self).__init__(parent)
		self.setupUi(self)
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.roi = None

	def updateMask(self):
		frameRect = self.frameGeometry()

		geometry = self.geometry()
		dx = frameRect.x() - geometry.x()
		dy = frameRect.y() - geometry.y()
		dw = frameRect.width() - geometry.width()
		dh = frameRect.height() - geometry.height()

		widgetGeometry = self.widget.geometry()
		widgetGeometry.moveTopLeft(self.widget.mapToGlobal(QPoint(0, 0)))  # 全局坐标
		globalGeometry = widgetGeometry.translated(0,0)
		self.roi = [globalGeometry.x(),
					globalGeometry.y(),
					globalGeometry.width(),
					globalGeometry.height()
					]

		geometry.moveTopLeft(QPoint(0, 0))
		geometry.adjust(dx, dy, dw, dh)

		widgetGeometry = self.widget.geometry()

		region = QRegion(geometry)
		region -= QRegion(widgetGeometry)
		self.setMask(region)

		self.textBrowser.setText("{},{},{},{}".format(
			str(globalGeometry.x()),
			str(globalGeometry.y()),
			str(globalGeometry.width()),
			str(globalGeometry.height())
			))

	def paintEvent(self, event):
		super().paintEvent(event)
		self.updateMask()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.updateMask()

	def moveEvent(self, event):
		super().moveEvent(event)
		self.updateMask() 

	def mousePressEvent(self, event):
		if event.button()==Qt.LeftButton:
			self.m_flag=True
			self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
			event.accept()
			self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
	def mouseMoveEvent(self, QMouseEvent):
		if Qt.LeftButton and self.m_flag:  
			self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_flag=False
		self.setCursor(QCursor(Qt.ArrowCursor))

	def screenshot(self):
		screen = QGuiApplication.primaryScreen()
		pixmap = screen.grabWindow(QApplication.desktop().winId(), *self.roi)
		channels_count = 4
		image = pixmap.toImage()
		s = image.bits().asstring(self.roi[2] * self.roi[3] * channels_count)
		arr = np.frombuffer(s, dtype=np.uint8).reshape((self.roi[3], self.roi[2], channels_count))
		return arr[:,:,:3]

	# def closeEvent(self, event):
	# 	super().closeEvent(event)
	# 	img = self.screenshot()
	# 	# print(img)
	# 	cv2.imwrite('test.png', img)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = ROI()
	window.show()
	print(window.frameGeometry())
	print(window.geometry())
	print(window.widget.geometry())
	app.exec_()
