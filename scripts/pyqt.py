import sys

import chess

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog
from PyQt6.QtWidgets import QInputDialog


imagemw = 'media/death-note-l-and-light-playing-chess-ft7rtfi086yvefyc.jpg'
imageplay = 'media/sakura.webp'
font_size = '17px'
font = 'Comic Sans MS'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global imagemw, font_size
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
        opponent, ok_pressed = QInputDialog.getItem(
            self, "Выбор противника", "Оппонент",
            ('Робот', 'Человек'), 1, False)
        if ok_pressed:
            if opponent == 'Человек':
                self.mw = New_play()
                self.mw.show()
                self.close()
            else:
                self.mw = New_play(vsrobot=True)
                self.mw.show()
                self.close()
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
        global font_size, font
        self.setWindowTitle('Выбор старой игры')
        self.setGeometry(100, 100, 600, 600)
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')
        # тут будет расшифровка cvv файла в доску, но позже
        self.button = QPushButton('BACK', self)
        self.button.clicked.connect(self.back)
        self.button.move(0, 0)
        self.button.resize(100, 50)
        self.button.setStyleSheet(f"""
                color: red;
                background-color: black;
                font-family: {font};
                font-size: {font_size};
            """)

    def back(self):
        self.mw = MainWindow()
        self.mw.showMaximized()
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
        image_path = 'media/settings.webp'
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


class New_play(QMainWindow):
    def __init__(self, vsrobot=True):
        super().__init__()
        self.initUI()
        self.vsrobot = vsrobot

    def initUI(self):
        global imageplay, font, font_size
        self.setWindowTitle('Шахматная доска')
        self.setGeometry(100, 100, 600, 600)
        self.background_widget = QWidget(self)
        self.background_widget.setStyleSheet(f'''
            background-image: url({imageplay});
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        ''')
        self.chess_board = ChessBoard()
        layout = QVBoxLayout()
        layout.addWidget(self.chess_board)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(central_widget)
        self.background_widget.resize(self.size())
        self.background_widget.lower()
        self.button = QPushButton('BACK', self)
        self.button.clicked.connect(self.back)
        self.button.move(0, 0)
        self.button.resize(100, 50)
        self.button.setStyleSheet(f"""
            color: red;
            background-color: black;
            font-family: {font};
            font-size: {font_size}
        """)
        self.resizeEvent = lambda event: self.background_widget.resize(event.size())

    def back(self):
        self.mw = MainWindow()
        self.mw.showMaximized()
        self.close()


class ChessBoard(QWidget):
    def __init__(self, vs_robot=False):
        super().__init__()
        self.vs_robot = vs_robot
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шахматная доска')
        self.setFixedSize(640, 640)
        self.board_size = 8
        self.selected_square = None
        self.highlighted_squares = []
        self.board = chess.Board()
        self.pieces = {
            'P': QPixmap('figures/wp.png'),
            'R': QPixmap('figures/wl.png'),
            'N': QPixmap('figures/wh.png'),
            'B': QPixmap('figures/wb.png'),
            'Q': QPixmap('figures/wq.png'),
            'K': QPixmap('figures/wk.png'),
            'p': QPixmap('figures/bp.png'),
            'r': QPixmap('figures/bl.png'),
            'n': QPixmap('figures/bh.png'),
            'b': QPixmap('figures/bb.png'),
            'q': QPixmap('figures/bq.png'),
            'k': QPixmap('figures/bk.png')
        }
        self.buttons = {}
        layout = QGridLayout()
        self.setLayout(layout)
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = QPushButton(self)
                button.setFixedSize(80, 80)
                button.setStyleSheet(self.get_button_color(row, col))
                button.clicked.connect(self.click_on_button)
                layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button
        self.update_board()

    def get_button_color(self, row, col):
        if (row + col) % 2 == 0:
            return 'background-color: white;'
        else:
            return 'background-color: pink;'

    def update_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[(row, col)]
                square = chess.square(col, 7 - row)
                piece = self.board.piece_at(square)
                button.setIcon(QIcon())
                if piece:
                    piece_symbol = piece.symbol()
                    pixmap = self.pieces.get(piece_symbol)
                    if pixmap:
                        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
                        button.setIcon(QIcon(pixmap))
                if self.selected_square and (row, col) == self.selected_square:
                    button.setStyleSheet('background-color: rgba(0, 250, 154, 255);')
                elif (row, col) in self.highlighted_squares:
                    button.setStyleSheet('background-color: rgba(0, 255, 0, 255);')
                else:
                    button.setStyleSheet(self.get_button_color(row, col))

    def click_on_button(self):
        button = self.sender()
        pos = self.get_button_position(button)
        if pos:
            row, col = pos
            square = chess.square(col, 7 - row)
            piece = self.board.piece_at(square)
            if not self.selected_square and piece is not None and piece.color == self.board.turn:
                # Если выбрана фигура, то подсвечиваем возможные ходы
                self.selected_square = (row, col)
                self.highlighted_squares = self.get_legal_moves(square)
            elif self.selected_square:
                # Если выбрана пустая клетка, проверяем возможность хода
                if (row, col) in self.highlighted_squares:
                    from_square = chess.square(self.selected_square[1], 7 - self.selected_square[0])
                    to_square = square
                    move = chess.Move(from_square, to_square)
                    if move in self.board.legal_moves:
                        self.make_move(move)
                self.selected_square = None
                self.highlighted_squares = []
            self.update_board()

    def make_move(self, move):
        self.board.push(move)
        self.update_board()
        if self.vs_robot and self.board.turn == chess.BLACK:
            self.move_black()  # Вызываем метод для хода черных

    def move_black(self):
        print("Черные ходят!")
        # Здесь вы можете добавить свою реализацию искусственного интеллекта
        # Пока что просто пропускаем ход
        pass

    def get_button_position(self, button):
        for (row, col), btn in self.buttons.items():
            if btn == button:
                return (row, col)
        return None

    def get_legal_moves(self, square):
        legal_moves = []
        moves = self.board.legal_moves
        for move in moves:
            if move.from_square == square:
                to_square = move.to_square
                to_row, to_col = divmod(to_square, 8)
                legal_moves.append((7 - to_row, to_col))
        return legal_moves

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())
