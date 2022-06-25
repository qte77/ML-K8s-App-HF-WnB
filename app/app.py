#!/usr/bin/env python
'''
Entrypoint for the app
'''
import parametrise, prepare, train, infer

class pipeline:

    def __init__(self, paramobj):
        self.paramobj = paramobj

    def get_task(self):
        return self.task

    def get_pipeobj(self):
        return self

    def show_env_info():
        #TODO unload module watermark
        #TODO use build-in functionality to provide info?
        import watermark
        watermark -u -i -v -iv

    def get_dataset_eda():
        #TODO implement with different dataset types, maybe separate module
        return -1

    def get_pre_trained_hyperparam(self):
        return self.modelobj.config
    
    def get_attention(self):
        return self.modelobj.base_model.encoder.layer[0]
        # print(modelobj.bert.encoder.layer[0])
    
    def get_embeddings(self):
        return self.modelobj.base_model.embeddings
        # print(modelobj.bert.embeddings)

    def do_prepare(self):
        #TODO object manipulation inside prepare class?
        self['metrics']['metrics_loaded'] = prepare.prepare(
            self.paramobj.dataset,
            self.paramobj.model_full_name,
            self.paramobj.metrics_to_load,
            self.paramobj.wandb
        )

    def do_train(self):
        train.train(
            self.
            self.paramobj.project_name,
            self.paramobj.metrics.metrics_to_optimize,
            self.paramobj.metrics.metrics_loaded
        )

    def do_infer(self, input):
        tokenizer = prepare.get_tokenizer(self.paramobj.model_full_name)
        model = prepare.get_model(self.paramobj.model_full_name)
        infer.infer(
            input,
            #tokenizer,
            #model,
            self['device']
        )

    def set_train_mode(self, train_mode: bool):
        '''
        Switch mode between train and infer
        '''
        self.paramobj.train_mode = train_mode

def main():

    pipeobj = pipeline(parametrise.get_param_object())
    pipeobj.do_prepare()
    pipeobj.do_infer() #test output, should not be correct before fine-tuning
    pipeobj.do_train() #fine-tune

if __name__ == "__main__":
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    main()
