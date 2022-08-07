#!/usr/bin/env python

# from model.infer_model import infer_model
# from model.train_model import train_model
from .prepare_ml_input import get_metrics_to_load_objects, prepare_ml_components


class Pipeline:
    """Create a pipeline object with a parameter object"""

    def __init__(self, paramobj: dict):
        self.paramobj = paramobj

    def set_train_mode(self, train_mode: bool) -> None:
        """Switch mode between train and infer"""
        self.paramobj.train_mode = train_mode

    def get_task(self):
        return self.task

    def get_pipeobj(self) -> object:  # TODO type hint Pipeline:
        return self

    def get_env_info():
        # TODO unload module watermark
        # TODO use build-in functionality to provide info?
        # import watermark
        # watermark -u -i -v -iv
        return NotImplementedError

    def prepare_ml_input(self) -> None:
        """Fill the TODO"""

        providerobj = {"wandb": self.paramobj["wandb"]}

        prepare_ml_components(
            self.paramobj["dataset"], self.paramobj["model_full_name"], providerobj
        )

        self.paramobj["metrics"]["metrics_loaded"] = get_metrics_to_load_objects(
            self.paramobj["metrics"]["metrics_to_load"]
        )
