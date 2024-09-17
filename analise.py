import os
import time
import json
from random import random
from datetime import datetime
import csv
from sys import argv

import requests
import pandas as pd
import seaborn as sns


import requests

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Retrieve the CDI rate from the Banco Central do Brasil (BCB) website

try: 
  response = requests.get(url=URL)
  response.raise_for_status()
except requests.HTTPError as exc:
  print('Dado não encontrado, continuando.')
  cdi = None
except Exception as exc:
  print('Error, parado a execução.')
  raise exc
else:
  dado = json.loads(response.text)[-1]['valor']

# criando a variável data e hora

for _ in range(0, 10):
  data_e_hora = datetime.now()
  data = data_e_hora.strftime('%Y/%m/%d')  
  hora = data_e_hora.strftime('%H:%M:%S')

  cdi = float(dado) + (random() - 0.5)

  # Verifica se o arquivo 'taxa-cdi.csv' existe

  if os.path.exists('./taxa-cdi.csv') == False:
    with open(file='./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
      fp.write(f'data,hora,taxa\n')
    

  # Salvando dados no arquivo 'taxa-cdi.csv' 

  with open(file='taxa-cdi.csv', mode='a', encoding='utf8') as fp:
    fp.write(f'{data},{hora},{cdi}\n')

  time.sleep(1)

# Extraindo as colunas hora e taxa

df = pd.read_csv('./taxa-cdi.csv')

# Salvando no grafico

grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
grafico.set_xticks(range(len(df['hora']))) 
_ = grafico.set_xticklabels(labels=df['hora'], rotation=90)
grafico.get_figure().savefig(f"{argv[1]}.png")

print('Sucesso')
