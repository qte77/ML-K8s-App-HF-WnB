#!/usr/bin/env python
'''
Create a pipeline object
'''
from prepareMLInput import prepare_ml_components, get_tokenizer, get_model
from trainModel import train_Model
from inferModel import infer_model

class Pipeline:
    
    def __init__(self, paramobj):
        self.paramobj = paramobj

    def set_train_mode(self, train_mode: bool) -> None:
        '''
        Switch mode between train and infer
        '''
        self.paramobj.train_mode = train_mode

    def do_prepare(self) -> None:
        #TODO object manipulation inside prepare class?
        self['metrics']['metrics_loaded'] = prepare_ml_components(
            self.paramobj.dataset,
            self.paramobj.model_full_name,
            self.paramobj.metrics_to_load,
            self.paramobj.wandb
        )

    def do_train(self) -> None:
        train_Model(
            self.paramobj.project_name,
            self.paramobj.metrics.metrics_to_optimize,
            self.paramobj.sweep.provider,
            self.paramobj.metrics.metrics_loaded
        )

    def do_infer(self, input):
        '''
        
        '''
        infer_model(
            input,
            get_tokenizer(self.paramobj.model_full_name),
            get_model(self.paramobj.model_full_name),
            self['device']
        )

    #TODO following functionality may be too much for basic MVP, exclude?

    # def get_env_info():
        #TODO unload module watermark
        #TODO use build-in functionality to provide info?
        # import watermark
        # watermark -u -i -v -iv

    # def get_task(self):
    #     return self.task

    # def get_pipeobj(self) -> pipeobj:
    #     return self

    # def get_dataset_eda():
    #     #TODO implement with different dataset types, maybe separate module
    #     return -1

    # def get_pre_trained_hyperparam(self):
    #     return self.modelobj.config
    
    # def get_attention(self):
    #     return self.modelobj.base_model.encoder.layer[0]
    #     # print(modelobj.bert.encoder.layer[0])
    
    # def get_embeddings(self):
    #     return self.modelobj.base_model.embeddings
    #     # print(modelobj.bert.embeddings)
