import pandas as pd
import os
from transformers import AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained(
   pretrained_model_name_or_path='nlptown/bert-base-multilingual-uncased-sentiment'
)
analyse = pipeline(
   task='sentiment-analysis', 
   model='nlptown/bert-base-multilingual-uncased-sentiment'
)
values = ['a']
max_length = 512
for value in values:
    tokens = tokenizer(
        value, 
        max_length=max_length, 
        padding=True, 
        truncation=True, 
        return_tensors="pt"
    )
    print(tokens)
    # res = analyse(
    #     tokenizer.decode(
    #         tokens["input_ids"].squeeze().tolist(), 
    #         skip_special_tokens=True
    #     )
    # )