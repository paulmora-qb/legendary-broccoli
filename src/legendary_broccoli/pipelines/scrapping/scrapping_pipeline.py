from kedro.pipeline import Pipeline, node

from .scrapping_functions import scrapping_images


def create_pipeline() -> Pipeline:
    """This function creates the scrapping pipeline

    Returns:
        Pipeline: The scrapping pipeline
    """

    nodes = [
        node(
            func=scrapping_images,
            inputs="params:scrapping",
            outputs="scrapped_images",
            name="scrapping_images",
            tags=["scrapping"],
        ),
    ]

    return Pipeline(nodes)
