from json import dumps
from transformers import pipeline

sentiment = pipeline(
    'sentiment-analysis',
    model='nlptown/bert-base-multilingual-uncased-sentiment'
)
phrase_1 = 'alegria muita alegria é encontrada aqui, alegria dimais'
phrase_2 = 'tristeza muita tristeza é encontrada aqui, tristeza dimais'
print(dumps(sentiment(phrase_1), indent=4))
print(dumps(sentiment(phrase_2), indent=4))

