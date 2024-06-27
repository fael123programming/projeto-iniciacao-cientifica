title, description = csv.iloc[i][['titulo', 'descricao']]                                        # type: ignore
response = openai.ChatCompletion.create(                                                         # type: ignore
    api_key=key,                                                                                 # type: ignore
    model='gpt-3.5-turbo',
    messages=get_messages(title, description)                                                    # type: ignore
)
answer = response['choices'][0]['message']['content'].replace('.', '')
csv.loc[i, 'subject'] = answer                                                   # type: ignore
