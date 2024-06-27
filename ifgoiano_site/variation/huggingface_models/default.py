from transformers import pipeline
import json

classifier = pipeline('sentiment-analysis')
print(json.dumps(classifier('We are very happy to introduce pipeline to the transformers repository.'), indent=4))