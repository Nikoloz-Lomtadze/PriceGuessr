from priceguessr.adaptive import CategoryAdapter
from priceguessr.analytics import Analytics
from priceguessr.auth import AuthManager
from priceguessr.bot import BotManager
from priceguessr.database import Database
from priceguessr.ebay_api import EbayApi
from priceguessr.game import GameManager
from priceguessr.history import MatchHistory
from priceguessr.items import EbayItemProvider
from priceguessr.models import Gamemodes
from priceguessr.multiplayer import MultiplayerManager

# მოცემული ფაილი გამართავს: თამაშის დაწყებას, არჩევნებს, ანალიტიკასა და ისოტირას

class PriceGuessrService:
    def __init__(self, dbname, client_id, client_secret, environment):
        self.database = Database(dbname) #ბაზა
        self.auth_manager = AuthManager(self.database) #login/signup

        self.ebay_api = EbayApi(client_id, client_secret, environment)
        self.item_provider = EbayItemProvider(self.ebay_api) #eby api

        self.game_manager = GameManager(self.database, self.item_provider) #game manager
        self.bot_manager = BotManager(self.database, self.item_provider) #bot manager
        self.multiplayer_manager = MultiplayerManager( #multiplayer
            self.database,
            self.item_provider
        )

        self.history_manager = MatchHistory(self.database) #match history query
        self.analytics_manager = Analytics(self.database) # alatikia
        self.category_adapter = CategoryAdapter(self.database) #algorith to adapt

    def signup(self, username, password):
        return self.auth_manager.signup(username, password) #user ობიექტი

    def login(self, username, password):
        return self.auth_manager.login(username, password) # user ონიექტი

    def start_game(self, user_id, mode): #დაიწყეთ თამაში
        if mode == Gamemodes.vsbot: # ბოტტან თამაში
            return self.bot_manager.start_game(user_id)
        if mode == Gamemodes.Multiplayer:
            raise ValueError("use start_multiplayer_game for multiplayer")

        category = self.category_adapter.get_next_category(user_id) # კატეგორიის მიღება
        return self.game_manager.start_game(user_id, mode, category) # დავიწყოთ თამაში სოლო

    def submit_guess(self, session, chosen_item):
        if session.mode == Gamemodes.vsbot:
            return self.bot_manager.submit_guess(session, chosen_item)
        return self.game_manager.submit_guess(session, chosen_item) # რომელი ნივთი ავირჩიეთ

    def start_multiplayer_game(self, player_one_id, player_two_id): # მულტიპლეიერის დაწყება
        return self.multiplayer_manager.start_game(player_one_id, player_two_id)

    def submit_multiplayer_guess(self, session, player_number, chosen_item): # მულტიპლეიერში რაუნდის დაწყებები
        return self.multiplayer_manager.submit_guess(
            session,
            player_number,
            chosen_item
        )

    def get_history(self, user_id): # ისტორიის მიღება
        return self.history_manager.get_last_matches(user_id)

    def get_analytics(self, user_id): # ანალიტიკის მიღება
        return self.analytics_manager.get_mode_stats(user_id)
