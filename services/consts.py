from enum import Enum


class Color(Enum):
    RANDOM = "random"
    BLACK = "black"
    WHITE = "white"


class Variant(Enum):
    STANDARD = "Standard"
    CRAZY_HOUSE = "Crazyhouse"
    CHESS_960 = "Chess960"
    KING_OF_THE_HILL = "King of the hill"
    THREE_CHECK = "Three-check"
    ANTICHESS = "Antichess"
    ATOMIC = "Atomic"
    HORDE = "Horde"
    RACING = "Racing"
    KINGS = "Kings"


class TimeMode(Enum):
    REAL_TIME = "Real time"
    CORRESPONDENCE = "Correspondence"
    UNLIMITED = "Unlimited"


# Game

MINUTES_PER_SIDE = 11.0
INCREMENT_MINUTES = 4

VARIANT = Variant.STANDARD.value
TIME_MODE = TimeMode.REAL_TIME.value
COLOR = Color.RANDOM.value
COLOR_BUTTON_XPATH = "//*[@name='color'][@value='{}']".format(COLOR)

# Chromedriver

CHROME_DRIVER_DIR_NAME = "{}/Chrome_Driver"
DELAY_SEC = 3


# Website

NUMBER_LOGIN_ATTEMPTS = 3
MAIN_WEBSITE = "https://lichess.org/"
LOGIN_URL = "https://lichess.org/login?referrer=/"
GAME_PREFERENCES_URL = "https://lichess.org/account/preferences/game-display"
GAME_SETUP_URL = "https://lichess.org/setup/hook"

USERNAME_ELEM_ID = "form3-username"
PASSWORD_ELEM_ID = "form3-password"

LOGIN_BUTTON_XPATH = '//*[@id="main-wrap"]/main/form/div[1]/button'
LOGIN_ERROR_MSG = "Invalid username or password"
LOGIN_CLASS_NAME_ERROR = "error"

BUTTON_TEXT_XPATH = '//button[text()="{}"]'
BUTTON_SOUND_XPATH = BUTTON_TEXT_XPATH.format("Sound")
BUTTON_SPEECH_XPATH = BUTTON_TEXT_XPATH.format("Speech")

SCRIPT_LINE = "arguments[0].setAttribute('{}',arguments[1])"
EXE_SCRIPT_CHECKED = SCRIPT_LINE.format("checked")
EXE_SCRIPT_VALUE = SCRIPT_LINE.format("value")


