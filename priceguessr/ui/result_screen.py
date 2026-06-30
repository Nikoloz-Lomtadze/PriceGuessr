import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect, QHBoxLayout, QLabel,QPushButton, QVBoxLayout, QWidget)
from priceguessr.paths import asset_path

# მოცემული კოდი ემსახურება შედეგის სქრინს

class ResultScreen(QWidget):

    def __init__(self, main_stack):
        super().__init__()
        self.main_stack = main_stack
        self.replay_callback = None
        self.exit_callback = None
        self.build_ui()

    def build_ui(self):
        self.setFixedSize(1920, 1080)
        self.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 35, 0, 35)
        main_layout.setSpacing(20)

        self.title_label = QLabel("YOU WON!")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(155)
        main_layout.addWidget(self.title_label)

        self.score_label = QLabel("SCORE: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFixedSize(700, 105)
        main_layout.addWidget(self.score_label, alignment=Qt.AlignCenter)

        self.winner_image = QLabel()
        self.winner_image.setFixedSize(440, 440)
        self.winner_image.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.winner_image, alignment=Qt.AlignCenter)

        self.details_label = QLabel()
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setFixedHeight(70)
        self.details_label.setStyleSheet(
            "font-family: 'Arial Black', 'Impact', sans-serif;"
            "font-size: 25px; font-weight: bold; color: white;"
            "background: transparent;"
        )
        main_layout.addWidget(self.details_label)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(50)
        buttons_layout.setAlignment(Qt.AlignCenter)

        button_style = """
            QPushButton {
                background-color: #240a46;
                border: 5px solid #00ffb3;
                border-radius: 35px;
                font-family: 'Arial Black', 'Impact', sans-serif;
                font-size: 34px;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #00ffb3;
                color: #17052e;
                border: 5px solid #ffffff;
            }
        """

        replay_button = QPushButton("PLAY AGAIN")
        replay_button.setFixedSize(380, 105)
        replay_button.setCursor(Qt.PointingHandCursor)
        replay_button.setStyleSheet(button_style)
        replay_button.clicked.connect(self.replay)
        buttons_layout.addWidget(replay_button)

        exit_button = QPushButton("MAIN MENU")
        exit_button.setFixedSize(380, 105)
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.setStyleSheet(button_style)
        exit_button.clicked.connect(self.exit_to_menu)
        buttons_layout.addWidget(exit_button)

        main_layout.addLayout(buttons_layout)

    def show_result(self, title, score_text, details, outcome,
                    replay_callback, exit_callback):
        colors = {
            "win": "#00ffb3",
            "lose": "#ff4f78",
            "tie": "#ffd34d"
        }
        color = colors.get(outcome, colors["tie"])
        title_size = 130 if len(title) <= 14 else 92

        self.title_label.setText(title)
        self.title_label.setStyleSheet(f"""
            font-family: 'Arial Black', 'Impact', sans-serif;
            font-size: {title_size}px;
            font-weight: 900;
            color: {color};
            background: transparent;
        """)

        glow = QGraphicsDropShadowEffect(self.title_label)
        glow.setBlurRadius(40)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        self.title_label.setGraphicsEffect(glow)

        self.score_label.setText(score_text)
        self.score_label.setStyleSheet(f"""
            background-color: #17052e;
            border: 5px solid {color};
            border-radius: 25px;
            font-family: 'Arial Black', 'Impact', sans-serif;
            font-size: 32px;
            font-weight: bold;
            color: {color};
        """)
        self.details_label.setText(details)

        winner_path = asset_path("winner.png")
        if outcome != "win" or not os.path.exists(winner_path):
            winner_path = asset_path("mascot-bag.png")
        self.winner_image.setPixmap(QPixmap(winner_path).scaled(
            440, 440, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

        self.replay_callback = replay_callback
        self.exit_callback = exit_callback
        self.main_stack.setCurrentWidget(self)

    def replay(self):
        if self.replay_callback is not None:
            self.replay_callback()

    def exit_to_menu(self):
        if self.exit_callback is not None:
            self.exit_callback()
