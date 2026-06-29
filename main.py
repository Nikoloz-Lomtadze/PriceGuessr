import sqlite3
import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QHBoxLayout, QVBoxLayout, QFrame,
                             QStackedWidget, QMessageBox, QMainWindow,
                             QInputDialog)
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QIcon, QPainter
from PyQt5.QtCore import Qt, QSize, QEvent

from Config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT
from priceguessr.models import Gamemodes
from priceguessr.paths import DATABASE_PATH, asset_path
from priceguessr.service import PriceGuessrService
from priceguessr.ui.active_game import ActiveGameScreen
from priceguessr.ui.result_screen import ResultScreen

class MainMenu(QWidget):
    """Login, tutorial, and game-mode selection screen."""

    def __init__(self, main_stack=None):
        super().__init__()
        self.main_stack = main_stack
        self.game_page = None
        self.service = PriceGuessrService(
            str(DATABASE_PATH),
            EBAY_CLIENT_ID,
            EBAY_CLIENT_SECRET,
            EBAY_ENVIRONMENT
        )
        self.current_user = None
        self.current_session = None
        self.build_ui()

    def get_sprite(self, sheet_path, index, item_width, item_height):
        """Return one icon from a horizontal sprite sheet."""
        try:
            sheet = QPixmap(sheet_path)
            if sheet.isNull():
                return QPixmap(item_width, item_height)
            return sheet.copy(index * item_width, 0, item_width, item_height)
        except Exception:
            return QPixmap(item_width, item_height)

    def build_ui(self):
        self.setWindowTitle('PriceGuessr - Main Menu (1080p)')
        self.setFixedSize(1920, 1080)

        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial Black', 'Impact', sans-serif;
                color: white;
            }
            #MainWindowFrame {
                background-color: #31115c;
                border: 8px solid #17052e;
                border-radius: 48px;
            }
            #MainContainerBox {
                background-color: #240a46;
                border: 8px solid #17052e;
                border-top-left-radius: 0px;
                border-top-right-radius: 38px;
                border-bottom-right-radius: 38px;
                border-bottom-left-radius: 38px;
            }
            #TutorialBox {
                background-color: #1a0438;
                border: 8px solid #17052e;
                border-radius: 38px;
            }
            .TabButton {
                font-size: 32px;
                font-weight: 900;
                border: 8px solid #17052e;
                border-bottom: none;
                border-top-left-radius: 28px;
                border-top-right-radius: 28px;
                padding-bottom: 8px;
            }
            .TabActive {
                background-color: #240a46;
                color: #00ffb3;
                border-color: #17052e;
            }
            .TabInactive {
                background-color: #1a0438;
                color: #8c73b3;
                border-color: #17052e;
                border-bottom: 8px solid #17052e;
            }
            QLineEdit {
                background-color: #17052e;
                border: 6px solid #000000;
                border-radius: 22px;
                padding: 10px 20px;
                font-size: 30px;
                font-weight: bold;
                color: #ffffff;
            }
            QPushButton {
                border: none;
                background: none;
            }

            #PopupContainer {
                background-color: #1a0438;
                border: 8px solid #17052e;
                border-radius: 44px;
            }
            #ClosePopupBtn {
                background-color: #ff0055;
                border: 4px solid #17052e;
                border-radius: 12px;
                font-size: 20px;
                font-weight: bold;
                color: white;
            }
            #ClosePopupBtn:hover {
                background-color: #ff3377;
            }

            .ModeCard {
                background-color: #240a46;
                border: 6px solid #17052e;
                border-radius: 24px;
            }

            .ModeTitle {
                font-size: 22px;
                font-weight: 900;
                color: #ffffff;
                background-color: rgba(23, 5, 46, 0.85);
                border-bottom-left-radius: 18px;
                border-bottom-right-radius: 18px;
                padding: 12px;
            }

            .ModeCard:hover {
                border-color: #00ffb3;
            }
        """)

        palette = QPalette()
        bg_pixmap = QPixmap(asset_path("background.png")).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(bg_pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(25, 25, 25, 25)

        window_frame = QFrame()
        window_frame.setObjectName("MainWindowFrame")
        outer_layout.addWidget(window_frame)

        canvas = QWidget(window_frame)
        canvas.setFixedSize(1870, 1030)

        lang_btn = QPushButton("EN", canvas)
        lang_btn.setFixedSize(195, 68)
        lang_btn.setStyleSheet("background-color: #17052e; border-radius: 18px; font-size: 20px; font-weight: bold; color: white;")
        lang_btn.move(40, 40)

        logo_label = QLabel(canvas)
        logo_label.setPixmap(QPixmap(asset_path("logo.png")).scaled(1000, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setFixedSize(1000, 250)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.move(435, 40)

        main_container_box = QFrame(canvas)
        main_container_box.setObjectName("MainContainerBox")
        main_container_box.setFixedSize(960, 560)
        main_container_box.move(40, 420)

        self.tab_login = QPushButton("LOG IN", canvas)
        self.tab_login.setProperty("class", "TabButton TabActive")
        self.tab_login.setFixedSize(360, 98)
        self.tab_login.move(40, 330)

        self.tab_signup = QPushButton("SIGN UP", canvas)
        self.tab_signup.setProperty("class", "TabButton TabInactive")
        self.tab_signup.setFixedSize(360, 98)
        self.tab_signup.move(412, 330)

        self.tab_login.raise_()
        self.tab_signup.raise_()

        mascot_view = QLabel(main_container_box)
        mascot_view.setPixmap(QPixmap(asset_path("mascot-bag.png")).scaled(405, 405, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        mascot_view.setFixedSize(405, 405)
        mascot_view.move(35, 75)

        self.page_switcher = QStackedWidget(main_container_box)
        self.page_switcher.setFixedSize(510, 510)
        self.page_switcher.move(420, 25)

        login_widget = QWidget()
        login_layout = QVBoxLayout(login_widget)
        login_layout.setContentsMargins(0, 20, 0, 10)
        login_layout.setSpacing(10)

        login_title = QLabel("ENTER YOUR NAME")
        login_title.setStyleSheet("font-size: 26px; color: #a385cc; font-weight: bold;")
        login_layout.addWidget(login_title, alignment=Qt.AlignCenter)

        self.login_name_input = QLineEdit()
        self.login_name_input.setPlaceholderText("Enter username...")
        self.login_name_input.setFixedSize(460, 65)
        login_layout.addWidget(self.login_name_input, alignment=Qt.AlignCenter)

        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText("Enter password...")
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_password_input.setFixedSize(460, 65)
        login_layout.addWidget(self.login_password_input, alignment=Qt.AlignCenter)

        login_layout.addSpacing(5)

        btn_start_game = QPushButton()
        btn_start_game.setIcon(QIcon(asset_path("start-button.png")))
        btn_start_game.setIconSize(QSize(510, 143))
        btn_start_game.setFixedSize(510, 143)
        login_layout.addWidget(btn_start_game, alignment=Qt.AlignCenter)

        sub_buttons_login = QHBoxLayout()
        sub_buttons_login.setSpacing(20)
        sub_buttons_login.setAlignment(Qt.AlignCenter)

        btn_action_signup = QPushButton()
        btn_action_signup.setIcon(QIcon(asset_path("sign-up-button.png")))
        btn_action_signup.setIconSize(QSize(220, 83))
        btn_action_signup.setFixedSize(220, 83)

        btn_exit_app1 = QPushButton()
        btn_exit_app1.setIcon(QIcon(asset_path("exit-button.png")))
        btn_exit_app1.setIconSize(QSize(220, 83))
        btn_exit_app1.setFixedSize(220, 83)

        sub_buttons_login.addWidget(btn_action_signup)
        sub_buttons_login.addWidget(btn_exit_app1)
        login_layout.addLayout(sub_buttons_login)
        self.page_switcher.addWidget(login_widget)

        signup_widget = QWidget()
        signup_layout = QVBoxLayout(signup_widget)
        signup_layout.setContentsMargins(0, 20, 0, 10)
        signup_layout.setSpacing(10)

        signup_title = QLabel("CREATE NEW ACCOUNT")
        signup_title.setStyleSheet("font-size: 26px; color: #a385cc; font-weight: bold;")
        signup_layout.addWidget(signup_title, alignment=Qt.AlignCenter)

        self.signup_name_input = QLineEdit()
        self.signup_name_input.setPlaceholderText("Enter username...")
        self.signup_name_input.setFixedSize(460, 65)
        signup_layout.addWidget(self.signup_name_input, alignment=Qt.AlignCenter)

        self.signup_password_input = QLineEdit()
        self.signup_password_input.setPlaceholderText("Create password...")
        self.signup_password_input.setEchoMode(QLineEdit.Password)
        self.signup_password_input.setFixedSize(460, 65)
        signup_layout.addWidget(self.signup_password_input, alignment=Qt.AlignCenter)

        signup_layout.addSpacing(5)

        btn_register = QPushButton()
        btn_register.setIcon(QIcon(asset_path("start-button.png")))
        btn_register.setIconSize(QSize(510, 143))
        btn_register.setFixedSize(510, 143)
        signup_layout.addWidget(btn_register, alignment=Qt.AlignCenter)

        sub_buttons_signup = QHBoxLayout()
        sub_buttons_signup.setSpacing(20)
        sub_buttons_signup.setAlignment(Qt.AlignCenter)

        btn_action_login = QPushButton()
        btn_action_login.setIcon(QIcon(asset_path("log-in-button.png")))
        btn_action_login.setIconSize(QSize(220, 83))
        btn_action_login.setFixedSize(220, 83)

        btn_exit_app2 = QPushButton()
        btn_exit_app2.setIcon(QIcon(asset_path("exit-button.png")))
        btn_exit_app2.setIconSize(QSize(220, 83))
        btn_exit_app2.setFixedSize(220, 83)

        sub_buttons_signup.addWidget(btn_action_login)
        sub_buttons_signup.addWidget(btn_exit_app2)
        signup_layout.addLayout(sub_buttons_signup)
        self.page_switcher.addWidget(signup_widget)

        def set_view_mode(index):
            self.page_switcher.setCurrentIndex(index)
            if index == 0:
                self.tab_login.setProperty("class", "TabButton TabActive")
                self.tab_signup.setProperty("class", "TabButton TabInactive")
            else:
                self.tab_login.setProperty("class", "TabButton TabInactive")
                self.tab_signup.setProperty("class", "TabButton TabActive")

            self.tab_login.style().unpolish(self.tab_login)
            self.tab_login.style().polish(self.tab_login)
            self.tab_signup.style().unpolish(self.tab_signup)
            self.tab_signup.style().polish(self.tab_signup)

        self.tab_login.clicked.connect(lambda: set_view_mode(0))
        self.tab_signup.clicked.connect(lambda: set_view_mode(1))
        btn_action_signup.clicked.connect(lambda: set_view_mode(1))
        btn_action_login.clicked.connect(lambda: set_view_mode(0))

        right_panel = QFrame(canvas)
        right_panel.setObjectName("TutorialBox")
        right_panel.setFixedSize(740, 560)
        right_panel.move(1090, 420)

        tutorial_layout = QVBoxLayout(right_panel)
        tutorial_layout.setContentsMargins(20, 20, 20, 15)
        tutorial_layout.setSpacing(10)

        tut_title = QLabel("HOW TO PLAY")
        tut_title.setStyleSheet("font-size: 36px; color: #00ffb3; font-weight: 900;")
        tut_title.setAlignment(Qt.AlignCenter)
        tutorial_layout.addWidget(tut_title)

        self.tut_switcher = QStackedWidget()
        tutorial_layout.addWidget(self.tut_switcher)

        slide1_widget = QWidget()
        slide1_layout = QVBoxLayout(slide1_widget)
        slide1_layout.setContentsMargins(0, 0, 0, 0)
        tut_img1 = QLabel()
        tut_img1.setPixmap(QPixmap(asset_path("how-to-play-illustration.png")).scaled(680, 290, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        tut_img1.setFixedSize(680, 290)
        tut_img1.setAlignment(Qt.AlignCenter)
        slide1_layout.addWidget(tut_img1)
        tut_caption1 = QLabel("1. CHOOSE A CATEGORY\nSelect your favorite item deck")
        tut_caption1.setStyleSheet("font-size: 22px; color: #ffffff; font-weight: bold; line-height: 28px;")
        tut_caption1.setAlignment(Qt.AlignCenter)
        slide1_layout.addWidget(tut_caption1)
        self.tut_switcher.addWidget(slide1_widget)

        slide2_widget = QWidget()
        slide2_layout = QVBoxLayout(slide2_widget)
        slide2_layout.setContentsMargins(0, 0, 0, 0)
        tut_img2 = QLabel()
        tut_img2.setPixmap(QPixmap(asset_path("how-to-play-illustration.png")).scaled(680, 290, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        tut_img2.setFixedSize(680, 290)
        tut_img2.setAlignment(Qt.AlignCenter)
        slide2_layout.addWidget(tut_img2)
        tut_caption2 = QLabel("2. STUDY THE ITEMS\nLook closely at the items displayed")
        tut_caption2.setStyleSheet("font-size: 22px; color: #ffffff; font-weight: bold; line-height: 28px;")
        tut_caption2.setAlignment(Qt.AlignCenter)
        slide2_layout.addWidget(tut_caption2)
        self.tut_switcher.addWidget(slide2_widget)

        slide3_widget = QWidget()
        slide3_layout = QVBoxLayout(slide3_widget)
        slide3_layout.setContentsMargins(0, 0, 0, 0)
        tut_img3 = QLabel()
        tut_img3.setPixmap(QPixmap(asset_path("how-to-play-illustration.png")).scaled(680, 290, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        tut_img3.setFixedSize(680, 290)
        tut_img3.setAlignment(Qt.AlignCenter)
        slide3_layout.addWidget(tut_img3)
        tut_caption3 = QLabel("3. GUESS THE PRICE\nPick the item that costs more")
        tut_caption3.setStyleSheet("font-size: 22px; color: #ffffff; font-weight: bold; line-height: 28px;")
        tut_caption3.setAlignment(Qt.AlignCenter)
        slide3_layout.addWidget(tut_caption3)
        self.tut_switcher.addWidget(slide3_widget)

        pagination_layout = QHBoxLayout()
        pagination_layout.setSpacing(15)
        pagination_layout.setAlignment(Qt.AlignCenter)

        btn_prev = QPushButton()
        btn_prev.setIcon(QIcon(asset_path("left.png")))
        btn_prev.setIconSize(QSize(60, 60))
        btn_prev.setFixedSize(60, 60)
        pagination_layout.addWidget(btn_prev)

        dots_row_layout = QHBoxLayout()
        dots_row_layout.setSpacing(12)

        self.dot_labels = []
        total_pages = self.tut_switcher.count()
        for i in range(total_pages):
            dot_label = QLabel()
            dot_label.setFixedSize(18, 18)
            dots_row_layout.addWidget(dot_label)
            self.dot_labels.append(dot_label)

        pagination_layout.addLayout(dots_row_layout)

        btn_next = QPushButton()
        btn_next.setIcon(QIcon(asset_path("right.png")))
        btn_next.setIconSize(QSize(60, 60))
        btn_next.setFixedSize(60, 60)
        pagination_layout.addWidget(btn_next)
        tutorial_layout.addLayout(pagination_layout)

        def update_pagination_dots():
            active_idx = self.tut_switcher.currentIndex()
            for idx, label in enumerate(self.dot_labels):
                asset_file = asset_path("teal.png") if idx == active_idx else asset_path("white.png")
                pix = QPixmap(asset_file).scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                label.setPixmap(pix)

        update_pagination_dots()

        def cycle_tutorial_page(direction):
            current_idx = self.tut_switcher.currentIndex()
            total_pages = self.tut_switcher.count()
            new_idx = (current_idx + direction) % total_pages
            self.tut_switcher.setCurrentIndex(new_idx)
            update_pagination_dots()

        btn_prev.clicked.connect(lambda: cycle_tutorial_page(-1))
        btn_next.clicked.connect(lambda: cycle_tutorial_page(1))

        footer_container = QWidget(canvas)
        footer_container.setFixedSize(1790, 80)
        footer_container.move(40, 990)
        footer_layout = QHBoxLayout(footer_container)
        footer_layout.setContentsMargins(0, 0, 0, 0)

        cart_icon = QLabel()
        cart_icon.setPixmap(self.get_sprite(asset_path("icons-sheet.png"), 0, 32, 32).scaled(63, 63, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        footer_layout.addWidget(cart_icon, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        footer_layout.addStretch()

        socials_strip = QHBoxLayout()
        socials_strip.setSpacing(24)
        for i in range(1, 6):
            social_item = QLabel()
            icon_asset = self.get_sprite(asset_path("icons-sheet.png"), i, 32, 32)
            social_item.setPixmap(icon_asset.scaled(63, 63, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            socials_strip.addWidget(social_item)
        footer_layout.addLayout(socials_strip)

        self.popup_overlay = QWidget(canvas)
        self.popup_overlay.setFixedSize(1870, 1030)
        self.popup_overlay.move(0, 0)
        self.popup_overlay.setStyleSheet("background-color: rgba(23, 5, 46, 0.88);")
        self.popup_overlay.hide()

        popup_box = QFrame(self.popup_overlay)
        popup_box.setObjectName("PopupContainer")
        popup_box.setFixedSize(980, 620)
        popup_box.move(445, 205)

        popup_layout = QVBoxLayout(popup_box)
        popup_layout.setContentsMargins(30, 20, 30, 40)
        popup_layout.setSpacing(15)

        header_hbox = QHBoxLayout()
        header_hbox.addStretch()

        popup_title = QLabel("SELECT GAME MODE")
        popup_title.setStyleSheet("font-size: 36px; color: #00ffb3; font-weight: 900; margin-left: 55px;")
        header_hbox.addWidget(popup_title, alignment=Qt.AlignCenter)
        header_hbox.addStretch()

        btn_close_popup = QPushButton(" X ")
        btn_close_popup.setObjectName("ClosePopupBtn")
        btn_close_popup.setFixedSize(45, 45)
        btn_close_popup.setCursor(Qt.PointingHandCursor)
        header_hbox.addWidget(btn_close_popup)
        popup_layout.addLayout(header_hbox)

        popup_layout.addSpacing(15)

        cards_hbox = QHBoxLayout()
        cards_hbox.setSpacing(25)
        cards_hbox.setAlignment(Qt.AlignCenter)

        # SOLO
        self.card_solo = QFrame()
        self.card_solo.setProperty("class", "ModeCard")
        self.card_solo.setFixedSize(280, 420)
        self.card_solo.setCursor(Qt.PointingHandCursor)
        layout_solo = QVBoxLayout(self.card_solo)
        layout_solo.setContentsMargins(0, 0, 0, 0)

        img_solo = QLabel()
        img_solo.setPixmap(QPixmap(asset_path("single-player.png")).scaled(280, 340, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        img_solo.setAlignment(Qt.AlignCenter)
        layout_solo.addWidget(img_solo)

        lbl_solo = QLabel("SOLO")
        lbl_solo.setProperty("class", "ModeTitle")
        lbl_solo.setAlignment(Qt.AlignCenter)
        layout_solo.addWidget(lbl_solo)
        cards_hbox.addWidget(self.card_solo)

        # MULTIPLAYER
        self.card_multi = QFrame()
        self.card_multi.setProperty("class", "ModeCard")
        self.card_multi.setFixedSize(280, 420)
        self.card_multi.setCursor(Qt.PointingHandCursor)
        layout_multi = QVBoxLayout(self.card_multi)
        layout_multi.setContentsMargins(0, 0, 0, 0)

        img_multi = QLabel()
        img_multi.setPixmap(QPixmap(asset_path("multiplayer.png")).scaled(280, 340, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        img_multi.setAlignment(Qt.AlignCenter)
        layout_multi.addWidget(img_multi)

        lbl_multi = QLabel("MULTIPLAYER")
        lbl_multi.setProperty("class", "ModeTitle")
        lbl_multi.setAlignment(Qt.AlignCenter)
        layout_multi.addWidget(lbl_multi)
        cards_hbox.addWidget(self.card_multi)

        #  PLAY WITH BOT
        self.card_bot = QFrame()
        self.card_bot.setProperty("class", "ModeCard")
        self.card_bot.setFixedSize(280, 420)
        self.card_bot.setCursor(Qt.PointingHandCursor)
        layout_bot = QVBoxLayout(self.card_bot)
        layout_bot.setContentsMargins(0, 0, 0, 0)

        img_bot = QLabel()
        img_bot.setPixmap(QPixmap(asset_path("play-with-bot.png")).scaled(280, 340, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        img_bot.setAlignment(Qt.AlignCenter)
        layout_bot.addWidget(img_bot)

        lbl_bot = QLabel("PLAY WITH BOT")
        lbl_bot.setProperty("class", "ModeTitle")
        lbl_bot.setAlignment(Qt.AlignCenter)
        layout_bot.addWidget(lbl_bot)
        cards_hbox.addWidget(self.card_bot)

        popup_layout.addLayout(cards_hbox)


        for widget in (self.card_solo, img_solo, lbl_solo):
            widget.setProperty("game_mode", "solo")
            widget.installEventFilter(self)

        for widget in (self.card_multi, img_multi, lbl_multi):
            widget.setProperty("game_mode", "multiplayer")
            widget.installEventFilter(self)

        for widget in (self.card_bot, img_bot, lbl_bot):
            widget.setProperty("game_mode", "bot")
            widget.installEventFilter(self)

        def close_game_modes():
            self.popup_overlay.hide()

        btn_start_game.clicked.connect(self.handle_login)
        btn_register.clicked.connect(self.handle_signup)
        btn_exit_app1.clicked.connect(QApplication.instance().quit)
        btn_exit_app2.clicked.connect(QApplication.instance().quit)
        btn_close_popup.clicked.connect(close_game_modes)

    def show_mode_popup(self):
        self.popup_overlay.show()
        self.popup_overlay.raise_()

    def handle_login(self):
        username = self.login_name_input.text().strip()
        password = self.login_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login", "Enter both username and password.")
            return

        user = self.service.login(username, password)
        if user is None:
            QMessageBox.warning(self, "Login", "Username or password is incorrect.")
            return

        self.current_user = user
        self.show_mode_popup()

    def handle_signup(self):
        username = self.signup_name_input.text().strip()
        password = self.signup_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Sign Up", "Enter both username and password.")
            return

        try:
            self.current_user = self.service.signup(username, password)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Sign Up", "That username already exists.")
            return

        QMessageBox.information(self, "Sign Up", "Account created successfully.")
        self.show_mode_popup()

    def start_solo_game(self):
        if self.current_user is None:
            QMessageBox.warning(self, "Game", "Log in before starting a game.")
            return

        self.popup_overlay.hide()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.current_session = self.service.start_game(
                self.current_user.user_id,
                Gamemodes.Singleplayer
            )
        except Exception as error:
            QMessageBox.critical(self, "Game Error", str(error))
            return
        finally:
            QApplication.restoreOverrideCursor()

        if self.game_page is None:
            QMessageBox.critical(self, "Game Error", "Game screen is not ready.")
            return
        self.game_page.start_session(self.current_session)

    def start_bot_game(self):
        if self.current_user is None:
            QMessageBox.warning(self, "Game", "Log in before starting a game.")
            return

        self.popup_overlay.hide()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.current_session = self.service.start_game(
                self.current_user.user_id,
                Gamemodes.vsbot
            )
        except Exception as error:
            QMessageBox.critical(self, "Bot Game Error", str(error))
            return
        finally:
            QApplication.restoreOverrideCursor()

        if self.game_page is None:
            QMessageBox.critical(self, "Game Error", "Game screen is not ready.")
            return
        self.game_page.start_session(self.current_session)

    def start_multiplayer_game(self):
        if self.current_user is None:
            QMessageBox.warning(self, "Game", "Log in before starting a game.")
            return

        player_two_name, accepted = QInputDialog.getText(
            self,
            "Local Multiplayer",
            "Player 2 name:"
        )
        if not accepted:
            return
        player_two_name = player_two_name.strip()
        if not player_two_name:
            QMessageBox.warning(
                self,
                "Local Multiplayer",
                "Enter a name for Player 2."
            )
            return

        guest_username = f"__local_player_two_{self.current_user.user_id}__"
        conn = self.service.database.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = ?",
                (guest_username,)
            )
            row = cursor.fetchone()
            if row is None:
                cursor.execute(
                    "INSERT INTO users (username, password) VALUES (?, ?)",
                    (guest_username, "local-multiplayer")
                )
                conn.commit()
                player_two_id = cursor.lastrowid
            else:
                player_two_id = row["id"]
        finally:
            conn.close()

        self.popup_overlay.hide()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.current_session = self.service.start_multiplayer_game(
                self.current_user.user_id,
                player_two_id
            )
        except Exception as error:
            QMessageBox.critical(self, "Multiplayer Error", str(error))
            return
        finally:
            QApplication.restoreOverrideCursor()

        if self.game_page is None:
            QMessageBox.critical(self, "Game Error", "Game screen is not ready.")
            return
        self.game_page.start_session(
            self.current_session,
            (self.current_user.username, player_two_name)
        )

    def show_unavailable_mode(self, mode_name):
        QMessageBox.information(
            self,
            mode_name,
            f"{mode_name} UI is connected, but its backend rules are not implemented yet."
        )

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            selected_mode = obj.property("game_mode")

            if selected_mode == "solo":
                self.start_solo_game()
                return True
            if selected_mode == "multiplayer":
                self.start_multiplayer_game()
                return True
            if selected_mode == "bot":
                self.start_bot_game()
                return True

        return super().eventFilter(obj, event)


class GameMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1920, 1080)
        self.setWindowTitle("PriceGuessr - Game Client")

        self.main_stack = QStackedWidget()
        self.setCentralWidget(self.main_stack)

        self.menu_page = MainMenu(self.main_stack)
        self.game_page = ActiveGameScreen(self.menu_page, self.main_stack)
        self.result_page = ResultScreen(self.main_stack)
        self.game_page.result_page = self.result_page
        self.menu_page.game_page = self.game_page

        self.main_stack.addWidget(self.menu_page)
        self.main_stack.addWidget(self.game_page)
        self.main_stack.addWidget(self.result_page)
        self.main_stack.setCurrentWidget(self.menu_page)

        self.background_pixmap = QPixmap(asset_path("background.png"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameMainWindow()
    ex.show()
    sys.exit(app.exec_())
