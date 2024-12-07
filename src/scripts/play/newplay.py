import chess
import chess.engine

import sys
import time
import json
# sys.path.append("..")

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog, QHBoxLayout, QLabel
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QLineEdit, QDialog


imagemw = 'media/death-note-l-and-light-playing-chess-ft7rtfi086yvefyc.jpg'
imageplay = 'sakura.webp'
font_size = '17px'
font = 'Comic Sans MS'

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

SCREEN_SIZE = [400, 400]


class Example(QMainWindow):
    def __init__(self, path=None):
        super().__init__()
        self.path = path
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        ## Изображение
        self.pixmap = QPixmap(self.path)
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.image = QLabel(self)
        self.image.move(80, 60)
        self.image.resize(1000, 1000)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.image.setPixmap(self.pixmap)


class New_play(QMainWindow):
    def __init__(self, board=chess.Board, vsrobot=False, mw=None):
        super().__init__()
        self.board = board
        self.mw = mw
        self.vsrobot = vsrobot
        self.initUI()

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
        self.chess_board = ChessBoard(board=self.board, vs_robot=self.vsrobot)
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

    # def back(self):
    #
    #     def save_board_to_json(board: chess.Board, filename: str):
    #         fen = board.fen()
    #         data = {
    #             "fen": fen,
    #         }
    #         with open(filename, 'w') as f:
    #             json.dump(data, f)
    #
    #    fname = ...
    #    save_board_to_json(self.board, f'{fname}.json')
    #    if self.vsrobot:
    #        self.back_robot()
    #    else:
    #        self.back_human()
    def back(self):

        def save_board_to_json(board: chess.Board, filename: str):
            fen = board.fen()
            data = {
                "fen": fen,
            }
            with open(filename, 'w') as f:
                json.dump(data, f)

        # Запрос подтверждения на сохранение партии
        reply = QMessageBox.question(
            self,
            'Сохранение партии',
            'Желаете ли вы сохранить партию?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            fname, ok_pressed = QInputDialog.getText(self, "Введите имя партии",
                                                    "Название партии")
            if ok_pressed:
                save_board_to_json(self.board, f'{fname}.json')

        else:
            # Если пользователь отказался от сохранения, просто продолжаем выполнение программы
            pass

        # Остальная часть вашего метода back
        if self.vsrobot:
            self.back_robot()
        else:
            self.back_human()


    def back_human(self):
        # self.chess_board.engine.quit()
        self.mw.showMaximized()
        self.close()

    def back_robot(self):
        self.chess_board.engine.quit()
        self.mw.showMaximized()
        self.close()

class Sidebar(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)

        # Устанавливаем белый фон для виджета
        self.setStyleSheet("background-color: white;")

        # Лейбл для отображения ходов
        self.moves_label = QLabel(f"Ходы: ")
        self.moves_label.setWordWrap(True)

        # Кнопки для управления партией
        self.best_move_button = QPushButton("Лучший ход")
        self.backward_move_button = QPushButton("Назад")
        self.best_move_button.clicked.connect(self.best_move)
        self.backward_move_button.clicked.connect(self.backward_move)

        # Лэйаут для элементов бокового виджета
        layout = QVBoxLayout()
        layout.addWidget(self.moves_label)
        layout.addStretch()  # Растягиваем пространство между элементами
        layout.addWidget(self.best_move_button)
        layout.addWidget(self.backward_move_button)

        self.setLayout(layout)

    def best_move(self):
        engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-sse41-popcnt.exe")
        result = engine.play(self.parent.board, chess.engine.Limit(time=0.100))
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(str(result.move))
        msg_box.setWindowTitle("ХОД")
        msg_box.exec()


    def backward_move(self):
        self.parent.board.pop()
        self.parent.update_board()


class ChessBoard(QWidget):
    def __init__(self, board=chess.Board, vs_robot=False):
        super().__init__()
        self.board = board
        self.vs_robot = vs_robot
        self.initUI()

    def initUI(self):
        if self.vs_robot:
            self.engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-sse41-popcnt.exe")
        self.setWindowTitle('Шахматная доска')
        self.setFixedSize(800, 640)
        self.board_size = 8
        self.selected_square = None
        self.highlighted_squares = []
        self.pieces = {
            'P': QPixmap('wp.png'),
            'R': QPixmap('wl.png'),
            'N': QPixmap('wh.png'),
            'B': QPixmap('wb.png'),
            'Q': QPixmap('wq.png'),
            'K': QPixmap('wk.png'),
            'p': QPixmap('bp.png'),
            'r': QPixmap('bl.png'),
            'n': QPixmap('bh.png'),
            'b': QPixmap('bb.png'),
            'q': QPixmap('bq.png'),
            'k': QPixmap('bk.png')
        }
        self.buttons = {}
        board_widget = QWidget()
        board_layout = QGridLayout()
        board_widget.setLayout(board_layout)
        board_layout.setSpacing(0)
        board_layout.setContentsMargins(0, 0, 0, 0)
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = QPushButton(self)
                button.setFixedSize(80, 80)
                button.setStyleSheet(self.get_button_color(row, col))
                button.clicked.connect(self.click_on_button)
                board_layout.addWidget(button, row, col)
                self.buttons[(row, col)] = button
        self.sidebar = Sidebar(self)
        main_layout = QHBoxLayout()
        main_layout.addWidget(board_widget)
        main_layout.addWidget(self.sidebar)
        self.setLayout(main_layout)
        self.update_board()

    def get_button_color(self, row, col):
        if (row + col) % 2 == 0:
            return 'background-color: white;'
        else:
            return 'background-color: pink;'

    def update_board(self):
        self.sidebar.moves_label.setText(f"Ходы: {'; '.join(list(map(str, self.board.move_stack)))}")
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
        self.show_result()

    def click_on_button(self):
        button = self.sender()
        pos = self.get_button_position(button)
        if pos:
            row, col = pos
            square = chess.square(col, 7 - row)
            piece = self.board.piece_at(square)
            if not self.selected_square and piece is not None and piece.color == self.board.turn:
                self.selected_square = (row, col)
                self.highlighted_squares = self.get_legal_moves(square)
            elif self.selected_square:
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
        if (self.vs_robot == True):
            self.move_black()

    def move_black(self):
        if self.vs_robot:
            result = self.engine.play(self.board, chess.engine.Limit(time=0.100))
        self.board.push(result.move)
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

    def show_result(self):
        if self.board.is_checkmate():
            image_path = 'win.jpg' if self.board.turn else 'lose.jpg'
        elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_fivefold_repetition() or self.board.can_claim_draw():
            image_path = 'draw.png'
        else:
            return None
        ex = Example(path=image_path)
        start_time = time.time()
        end_time = start_time + 3
        while time.time() < end_time:
            ex.showMaximized()