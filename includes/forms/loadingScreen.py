from PyQt5.QtWidgets import QWidget,QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie
from appIcons import Icons


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(70,70)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        
        self.label_animation = QLabel(self)

        self.movie = QMovie(Icons["Loading"])
        self.label_animation.setMovie(self.movie)

        timer = QTimer(self)
        self.startAnimation()
        timer.singleShot(1000, self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()

