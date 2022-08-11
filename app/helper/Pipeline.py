#!/usr/bin/env python
"""Create a pipeline object with a parameter object"""

from dataclasses import dataclass

# from model.infer_model import infer_model
# from model.train_model import train_model
from .prepare_ml_input import (  # prepare_ml_components,; set_provider_env,
    get_metrics_to_load_objects,
)


@dataclass
class Pipeline:
    """Create a pipeline object with a parameter object"""

    paramobj: dict

    def set_train_mode(self, train_mode: bool) -> None:
        """Switch mode between train and infer"""
        self.paramobj.train_mode = train_mode

    def get_task(self) -> None:
        return self.task

    def get_paramobj(self) -> object:  # TODO type hint as Pipeline or dict
        return self.paramobj

    def get_sys_info() -> None:
        # TODO unload module watermark
        # TODO use build-in functionality to provide info?
        # import watermark
        # watermark -u -i -v -iv
        return NotImplementedError

    def prepare_ml_external_components(self) -> None:
        """
        Gets dateset and model from Hugging Face if not locally cached.\n
        Downloads the Metrics Builder Scripts from HF and returns their objects.\n
        Sets the environment variables the sweep provider needs.
        """

        try:

            # prepare_ml_components(
            #     self.paramobj["dataset"], self.paramobj["model_full_name"]
            # )

            # get metrics
            self.paramobj["metrics"]["metrics_loaded"] = get_metrics_to_load_objects(
                self.paramobj["metrics"]["metrics_to_load"]
            )

            # provider = self.paramobj["sweep"]["provider"]
            # set_provider_env(provider, self.paramobj[provider])
        except Exception as e:
            return e

    def do_train(self) -> None:
        """TODO"""
        return NotImplementedError

    def do_infer(self) -> None:
        """TODO"""
        return NotImplementedError
