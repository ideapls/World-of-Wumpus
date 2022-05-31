import csv
from math import sqrt
from math import pow
from character import Character

mapa = open("mapa")
leitor_problema = csv.reader(mapa)
entrada = list(leitor_problema)  # lista de nós do mapa

c = Character(1, 0, 0)


def encontra_posicoes(matriz, M, N, valor):  # Retorna posição dado o mapa, o tamanho do mapa e o valor a ser encontrado
    # no mapa
    posicoes = []
    for i in range(0, M):
        for j in range(0, N):
            if matriz[i][j] == valor:
                posicoes.append((i, j))
    return posicoes


def encontra_estados_sucessores(matriz, M, N, posicao_atual):  # A partir do estado atual, retorna os nós vizinhos
    i = posicao_atual[0]
    j = posicao_atual[1]
    estados_sucessores = []
    if i > 0 and (matriz[i - 1][j] != 'm' and matriz[i - 1][j] != 'p'):  # Cima
        estados_sucessores.append((i - 1, j))
    if i + 1 < M and (matriz[i + 1][j] != 'm' and matriz[i + 1][j] != 'p'):  # Baixo
        estados_sucessores.append((i + 1, j))
    if j > 0 and (matriz[i][j - 1] != 'm' and matriz[i][j - 1] != 'p'):  # Esquerda
        estados_sucessores.append((i, j - 1))
    if j + 1 < N and (matriz[i][j + 1] != 'm' and matriz[i][j + 1] != 'p'):  # Direita
        estados_sucessores.append((i, j + 1))
    return estados_sucessores


def encontra_estado_mais_promissor(franja, heuristica_estados):
    valor_mais_promissor = 1000000000
    estado_mais_promissor = None
    indice_mais_promissor = 0
    indice = 0
    for estado in franja:
        if heuristica_estados[estado] < valor_mais_promissor:
            estado_mais_promissor = estado
            valor_mais_promissor = heuristica_estados[estado]
            indice_mais_promissor = indice
        indice = indice + 1
    return indice_mais_promissor


def calcula_distancia_meta(estado, estados_finais):
    x = estado[0]
    y = estado[1]
    distancia_minima = 1000000000

    for estado_final in estados_finais:
        x_estado_final = estado_final[0]
        y_estado_final = estado_final[1]
        diff1 = x_estado_final - x
        diff2 = y_estado_final - y
        soma_diffs = pow(diff1, 2) + pow(diff2, 2)
        distancia_atual = sqrt(soma_diffs)
        if distancia_atual < distancia_minima:
            distancia_minima = distancia_atual
    return distancia_minima


def apresenta_solucao(estado, predecessores, iteracao):
    caminho = [estado]
    print("Solução encontrada com " + str(iteracao) + "ações.")
    while predecessores[estado] is not None:
        caminho.append(predecessores[estado])
        estado = predecessores[estado]
    caminho = caminho[::-1]
    print(caminho)


def busca_a_estrela(matriz, M, N, estado_inicial, estados_finais):
    distancia_meta = {}
    distancia_percorrida = {}
    heuristica = {}
    predecessores = {}
    estados_expandidos = []
    solucao_encontrada = False

    print("Algoritmo: A* (A Estrela)")

    # Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
    distancia_percorrida[estado_inicial] = 0
    distancia_meta[estado_inicial] = calcula_distancia_meta(estado_inicial, estados_finais)
    heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_meta[estado_inicial]
    predecessores[estado_inicial] = None
    print("Heuristica da Distancia no Estado Inicial: " + str(heuristica[estado_inicial]))
    franja = []
    franja.append(estado_inicial)
    iteracao = 1
    while len(franja) != 0:
        # mostra_valores_franja (franja, heuristica)
        indice_mais_promissor = encontra_estado_mais_promissor(franja, heuristica)
        estado = franja.pop(indice_mais_promissor)
        if estado in estados_finais:
            solucao_encontrada = True
            break
        estados_sucessores = encontra_estados_sucessores(matriz, M, N, estado)
        estados_expandidos.append(estado)
        for i in range(0, len(estados_sucessores)):
            sucessor = estados_sucessores[i]
            if sucessor not in estados_expandidos and sucessor not in franja:
                franja.append(sucessor)
                if sucessor not in heuristica.keys():
                    distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
                    distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
                    heuristica[sucessor] = distancia_meta[sucessor] + distancia_percorrida[sucessor]
                    predecessores[sucessor] = estado
        iteracao = iteracao + 1

    if solucao_encontrada:
        apresenta_solucao(estado, predecessores, iteracao)
    else:
        print("Não foi possível encontrar uma solução para o problema.")


M = int(entrada[0][0])
N = int(entrada[0][1])
matriz = entrada[1:]

estado_inicial = encontra_posicoes(matriz, M, N, 'c')
estados_finais = encontra_posicoes(matriz, M, N, 'g')

#print(encontra_estados_sucessores(matriz, M, N, ))
for m in matriz:
    print(m)
#print(estados_finais)
busca_a_estrela(matriz, M, N, estado_inicial[0], estados_finais)
