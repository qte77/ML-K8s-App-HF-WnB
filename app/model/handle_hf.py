#!/usr/bin/env python
"""Offers functions to handle [Hugging Face (HF)](https://huggingface.co)"""


# from datasets import Metric
from transformers import Trainer, TrainingArguments

# from ..utils.configure_logging import debug_on_global, logging_facility
# from ..pipeline.prepare_ml_input import PipelineOutput


def _create_trainer_hf(args: TrainingArguments) -> Trainer:
    """TODO"""

    # TODO implement
    # TODO save locally

    # trainer = Trainer(
    #   model = modelobj,
    #   args = args,
    #   train_dataset = dataset_tokenized['train'],
    #   eval_dataset = dataset_tokenized['test'],
    #   tokenizer = tokenizer,
    #   compute_metrics = compute_metrics #()
    # )

    #   print(orange,"*************")
    #   print("Metric: %s, #Labels: %s, Avg: %s" %
    #   (metric_to_optimize, num_labels, ds_avg))
    #   print("eval_steps: %s, save_steps: %s" % (eval_steps, save_steps))
    #   print(orange,"*************")

    # return trainer

    return NotImplementedError


def _create_trainer_args_hf():
    """TODO"""

    #   eval_steps = round(config.max_steps / 5)
    #   save_steps = eval_steps * 2

    #   # args need to be assigned here to avoid wandb runtime TypeError()
    #   # "'TrainingArguments' object does not support item assignment"
    #   args = TrainingArguments(
    #     report_to = provider # 'wandb',
    #     output_dir = os.environ['WANDB_PROJECT'],
    #     overwrite_output_dir = True,
    #     # check evaluation metrics at each epoch
    #     evaluation_strategy = 'steps',
    #     logging_steps = 100,
    #     load_best_model_at_end = True,
    #     run_name = os.environ['WANDB_PROJECT'],
    #     eval_steps = eval_steps,
    #     save_steps = save_steps,
    #     metric_for_best_model = metric_to_optimize,
    #     greater_is_better = greaterBool,
    #     # avoid info 'The following columns in the evaluation set
    #     # don't have a corresponding argument'
    #     # remove_unused_columns = True,
    #     # the following will be changed by sweep agent
    #     learning_rate = config.learning_rate,
    #     max_steps = config.max_steps,
    #     seed = config.seed,
    #     optim = config.optim
    #   )

    pass


def compute_metrics_hf():
    """TODO"""

    # predictions, labels = eval_pred
    # predictions = argmax(predictions, axis=1)  # predictions.argmax(-1)

    # print("*************")

    # for i, m in enumerate(metrics_loaded):

    #     if metrics_loaded[i] in ["precision", "recall", "f1"]:
    #         met = m.compute(
    #             predictions=predictions, references=labels, average=metrics_avg
    #         )
    #     else:
    #         met = m.compute(predictions=predictions, references=labels)

    #     if metrics_loaded[i] == "accuracy":
    #         ret = met

    #     log(met)
    #     print(met)

    # print("*************")

    pass
