import sqlite3 as db
import pandas as pd
from transformers import pipeline
import sqlite3
from matplotlib import pyplot as plt


# PyTorch, TensorFlow, BERT to sentiment analysis.
# Label: how many stars?
# Score: how closer to
'''
BERT (Bidirectional Encoder Representations from Transformers) is a pre-trained natural language processing model developed by Google. It belongs to the transformer architecture family. Here's an overview of how pre-trained BERT models work:

1. Pre-training:
   - Unsupervised Learning: BERT is pre-trained using unsupervised learning on a massive amount of text data. During this phase, BERT learns to predict missing words in sentences. It does this by training on a masked language modeling (MLM) task, where some words in a sentence are randomly replaced with a special [MASK] token, and the model learns to predict these masked words.
   - Bidirectional Context: BERT differs from traditional language models by considering context from both left and right sides of a word. This bidirectional context allows BERT to capture richer semantic meaning.

2. Architecture:
   - Transformer Architecture: BERT utilizes the transformer architecture, which includes self-attention mechanisms to capture relationships between words in a sentence. This attention mechanism allows BERT to weigh the importance of different words based on their contextual relevance.

3. Layers and Attention Heads:
   - BERT consists of multiple layers, each with attention heads. Each layer captures different levels of abstraction, from low-level features to high-level semantic information.
   - Attention heads enable BERT to focus on different aspects of the input sentence simultaneously.

4. Tokenization:
   - BERT tokenizes input text into subwords or tokens. It uses WordPiece tokenization, breaking words into subword units.
   - Special tokens, such as [CLS] (classification) and [SEP] (separator), are added to the input to indicate the beginning and separation of sentences.

5. Fine-Tuning:
   - After pre-training, BERT can be fine-tuned for specific tasks, such as sentiment analysis, question answering, or named entity recognition. Fine-tuning involves training the model on a smaller dataset labeled for the target task.

6. Inference:
   - During inference, the pre-trained BERT model can be used as a feature extractor or as part of a larger model for downstream tasks. For example, in sentiment analysis, the [CLS] token's output may be used as a representation of the entire input sentence.

The pre-trained BERT model is powerful because it captures contextual relationships between words, allowing it to understand the nuances of language. Fine-tuning on task-specific datasets tailors the model to perform well on specific applications. The multilingual variant of BERT, as in the example you provided, is trained to understand and handle multiple languages.

'''
sentiment_analyser = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

if __name__ == '__main__':
   # with sqlite3.connect('./varit/database.db') as conn:
   #    desc = pd.read_sql_query('SELECT descricao FROM data LIMIT 10', conn)
   # descs = desc['descricao'].tolist()
   descs = [
      'Reconduzido ao cargo, o reitor do Instituto renovou a gestão central da instituição para o novo mandato. Lideranças iniciaram os trabalhos em uma semana marcada por reuniões e atividades de apresentações, alinhamento e capacitação.',
      'Inscrições para as seleções foram prorrogadas até 25 de fevereiro de 2024 para inscrição de obras originais.',
      'Matrículas serão realizadas pelo gov.br nos dias 6 e 7 de fevereiro. Aprovados no Campus Posse devem efetuar matrícula por e-mail. ',
      'Vagas são para a modalidade Supervisor Multissistêmico, nas unidades de Campos Belos, Catalão, Ceres, Hidrolândia, Ipameri, Iporá e Rio Verde',
      'Bolsa é para áreas de Engenharia na Universidad de Jaén. Processo Seletivo é realizado pelo Conif em parceria com o Escritório de Educação da Embaixada da Espanha. Interessados devem se inscrever até 15 de fevereiro.'
   ]
   corpus = [
      '''A semana na Reitoria do Instituto Federal Goiano (IF Goiano) começou agitada em meio a mudanças de salas e com algumas personalidades novas circulando pelos corredores da unidade. Isso porque, tiveram início as reuniões e atividades de apresentações, alinhamento e capacitação da nova gestão central da Instituição. As ações tiveram início na segunda-feira, 5, com a primeira reunião do novo Comitê Gestor da Reitoria, e seguiram na terça e quarta-feira, 6 e 7, com um momento de capacitação e alinhamento para as novas lideranças e outro com apresentação dos novos gestores a todos os servidores do IF Goiano, respectivamente.

Reconduzido ao cargo de reitor, Elias de Pádua Monteiro, investiu em nova composição da equipe e alterações no organograma da reitoria para continuar o trabalho à frente da Instituição. O reitor explica que o grande desafio apresentado pelo cenário atual exige que o IF Goiano continue crescendo em excelência, inovando e sem espaço para ocupar zonas de conforto. “Somos uma Instituição renomada e o momento pede uma instituição mais dinâmica, viva e remodelada", afirma. "Se caminharmos pelas mesmas estradas chegaremos aos mesmos lugares", complementa. Elias compreende que toda mudança que se faz necessária pode gerar desconfortos e precisa de tempo e paciência para ser processada, mas se colocou aberto à possibilidade de reposicionamentos, desde que necessários, destacando que todo trabalho é realizado em prol da Instituição.

Para compor a nova equipe, foram selecionados perfis de lideranças consolidadas na Instituição com o objetivo de formar um grupo com um mesmo nível de excelência. O objetivo do reitor é, com isso, garantir que as metas sejam alcançadas num prazo mais curto de tempo, uma vez que o grupo está nivelado em diferentes capacitações. “Com isso ganhamos tempo e o objetivo é colocar o IF Goiano entre os cinco melhores institutos do país”, afirma. “A ideia é que o trabalho tenha mais sintonia possível”, completa.

Em relação à alterações no organograma, das cinco pró-reitorias existentes anteriormente, o IF Goiano deixará de contar com a pró-reitoria de Desenvolvimento Institucional (Prodi) e passará a ter a pró-reitoria de Gestão de Pessoas (Progep) (Veja abaixo como ficou o organograma e quem está a frente de cada pasta). As novas lideranças foram nomeadas por meio de portaria expedida na última quinta-feira, 1º de fevereiro. O reitor será reconduzido ao cargo em março pelo Ministério da Educação (MEC). Após sua recondução, será realizada a cerimônia de posse dos novos diretores gerais dos campi.

Valores – Equidade, comprometimento e integração. Esses foram os três valores definidos pelo novo Comitê Gestor e que nortearão as ações da gestão em 2024.

Elias destaca que a equidade não está no tratamento igualitário, mas sim no reconhecimento das diferenças. De acordo com a nova gestão, ela garante que os servidores tenham acesso ao que cada um precisa, para que todos tenham as mesmas oportunidades. Já o comprometimento está relacionado ao compromisso com a Instituição, sentimento de pertencimento e ao agir com vigor, dedicação, responsabilidade e envolvimento. Enquanto a Integração busca a colaboração, cooperação e sinergia entre setores ou unidades, por meio de uma comunicação aberta e humanizada.

Além dos valores, o reitor também pautará suas ações na consolidação da identidade dos Institutos Federais no IF Goiano. Para o dirigente máximo do IF Goiano, o projeto pedagógico dos IFs é único no mundo. “Somos ilhas de excelência dentro desta proposta e afastar desse projeto pode nos fragilizar, pois já existem outros modelos pedagógicos”, explica.''',
      '''O Instituto Federal Goiano (IF Goiano), por meio da Editora IF Goiano, publica novo prazo para chamamento de obras originais. Inscrições para as seleções vão até 25 de fevereiro e devem ser realizadas via e-mail: editora@ifgoiano.edu.br .

Esta chamada captará obras por grande área do conhecimento (Ciências: Humanas, Exatas e da Terra, Sociais Aplicadas, Biológicas, Agrárias e da Saúde; Linguística, Letras e Artes; Engenharias e Multidisciplinar). Serão selecionadas até 15 obras. A divulgação do resultado final está prevista para 21 de maio de 2024.

 

Clique e acesse:

Retificação Edital 1 - Chamamento de Obras Originais

Edital nº 1/2023 – Chamamento de Obras Originais 

Edital nº 2/2023 – Chamamento de Artigos Científicos, Poemas e Ilustrações sobre Diversidade e Inclusão Social

 

 

Diretoria de Comunicação Social e Eventos''',
'''O Instituto Federal Goiano (IF Goiano) divulga a segunda chamada do Processo Seletivo para cursos Superiores da Instituição. A matrícula dos aprovados será realizada de forma online, pelo gov.br nos dias 6 e 7 de fevereiro. Aprovados no Campus Posse, no entanto, deverão efetuar matrícula por e-mail conforme orientações disponíveis no sistema (veja link abaixo). 

O processo seletivo não aplica provas no formato de vestibular - a seleção se dá por meio da nota do Exame Nacional do Ensino Médio (Enem). Esta seleção considerou a pontuação obtida nas edições do exame nos anos de 2016, 2017, 2018, 2019, 2020, 2021, 2022 ou 2023 podendo concorrer com pelo menos uma das edições. 

 

 Acesse a página do Processo Seletivo e confira os resultados

 Clique e acesse os tutoriais de matrícula


Diretoria de Comunicação Social''',
'''O Instituto Federal Goiano (IF Goiano) divulga resultado final do edital para seleção de bolsistas internos para o desempenho de atividades referentes aos cursos de Formação Inicial e Continuada (FIC) do Programa Mulheres Mil. As vagas são para a modalidade Supervisor Multissistêmico. 

Os bolsistas atuarão nos campi Campos Belos, Catalão, Ceres, Hidrolândia, Ipameri, Iporá ou Rio Verde como possibilidades. Haverá também formação de cadastro de reserva. O valor da bolsa é de R$ 36 hora-relógio, sendo a carga horária máxima semanal de 15 horas-relógio. As atribuições do cargo estão previstas no edital. 

 

Clique e acesse o resultado final

Acesse os documentos

 

Diretoria de Comunicação Social - republicada com alterações''',
'''O Instituto Federal Goiano (IF Goiano) divulga o edital do processo seletivo estudantes de ensino médio da Rede Federal de Educação Profissional, Científica e Tecnológica para receberem bolsas de estudo de graduação oferecidos pela Universidad de Jaén, na Espanha. A seleção está sendo promovida pelo Conselho Nacional das Instituições da Rede Federal de Educação Profissional, Científica e Tecnológica (Conif) em parceria com o Escritório de Educação da Embaixada da Espanha. Interessados devem se inscrever até 15 de fevereiro, pela internet.

O edital disponibiliza uma vaga, com formação de cadastro de reserva de até dez vagas, que constituirá lista única composta por candidatos de todas as instituições da Rede. A seleção contempla as áreas de Engenharias Civil, Elétrica, Geomática e Topografia, Mecânica, Química Industrial, Recursos Energéticos, Tecnologias Minerais e Telemática.

A bolsa disponibilizada inclui cobertura de cem por cento dos gastos de matrícula dos créditos requeridos para a formação completa do programa de graduação, ajuda de custo anual no valor de Є2.200,00 (dois mil e duzentos euros) por beneficiário, auxílio financeiro para o seguro de saúde (enfermidade/hospitalização), repatriação, acidentes e responsabilidade civil de até Є190,00 (cento e noventa euros) durante o período de vigência da bolsa, oferta de curso de espanhol gratuito, incluindo os custos de deslocamento entre campus para as aulas do curso, caso seja necessário, cobertura de cem por cento dos gastos para reconhecimento de créditos para os estudantes que solicitarem e, em casos justificados, outros gastos necessários para a estadia na Universidad de Jaén poderão ser cobertos.'''
   ]
   summa = []
   for c in corpus:
      summa.append(summarizer(c[:1024], max_length=130, min_length=30, do_sample=False)[0]['summary_text'])
   descs_results = sentiment_analyser(descs)
   ana_descs_stars = [int(desc_result['label'].split(' ')[0]) for desc_result in descs_results]
   ana_descs_scores = [desc_result['score'] for desc_result in descs_results]
   summa_results = sentiment_analyser(descs)
   ana_summa_stars = [int(summa_result['label'].split(' ')[0]) for summa_result in summa_results]
   ana_summa_scores = [summa_result['score'] for summa_result in summa_results]
   df = pd.DataFrame(
      {
         'estrelas': ana_descs_stars.extends(ana_summa_stars),
         'pontuacao': ana_descs_scores.extends(ana_summa_scores),
         'tipo': ['ifgoiano' for _ in ana_descs_stars] + ['bart' for _ in ana_summa_stars]
      }
   )
   stars_df = df.groupby('estrelas').mean()
   stars_df.plot(kind='bar')
   plt.title('Média de Estrelas por Tipo')
   plt.xlabel('Tipo')
   plt.ylabel('Média')
   plt.xticks(rotation=0)  # Rotate x-axis labels if needed
   plt.gcf().set_size_inches(9, 5)
   plt.savefig('media_estrelas_if_bart.png')
   # plt.clf()

   pont_df = df.groupby('pontuacao').mean()
   pont_df.plot(kind='bar')
   plt.title('Média de Pontuacao por Tipo')
   plt.xlabel('Tipo')
   plt.ylabel('Média')
   plt.xticks(rotation=0)  # Rotate x-axis labels if needed
   plt.gcf().set_size_inches(9, 5)
   plt.savefig('media_pontuacao_if_bart.png')
   plt.clf()
# def to_string(result):
   #  return str(result).replace('[', '').replace(']', '').replace('{\'label\': \'', '(').replace('}', ')').replace(' stars\'', '').replace(' \'score\': ', '')


# with db.connect('./varit/database.db') as conn:
#     cursor = conn.cursor()
#     cursor.execute('SELECT titulo, estrelas_bert, pontuacao_bert FROM data')
#     conn.commit()
#     all = cursor.fetchall()
#     print(all[-10::])
    # cursor.executescript('''
    #     ALTER TABLE data
    #     ADD COLUMN estrelas_bert INTEGER;
    #     ALTER TABLE data
    #     ADD COLUMN pontuacao_bert REAL;
    # ''')
   #  exit(0)
   #  cursor.execute('SELECT titulo||\' \'||descricao AS text FROM data')
   #  conn.commit()
   #  texts = cursor.fetchall()
   #  print(texts[:3])
   #  result = analyse(texts[:3])
   #  print(result)
   #  print(to_string(result))
    # sql = '''
    # INSERT INTO data (estrelas_bert, pontuacao_bert)
    # VALUES {};
    # '''
    # cursor.execute(sql.format(to_string(result)))
    # conn.commit()

# resultados = sentiment_analyzer(texto)

# # Exibir os resultados
# for resultado in resultados:
#     sentimento = resultado['label']
#     pontuacao = resultado['score']
#     print(f"Sentimento: {sentimento}, Pontuação: {pontuacao}")
