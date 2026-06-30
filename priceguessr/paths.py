#AI-თი დავწერე ეს, რომ გამართოს Path-ები
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = PROJECT_DIR / "assets" / "images"
AUDIO_DIR = PROJECT_DIR / "assets" / "audio"
DATABASE_PATH = PROJECT_DIR / "priceguessr.db"


def asset_path(filename):
    """Return the absolute path of an image in the assets folder."""
    return str(IMAGES_DIR / filename)


def audio_path(filename):
    """Return the absolute path of a sound in the audio folder."""
    return str(AUDIO_DIR / filename)
