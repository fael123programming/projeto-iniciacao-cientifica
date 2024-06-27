import spacy

nlp = spacy.load("pt_core_news_sm")

text = "O Brasil é um país maravilhoso."

doc = nlp(text)

for token in doc:
    print(token.text, token.pos_, token.dep_)
