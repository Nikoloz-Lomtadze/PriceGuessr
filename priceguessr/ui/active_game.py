import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,QHBoxLayout, QVBoxLayout, QFrame, QMessageBox,QGridLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
from priceguessr.models import Gamemodes
from priceguessr.paths import asset_path

# მოცემული კოდი ემსახურება აქტიური თამაშის სქრინს

class ActiveGameScreen(QWidget):
    """Shared game screen for solo, bot, and local multiplayer modes."""

    def __init__(self, menu_page, main_stack):
        super().__init__()
        self.menu_page = menu_page
        self.main_stack = main_stack
        self.session = None
        self.seconds_left = 15
        self.answer_locked = False
        self.player_turn = 1
        self.player_names = ("Player 1", "Player 2")
        self.result_page = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.build_ui()

    def build_ui(self):
        self.setFixedSize(1920, 1080)
        self.setStyleSheet("""
            ActiveGameScreen {
                background: transparent;
            }
            QWidget {
                font-family: 'Arial Black', 'Impact', sans-serif;
                color: white;
            }
            .ItemCard {
                background-color: #240a46;
                border: 8px solid #17052e;
                border-radius: 44px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 35, 50, 25)

        header_layout = QHBoxLayout()

        self.rounds_panel = QLabel()
        self.rounds_panel.setFixedSize(340, 110)
        self.rounds_panel.setAlignment(Qt.AlignCenter)
        self.rounds_panel.setStyleSheet(
            "background: transparent; font-size: 34px; font-weight: 900;"
        )
        self.set_round_counter(1, 10)
        header_layout.addWidget(self.rounds_panel)
        header_layout.addStretch()

        logo = QLabel()
        logo.setPixmap(QPixmap(asset_path("logo.png")).scaled(
            450, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        logo.setFixedSize(450, 130)
        header_layout.addWidget(logo, alignment=Qt.AlignCenter)
        header_layout.addStretch()

        self.score_panel = QLabel()
        self.score_panel.setFixedSize(320, 110)
        self.score_panel.setAlignment(Qt.AlignCenter)
        self.score_panel.setStyleSheet(
            "background: transparent; font-size: 30px; font-weight: 900;"
        )
        self.set_score_counter(0)
        header_layout.addWidget(self.score_panel)

        exit_button = QPushButton()
        exit_button.setIcon(QIcon(asset_path("x-button.png")))
        exit_button.setIconSize(QSize(110, 110))
        exit_button.setFixedSize(110, 110)
        exit_button.setCursor(Qt.PointingHandCursor)
        exit_button.setStyleSheet("background: transparent; border: none;")
        exit_button.clicked.connect(self.return_to_menu)
        header_layout.addWidget(exit_button)

        main_layout.addLayout(header_layout)

        game_layout = QHBoxLayout()
        game_layout.setSpacing(40)
        game_layout.setAlignment(Qt.AlignCenter)

        left_card, self.left_image, self.left_name, self.left_button = \
            self.create_item_card()
        self.left_button.clicked.connect(lambda: self.make_guess("left"))
        game_layout.addWidget(left_card)

        vs_icon = QLabel()
        vs_icon.setPixmap(QPixmap(asset_path("vs.png")).scaled(
            190, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        vs_icon.setFixedSize(190, 190)
        game_layout.addWidget(vs_icon, alignment=Qt.AlignCenter)

        right_card, self.right_image, self.right_name, self.right_button = \
            self.create_item_card()
        self.right_button.clicked.connect(lambda: self.make_guess("right"))
        game_layout.addWidget(right_card)

        main_layout.addLayout(game_layout)

        footer = QWidget()
        footer.setFixedHeight(190)
        footer_layout = QGridLayout(footer)
        footer_layout.setContentsMargins(10, 0, 10, 0)

        mascot = QLabel()
        mascot.setPixmap(QPixmap(asset_path("mascot-bag.png")).scaled(
            180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        mascot.setFixedSize(180, 180)
        footer_layout.addWidget(mascot, 0, 0, Qt.AlignBottom | Qt.AlignLeft)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(2)

        question = QLabel()
        question.setPixmap(QPixmap(asset_path("which-costs-more-txt.png")).scaled(
            760, 75, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        question.setFixedSize(760, 75)
        center_layout.addWidget(question, alignment=Qt.AlignCenter)

        self.status_label = QLabel("CHOOSE BEFORE TIME RUNS OUT!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            "font-size: 22px; color: #00ffb3; background: transparent;"
        )
        center_layout.addWidget(self.status_label)

        self.timer_label = QLabel("15")
        self.timer_label.setFixedSize(520, 78)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            background-color: #17052e;
            border: 6px solid #00ffb3;
            border-radius: 30px;
            color: white;
            font-size: 45px;
        """)
        center_layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)
        footer_layout.addLayout(center_layout, 0, 1, Qt.AlignCenter)

        balance = QWidget()
        balance.setFixedSize(180, 180)
        footer_layout.addWidget(balance, 0, 2, Qt.AlignRight)
        footer_layout.setColumnStretch(0, 1)
        footer_layout.setColumnStretch(1, 2)
        footer_layout.setColumnStretch(2, 1)
        main_layout.addWidget(footer)

    def set_round_counter(self, current_round, total_rounds):
        self.rounds_panel.setText(
            "<span style='color: white;'>ROUND</span> "
            f"<span style='color: #00ffb3;'>{current_round} / "
            f"{total_rounds}</span>"
        )

    def set_score_counter(self, score):
        if (self.session is not None and
                self.session.mode == Gamemodes.Multiplayer):
            self.score_panel.setText(
                "<span style='color: white;'>P1</span> "
                f"<span style='color: #00ffb3;'>{score}</span> "
                "<span style='color: white;'>| P2</span> "
                f"<span style='color: #ffd34d;'>"
                f"{self.session.player_two_score}</span>"
            )
        elif self.session is not None and self.session.mode == Gamemodes.vsbot:
            self.score_panel.setText(
                "<span style='color: white;'>YOU</span> "
                f"<span style='color: #00ffb3;'>{score}</span> "
                "<span style='color: white;'>| BOT</span> "
                f"<span style='color: #ffd34d;'>{self.session.bot_score}</span>"
            )
        else:
            self.score_panel.setText(
                "<span style='color: white;'>SCORE</span> "
                f"<span style='color: #ffd34d;'>{score}</span>"
            )

    def create_item_card(self):
        card = QFrame()
        card.setProperty("class", "ItemCard")
        card.setFixedSize(760, 625)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 30, 40, 30)

        image = QLabel()
        image.setFixedSize(640, 330)
        image.setAlignment(Qt.AlignCenter)
        layout.addWidget(image, alignment=Qt.AlignCenter)

        name = QLabel()
        name.setFixedHeight(75)
        name.setWordWrap(True)
        name.setAlignment(Qt.AlignCenter)
        name.setStyleSheet("font-size: 20px; background: transparent;")
        layout.addWidget(name)

        button = QPushButton()
        button.setIcon(QIcon(asset_path("this-costs-more-button.png")))
        button.setIconSize(QSize(620, 120))
        button.setFixedSize(620, 120)
        button.setStyleSheet("background: transparent; border: none;")
        button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        return card, image, name, button

    def start_session(self, session, player_names=None):
        self.session = session
        self.player_turn = 1
        if player_names is None:
            self.player_names = ("Player 1", "Player 2")
        else:
            self.player_names = player_names
        self.main_stack.setCurrentWidget(self)
        self.show_round()

    def show_round(self):
        game_round = self.session.get_current_round()
        total_rounds = len(self.session.rounds)
        self.set_round_counter(game_round.round_number, total_rounds)
        self.set_score_counter(self.session.score)
        self.left_name.setText(game_round.left_item.name)
        self.right_name.setText(game_round.right_item.name)
        self.load_item_image(
            self.left_image, game_round.left_item.image_url, asset_path("headset.png")
        )
        self.load_item_image(
            self.right_image, game_round.right_item.image_url, asset_path("keyboard.png")
        )

        self.answer_locked = False
        self.left_button.setEnabled(True)
        self.right_button.setEnabled(True)
        if self.session.mode == Gamemodes.Multiplayer:
            player_name = self.player_names[self.player_turn - 1]
            self.status_label.setText(
                f"{player_name.upper()}: CHOOSE WHICH COSTS MORE!"
            )
        elif self.session.mode == Gamemodes.vsbot:
            self.status_label.setText("CHOOSE FAST AND BEAT THE BOT!")
        else:
            self.status_label.setText("CHOOSE BEFORE TIME RUNS OUT!")
        self.status_label.setStyleSheet(
            "font-size: 22px; color: #00ffb3; background: transparent;"
        )
        self.seconds_left = 15
        self.timer_label.setText(str(self.seconds_left))
        self.timer.start(1000)

    def load_item_image(self, label, image_url, fallback_path):
        pixmap = QPixmap()
        if image_url:
            try:
                response = requests.get(image_url, timeout=5)
                response.raise_for_status()
                pixmap.loadFromData(response.content)
            except requests.RequestException:
                pass

        if pixmap.isNull():
            pixmap = QPixmap(fallback_path)
        label.setPixmap(pixmap.scaled(
            640, 330, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))

    def update_timer(self):
        self.seconds_left -= 1
        self.timer_label.setText(str(self.seconds_left))
        if self.seconds_left <= 0:
            self.timer.stop()
            game_round = self.session.get_current_round()
            if game_round.left_item.price <= game_round.right_item.price:
                timed_out_item = game_round.left_item
            else:
                timed_out_item = game_round.right_item
            self.submit_item(timed_out_item, timed_out=True)

    def make_guess(self, side):
        if self.answer_locked:
            return
        game_round = self.session.get_current_round()
        if side == "left":
            chosen_item = game_round.left_item
        else:
            chosen_item = game_round.right_item
        self.submit_item(chosen_item)

    def submit_item(self, chosen_item, timed_out=False):
        if self.answer_locked:
            return
        self.answer_locked = True
        self.timer.stop()
        self.left_button.setEnabled(False)
        self.right_button.setEnabled(False)

        if self.session.mode == Gamemodes.Multiplayer:
            self.submit_multiplayer_item(chosen_item)
            return

        try:
            result = self.menu_page.service.submit_guess(
                self.session, chosen_item
            )
        except Exception as error:
            QMessageBox.critical(self, "Game Error", str(error))
            self.return_to_menu()
            return

        if self.session.mode == Gamemodes.vsbot:
            round_result = result.user_result
            if result.bot_correct:
                bot_message = "BOT WAS CORRECT +10"
            else:
                bot_message = "BOT WAS WRONG"
        else:
            round_result = result
            bot_message = ""

        if timed_out or not round_result.correct:
            self.menu_page.audio.play_incorrect()
        else:
            self.menu_page.audio.play_correct()

        self.set_score_counter(self.session.score)
        left_price = round_result.left_item.price
        right_price = round_result.right_item.price
        prices = f"${left_price:,.2f}  VS  ${right_price:,.2f}"

        if timed_out:
            message = f"TIME IS UP!  {prices}"
            color = "#ffcc00"
        elif round_result.correct:
            message = f"CORRECT! +{round_result.points_earned}  {prices}"
            color = "#00ffb3"
        else:
            message = f"WRONG!  {prices}"
            color = "#ff4f78"

        if bot_message:
            message = f"{message}  |  {bot_message}"

        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"font-size: 22px; color: {color}; background: transparent;"
        )
        QTimer.singleShot(1400, self.next_round)

    def submit_multiplayer_item(self, chosen_item):
        try:
            result = self.menu_page.service.submit_multiplayer_guess(
                self.session,
                self.player_turn,
                chosen_item
            )
        except Exception as error:
            QMessageBox.critical(self, "Multiplayer Error", str(error))
            self.return_to_menu()
            return

        if result is None:
            self.player_turn = 2
            QMessageBox.information(
                self,
                "Player 2 Turn",
                f"{self.player_names[0]}'s choice is locked.\n\n"
                f"Pass the computer to {self.player_names[1]}."
            )
            self.answer_locked = False
            self.left_button.setEnabled(True)
            self.right_button.setEnabled(True)
            self.status_label.setText(
                f"{self.player_names[1].upper()}: CHOOSE WHICH COSTS MORE!"
            )
            self.status_label.setStyleSheet(
                "font-size: 22px; color: #ffd34d; background: transparent;"
            )
            self.seconds_left = 15
            self.timer_label.setText(str(self.seconds_left))
            self.timer.start(1000)
            return

        self.set_score_counter(self.session.score)
        player_one_result = result.player_one_result
        player_two_result = result.player_two_result
        if player_one_result.correct or player_two_result.correct:
            self.menu_page.audio.play_correct()
        else:
            self.menu_page.audio.play_incorrect()
        left_price = player_one_result.left_item.price
        right_price = player_one_result.right_item.price

        if player_one_result.correct:
            player_one_text = "CORRECT"
        else:
            player_one_text = "WRONG"

        if player_two_result.correct:
            player_two_text = "CORRECT"
        else:
            player_two_text = "WRONG"

        self.status_label.setText(
            f"P1 {player_one_text}  |  P2 {player_two_text}  |  "
            f"${left_price:,.2f} VS ${right_price:,.2f}"
        )
        self.status_label.setStyleSheet(
            "font-size: 22px; color: #00ffb3; background: transparent;"
        )
        QTimer.singleShot(1800, self.next_round)

    def next_round(self):
        if self.session is None:
            return
        if self.session.is_finished():
            if self.session.mode == Gamemodes.Multiplayer:
                if self.session.score > self.session.player_two_score:
                    result_text = f"{self.player_names[0].upper()} WINS!"
                    outcome = "win"
                elif self.session.player_two_score > self.session.score:
                    result_text = f"{self.player_names[1].upper()} WINS!"
                    outcome = "lose"
                else:
                    result_text = "IT IS A TIE!"
                    outcome = "tie"

                self.open_result_screen(
                    result_text,
                    f"{self.player_names[0]}: {self.session.score}  |  "
                    f"{self.player_names[1]}: {self.session.player_two_score}",
                    f"{len(self.session.rounds)} rounds completed",
                    outcome
                )
                return

            if self.session.mode == Gamemodes.vsbot:
                if self.session.score > self.session.bot_score:
                    result_text = "YOU WIN!"
                    outcome = "win"
                elif self.session.bot_score > self.session.score:
                    result_text = "YOU LOST!"
                    outcome = "lose"
                else:
                    result_text = "IT IS A TIE!"
                    outcome = "tie"

                self.open_result_screen(
                    result_text,
                    f"YOU: {self.session.score}  |  BOT: "
                    f"{self.session.bot_score}",
                    f"Correct answers: {self.session.rounds_won} / "
                    f"{len(self.session.rounds)}",
                    outcome
                )
                return

            if self.session.rounds_won > len(self.session.rounds) / 2:
                result_text = "YOU WON!"
                outcome = "win"
            else:
                result_text = "YOU LOST!"
                outcome = "lose"
            self.open_result_screen(
                result_text,
                f"SCORE: {self.session.score}",
                f"Correct answers: {self.session.rounds_won} / "
                f"{len(self.session.rounds)}",
                outcome
            )
            return
        if self.session.mode == Gamemodes.Multiplayer:
            self.player_turn = 1
        self.show_round()

    def open_result_screen(self, title, score_text, details, outcome):
        self.timer.stop()
        if self.result_page is None:
            QMessageBox.information(
                self,
                "Game Complete",
                f"{title}\n\n{score_text}\n{details}"
            )
            self.return_to_menu()
            return
        self.result_page.show_result(
            title,
            score_text,
            details,
            outcome,
            self.replay_session,
            self.return_to_menu
        )

    def replay_session(self):
        if self.session is None:
            self.return_to_menu()
            return

        mode = self.session.mode
        if mode == Gamemodes.Singleplayer:
            self.menu_page.start_solo_game()
            return
        if mode == Gamemodes.vsbot:
            self.menu_page.start_bot_game()
            return

        player_one_id = self.session.user_id
        player_two_id = self.session.player_two_id
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            new_session = self.menu_page.service.start_multiplayer_game(
                player_one_id,
                player_two_id
            )
        except Exception as error:
            QMessageBox.critical(self, "Multiplayer Error", str(error))
            return
        finally:
            QApplication.restoreOverrideCursor()

        self.menu_page.current_session = new_session
        self.start_session(new_session, self.player_names)

    def return_to_menu(self):
        self.timer.stop()
        self.session = None
        self.player_turn = 1
        self.main_stack.setCurrentWidget(self.menu_page)
