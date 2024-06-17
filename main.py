from flask import Flask, request, render_template, redirect
import json
from uuid import uuid4
import xml.etree.ElementTree as ET

app = Flask(__name__)

#Parte nova
@app.route('/home')
def flor_list():
  try:
    florlist = []
    with open("db.json") as arq:
      florlist = json.loads(arq.read())
      for i in range(len(florlist)):
        florlist[i]["url"] = 'https://8da8fe9e-86d1-4fa2-b7bd-7a00fb7ec0ec-00-3jn59t72e4ixa.kirk.replit.dev:3000/flores/%s'%florlist[i]["id"] #!!!!!
    return render_template("list.html", florlist=florlist)
  except:
    return "Erro interno do servidor", 500
    

@app.route('/form', methods=["GET", "POST"])
def flor_form():
  try:
    vazio = {"flor": {}}
    if request.method == "POST":
      with open("db.json", "r+") as arq:
        florlist = json.loads(arq.read())
        new_flor = dict(request.form)
        new_flor["id"] = str(uuid4())
        florlist.append(new_flor)
  
        arq.seek(0)
        arq.truncate()
        arq.write(json.dumps(florlist))
      return redirect("/home")
    return render_template("form.html", flor=vazio)
  except:
    return "Erro interno do servidor", 500

@app.route('/edit/<string:id>', methods=["GET", "POST"])
def flor_edit(id):
  try:
    florlist = []
    with open("db.json", "r+") as arq:
      florlist = json.loads(arq.read())
      old_flor = dict(request.form)
      old_flor_id = find_by_id(id, florlist)
  
      if old_flor_id != -1:
        old_flor["id"] = id
        if request.method == "POST":
          florlist[old_flor_id] = old_flor
          arq.seek(0)
          arq.truncate()
          arq.write(json.dumps(florlist))
  
          return redirect("/home")
      else:
        return "Flor não encontrada", 404
  
    return render_template("form.html", flor=florlist[old_flor_id])
  except:
    return "Erro interno do servidor", 500

@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def flor_delete(id):
  try:
    florlist = []
    
    with open("db.json", "r+") as arq:
      florlist = json.loads(arq.read())
      florIdDeleta = find_by_id(id, florlist)
      if florIdDeleta != -1:
          florlist.pop(florIdDeleta)
          arq.seek(0)
          arq.truncate()
          arq.write(json.dumps(florlist))
    return redirect("/home")
  except:
    return "Erro interno do servidor", 500

#Parte antiga
def find_by_id(id, lista):
  for i in range(len(lista)):
    if lista[i]["id"] == id:
      return i
  return -1

@app.route('/flores')  
def read_all():
  flores = []
  try:
    with open("db.json") as arq:
      flores = json.loads(arq.read())
    return flores, 200
  except:
    return "Erro interno do servidor", 500

@app.route('/flores/<string:id>') 
def read_one(id):
  flores = []
  try:
    with open("db.json") as arq:
      flores = json.loads(arq.read())
      florId = find_by_id(id, flores)
      if florId != -1:
        return flores[florId], 200
  except:
    return "Erro interno do servidor", 500

@app.route('/flores', methods=['POST'])
def create_one():
  flores = []
  try:
    with open("db.json", "r+") as arq:
      flores = json.loads(arq.read())
      nova_flor = request.json
      nova_flor["id"] = str(uuid4())
      flores.append(nova_flor)

      arq.seek(0)
      arq.truncate()
      arq.write(json.dumps(flores))
      
    tree = ET.parse("dados.xml")
    root = tree.getroot()
    elemento = ET.Element("flor", attrib={"id": nova_flor["id"]})
    flor_nome = ET.SubElement(elemento, "nome")
    flor_nome.text = nova_flor["nome"]
    flor_cor = ET.SubElement(elemento, "cor")
    flor_cor.text = nova_flor["cor"]
    flor_preco = ET.SubElement(elemento, "preco")
    flor_preco.text = str(nova_flor["preco"])
    flor_data = ET.SubElement(elemento, "data")
    flor_data.text = nova_flor["data"]
    flor_especie = ET.SubElement(elemento, "especie")
    flor_especie.text = nova_flor["especie"]
    
    root.append(elemento)
    tree.write("dados.xml")
        
    return flores, 201
  except:
    return "Erro interno do servidor", 500


@app.route('/flores/<string:id>', methods=['PUT'])
def update_one(id):
  flores = []
  try:
    with open("db.json", "r+") as arq:
      flores = json.loads(arq.read())
      flor_update = request.json
      flor_updateId = find_by_id(id, flores)
      if flor_updateId != -1:
        flor_update["id"] = id
        flores[flor_updateId] = flor_update
  
      else:
        return "flormon não encontrado", 404
  
      arq.seek(0)
      arq.truncate()
      arq.write(json.dumps(flores))

    tree = ET.parse("dados.xml")
    root = tree.getroot()
    for flor in root.findall("flor"):
      if flor.attrib["id"] == id:
        flor.find("nome").text = flor_update["nome"]
        flor.find("cor").text = flor_update["cor"]
        flor.find("preco").text = str(flor_update["preco"])
        flor.find("data").text = flor_update["data"]
        flor.find("especie").text = flor_update["especie"]
        
    tree.write("dados.xml")
    return flor_update, 201
  except:
    return "Erro interno do servidor", 500

@app.route('/flores/<string:id>', methods=['DELETE'])
def delete_one(id):
  flores = []
  try:
    with open("db.json", "r+") as arq:
      flores = json.loads(arq.read())
      flor_deletaId = find_by_id(id, flores)
      if flor_deletaId != -1:
        flores.pop(flor_deletaId)
  
      else:
        return "Flor não encontrada", 404
  
      arq.seek(0)
      arq.truncate()
      arq.write(json.dumps(flores))

    tree = ET.parse("dados.xml")
    root = tree.getroot()
    for flor in root.findall("flor"):
      if flor.attrib["id"] == id:
        root.remove(flor)

    tree.write("dados.xml")
    return flores, 200
  except:
    return "Erro interno do servidor", 500


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)  