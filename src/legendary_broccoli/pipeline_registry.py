"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from legendary_broccoli.pipelines.ocr.ocr_pipeline import (
    create_pipeline as applying_ocr,
)
from legendary_broccoli.pipelines.scrapping.scrapping_pipeline import (
    create_pipeline as scrapping,
)


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    return {"applying_ocr": applying_ocr(), "scrapping_images": scrapping()}
