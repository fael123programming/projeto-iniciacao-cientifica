from transformers import AutoTokenizer  # Or BertTokenizer
from transformers import AutoModelForPreTraining  # Or BertForPreTraining for loading pretraining heads
from transformers import AutoModel  # or BertModel, for BERT without pretraining heads
from transformers import pipeline
import json

model_name = 'neuralmind/bert-large-portuguese-cased'
model = AutoModelForPreTraining.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, do_lower_case=False)

pipe = pipeline('sentiment-analysis', model=model_name, tokenizer=tokenizer)

print(json.dumps(pipe('alegria muita alegria é encontrada aqui, alegria dimais'), indent=4))
print(json.dumps(pipe('tristeza muita tristeza é encontrada aqui, tristeza dimais'), indent=4))
# print(pipe('Eu [MASK] [MASK] JESUS.'))