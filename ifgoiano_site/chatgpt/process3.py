import os, pandas
from process2 import PATH
from process import EXPORT_ARGS


def multiple_in(txt, *args):
    for arg in args:
        if arg.lower() in txt.lower():
            return True
    return False


if __name__ == '__main__':
    df = pandas.read_csv(PATH)
    for i in range(df.shape[0]):
        assunto = df.loc[i, 'assunto']
        if multiple_in(assunto, 'ações', 'ação', 'extensão', 'evento', 'competição', 'competições', 'participa', 'cerimônia', 'live', 'arte', 'cultura', 'parcerias', 'evento', 'lançamento', 'pesquisadores', 'docência', 'projeto', 'pesquisa', 'conselhos', 'congresso', 'reunião', 'workshop', 'visita', 'esporte', 'seminário', 'simpósio'):
            assunto = 'acoes de extensao'
        elif multiple_in(assunto, 'comunicado', 'ead', 'plano', 'calendário', 'marca'):
            assunto = 'comunicados oficiais'
        elif multiple_in(assunto, 'conquista'):
            assunto = 'conquistas de membros'
        elif multiple_in(assunto, 'campanha'):
            assunto = 'campanhas'
        elif multiple_in(assunto, 'edital', 'editais', 'resultados', 'benefícios', 'fest'):
            assunto = 'editais'
        elif multiple_in(assunto, 'processo', 'seletivo', 'processo seletivo', 'resultado'):
            assunto = 'processos seletivos'
        elif multiple_in(assunto, 'publicações', 'publicacao', 'obra literária', 'boletim', 'boletins'):
            assunto = 'publicacoes'
        elif multiple_in(assunto, 'avaliação', 'avaliações'):
            assunto = 'avaliacao'
        df.loc[i, 'assunto'] = assunto
    print(df['assunto'].unique())
    df.to_csv(PATH, **EXPORT_ARGS)