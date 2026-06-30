from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,QHeaderView, QLabel, QPushButton, QTableWidget,QTableWidgetItem, QVBoxLayout, QWidget)
from priceguessr.paths import asset_path

# მოცემული კოდი ემსახურება თამაშების ისტორიის სქრინს


MODE_DETAILS = {
    "singleplayer": ("SOLO", "solo-icon.png"),
    "vsbot": ("PLAY WITH BOT", "bot-icon.png"),
    "multiplayer": ("MULTIPLAYER", "multiplayer-icon.png"),
                }


class GameHistoryScreen(QWidget):
    def __init__(self, main_stack, menu_page):
        super().__init__()
        self.main_stack = main_stack
        self.menu_page = menu_page
        self.matches = []
        self.build_ui()

    def build_ui(self):
        self.setFixedSize(1920, 1080)
        self.setStyleSheet("QWidget { font-family: 'Arial Black', 'Impact', sans-serif; color: white; } #HistoryBox { background-color: #240a46; border: 6px solid #ff0055; border-radius: 48px; }")
        screen_layout = QVBoxLayout(self)
        screen_layout.setAlignment(Qt.AlignCenter)
        screen_layout.setContentsMargins(0, 20, 0, 20)

        center_box = QFrame()
        center_box.setObjectName("HistoryBox")
        center_box.setFixedSize(1720, 960)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(50)
        glow.setColor(QColor(255, 0, 85, 130))
        glow.setOffset(0, 0)
        center_box.setGraphicsEffect(glow)

        box_layout = QVBoxLayout(center_box)
        box_layout.setContentsMargins(60, 35, 60, 30)
        box_layout.setSpacing(12)
        logo = QLabel()
        logo.setPixmap(QPixmap(asset_path("prg.png")).scaled(550, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setFixedSize(550, 140)
        box_layout.addWidget(logo, alignment=Qt.AlignCenter)

        subtitle = QLabel("GAME HISTORY")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 38px; color: #ff0055; font-weight: 900; letter-spacing: 6px; background: transparent;")
        box_layout.addWidget(subtitle)

        filters = QHBoxLayout()
        filters.setSpacing(20)
        filter_style = "QPushButton { background-color: #17052e; border: 3px solid #ff0055; border-radius: 15px; font-size: 18px; font-weight: bold; color: white; padding: 0 15px; } QPushButton:hover { background-color: #ff0055; color: #17052e; border-color: white; }"
        for text, mode, icon_name, width in (
            ("ALL", None, None, 180),
            ("SOLO", "singleplayer", "solo-icon.png", 180),
            ("BOT", "vsbot", "bot-icon.png", 180),
            ("MULTIPLAYER", "multiplayer", "multiplayer-icon.png", 240),
        ):
            button = QPushButton(f"  {text}")
            if icon_name:
                button.setIcon(QIcon(asset_path(icon_name)))
                button.setIconSize(QSize(22, 22))
            button.setFixedSize(width, 55)
            button.setStyleSheet(filter_style)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked=False, selected=mode: self.filter_table(selected))
            filters.addWidget(button)
        filters.addStretch()
        box_layout.addLayout(filters)

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["MODE", "ROUNDS WON", "SCORE", "DATE", "STATUS"])
        self.history_table.setFixedSize(1600, 475)
        self.history_table.setStyleSheet("""
            QTableWidget { background-color: #17052e; border: 4px solid #1a0438; border-radius: 24px; gridline-color: #240a46; font-size: 22px; color: white; }
            QTableWidget::item { padding: 12px; border-bottom: 2px solid #240a46; }
            QHeaderView::section { background-color: #1a0438; color: #ff0055; font-weight: bold; font-size: 22px; border: none; padding: 15px; }
            QScrollBar:vertical { border: none; background: #17052e; width: 14px; margin: 0; }
            QScrollBar::handle:vertical { background: #ff0055; min-height: 30px; border-radius: 7px; }
        """)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.verticalHeader().setMinimumSectionSize(58)
        self.history_table.verticalHeader().setDefaultSectionSize(58)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionMode(QTableWidget.NoSelection)
        box_layout.addWidget(self.history_table, alignment=Qt.AlignCenter)
        box_layout.addStretch()

        back = QPushButton("BACK TO MENU")
        back.setFixedSize(440, 95)
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet("QPushButton { background-color: #17052e; border: 6px solid #ff0055; border-radius: 32px; font-size: 30px; font-weight: bold; color: white; } QPushButton:hover { background-color: #ff0055; color: #17052e; }")
        back.clicked.connect(lambda: self.main_stack.setCurrentWidget(self.menu_page))
        box_layout.addWidget(back, alignment=Qt.AlignLeft)
        screen_layout.addWidget(center_box, alignment=Qt.AlignCenter)

    def refresh(self, service, user_id):
        self.matches = service.get_history(user_id)
        self.history_table.setRowCount(len(self.matches))
        for row_index, match in enumerate(self.matches):
            mode_text, icon_name = MODE_DETAILS.get(match.mode, (match.mode.upper(), "solo-icon.png"))
            mode_container = QWidget()
            mode_container.setProperty("mode", match.mode)
            mode_layout = QHBoxLayout(mode_container)
            mode_layout.setContentsMargins(15, 4, 15, 4)
            mode_layout.setSpacing(12)
            mode_layout.setAlignment(Qt.AlignCenter)
            icon = QLabel()
            icon.setFixedSize(32, 32)
            icon.setAlignment(Qt.AlignCenter)
            icon.setPixmap(QPixmap(asset_path(icon_name)).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label = QLabel(mode_text)
            label.setStyleSheet("font-size: 22px; color: white; background: transparent; font-weight: bold;")
            mode_layout.addWidget(icon)
            mode_layout.addWidget(label)
            self.history_table.setCellWidget(row_index, 0, mode_container)

            values = (
                f"{match.rounds_won}/{match.rounds_played}",
                str(match.points_count),
                str(match.played_at).split(" ")[0],
                "WIN" if match.won else "LOST",
            )
            for column, value in enumerate(values, start=1):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                if column == 4:
                    item.setForeground(QColor("#00ffb3" if match.won else "#ff0055"))
                self.history_table.setItem(row_index, column, item)
        self.filter_table(None)

    def filter_table(self, mode):
        for row_index in range(self.history_table.rowCount()):
            cell = self.history_table.cellWidget(row_index, 0)
            self.history_table.setRowHidden(row_index, bool(mode and cell.property("mode") != mode))
