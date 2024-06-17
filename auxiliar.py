import requests
import re
import json
from bs4 import BeautifulSoup

def buscar_buque():
  url = "https://www.giulianaflores.com.br/tipos-de-flores/d1138/"
  response = requests.get(url)
  soup = BeautifulSoup(response.text, "html.parser")

  auxiliar = soup.find_all("h3", class_="title-item")

  precos = soup.find_all(class_="actual-price")

  busca = input("Digite o nome da flor: ")

  print("Buscando buquês... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
  achou = False
  for (i,flor) in enumerate(auxiliar):
    # print(i,flor.text.strip())
    if busca in flor.text.strip():
      print("\n%s"%flor.text.strip(),end=' - ')
      print(precos[i].text.strip())
      achou = True
  if not achou:
    print("\nNão foi possível encontrar o buquê desejado! =C")

  print('\n')


def busca_api():
  url = "https://zenquotes.io/api/random"
  response = requests.get(url)
  if response.status_code == 200:
    print("Extraindo frase... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
    dic = response.json()
    print("'" + dic[0]["q"] + "'")
    print(" -" + dic[0]["a"])
  else:
    print("Erro ao extrair frase de API =c")

def extrair_json_server():
  url = "https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores"
  response = requests.get(url)
  print("Extraindo informações... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
  if response.status_code == 200:
    lista = response.json()
    return lista
    