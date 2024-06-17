from os import listxattr
from auxiliar import buscar_buque,busca_api,extrair_json_server
from datetime import datetime
import requests

#Definindo Classes
class Flor:
  def __init__(self,id,nome,cor,preco,data,especie):
    self.id = id
    self.nome = nome
    self.cor = cor
    self.preco = preco
    self.data = data
    self.especie = especie

  def adicionar(self):
    dados = {"id":self.id,
             "nome":self.nome,
             "cor":self.cor,
             "preco":self.preco,
             "data":self.data,
             "especie":self.especie}
    url = "https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores"
    response = requests.post(url, json=dados)
    print("Adicionando flor... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
    if response.status_code == 201:
      print("Flor adicionada com sucesso... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
    else:
      print("Erro ao adicionar flor =c\n")


#Definindo Funções
def menu():
  print("\n✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿\n")
  print("Bem-vindo(a) à Floricultura!\nO que deseja fazer?\n\n")
  print("1 - Adicionar Flor\n2 - Remover Flor\n3 - Atualizar Flor\n4 - Listar Flores\n5 - Acessar Flor\n6 - Buscar preço do buquê\n7 - Buscar frase motivacional para cartão do buquê\n8 - Sair\n\n")
  print("✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿\n")


def eh_data(data):
  formato = "%d/%m/%Y"
  try:
    res = bool(datetime.strptime(data, formato))
  except ValueError:
    res = False
  return res

def remover_flor():
  id_remover = input("Digite o ID da flor que deseja remover: ")
  certeza = input("Tem certeza que deseja remover essa flor (s/n)? ")
  if certeza.upper() == "S":
    print("Removendo Flor... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
    url = "https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores/%s"%id_remover
    response = requests.delete(url)
    if response.status_code == 200:
      print("Flor de Id %s removida com sucesso!\n"%id_remover) 
    else:
      print("Erro ao remover flor =c\n")
  else:
    print("\nOperação cancelada!\n")


def atualizar_flor():
  id_achado = False
  id_desejado = input("Qual o ID da flor que deseja atualizar? ") 
  for flor in lista:
    if flor.id == id_desejado:
      print("Atualizando Flor %s... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n"%flor.nome)
      nome = input("Digite o novo nome da flor: ")
      cor = input("Digite a nova cor da flor: ")
      try:
        preco = float(input("Digite o novo preço da flor: "))
      except ValueError:
        print("\nPreço inválido! Digite um número!\n")
        return
      data = input("Digite a nova data de entrada da flor (dd/mm/aaaa): ")
      while not eh_data(data):
        print("\nData inválida! Tente novamente!!\n")
        data = input("Digite a nova data de entrada da flor (dd/mm/aaaa): ")
      especie = input("Digite a nova especie da flor: ")
      id_achado = True
  if id_achado:
    dados = {"id":id_desejado,
       "nome":nome,
       "cor":cor,
       "preco":preco,
       "data":data,
       "especie":especie} 
    url = "https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores/%s"%id_desejado
    response = requests.put(url,json=dados)
    if response.status_code == 201:
      print("Flor de Id %s atualizada com sucesso!\n"%id_desejado) 
    else:
      print("\nErro ao atualizar flor =c\n")
  else:
    print("\nFlor não encontrada!\n")


def acessar_flor():
  id_desejado = input("Qual o ID da flor que deseja acessar? ")
  url = "https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores/%s"%id_desejado
  response = requests.get(url)
  print("Acessando flor... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
  if response.status_code == 200:
    print("Acessando Flor de Id %s... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n"%id_desejado) 
    dic = response.json()
    print("Nome: %s\nCor: %s\nPreço: %.2f\nData de entrada: %s\nEspécie: %s\n"%(dic["nome"],dic["cor"],dic["preco"],dic["data"],dic["especie"]))
  else:
    print("Erro ao acessar flor =c\n")


def listar_flores():
  print("Listando Flores... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
  for flor in lista:
    print("%s: %s - R$%.2f\n"%(flor.id, flor.nome,flor.preco))
  print("⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")


#Bloco Principal

parar = True

while parar:
  menu()

  global lista
  lista = []
  lista_json = []
  lista_json = extrair_json_server()
  if lista_json == None:
    print('Ocorreu um erro ao extrair os dados do JSON-Server =c')
    break
  for elemento in lista_json:
    if elemento:
      florzinha = Flor(
        elemento['id'],
        elemento['nome'],
        elemento['cor'],
        float(elemento['preco']),
        elemento['data'],
        elemento['especie'])
      lista.append(florzinha)

  resposta = int(input("Digite uma das opções acima: "))
  print('\n')

  if resposta == 1:
    print("Adicionando Flor... ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘ ⚘\n")
    nome = input("Digite o nome da flor: ")
    cor = input("Digite a cor da flor: ")
    try:
      preco = float(input("Digite o preço da flor: "))
    except ValueError:
      print("\nPreço inválido! Digite um número!\n")
      continue
    data = input("Digite a data de entrada da flor (dd/mm/aaaa): ")
    while not eh_data(data):
      print("\nData inválida! Tente novamente!!\n")
      data = input("Digite a data de entrada da flor (dd/mm/aaaa): ")
    especie = input("Digite a espécie da flor: ")
    flor = Flor("",nome,cor,preco,data,especie)
    flor.adicionar()

  elif resposta == 2:
    remover_flor()

  elif resposta == 3:
    atualizar_flor() 

  elif resposta == 4:
    listar_flores()

  elif resposta == 5:
    acessar_flor() 

  elif resposta == 6:
    buscar_buque()

  elif resposta == 7:
    busca_api()

  elif resposta == 8:
    parar = False 
  else:
    print("Opção inválida! Tente novamente.\n")
