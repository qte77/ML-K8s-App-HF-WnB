#!/usr/bin/env python
"""Model inference"""
from transformers import AutoTokenizer
# from torch import cuda, no_grad

def test_model(
    inputs: str,
    device: str
) -> str:
    """"""
    
    #TODO source for test function, WandB colab?
    #TODO multi inputs
    device = device.tolower()
    if device == "cuda":
        for i in inputs:
            # print(i)
            # inputs = tokenizer(sentence, return_tensors='pt')
            # ensure model and inputs are on the same device (GPU)
            # inputs = {name: tensor.cuda() for name, tensor in inputs.items()}
            # model = model.cuda()
            # get prediction - 10 classes "probabilities" (not really true because they still need to be normalized)
            # with torch.no_grad(): 
            #     predictions = model(**inputs)[0].cpu().numpy()
            # get the top prediction class and convert it to its associated label
            # top_prediction = predictions.argmax().item()
            # return ds['train'].features['labels'].int2str(top_prediction)
            pass
        return "not implemented"
    else:
        return "NO CUDA"

def infer_model(
    input: str,
    device: str
) -> str: #TODO
    """Infers result from model given input"""

    #TODO adopt to model and task
    #if dataset == 'YAHOO':
    input = 'Why is cheese so much better with wine?'
    return test_model(input, device)
    # elif dataset == 'MRPC':
    #   print(test_model('hallo', 'hedda'))
