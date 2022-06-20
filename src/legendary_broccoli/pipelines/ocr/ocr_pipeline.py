from kedro.pipeline import Pipeline, node

from .ocr_functions import extracting_ocr


def create_pipeline() -> Pipeline:
    """This function creates the scrapping pipeline

    Returns:
        Pipeline: The scrapping pipeline
    """

    nodes = [
        node(
            func=extracting_ocr,
            inputs="params:scrapping.image_scrapping",
            outputs="ocr_summary",
            name="extracting_ocr_from_images",
            tags=["ocr"],
        ),
    ]

    return Pipeline(nodes)
