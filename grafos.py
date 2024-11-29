import time
import os

def ordem(grafo):
  return len(grafo) - 1

def tamanho(grafo):
  tamanho = 0
  for linha in grafo:
    for i in range(1, ordem(grafo)+1):
      if linha[i] != 0:
        tamanho += 1
  return tamanho // 2

def densidade(grafo):
  return tamanho(grafo)/ordem(grafo)

def vizinhos(grafo, vertice):
  vizinhos = []
  for i in range(1, ordem(grafo)+1):
    if grafo[vertice][i] != 0:
      vizinhos.append(i)
  return vizinhos

def grauVertice(grafo, vertice):
  return len(vizinhos(grafo, vertice))

def verificaArticulacao(grafo, vertice):
  def dfs(grafo, vertice, visitados): #Busca em profundidade
    visitados[vertice] = True
    for vizinho in vizinhos(grafo, vertice):
      if not visitados[vizinho]:
        dfs(grafo, vizinho, visitados)

  buscaOriginal =  [False] * (ordem(grafo) + 1)
  dfs(grafo, 1, buscaOriginal)

  visitados = [False] * (ordem(grafo) + 1)
  visitados[vertice] = True  
 
  if vertice == 1:
    dfs(grafo, 2, visitados)
  else:
    dfs(grafo, 1, visitados)

  for i in range(1, ordem(grafo) + 1):
    if visitados[i] != buscaOriginal[i] and i != vertice:
      return True
  return False


def bfs(grafo, vertice, operacao):  #Busca em largura 
  visitados = [False] * (ordem(grafo) + 1)
  ordemVisita = []
  fila = [vertice]
  visitados[vertice] = True
  ordemVisita.append(vertice)
  arestasRetorno = []
  arestasNormal = []

  while fila:
    atual = fila.pop(0)
    for vizinho in vizinhos(grafo, atual):
      print(atual, vizinho)
      if not visitados[vizinho]:
        visitados[vizinho] = True
        fila.append(vizinho)
        ordemVisita.append(vizinho)
        arestasNormal.append((atual, vizinho))
      else:
        if(atual != vertice and vizinho != vertice and (vizinho, atual) not in arestasRetorno and (vizinho, atual) not in arestasNormal):
          arestasRetorno.append((atual, vizinho))
  if operacao == 1:
    return ordemVisita
  elif operacao == 2:
    return arestasRetorno  
  else:
    print("Ordem de visita:", ordemVisita)
    print("Arestas de retorno:", arestasRetorno)


def componentesConexas(grafo):
  visitados = [False] * (ordem(grafo) + 1)
  componentes = []

  def dfs(grafo, vertice, componente):
    visitados[vertice] = True
    componente.append(vertice)
    for vizinho in vizinhos(grafo, vertice):
      if not visitados[vizinho]:
        dfs(grafo, vizinho, componente)

  for vertice in range(1, ordem(grafo) + 1):
    if not visitados[vertice]:
      componente = []
      dfs(grafo, vertice, componente)
      componentes.append(componente)

  return componentes

def qtdComponentesConexas(grafo):
  return len(componentesConexas(grafo))


def possuiCiclo(grafo):
  def dfs(grafo, vertice, visitados, pai):  # Busca em profundidade
    visitados[vertice] = True
    for vizinho in vizinhos(grafo, vertice):
      if not visitados[vizinho]:  # Explora apenas vértices não visitados
        if dfs(grafo, vizinho, visitados, vertice):  # Passa o vértice atual como pai
          return True
      elif vizinho != pai:  # Vizinho já visitado que não é o pai indica ciclo
          return True
    return False
  """
    LOGICA DO GUILHERME

    FOR COMPONENTE IN COMPONENTES:
    ...
  """
  visitados = [False] * (ordem(grafo) + 1)  # Assumindo vértices indexados de 1 a n

  for vertice in range(1, ordem(grafo) + 1):  # Lida com componentes desconexas
    if not visitados[vertice]:
      if dfs(grafo, vertice, visitados, -1):  # Usa -1 como pai inicial
        return True
  return False


def leituraArquivo(nome):
  grafo = []
  try:
    with open(nome, 'r') as arquivo:
      tamanho = int(arquivo.readline().strip()) 
      grafo = [[0 for _ in range(tamanho + 1)] for _ in range(tamanho + 1)]
      
      linhas =  arquivo.readlines()
      for linha in linhas:
        inicio, fim, peso = map(str, linha.split())
        inicio = int(inicio) 
        fim = int(fim) 
        peso = float(peso)
        grafo[inicio][fim] = peso
        grafo[fim][inicio] = peso

  except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado.")
  except Exception as nome:
    print(f"Erro ao ler o arquivo: {nome}")

  return grafo

def main():
  #nome = input("Digite o caminho do arquivo: ")
  nome = "teste.txt"
  grafo = leituraArquivo(nome)

  print("Bem-vindo à biblioteca de grafos não direcionados ponderados!\n")

  print("Matriz de pesos:")
  for linha in grafo:
    print(linha)

  opcao = int(1)
  while (opcao != 0):
      print("\nEscolha uma opção:")
      print("1 - Retornar a ordem do grafo")
      print("2 - Retornar o tamanho do grafo")
      print("3 - Retornar a densidade ε(G) do grafo")
      print("4 - Retornar os vizinhos de um vértice fornecido")
      print("5 - Retornar o grau de um vértice fornecido")
      print("6 - Verificar se um vértice é articulação")
      print("7 - Retornar a sequência de vértices visitados na busca em largura e informar a(s) aresta(s) que não faz(em) parte da árvore de busca em largura")
      print("8 - Retornar o número de componentes conexas do grafo e os vértices de cada componente")
      print("9 - Verificar se um grafo possui ciclo")
      print("10 - Retornar a distância e o caminho mínimo")
      print("0 - Sair\n")

      opcao = int(input("Digite a opção desejada: "))

      match opcao:
        case 0:
          break
        case 1:
          print("Ordem do grafo:", ordem(grafo))
        case 2:
          print("Tamanho do grafo:", tamanho(grafo))
        case 3:
          print("Densidade do grafo:", densidade(grafo))
        case 4:
          vertice = int(input("Digite o vértice: "))
          print(f"Vizinhos do vértice {vertice}: {vizinhos(grafo, vertice)}")
        case 5:
          vertice = int(input("Digite o vértice: "))
          print(f"Grau do vértice {vertice}: {grauVertice(grafo, vertice)}")
        case 6:
          vertice = int(input("Digite o vértice: "))
          if(verificaArticulacao(grafo, vertice) == True):
            print(f"O vértice {vertice} é uma articulação")
          else:
            print(f"O vértice {vertice} não é uma articulação")
        case 7:
          vertice = int(input("Digite o vértice pelo qual deseja iniciar a busca: "))
          print(f"Busca em largura a partir do vértice {vertice}: ")
          bfs(grafo, vertice, 3)
        case 8:
          componentes = componentesConexas(grafo)
          print("Número de componentes conexas:", len(componentes))
          for i, componente in enumerate(componentes):
            print(f"Componente {i+1}: {componente}")
        case 9:
          if({possuiCiclo(grafo)} == True):
            print("O grafo possui ciclo")
          else:
            print("O grafo não possui ciclo")
        case 10:
          print("Função de determinar distância e caminho mínimo ainda não implementada.")
        case _:
          print("Opção inválida. Tente novamente.")
      input("Pressione Enter para continuar...")
      os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
  main()