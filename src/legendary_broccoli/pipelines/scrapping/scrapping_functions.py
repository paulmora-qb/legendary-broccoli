from typing import Any, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


def create_driver(params: Dict[str, Any]) -> WebDriver:
    """This function creates a chrome web-driver.

    Args:
        params (Dict[str, Any]): The parameters contain the driver-path of the chrom
            driver

    Returns:
        WebDriver: Chrome webdriver
    """

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    driver_path = params["driver_path"]

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    return driver


def scrapping_images(driver: WebDriver, params: Dict[str, Any]):
    a = 1
    pass
