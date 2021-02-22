# PyQt5 Video player
#!/usr/bin/env python

from PyQt5.QtCore import QDir, Qt, QUrl,QRect, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,QProgressBar,QFrame)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys,os

class VideoWindow(QMainWindow):
    closeSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)

    def setupUi(self,window):
        self.window = window
        self.window.setFixedSize(784,441)
        #self.window.setFixedSize(884,542)
        self.window.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.WA_TranslucentBackground)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        widget = QWidget(self.window)

        widget.setObjectName('Custom_Widget')
        widget.setStyleSheet("""
        #Custom_Widget {
            background: #002025;
            border-radius: 20px;
            opacity: 100;
            border: 2px solid #ff2025;
        }
        """)

        videoWidget = QVideoWidget(widget)
        videoWidget.setGeometry(QRect(0,0,784, 441))

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(os.getcwd() + "\\logo-anim.avi")))
        self.mediaPlayer.play()
        self.mediaPlayer.stateChanged.connect(lambda x: self.closeSignal.emit(x))
        #self.mediaPlayer.stateChanged.connect(lambda x: sys.exit())
        
        self.window.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QMainWindow()
    player = VideoWindow()
    player.setFixedSize(784, 442)
    player.setupUi(w)
    w.show()
    sys.exit(app.exec_())