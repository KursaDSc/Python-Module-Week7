from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMovie
import os

class LoadingSpinner(QLabel):
    def __init__(self, parent=None, gif_path=None):
        super().__init__(parent)
        if gif_path is None:
            gif_path = os.path.join(os.path.dirname(__file__), '..', 'resorces', '1495.gif')
            gif_path = os.path.abspath(gif_path)
        self.setFixedSize(128, 128)
        self.setStyleSheet("background: transparent;")
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)
        self.hide()

    def center_in_parent(self):
        """Centers the spinner in its parent widget."""
        if self.parent():
            parent_width = self.parent().width()
            parent_height = self.parent().height()
            spinner_width = self.width()
            spinner_height = self.height()
            x = (parent_width - spinner_width) // 2
            y = (parent_height - spinner_height) // 2
            self.move(x, y)

    def start(self):
        self.center_in_parent()
        self.show()
        self.movie.start()

    def stop(self):
        self.movie.stop()
        self.hide()