#!/usr/bin/env python
'''
Entrypoint for the app
'''
#TODO conditional import possible and best practice ?
#TODO use color for CLI ?
from helper.create_pipeline_object import Pipeline
from helper.parametrise_pipeline import get_param_object
# from sys import color #or os?

def main():
    '''
    Create pipeline object parametrised with parameter object
    '''
    
    # COLOR = {
    #   'red' : '\033[31m',
    #   'green' : '\033[32m',
    #   'orange' : '\033[33m',
    #   'endclr' : '\033[0m'
    # }

    pipeobj = Pipeline(get_param_object())
    pipeobj.do_prepare()
    pipeobj.do_infer() #test output, should not be correct before fine-tuning
    pipeobj.do_train() #fine-tune


if __name__ == "__main__":
    #main(sys.argv[1], sys.argv[2], sys.argv[3])
    main()
