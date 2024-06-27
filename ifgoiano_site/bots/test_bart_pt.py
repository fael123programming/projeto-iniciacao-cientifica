from transformers import pipeline, BartForConditionalGeneration, BartTokenizer

MODEL = 'facebook/bart-large-cnn'

tokenizer = BartTokenizer.from_pretrained(MODEL)
model = BartForConditionalGeneration.from_pretrained(MODEL)

inputs = tokenizer(
'''O futebol, um esporte apaixonante que cativa milhões ao redor do mundo, transcende as fronteiras geográficas e culturais, unindo pessoas de diferentes origens em torno de uma paixão comum. Desde os campos de várzea até os estádios monumentais, o futebol exerce um fascínio que vai além das meras disputas esportivas, tornando-se um verdadeiro fenômeno social.
Com suas regras simples e dinâmicas, o futebol proporciona um espetáculo cheio de emoção e adrenalina. Cada partida é um capítulo novo, repleto de reviravoltas inesperadas, lances geniais e momentos de glória que ficam gravados na memória dos torcedores para sempre. Os jogadores, verdadeiros artistas em campo, exibem suas habilidades técnicas e táticas, transformando o gramado em um palco de performances memoráveis.
Além do aspecto competitivo, o futebol também é uma poderosa ferramenta de inclusão social e integração comunitária. Por meio do esporte, jovens de diferentes origens têm a oportunidade de desenvolver valores como trabalho em equipe, disciplina e respeito mútuo, contribuindo para a formação de cidadãos mais conscientes e solidários.
Os clubes de futebol, verdadeiras instituições que atravessam gerações, são o coração pulsante desse universo apaixonante. Suas cores, hinos e símbolos carregam consigo a história e a identidade de comunidades inteiras, unindo torcedores em uma só voz, capaz de ecoar pelos quatro cantos do mundo.
E não podemos deixar de mencionar os grandes eventos futebolísticos, como a Copa do Mundo e a UEFA Champions League, que mobilizam multidões e transcendem as barreiras do esporte, tornando-se verdadeiros espetáculos globais capazes de parar nações inteiras para acompanhar cada lance, cada gol, cada emoção.
Assim, o futebol não é apenas um jogo. É uma paixão que pulsa em cada torcedor, uma linguagem universal que une povos e culturas, uma fonte inesgotável de emoções que alimenta o imaginário coletivo e enriquece as vidas de milhões ao redor do mundo.''', 
    max_length=1024, 
    return_tensors='pt',
    padding=True,
    truncation=True
)
summary_ids = model.generate(
    inputs['input_ids'], 
    num_beams=4, 
    min_length=100, 
    max_length=150, 
    early_stopping=True
)
decoded = tokenizer.decode(
    summary_ids[0], 
    skip_special_tokens=True
)

summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
summary_text = summarizer(
    decoded, 
    min_length=32, 
    max_length=128, 
    do_sample=False
)[0]['summary_text']
print(summary_text)