from Config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT

from priceguessr.database import Database
from priceguessr.auth import AuthManager
from priceguessr.ebay_api import EbayApi
from priceguessr.items import EbayItemProvider
from priceguessr.game import GameManager
from priceguessr.models import Gamemodes,Matchrecord


database = Database("priceguessr.db")
auth = AuthManager(database)


if user is None:
    user = auth.signup("test", "123")
    print("Test user created")
else:
    print("Test user logged in")

api = EbayApi(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT)
item_provider = EbayItemProvider(api)

game_manager = GameManager(database, item_provider)

session = game_manager.start_game(user.user_id, Gamemodes.Singleplayer)

print("Game started")
print("Rounds created:", len(session.rounds))

while not session.is_finished():
    current_round = session.get_current_round()

    print()
    print("Round:", current_round.round_number)
    print("Left:", current_round.left_item.name, "-", current_round.left_item.price)
    print("Right:", current_round.right_item.name, "-", current_round.right_item.price)

    # For testing, always choose left item
    result = game_manager.submit_guess(session, current_round.left_item)

    if result.correct:
        print("Result: Correct")
    else:
        print("Result: Wrong")

    print("Correct item:", result.correct_item.name)
    print("Current score:", session.score)
    print("Rounds won:", session.rounds_won)

print()
print("Game finished")
print("Final score:", session.score)
print("Rounds won:", session.rounds_won)

conn = database.connect()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) AS count FROM games")
games_count = cursor.fetchone()["count"]

cursor.execute("SELECT COUNT(*) AS count FROM game_rounds")
rounds_count = cursor.fetchone()["count"]

conn.close()

print()
print("Saved games in database:", games_count)
print("Saved rounds in database:", rounds_count)