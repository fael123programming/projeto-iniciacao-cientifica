import openai, decouple
# import openai

openai.api_key = decouple.config('TEST_KEY')
# openai.api_key = 'chave'
# KEY = decouple.config('API_KEY')


def ask(*questions) -> str:
    msgs = list()
    for q in questions:
        msgs.append(
            {
                'role': 'user',
                'content': q
            }
        )
    response = openai.ChatCompletion.create(
        # api_key=KEY,
        model='gpt-3.5-turbo',
        messages=msgs
    )
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    print(ask("Who is Lula?"))
    