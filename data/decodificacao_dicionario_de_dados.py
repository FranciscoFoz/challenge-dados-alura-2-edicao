#Decodificação do dicionário de dados

import requests

dicionario = requests.get('https://challenge-data-science-3ed.s3.amazonaws.com/dicionario.md').text.encode('latin1').decode('utf-8')

with open('dicionario_de_dados.md', 'w', encoding='utf-8') as arquivo:
    arquivo.write(dicionario)