from priceguessr.database import Database
from priceguessr.auth import AuthManager
from priceguessr.ebay_api import EbayApi
from priceguessr.items import EbayItemProvider
from priceguessr.game import GameManager
from priceguessr.history import MatchHistory
from priceguessr.analytics import Analytics
from priceguessr.adaptive import CategoryAdapter
from priceguessr.models import Gamemodes


class PriceGuessrService:
    def __init__(self, dbname, client_id, client_secret, environment):
        self.database = Database(dbname)

        self.auth_manager = AuthManager(self.database)

        self.ebay_api = EbayApi(client_id, client_secret, environment)
        self.item_provider = EbayItemProvider(self.ebay_api)

        self.game_manager = GameManager(self.database, self.item_provider)

        self.history_manager = MatchHistory(self.database)
        self.analytics_manager = Analytics(self.database)
        self.category_adapter = CategoryAdapter(self.database)

    def signup(self, username, password):
        return self.auth_manager.signup(username, password)

    def login(self, username, password):
        return self.auth_manager.login(username, password)

    def start_game(self, user_id, mode):
        category = None

        if mode == Gamemodes.Singleplayer:
            category = self.category_adapter.get_next_category(user_id)

        return self.game_manager.start_game(user_id, mode, category)

    def submit_guess(self, session, chosen_item):
        return self.game_manager.submit_guess(session, chosen_item)

    def get_history(self, user_id):
        return self.history_manager.get_last_matches(user_id)

    def get_analytics(self, user_id):
        return self.analytics_manager.get_mode_stats(user_id)