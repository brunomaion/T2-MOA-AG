import random
import functions as fn
import copy



def elitismo(populacao, elitismo_porcentagem):
  n_elites=int(len(populacao) * elitismo_porcentagem)
  populacao_ordenada = sorted(populacao, key=lambda x: x[1])
  return populacao_ordenada[:n_elites]


def cria_roleta(populacao):
    valores_invertidos = []
    for _, fit in populacao:
        valores_invertidos.append(1 / fit)
    fit_total = sum(valores_invertidos)
    roleta = []
    soma = 0
    for vi in valores_invertidos:
        x = vi / fit_total
        roleta.append(x)
        soma+=x
    return roleta


def selecionar_indice_roleta(roleta):
  while True:
    numero_sorteado = random.uniform(0, 1)
    soma = 0
    for i, prob in enumerate(roleta):
        soma += prob
        if numero_sorteado <= soma:
            indice_pai1 = i
            break
    numero_sorteado = random.uniform(0, 1)
    soma = 0
    for j, prob in enumerate(roleta):
        soma += prob
        if numero_sorteado <= soma:
            indice_pai2 = j
            break
    if indice_pai2 != indice_pai1:
        break
  return indice_pai1, indice_pai2


def selecao_torneio(pop, k):
    participantes = random.sample(pop, k)
    pai1 = min(participantes, key=lambda x: x[1])
    while True:
        participantes = random.sample(pop, k)
        pai2 = min(participantes, key=lambda x: x[1])
        if pai2 != pai1:
            break
    return pai1, pai2


def gerar_populacao_inicial(grafo, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = list(grafo.vertices)
        random.shuffle(individuo)
        fit = fn.funcao_objetiva_por_matriz(individuo, grafo.matriz_adj)
        populacao.append([individuo, fit])
    return populacao


def gerar_nova_populacao_roleta(populacao, tam_p):
    nova_pop = []
    roleta = cria_roleta(populacao)

    while len(nova_pop) < tam_p:
        i1, i2 = selecionar_indice_roleta(roleta)
        p1 = populacao[i1][0][:]
        p2 = populacao[i2][0][:]
        f1, f2 = fn.operador_ox(p1, p2)
        nova_pop.append(f1)
        nova_pop.append(f2)
    return nova_pop[:tam_p]


def gerar_nova_populacao_torneio(populacao, tam_p, tamanho_torneio=3):
    nova_pop = []
    while len(nova_pop) < tam_p:
        pai1, pai2 = selecao_torneio(populacao, tamanho_torneio)  # retorna [ind, fit], [ind, fit]
        p1 = pai1[0][:]   # copia do cromossomo do pai1
        p2 = pai2[0][:]   # copia do cromossomo do pai2
        f1, f2 = fn.operador_ox(p1, p2)
        nova_pop.append(f1)
        nova_pop.append(f2)
    return nova_pop[:tam_p]



def mutacao(populacao, grafo, n_mutacoes):
    nova = []
    for sol in populacao:
        mutado = sol[:]  
        for i in range(n_mutacoes):
          mutado = fn.mutacao_dois_pontos(mutado)
        #fit = fn.funcao_objetiva_por_matriz(mutado, grafo.matriz_adj)
        fit = fn.funcao_objetiva_por_calculo(mutado)
        nova.append([mutado, fit])         
    return nova


def algoritmo_genetico(pop_init, grafo, n_geracoes, tam_pop, elit_pct):
    pop = copy.deepcopy(pop_init)
    melhor_inicial = min(pop, key=lambda x: x[1])

    for g in range(n_geracoes):
        elites = elitismo(pop, elit_pct)
        filhos = gerar_nova_populacao_torneio(pop, tam_pop, tamanho_torneio=3)
        filhos = mutacao(filhos, grafo, n_mutacoes=1)
        pop = (elites + filhos)[:tam_pop]
        print("Geração:", g+1, "Melhor =", min(pop, key=lambda x: x[1])[1])

    melhor = min(pop, key=lambda x: x[1])

    print("\nSolução inicial:", melhor_inicial[1])
    print("Melhor solução encontrada:", melhor[1])

    return melhor[0]

