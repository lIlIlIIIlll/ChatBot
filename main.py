from openai import OpenAI
import time
import os
from tinydb import TinyDB, Query


def cls():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")


if not os.path.exists('api.txt'):
  api = input("Por favor, forneça a chave API para que possamos começar.\n")
  with open('api.txt', 'w') as f:
    f.write(api)
else:
  with open('api.txt', 'r') as f:
    api = f.read()


def chat(inpu, mod):
  client = OpenAI(api_key=api)
  historico.append({"role": "user", "content": inpu})
  completion = client.chat.completions.create(model=mod, messages=historico)
  historico.append({
      "role": "assistant",
      "content": completion.choices[0].message.content
  })
  return completion.choices[0].message.content


while True:
  cls()
  q = input("Deseja carregar algum log? (s/n)\n")
  if q == "n":
    historico = []
    break
  elif q == "s":
    if not os.path.exists("logs"):
      print("Pelo visto, você não tem uma pasta logs, eu irei criar uma para você e se você tiver algum arquivo de log, coloque nela para que possamos carrega-lo.")
      os.makedirs("logs")
      time.sleep(3)
    else:
      arquivos = os.listdir("logs")
      if not arquivos:
        print("Não existem logs na pasta de logs, por favor, insira algum arquivo de log para que ele possa ser carregado.")
        time.sleep(3)
      else:
        print("Existem os seguintes Logs:")
        for arquivo in arquivos:
          print(" - "+arquivo)
        namor = input("\nLog Selecionado: ")
        patr = os.path.join("logs",namor)
        db = TinyDB(patr)
        historico = db.all()
        break
  elif q != "n":
      print("Resposta inválida. Use apenas 's' ou 'n'.")
      time.sleep(2)
      continue

while True:
  cls()
  if historico == []:
    q = input("Deseja colocar mensagens do sistema? (s/n)\n")
    if q == "n":
      historico = []
      break
    elif q == "s":
      historico = []
      for i in range(int(input("Quantas?\n"))):
        cls()
        historico.append({
            "role": "system",
            "content": input(f"Digite a mensagem número {i+1}\n")
        })
      break
    elif q != "n":
      print("Resposta inválida. Use apenas 's' ou 'n'.")
      time.sleep(2)
      continue
  else:
    break

while True:
  cls()
  q = input("Quer setar um nome para você? Padrão = 'Usuário' (s/n)\n")
  if q != "s" and q != "n":
    print("Resposta Inválida. Responda apenas com 's' ou 'n'.")
    time.sleep(2)
    continue
  elif q == "s":
    nome = input("Qual será o nome?\n")
    break
  else:
    nome = "Usuário"
    break

while True:
  cls()
  q = input("Quer setar um nome para o ChatGPT? Padrão = 'ChatGPT' (s/n)\n")
  if q != "s" and q != "n":
    print("Resposta Inválida. Responda apenas com 's' ou 'n'.")
    time.sleep(2)
    continue
  elif q == "s":
    nomeGPT = input("Qual será o nome?\n")
    break
  else:
    nomeGPT = "ChatGPT"
    break

while True:
  contador = 0
  envio = ""
  for i, e in reversed(list(enumerate(historico))):
    if historico[i]["role"] == "user":
      contador += 1
      envio += f"{nome}:{historico[i]['content']}, "
    elif historico[i]["role"] == "assistant":
      contador += 1
      envio += f"{nomeGPT}:{historico[i]['content']}, "

  if contador == 8:
    envio += "Quero que você faça um resumo em bullet-points dos acontecimentos mais impactantes. Tente ser objetivo e escrever pouco, o resumo deve ser escrito de uma forma que você, ChatGPT, consiga entender facilmente o que se passa na cena. Não cite que eu solicitei esse resumo."
    for i, e in reversed(list(enumerate(historico))):
      if historico[i]["role"] == "user":
        del historico[i]
      elif historico[i]["role"] == "assistant":
        del historico[i]
    resumo = chat(envio, "gpt-3.5-turbo")
    for i, e in reversed(list(enumerate(historico))):
      if historico[i]["role"] == "user":
        del historico[i]
      elif historico[i]["role"] == "assistant":
        del historico[i]
    historico.append({"role": "assistant", "content": resumo})

  intup = input(f"\n{nome}: ")
  if intup == "cls":
    cls()
  elif intup == "hist":
    print(historico)
  elif intup == "save":
    nam = input("\n\nNome do Log: ")
    if not os.path.exists("logs"):
      nam = nam+".json"
      os.makedirs("logs")
      pat = os.path.join("logs",nam)
      db = TinyDB(pat)
      for msg in historico:
        if msg["role"] == "system":
          db.insert({"role":"system","content":msg["content"]})
        if msg["role"] == "assistant":
          db.insert({"role":"assistant","content":msg["content"]})
        if msg["role"] == "user":
          db.insert({"role":"user","content":msg["content"]})
      print("\n\nLog salvo com sucesso.")
    else:
      nam = nam+".json"
      pat = os.path.join("logs",nam)
      db = TinyDB(pat)
      for msg in historico:
        if msg["role"] == "system":
          db.insert({"role":"system","content":msg["content"]})
        if msg["role"] == "assistant":
          db.insert({"role":"assistant","content":msg["content"]})
        if msg["role"] == "user":
          db.insert({"role":"user","content":msg["content"]})
      print("\n\nLog salvo com sucesso.")
  elif intup == "del":
    inte = 0
    print("\n\nQual mensagem você deseja apagar?\n")
    for msg in historico:
      if msg["role"] == "assistant":
        print(f"- {nomeGPT}: {msg['content']} | Mensagem N°{inte}")
      elif msg["role"] == "user":
        print(f"- {nome}: {msg['content']} | Mensagem N°{inte}")
      elif msg["role"] == "system":
        print(f"- Sistema: {msg['content']} | Mensagem N°{inte}")
      inte+=1
    print("\n")
    inpo = int(input(""))
    if inpo > len(historico):
      print("Desculpe, mas o número é maior que a quantidade de mensagens, por favor, digite um número válido e correspondente à mensagem que você deseja apagar.")
    else:
      historico.pop(inpo) 
  elif intup == "edit":
    inte = 0
    print("\n\nQual mensagem você deseja editar?\n")
    for msg in historico:
      if msg["role"] == "assistant":
        print(f"- {nomeGPT}: {msg['content']} | Mensagem N°{inte}")
      elif msg["role"] == "user":
        print(f"- {nome}: {msg['content']} | Mensagem N°{inte}")
      elif msg["role"] == "system":
        print(f"- Sistema: {msg['content']} | Mensagem N°{inte}")
      inte+=1
    print("\n")
    inpo = int(input(""))
    msgn = input("\nMensagem editada: ")
    historico[inpo]["content"] = msgn
    print("\nMensagem editada com sucesso.\n\n")
  else:
    ai = chat(intup, "gpt-4-1106-preview")
    print(f"\n{nomeGPT}: {ai}")
