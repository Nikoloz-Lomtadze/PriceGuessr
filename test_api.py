from Config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_ENVIRONMENT

from priceguessr.service import PriceGuessrService
from priceguessr.models import Gamemodes


service = PriceGuessrService(
    "priceguessr.db",
    EBAY_CLIENT_ID,
    EBAY_CLIENT_SECRET,
    EBAY_ENVIRONMENT
)

user = service.login("service_test", "123")

if user is None:
    user = service.signup("service_test", "123")
    print("User created")
else:
    print("User logged in")

session = service.start_game(user.user_id, Gamemodes.Singleplayer)

print("Game started from service")
print("Rounds:", len(session.rounds))

while not session.is_finished():
    current_round = session.get_current_round()

    print()
    print("Round:", current_round.round_number)
    print("Left:", current_round.left_item.name, "-", current_round.left_item.price)
    print("Right:", current_round.right_item.name, "-", current_round.right_item.price)

    # automatic test choice
    result = service.submit_guess(session, current_round.left_item)

    if result.correct:
        print("Correct")
    else:
        print("Wrong")

    print("Score:", session.score)

print()
print("Game finished")
print("Final score:", session.score)
print("Rounds won:", session.rounds_won)

print()
print("History:")
history = service.get_history(user.user_id)

for match in history:
    print(match.match_id, match.mode, match.rounds_won, match.points_count)

print()
print("Analytics:")
analytics = service.get_analytics(user.user_id)

for row in analytics:
    print(row)