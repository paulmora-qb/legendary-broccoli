from kedro.pipeline import Pipeline, node

from .scrapping_functions import create_driver, scrapping_images


def create_pipeline() -> Pipeline:
    """This function creates the scrapping pipeline

    Returns:
        Pipeline: The scrapping pipeline
    """

    nodes = [
        node(
            func=create_driver,
            inputs="params:scrapping.webdriver",
            outputs="webdriver",
            name="create_webdriver",
            tags=["scrapping"],
        ),
        node(
            func=scrapping_images,
            inputs=["webdriver", "params:image_scrapping"],
            outputs="images",
            name="scrapping_images",
            tags=["scrapping"],
        ),
    ]

    return Pipeline(nodes)
