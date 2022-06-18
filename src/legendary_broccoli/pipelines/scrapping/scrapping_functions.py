import logging
import random
import time
from typing import Any, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

logger = logging.getLogger(__name__)


def _create_initial_driver(driver_path: str, search_url: str) -> WebDriver:
    """This function creates a chrome web-driver.

    Args:
        driver_path (str): Path of where the webdriver is saved
        search_url (str): String of which website to scrape

    Returns:
        WebDriver: Chrome webdriver
    """

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    driver.get(search_url)

    assert driver.title is not "", "The driver did not fetch the website"
    return driver


def _find_number_of_images(driver: WebDriver) -> int:
    """Returns the number of images visible for the driver

    Args:
        driver (WebDriver): driver for the website

    Returns:
        int: Number of images visible for the driver
    """
    image_elements = driver.find_elements_by_css_selector(
        ".ReactGridGallery_tile-viewport"
    )
    return len(image_elements)


def _random_waiting_time(min_seconds_sleep: int, max_seconds_sleep: int) -> float:
    return random.uniform(min_seconds_sleep, max_seconds_sleep)


def _create_expanded_driver(driver_params, image_params) -> WebDriver:

    driver_path = driver_params["driver_path"]
    max_seconds_sleep = driver_params["max_seconds_sleep"]
    min_seconds_sleep = driver_params["min_seconds_sleep"]
    search_url = image_params["url"]
    max_number_of_images = image_params["max_number_of_images"]

    driver = _create_initial_driver(driver_path, search_url)

    number_of_images_visible = _find_number_of_images(driver)

    while number_of_images_visible < max_number_of_images:
        time.sleep(_random_waiting_time(min_seconds_sleep, max_seconds_sleep))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        number_of_images_visible = _find_number_of_images(driver)
        logger.info(f"Images found {number_of_images_visible} of {max_seconds_sleep}")

    logger.info(f"In total we found {number_of_images_visible} images")

    return driver


# TODO: Implement the scrapping of the images
def scrapping_images(params: Dict[str, Any]):

    driver_params = params["driver"]
    image_params = params["image_scrapping"]

    driver = _create_expanded_driver(driver_params, image_params)
    number_of_total_entries = _find_number_of_images(driver)

    images = []

    for image_num in tqdm(enumerate(number_of_total_entries)):
        a
