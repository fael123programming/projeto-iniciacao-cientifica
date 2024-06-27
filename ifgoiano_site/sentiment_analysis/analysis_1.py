from transformers import pipeline

sentiment_analyzer = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')

# Exemplo de texto em português
texto = "ce e bom parça"

resultados = sentiment_analyzer(texto)

# Exibir os resultados
for resultado in resultados:
    sentimento = resultado['label']
    pontuacao = resultado['score']
    print(f"Sentimento: {sentimento}, Pontuação: {pontuacao}")
