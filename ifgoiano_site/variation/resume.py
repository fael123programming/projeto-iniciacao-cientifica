from transformers import BartForConditionalGeneration, BartTokenizer

model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

texto = """
Divulgada segunda chamada para cursos superiores
O Instituto Federal Goiano (IF Goiano) divulga a segunda chamada do Processo Seletivo para cursos Superiores da Instituição. A matrícula dos aprovados será realizada de forma online, pelo gov.br nos dias 6 e 7 de fevereiro. Aprovados no Campus Posse, no entanto, deverão efetuar matrícula por e-mail conforme orientações disponíveis no sistema (veja link abaixo). 
O processo seletivo não aplica provas no formato de vestibular - a seleção se dá por meio da nota do Exame Nacional do Ensino Médio (Enem). Esta seleção considerou a pontuação obtida nas edições do exame nos anos de 2016, 2017, 2018, 2019, 2020, 2021, 2022 ou 2023 podendo concorrer com pelo menos uma das edições. 
Acesse a página do Processo Seletivo e confira os resultados
Clique e acesse os tutoriais de matrícula
Diretoria de Comunicação Social
"""

# Tokenize the text
inputs = tokenizer(texto, max_length=1024, return_tensors="pt", truncation=True)

# Generate the summary
summary_ids = model.generate(inputs["input_ids"], num_beams=4, min_length=30, max_length=150, early_stopping=True)
summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Texto Original:")
print(texto)

print("\nResumo:")
print(summary_text)
