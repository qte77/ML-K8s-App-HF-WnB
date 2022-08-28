#!/usr/bin/env python
"""Model training"""

from datasets import Metric

from ..utils.handle_logging import debug_on_global, logging_facility
from ..utils.prepare_pipe_data import Pipeline

# from numpy import argmax
# from transformers import Trainer, TrainingArguments


# from wandb import log

# from .handle_model_sweep import start_sweep


def train_model(pipeobj: Pipeline = None) -> None:
    """Fine-tune the model on down-stream task"""

    if debug_on_global:
        logging_facility("log", "Starting training")

    # start_sweep(provider)

    # train_model(
    #     self.paramobj.project_name,
    #     self.paramobj.metrics.metrics_to_optimize,
    #     self.paramobj.sweep.provider,
    #     self.paramobj.metrics.metrics_loaded,
    # )

    return NotImplementedError


def _compute_metrics(eval_pred: list, metrics_loaded: list, metrics_avg: str) -> Metric:
    """TODO"""

    # TODO refactor

    # return compute_metrics_hf()

    return NotImplementedError
