import logging
import os
import random
import time
import urllib
from typing import Any, Dict, List, Tuple

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

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


def _find_images(driver: WebDriver) -> Tuple[List[WebElement], int]:
    image_elements = driver.find_elements_by_css_selector(
        ".ReactGridGallery_tile-viewport"
    )
    return image_elements, len(image_elements)


def _random_waiting_time(min_seconds_sleep: int, max_seconds_sleep: int) -> float:
    return random.uniform(min_seconds_sleep, max_seconds_sleep)


def _create_expanded_driver(driver_params, image_params) -> WebDriver:

    driver_path = driver_params["driver_path"]
    max_seconds_sleep = driver_params["max_seconds_sleep"]
    min_seconds_sleep = driver_params["min_seconds_sleep"]
    search_url = image_params["url"]
    max_number_of_images = image_params["max_number_of_images"]

    driver = _create_initial_driver(driver_path, search_url)

    _, number_of_images_visible = _find_images(driver)

    while number_of_images_visible < max_number_of_images:
        time.sleep(_random_waiting_time(min_seconds_sleep, max_seconds_sleep))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        _, number_of_images_visible = _find_images(driver)
        logger.info(f"Images found {number_of_images_visible} of {max_seconds_sleep}")

    logger.info(f"In total we found {number_of_images_visible} images")

    return driver


def _retrieve_image_source(image_element, image_num) -> str:
    try:
        image_src_element = image_element.find_element_by_css_selector("img")
        img_src = image_src_element.get_attribute("src")
        return img_src
    except NoSuchElementException:
        return None


def _delete_all_files_in_folder(folder_path: str) -> None:
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def _scrape_images(
    image_folder_path: str,
    image_elements: List[WebElement],
    number_of_total_entries: int,
) -> None:

    for image_num, image_element in tqdm(enumerate(image_elements)):

        image_path = os.path.join(image_folder_path, f"marathon_{image_num}.png")
        img_src = _retrieve_image_source(image_element, image_num)
        if img_src is None:
            f"Image {image_num} could not be retrieved"

        urllib.request.urlretrieve(img_src, image_path)


def scrapping_images(params: Dict[str, Any]) -> None:

    driver_params = params["driver"]
    image_params = params["image_scrapping"]
    image_folder_path = image_params["image_folder"]
    rescrape_bool = image_params["rescrape"]

    driver = _create_expanded_driver(driver_params, image_params)
    image_elements, number_of_total_entries = _find_images(driver)

    if rescrape_bool:
        _delete_all_files_in_folder(image_folder_path)
        _scrape_images(image_folder_path, image_elements, number_of_total_entries)
        logger.info("Image re-scrapping finished")
    else:
        logger.info("No re-scraping was conducted")
