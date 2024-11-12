import sys

import chess

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Главное меню')
        self.setGeometry(100, 100, 600, 600)
        layout = QVBoxLayout()
        button_playnew = QPushButton('Новая партия')
        button_playold = QPushButton('Старая партия')
        button_settings = QPushButton('Настройки')
        button_playnew.setMaximumSize(100, 50)
        button_playold.setMaximumSize(100, 50)
        button_settings.setMaximumSize(100, 50)
        layout.addWidget(button_playnew)
        layout.addWidget(button_playold)
        layout.addWidget(button_settings)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget = QWidget()
        image_path = 'death-note-l-and-light-playing-chess-ft7rtfi086yvefyc.jpg'
        central_widget.setStyleSheet(f'''
            background-image: url({image_path});
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
        self.mw = New_play()
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
        self.setWindowTitle('Выбор старой игры')
        self.setGeometry(100, 100, 600, 600)
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')
        # тут будет расшифровка cvv файла в доску, но позже

class Settings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Выбор старой игры')
        self.setGeometry(100, 100, 600, 600)
        # тут будут настройки, описанные в README


class Settings(QMainWindow):
    pass

class New_play(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Шахматная доска')
        self.setGeometry(100, 100, 600, 600)
        self.background_widget = QWidget(self)
        self.background_widget.setStyleSheet('''
            background-image: url(sakura.webp);
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
        self.resizeEvent = lambda event: self.background_widget.resize(event.size())

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
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
                    button.setStyleSheet('background-color: rgba(0, 250, 154, 100);')
                elif (row, col) in self.highlighted_squares:
                    button.setStyleSheet('background-color: rgba(0, 255, 0, 100);')
                else:
                    button.setStyleSheet(self.get_button_color(row, col))

    def click_on_button(self):
        button = self.sender()
        pos = self.get_button_position(button)
        if pos:
            row, col = pos
            square = chess.square(col, 7 - row)
            piece = self.board.piece_at(square)
            if piece:
                self.selected_square = (row, col)
                self.highlighted_squares = self.get_legal_moves(square)
            else:
                self.selected_square = None
                self.highlighted_squares = []
            self.update_board()

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
