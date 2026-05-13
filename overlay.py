from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QFont,
    QColor,
    QPainter,
    QLinearGradient
)

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from player import Player
from table import PlayerRow


class Overlay(QWidget):

    def __init__(self, _players):
        super().__init__()

        self.players = _players

        self.initUI()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        gradient = QLinearGradient(
            0,
            0,
            self.width(),
            self.height()
        )

        gradient.setColorAt(
            0,
            QColor(6, 6, 6, 190)
        )

        gradient.setColorAt(
            1,
            QColor(18, 14, 10, 190)
        )

        painter.setBrush(gradient)

        painter.setPen(
            QColor(160, 120, 50, 120)
        )

        painter.drawRoundedRect(
            self.rect(),
            10,
            10
        )

    def initUI(self):

        self.setWindowTitle("AoM Overlay")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.setGeometry(
            1480,
            120,
            270,
            96
        )

        self.root = QVBoxLayout()

        self.root.setContentsMargins(
            6,
            6,
            6,
            6
        )

        self.root.setSpacing(1)

        # TITLE
        self.title = QLabel("RANKED")

        self.title.setFont(
            QFont(
                "Segoe UI",
                8,
                QFont.Weight.Bold
            )
        )

        self.title.setStyleSheet("""
            color: #d6b36a;
            background: transparent;
            border: none;
        """)

        self.root.addWidget(self.title)

        self.setLayout(self.root)

        self.update_players(self.players)

    def clear_players(self):

        # borrar widgets excepto titulo
        while self.root.count() > 1:

            item = self.root.takeAt(1)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    def update_players(self, players):

        self.players = players

        self.clear_players()

        for alias in self.players:

            try:

                player = Player(alias)

                row = PlayerRow(player)

                self.root.addWidget(row)

            except Exception as e:

                print(e)

        self.adjustSize()