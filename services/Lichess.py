# third-party libraries
import os
import sys
import time
from selenium.common.exceptions import TimeoutException

# inner classes
from classes.ChromeDriver import ChromeDriver
from Utils.logger import logger
from services import consts


class Lichess:

    def __init__(self, username, password):
        if username is None or password is None:
            logger.error("empty username or password.\nExiting...")
            sys.exit()
        self._username = username
        self._password = password

        curr_dir: str = os.getcwd()
        chromedriver_path: str = consts.CHROME_DRIVER_DIR_NAME.format(curr_dir)
        self._driver = ChromeDriver(install_path=chromedriver_path, is_silent=False)
        if self._driver is None:
            logger.error("Chromedriver does not exits.\nExiting...")
            sys.exit()

    def _login(self) -> bool:
        try:
            self._driver.get(consts.LOGIN_URL)
            time.sleep(consts.DELAY_SEC)    # need to find replacement for sleep

            self._driver.send_login_info(self._username, self._password,
                                         consts.USERNAME_ELEM_ID, consts.PASSWORD_ELEM_ID)

            self._driver.click_button_by_xpath(consts.LOGIN_BUTTON_XPATH)
            time.sleep(consts.DELAY_SEC)

            return self._driver.verify_login(consts.MAIN_WEBSITE)

        except TimeoutException:
            logger.error("The page wasn't loaded yet.")
        except Exception as e:
            logger.error(str(e))
        return False

    def _setting_blind_mode_pref(self):
        self._driver.get(consts.GAME_PREFERENCES_URL)
        time.sleep(consts.DELAY_SEC)

        self._driver.elem_execute_script_by_id("irdisplay_blindfold_1", consts.EXE_SCRIPT_CHECKED, "true")
        self._driver.elem_execute_script_by_id("irdisplay_blindfold_0", consts.EXE_SCRIPT_CHECKED, "false")

    def _create_game(self):
        self._driver.get(consts.GAME_SETUP_URL)
        time.sleep(consts.DELAY_SEC)

        self._driver.select_elem_by_visible_text("sf_variant", consts.VARIANT)

        self._driver.select_elem_by_visible_text("sf_timeMode", consts.TIME_MODE)

        self._driver.elem_execute_script_by_name("time", consts.EXE_SCRIPT_VALUE, str(consts.MINUTES_PER_SIDE))
        self._driver.elem_execute_script_by_name("increment", consts.EXE_SCRIPT_VALUE, str(consts.INCREMENT_MINUTES))

        self._driver.elem_execute_script_by_id("sf_mode_1", consts.EXE_SCRIPT_CHECKED, "false")
        self._driver.elem_execute_script_by_id("sf_mode_0", consts.EXE_SCRIPT_CHECKED, "true")

        self._driver.click_button_by_xpath(consts.COLOR_BUTTON_XPATH)

    def _login_lichess(self) -> bool:
        attempt: int = 1
        success: bool = self._login()
        while not success and attempt <= consts.NUMBER_LOGIN_ATTEMPTS:
            logger.error("Login attempt #{} failed.".format(attempt))
            attempt += 1
            success = self._login()
        if success:
            return True
        else:
            return False

    def run(self):
        login_success: bool = self._login_lichess()
        if login_success:
            self._setting_blind_mode_pref()
            self._create_game()

