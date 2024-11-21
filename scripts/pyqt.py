import sys

import chess
import chess.engine

import json
from play.newplay import New_play

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog
from PyQt6.QtWidgets import QInputDialog

sys.path.append("..")
imagemw = 'media/death-note-l-and-light-playing-chess-ft7rtfi086yvefyc.jpg'
imageplay = 'media/sakura.webp'
font_size = '17px'
font = 'Comic Sans MS'
vsrobot = False

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global imagemw, font_size, vsrobot
        if vsrobot:
            self.engine.quit()
        self.setWindowTitle('Главное меню')
        layout = QVBoxLayout()
        button_playnew = QPushButton('Новая партия')
        button_playold = QPushButton('Старая партия')
        button_settings = QPushButton('Настройки')
        button_playnew.setMaximumSize(300, 150)
        button_playold.setMaximumSize(300, 150)
        button_settings.setMaximumSize(300, 150)
        button_playnew.setMinimumSize(100, 50)
        button_playold.setMinimumSize(100, 50)
        button_settings.setMinimumSize(100, 50)
        button_settings.setStyleSheet(f"""
                font-family: {font};
                font-size: {font_size};
        """)
        button_playold.setStyleSheet(f"""
                font-family: {font};
                font-size: {font_size};
        """)
        button_playnew.setStyleSheet(f"""
                font-family: {font};
                font-size: {font_size};
        """)
        layout.addWidget(button_playnew)
        layout.addWidget(button_playold)
        layout.addWidget(button_settings)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget = QWidget()
        central_widget.setStyleSheet(f'''
            background-image: url({imagemw});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        ''')
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        button_playnew.clicked.connect(self.new_play)
        button_playold.clicked.connect(self.old_play)
        button_settings.clicked.connect(self.settings)

    def new_play(self):
        global vsrobot
        opponent, ok_pressed = QInputDialog.getItem(
            self, "Выбор противника", "Оппонент",
            ('Робот', 'Человек'), 1, False)
        if ok_pressed:
            if opponent == 'Человек':
                mw = New_play(board=chess.Board(), mw=self)
                mw.show()
                self.hide()
            else:
                mw = New_play(board=chess.Board(), vsrobot=True, mw=self)
                # self.engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-sse41-popcnt.exe")
                vsrobot = True
                mw.show()
                self.hide()
    def old_play(self):
        self.mw = Old_play()
        self.mw.show()
        self.close()

    def settings(self):
        self.mw = Settings()
        self.mw.show()
        self.close()

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

class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global font_size, font
        self.setWindowTitle('Настройки')
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(500, 500)
        # тут будут настройки, описанные в README
        layout = QVBoxLayout()
        central_widget = QWidget()
        image_path = 'settings.jpg'
        central_widget.setStyleSheet(f'''
            background-image: url({image_path});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        ''')
        central_widget.lower()
        button_chooseimagemw = QPushButton('Установить изображение на задний фон главного экрана')
        button_chooseimageplay = QPushButton('Установить изображение на задний фон партии')
        button_font = QPushButton('Изменить шрифт')
        button_font_size = QPushButton('Изменить размер шрифта')
        button_chooseimagemw.setMinimumSize(100, 50)
        button_chooseimageplay.setMinimumSize(100, 50)
        button_font_size.setMinimumSize(100, 50)
        button_font.setMinimumSize(100, 50)
        button_font_size.setStyleSheet(f"""
            color: white;
            font-family: {font};
            font-size: {font_size};
        """)
        button_font.setStyleSheet(f"""
            color: white;
            font-family: {font};
            font-size: {font_size};
        """)
        button_chooseimageplay.setStyleSheet(f"""
            color: white;
            font-family: {font};
            font-size: {font_size};
        """)
        button_chooseimagemw.setStyleSheet(f"""
            color: white;
            font-family: {font};
            font-size: {font_size};
        """)
        layout.addWidget(button_chooseimagemw)
        layout.addWidget(button_chooseimageplay)
        layout.addWidget(button_font)
        layout.addWidget(button_font_size)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        button_chooseimagemw.clicked.connect(self.chooseimagemw)
        button_chooseimageplay.clicked.connect(self.chooseimageplay)
        button_font.clicked.connect(self.font_)
        button_font_size.clicked.connect(self.font_size)
        self.button = QPushButton('BACK', self)
        self.button.clicked.connect(self.back)
        self.button.move(0, 0)
        self.button.resize(100, 50)
        self.button.setStyleSheet(f"""
                                font-family: {font};
                                font-size: {font_size};
                                color: red;
                                background-color: black;
                                """)

    def back(self):
        self.mw = MainWindow()
        self.mw.showMaximized()
        self.close()

    def chooseimagemw(self):
        global imagemw
        imagemw = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.png)')[0]

    def chooseimageplay(self):
        global imageplay
        imageplay = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '', 'Картинка (*.jpg);;Картинка (*.png)')[0]

    def font_(self):
        global font
        name, ok_pressed = QInputDialog.getText(self, "Изменение шрифта",
                                                "Введите шрифт")
        if ok_pressed:
            font = name
            self.back()

    def font_size(self):
        global font_size
        size, ok_pressed = QInputDialog.getInt(self, 'Изменение размера шрифта', 'Введите размер шрифта в px')
        if ok_pressed:
            if size <= 17:
                font_size = str(size) + 'px'
                self.back()
            else:
                font_size = '17px'
                self.back()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.excepthook = except_hook
    sys.exit(app.exec())
