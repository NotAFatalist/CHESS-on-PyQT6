import sys

import chess
import chess.engine

import json

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog
from PyQt6.QtWidgets import QInputDialog


class Old_play(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        def load_board_from_json(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                fen = data["fen"]
                board = chess.Board(fen)
                return board

        self.setWindowTitle('Выбор старой игры')
        self.setGeometry(100, 100, 600, 600)
        fname = QFileDialog.getOpenFileName(self, 'Выбрать партию', '')[0]
        mw = New_play(board=load_board_from_json(fname))
        mw.show()
        self.close()
