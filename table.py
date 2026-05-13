from PyQt6.QtCore import Qt

from PyQt6.QtGui import (
    QFont,
    QColor,
    QPainter,
    QLinearGradient
)

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt6.QtSvgWidgets import QSvgWidget

from player import Player

class PlayerRow(QWidget):

    def __init__(self, player: Player):
        super().__init__()

        self.player = player
        self.setFixedHeight(26)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(10, 8, 6, 170);
                border: 1px solid rgba(212, 175, 55, 90);
                border-radius: 5px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(6, 0, 6, 0)
        layout.setSpacing(4)

        # FLAG
        self.flag = QSvgWidget()
        self.flag.setFixedSize(18, 12)

        # NAME
        self.nameLabel = QLabel()
        self.nameLabel.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))

        self.nameLabel.setStyleSheet("""
            color: #f0e6d2;
            background: transparent;
            border: none;
        """)

        # RATING
        self.ratingLabel = QLabel()
        self.ratingLabel.setFont(
            QFont("Segoe UI", 8)
        )
        self.ratingLabel.setStyleSheet("""
            color: #d6b36a;
            background: transparent;
            border: none;
        """)

        # RANK
        self.rankLabel = QLabel()
        self.rankLabel.setFont(
            QFont("Segoe UI", 7)
        )
        self.rankLabel.setStyleSheet("""
            color: #8f8f8f;
            background: transparent;
            border: none;
        """)

        layout.addWidget(self.flag)
        layout.addWidget(self.nameLabel)
        layout.addStretch()
        layout.addWidget(self.ratingLabel)
        layout.addWidget(self.rankLabel)

        self.setLayout(layout)
        self.refresh()

    def refresh(self):

        self.player.fetch()

        # FLAG
        if self.player.countrySVGFlag:
            self.flag.load(
                bytearray(
                    self.player.countrySVGFlag,
                    encoding="utf-8"
                )
            )

        self.nameLabel.setText(self.player.alias)
        self.ratingLabel.setText(str(self.player.sup_team_rating))
        self.rankLabel.setText(f"#{self.player.sup_team_rank}")