\About the game

PriceGuessr is an entertainment game built on the OOP paradigm. The goal is to guess which of two items taken from the eBay marketplace is more expensive. The game has 3 modes: Solo, Multiplayer and VsBot. It's an ideal game when you want to pass time quickly during a boring moment. To track progress, the game offers two options: a game history, where you can see the last 10 games, and analytics, which shows your progress in more detail.

Requirements
Windows
Python 3
Internet connection
API data
How to run the game
Make sure Python 3.13 is installed (winget install --exact --id Python.Python.3.13)
Run in the console: py -3.13 -m pip install -r requirements.txt
Also in the console, run: py -3.13 main.py
Modules used
pyqt5 (visuals)
pygame (audio)
requests (sending API requests)
sqlite3 (local database)
sys (starting and closing the application)
random (picking random items)
base64 (encoding for the API)
enum (defining game modes)
pathlib (handling directories)
What is what

Main files

main.py launches the application, creates the main menu and connects the screens to each other.
Config.py stores the eBay API data.
requirements.txt contains the Python libraries the project needs.

Game logic

adaptive.py chooses the next product category based on the player's previous answers.
analytics.py calculates statistics for games, wins, scores and best results.
audio.py manages background music and sound effects.
auth.py manages user registration and login.
bot.py manages the bot's choices, scores and results.
database.py connects to SQLite and creates the required tables.
ebay_api.py connects to the eBay API and retrieves product information.
game.py creates rounds, checks answers, calculates scores and saves results.
history.py retrieves the user's previous games from the database.
items.py selects products and converts API data into game objects.
models.py describes the user, product, round, session and result objects.
multiplayer.py manages the two-player game, answers, scores and the winner.
paths.py defines the paths for images, audio and the database.
service.py connects the interface, game logic, API and database to each other.

User interface

active_game.py displays products, loads images and processes the player's answers.
analytics_screen.py displays statistics, progress and the score chart.
history_screen.py displays and filters the user's previous games.
result_screen.py displays the winner, the final score and the replay buttons.

Resources

assets/images/ contains backgrounds, logos, buttons, icons and other graphics.
assets/audio/ contains background music and sound effects.
How the code flows
Startup: main.py → service.py → database.py → main menu
Login: main.py → service.py → auth.py → database.py
Starting a game: main.py → service.py → adaptive.py → game.py
Fetching a product: game.py → items.py → ebay_api.py → eBay API
Displaying a product: game.py → service.py → active_game.py
Checking an answer: active_game.py → service.py → game.py → models.py
Ending a game: game.py → database.py → priceguessr.db
Showing results: game.py → active_game.py → result_screen.py
History and analytics: history_screen.py → service.py → history.py → database.py, and analytics_screen.py → service.py → analytics.py → database.py
Authors and contributions
Nikoloz Lomtadze: game logic
Lile Tvildiani: design and interface
About AI

As for AI, we used it as an assistant, not as a code creator!!

Project planning (what to do, and in what order)
Tips in the code
Testing and finding bugs
PNG generation

The project has 3000 lines of code, 100% of which is Python. Thank you for your interest and for reading all the way down here.

The last three items sit under the AI section in the original, so they look like the ways you used AI.

This also shows my earlier CV description was partly wrong: you did the game logic, and your teammate did the design and interface. Here's a corrected version:

PriceGuessr: Python desktop game (team project)

Developed the game logic for a PyQt5 desktop game where players guess which of two eBay items is more expensive, with Solo, Multiplayer, and VsBot modes
Integrated the eBay API for live item data, plus SQLite for user accounts, game history, and analytics
Designed the project with object-oriented programming, about 3,000 lines of Python
