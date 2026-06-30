from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QProgressBar,
                             QPushButton, QVBoxLayout, QWidget)

from priceguessr.paths import asset_path

# მოცემული კოდი ემსახურება ანალიტიკის  სქრინს
MODE_LABELS = {
    "singleplayer": "SOLO",
    "vsbot": "VS BOT",
    "multiplayer": "MULTIPLAYER",
}

MODE_COLORS = {
    "singleplayer": "#00ffb3",
    "vsbot": "#ff0055",
    "multiplayer": "#ffcc00",
}


class ScoreGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(680, 280)
        self.scores = []

    def set_scores(self, scores):
        self.scores = list(reversed(scores[:7]))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        left, right, top, bottom = 60, 30, 40, 40
        graph_width = self.width() - left - right
        graph_height = self.height() - top - bottom

        painter.setFont(QFont("Arial", 9, QFont.Bold))
        for value in (0, 25, 50, 75, 100):
            y = top + graph_height - int(value / 100 * graph_height)
            painter.setPen(QPen(QColor("#2c144d"), 1, Qt.DashLine))
            painter.drawLine(left, y, left + graph_width, y)
            painter.setPen(QColor("#ffffff"))
            painter.drawText(left - 45, y + 5, str(value))

        painter.setPen(QPen(QColor("#4c2a75"), 2))
        painter.drawLine(left, top + graph_height, left + graph_width, top + graph_height)
        painter.drawLine(left, top, left, top + graph_height)

        if not self.scores:
            painter.setPen(QColor("#8c73b3"))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(self.rect(), Qt.AlignCenter, "PLAY A GAME TO SEE YOUR PERFORMANCE")
            return

        count = len(self.scores)
        x_step = graph_width / max(count - 1, 1)
        average = sum(self.scores) / count

        painter.setPen(QColor("#8c73b3"))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        for index in range(count):
            x = left + int(index * x_step) if count > 1 else left + graph_width // 2
            painter.drawText(x - 20, top + graph_height + 25, f"GAME {index + 1}")

        average_y = top + graph_height - int(average / 100 * graph_height)
        painter.setPen(QPen(QColor("#ff0055"), 3, Qt.DashLine))
        painter.drawLine(left, average_y, left + graph_width, average_y)

        points = []
        for index, score in enumerate(self.scores):
            x = left + index * x_step if count > 1 else left + graph_width / 2
            y = top + graph_height - score / 100 * graph_height
            points.append(QPointF(x, y))

        path = QPainterPath()
        path.moveTo(points[0])
        for point in points[1:]:
            path.lineTo(point)
        painter.setPen(QPen(QColor("#00ffb3"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        painter.setFont(QFont("Arial Black", 10, QFont.Bold))
        for point, score in zip(points, self.scores):
            painter.setPen(QPen(QColor("#00ffb3"), 3))
            painter.setBrush(QColor("#ffffff"))
            painter.drawEllipse(point, 6, 6)
            painter.setPen(QColor("#00ffb3"))
            painter.drawText(int(point.x() - 10), int(point.y() - 12), str(score))


class AnalyticsScreen(QWidget):
    def __init__(self, main_stack, menu_page):
        super().__init__()
        self.main_stack = main_stack
        self.menu_page = menu_page
        self.mode_rows = {}
        self.build_ui()

    def build_ui(self):
        self.setFixedSize(1920, 1080)
        self.setStyleSheet("""
            QWidget { font-family: 'Arial Black', sans-serif; color: white; }
            #AnalyticsBox { background-color: #31115c; border: 8px solid #17052e; border-radius: 48px; }
            .MiniCard { background-color: #1a0438; border: 4px solid #4c2a75; border-radius: 24px; padding: 10px; }
            .PanelBox { background-color: #17052e; border: 4px solid #4c2a75; border-radius: 32px; }
            .PanelTitle { font-size: 24px; color: #00ffb3; font-weight: 900; letter-spacing: 2px; }
            QProgressBar { background-color: #1a0438; border: none; border-radius: 10px; text-align: center; }
            QProgressBar::chunk { border-radius: 10px; }
        """)

        screen_layout = QVBoxLayout(self)
        screen_layout.setContentsMargins(30, 30, 30, 30)
        analytics_frame = QFrame()
        analytics_frame.setObjectName("AnalyticsBox")
        screen_layout.addWidget(analytics_frame)

        content_layout = QVBoxLayout(analytics_frame)
        content_layout.setContentsMargins(60, 20, 60, 35)
        content_layout.setSpacing(0)

        logo = QLabel()
        logo.setPixmap(QPixmap(asset_path("prg.png")).scaled(620, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        content_layout.addWidget(logo, alignment=Qt.AlignCenter)

        title = QLabel("⚡ ANALYTICS ⚡")
        title.setStyleSheet("font-size: 32px; color: white; font-weight: 900; letter-spacing: 4px; margin-bottom: 15px;")
        content_layout.addWidget(title, alignment=Qt.AlignCenter)

        cards = QHBoxLayout()
        cards.setSpacing(40)
        cards.addStretch()
        self.games_value = self.create_card(cards, "games-played.png", "GAMES PLAYED", "#00ffb3")
        self.win_rate_value = self.create_card(cards, "win-rate.png", "WIN RATE", "#ff0055")
        self.best_score_value = self.create_card(cards, "best-score.png", "BEST SCORE", "#ffcc00")
        cards.addStretch()
        content_layout.addLayout(cards)
        content_layout.addSpacing(25)

        panels = QHBoxLayout()
        panels.setSpacing(40)

        performance = QFrame()
        performance.setProperty("class", "PanelBox")
        performance.setFixedSize(850, 440)
        performance_layout = QVBoxLayout(performance)
        performance_title = QLabel(" ➔ PERFORMANCE ➔ ")
        performance_title.setProperty("class", "PanelTitle")
        performance_title.setAlignment(Qt.AlignCenter)
        performance_layout.addWidget(performance_title)
        self.graph = ScoreGraph()
        performance_layout.addWidget(self.graph, alignment=Qt.AlignCenter)
        legend = QLabel("<span style='color:#00ffb3;'>▬</span> YOUR SCORE &nbsp;&nbsp; <span style='color:#ff0055;'>┈</span> YOUR AVERAGE")
        legend.setAlignment(Qt.AlignCenter)
        performance_layout.addWidget(legend)
        panels.addWidget(performance)

        modes = QFrame()
        modes.setProperty("class", "PanelBox")
        modes.setFixedSize(850, 440)
        modes_layout = QVBoxLayout(modes)
        modes_layout.setContentsMargins(40, 25, 40, 25)
        modes_layout.setSpacing(20)
        modes_title = QLabel(" ➔ MODE STATS ➔ ")
        modes_title.setProperty("class", "PanelTitle")
        modes_title.setAlignment(Qt.AlignCenter)
        modes_layout.addWidget(modes_title)
        for mode in ("singleplayer", "vsbot", "multiplayer"):
            row = QHBoxLayout()
            label = QLabel(MODE_LABELS[mode])
            label.setFixedWidth(170)
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setStyleSheet(f"QProgressBar::chunk {{ background-color: {MODE_COLORS[mode]}; }}")
            value = QLabel("0%")
            value.setFixedWidth(60)
            row.addWidget(label)
            row.addWidget(bar, stretch=1)
            row.addWidget(value)
            modes_layout.addLayout(row)
            self.mode_rows[mode] = (bar, value)
        modes_layout.addStretch()
        panels.addWidget(modes)
        content_layout.addLayout(panels)
        content_layout.addSpacing(20)

        footer = QHBoxLayout()
        mascot = QLabel()
        mascot.setPixmap(QPixmap(asset_path("mascot-bag.png")).scaled(180, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        mascot.setFixedSize(200, 145)
        footer.addWidget(mascot)

        average_panel = QFrame()
        average_panel.setProperty("class", "PanelBox")
        average_panel.setFixedSize(350, 110)
        average_layout = QVBoxLayout(average_panel)
        average_title = QLabel("AVERAGE SCORE")
        average_title.setStyleSheet("font-size: 14px; color: #00ffb3;")
        self.average_value = QLabel("0 ⚡")
        self.average_value.setStyleSheet("font-size: 28px; font-weight: 900;")
        average_layout.addWidget(average_title)
        average_layout.addWidget(self.average_value)
        footer.addWidget(average_panel, alignment=Qt.AlignVCenter)
        footer.addStretch()

        back = QPushButton("⬅ BACK TO MENU")
        back.setFixedSize(380, 85)
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet("QPushButton { background-color: white; border-radius: 28px; font-size: 24px; font-weight: 900; color: #17052e; } QPushButton:hover { background-color: #00ffb3; }")
        back.clicked.connect(lambda: self.main_stack.setCurrentWidget(self.menu_page))
        footer.addWidget(back, alignment=Qt.AlignVCenter)
        content_layout.addLayout(footer)

    def create_card(self, layout, icon_name, title, color):
        card = QFrame()
        card.setProperty("class", "MiniCard")
        card.setFixedSize(360, 120)
        card_layout = QHBoxLayout(card)
        icon = QLabel()
        icon.setPixmap(QPixmap(asset_path(icon_name)).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 15px; color: {color}; font-weight: bold;")
        value_label = QLabel("0")
        value_label.setStyleSheet("font-size: 38px; color: white; font-weight: 900;")
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        card_layout.addWidget(icon)
        card_layout.addLayout(text_layout)
        layout.addWidget(card)
        return value_label

    def refresh(self, service, user_id):
        stats = service.get_analytics(user_id)
        history = service.get_history(user_id)
        games_played = sum(row["games_count"] for row in stats)
        wins = sum(row["wins_count"] or 0 for row in stats)
        win_rate = round(wins * 100 / games_played) if games_played else 0
        scores = [match.points_count for match in history]
        best_score = max((row["best_points"] or 0 for row in stats), default=0)
        total_points = sum(row["total_points"] or 0 for row in stats)
        average_score = round(total_points / games_played) if games_played else 0

        self.games_value.setText(str(games_played))
        self.win_rate_value.setText(f"{win_rate}%")
        self.best_score_value.setText(str(best_score))
        self.average_value.setText(f"{average_score} ⚡")
        self.graph.set_scores(scores)

        stats_by_mode = {row["mode"]: row for row in stats}
        for mode, (bar, label) in self.mode_rows.items():
            row = stats_by_mode.get(mode)
            rate = round((row["wins_count"] or 0) * 100 / row["games_count"]) if row else 0
            bar.setValue(rate)
            label.setText(f"{rate}%")
