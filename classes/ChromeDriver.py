# third-party libraries
import io
import os
import requests
import sys
import zipfile
from http import HTTPStatus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

# inner classes
from classes import consts
from utils.logger import logger


class ChromeDriver:

    def __init__(self, install_path: str, is_silent=True):
        self._driver = None

        zip_url = "{}/{}".format(consts.CHROME_DRIVER_INSTALL_URL, consts.WIN_ZIP_NAME)
        executable_name = consts.WIN_EXECUTABLE_NAME

        if sys.platform.lower() == "darwin":
            zip_url = "{}/{}".format(consts.CHROME_DRIVER_INSTALL_URL, consts.MAC_ZIP_NAME)
            executable_name = consts.MAC_EXECUTABLE_NAME

        full_install_path = "{}/{}".format(install_path, executable_name)

        install_success = False
        driver_already_exits = os.path.exists(full_install_path)
        if not driver_already_exits:
            install_success = ChromeDriver._install_file_from_zip_url(zip_url, install_path)

        if driver_already_exits or install_success:
            chromedriver_path = "/".join([install_path, executable_name])
            chromedriver_options = Options()
            chromedriver_options.add_experimental_option("detach", True)
            chromedriver_options.add_argument("start-maximized")
            chromedriver_options.add_argument("disable-infobars")
            chromedriver_options.add_argument("--disable-extensions")
            if is_silent:
                chromedriver_options.add_argument('headless')
            self._driver = webdriver.Chrome(executable_path=chromedriver_path, options=chromedriver_options)

    @staticmethod
    def _install_file_from_zip_url(zip_url: str, install_path: str) -> bool:
        try:
            response = requests.get(zip_url, stream=True)
            status_code = response.status_code
            if status_code == HTTPStatus.OK:
                z = zipfile.ZipFile(io.BytesIO(response.content))
                z.extractall(install_path)
                return True
            else:
                logger.error("Install zip url status code: {}.".format(status_code))
        except requests.exceptions.Timeout:
            logger.error("Chromedriver download Error:\n"
                         "Timeout for zip url: {}.".format(zip_url))
        except requests.exceptions.TooManyRedirects:
            logger.error("Chromedriver download Error:\n"
                         "The zip url {} is bad, try a different one.".format(zip_url))
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        except requests.exceptions.ContentDecodingError:
            logger.error("Chromedriver download Error:\n"
                         "Failed to decode response content for zip url {}.".format(zip_url))
        except requests.exceptions.RequestException as e:
            logger.error("Chromedriver download Error:\n"
                         "Request failed for zip url {}.\n"
                         "Error: {}.", zip_url, e)
            raise SystemExit(e)
        except zipfile.BadZipfile:
            logger.error("Chromedriver download Error:\n"
                         "Bad zip file.")
        except ValueError:
            logger.error("Chromedriver download Error:\n"
                         "Could not extract zip file.")
        except Exception as e:
            logger.error("Chromedriver download Error:\n"
                         "Unexpected general error: {}.".format(str(e)))
        return False

    def get(self, url):
        self._driver.get(url)

    def quit(self):
        self._driver.quit()

    def implicitly_wait(self, delay_sec):
        self._driver.implicitly_wait(delay_sec)

    def send_login_info(self, username: str, password: str, user_elem_id: str, password_elem_id: str):
        username_elem = self._driver.find_element_by_id(user_elem_id)
        password_elem = self._driver.find_element_by_id(password_elem_id)
        username_elem.send_keys(username)
        password_elem.send_keys(password)

    def verify_login(self, expected_url: str) -> bool:
        actual_url = self._driver.current_url
        if actual_url == expected_url:
            logger.info("Successfully logged in!")
            return True
        logger.error("Actual url does not match to after login expected url:\n"
                     "Actual url: {}".format(actual_url))
        return False

    def find_element_by_id(self, elem_id: str):
        return self._driver.find_element_by_id(elem_id)

    def find_element_by_name(self, name: str):
        return self._driver.find_element_by_name(name)

    def select_elem_by_visible_text(self, elem_id: str, text: str):
        elem = Select(self.find_element_by_id(elem_id))
        elem.select_by_visible_text(text)

    def click_button_by_xpath(self, xpath: str):
        button = self._driver.find_elements_by_xpath(xpath)[0]
        button.click()

    def elem_execute_script_by_id(self, elem_id: str, script: str, elem_value: str):
        elem = self._driver.find_element_by_id(elem_id)
        self._execute_script(script, elem, elem_value)

    def elem_execute_script_by_name(self, elem_name: str, script: str, elem_value: str):
        elem = self._driver.find_element_by_name(elem_name)
        self._execute_script(script, elem, elem_value)

    def _execute_script(self, script: str, elem: str, elem_value: str):
        self._driver.execute_script(script, elem, elem_value)

