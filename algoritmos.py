import random
import functions as fn
import copy
import time


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


def gerar_populacao_inicial(pontos, tamanho_populacao):
    populacao = []
    for _ in range(tamanho_populacao):
        individuo = list(pontos)
        random.shuffle(individuo)
        fit = fn.funcao_objetiva_por_calculo(individuo)
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

def avaliar_pop(populacao):
    nova = []
    for sol in populacao:
        fit = fn.funcao_objetiva_por_calculo(sol)
        nova.append([sol, fit])
    return nova

def mutacao(populacao, n_mutacoes):
    nova = []
    for sol in populacao:
        mutado = sol[:]  
        for i in range(n_mutacoes):
          mutado = fn.mutacao_dois_pontos(mutado)
        nova.append(mutado)         
    return nova

def mutacao_deletecross(populacao, n_mutacoes):
    nova = []
    for sol in populacao:
        mutado = sol[:]  
        for i in range(n_mutacoes):
          mutado = fn.operador_delete_cross(mutado)
        nova.append(mutado)         
    return nova

def mutacao_1deletecross(populacao, n_mutacoes):
    nova = []
    for sol in populacao:
        mutado = sol[:]  
        for i in range(n_mutacoes):
          mutado = fn.operador_1delete_cross(mutado)
        nova.append(mutado)         
    return nova

def algoritmo_genetico(pontos, n_geracoes, tam_pop, elit_pct):
    pop_init = gerar_populacao_inicial(pontos, tam_pop)
    tempo_inicio = time.time()
    pop = copy.deepcopy(pop_init)
    melhor_inicial = min(pop, key=lambda x: x[1])

    for g in range(n_geracoes):
        elites = elitismo(pop, elit_pct)
        filhos = gerar_nova_populacao_torneio(pop, tam_pop, tamanho_torneio=3)
        filhos = mutacao(filhos, n_mutacoes=1)
        filhos = avaliar_pop(filhos)
        pop = (elites + filhos)[:tam_pop]
        #print("Geração:", g+1, "Melhor =", min(pop, key=lambda x: x[1])[1])

    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    melhor = min(pop, key=lambda x: x[1])
    fit_melhor = melhor[1]
    ganho_relativo = ((melhor_inicial[1] - melhor[1]) / melhor_inicial[1]) * 100
    #print("\nSolução inicial:", melhor_inicial[1])
    #print("Melhor solução encontrada:", melhor[1])
    #print("Tempo de execução (s):", tempo_execucao)
    #print("Ganho relativo (%):", ganho_relativo)
    fit_inicial = melhor_inicial[1]
    melhor_solucao = melhor[0]
    return fit_inicial, melhor_solucao, fit_melhor, tempo_execucao, ganho_relativo


def ag_deletecross(pontos, n_geracoes, tam_pop, elit_pct):
    pop_init = gerar_populacao_inicial(pontos, tam_pop)
    tempo_inicio = time.time()
    pop = copy.deepcopy(pop_init)
    melhor_inicial = min(pop, key=lambda x: x[1])

    for g in range(n_geracoes):
        elites = elitismo(pop, elit_pct)
        filhos = gerar_nova_populacao_torneio(pop, tam_pop, tamanho_torneio=3)
        filhos = mutacao_deletecross(filhos, n_mutacoes=1)
        filhos = avaliar_pop(filhos)
        pop = (elites + filhos)[:tam_pop]
        #print("Geração:", g+1, "Melhor =", min(pop, key=lambda x: x[1])[1])

    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    melhor = min(pop, key=lambda x: x[1])
    fit_melhor = melhor[1]
    ganho_relativo = ((melhor_inicial[1] - melhor[1]) / melhor_inicial[1]) * 100
    fit_inicial = melhor_inicial[1]
    melhor_solucao = melhor[0]
    return fit_inicial, melhor_solucao, fit_melhor, tempo_execucao, ganho_relativo

def ag_1deletecross(pop_init, n_geracoes, tam_pop, elit_pct):
    tempo_inicio = time.time()
    pop = copy.deepcopy(pop_init)
    melhor_inicial = min(pop, key=lambda x: x[1])

    n_mutacoes = int(len(pop_init[0][0]) *.05)
    for g in range(n_geracoes):
        elites = elitismo(pop, elit_pct)
        filhos = gerar_nova_populacao_torneio(pop, tam_pop, tamanho_torneio=3)
        filhos = mutacao_1deletecross(filhos, n_mutacoes=n_mutacoes)
        #filhos = mutacao(filhos, n_mutacoes=1)
        filhos = avaliar_pop(filhos)
        pop = (elites + filhos)[:tam_pop]
        #print("Geração:", g+1, "Melhor =", min(pop, key=lambda x: x[1])[1])

    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    melhor_individuo = min(pop, key=lambda x: x[1])
    melhor_solucao = melhor_individuo[0]
    fit_melhor = melhor_individuo[1]
    ganho_relativo = ((melhor_inicial[1] - fit_melhor) / melhor_inicial[1]) * 100
    fit_inicial = melhor_inicial[1]
    return fit_inicial, melhor_solucao, fit_melhor, tempo_execucao, ganho_relativo, pop


def ag_1deletecross_cluster_solucao(pontos, n_geracoes, tam_pop, elit_pct, n_cluster=2):
    grafos_cluster = fn.separar_grupos(pontos, n_cluster)

    tempo_inicio = time.time()
    melhores_finais_grupos = []

    pop_inicial = gerar_populacao_inicial(pontos, tam_pop)
    melhor_inicial = min(pop_inicial, key=lambda x: x[1])
    fit_melhor_inicial = melhor_inicial[1]

    for i in grafos_cluster:  
        grupo = grafos_cluster[i]  
        pop_inicial = gerar_populacao_inicial(grupo, tam_pop)
        sol_final = ag_1deletecross(
            pop_inicial,
            n_geracoes,
            tam_pop,
            elit_pct
        )
        melhor_solucao = sol_final[1]
        #print("Tamanho grupo", len(melhor_solucao))
        #print("\nCusto grupo", fn.funcao_objetiva_por_calculo(melhor_solucao))
        melhores_finais_grupos.append(melhor_solucao)
        
    melhor_solucao_final = fn.juntar_grupos_por_centro(melhores_finais_grupos)
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    #print("Tamanho solução final:", len(melhor_solucao_final))
    #print(len(melhor_solucao_final))
    #print(fn.duplicados(melhor_solucao_final))
    fit_melhor = fn.funcao_objetiva_por_calculo(melhor_solucao_final)

    ganho_relativo = ((melhor_inicial[1] - fit_melhor) / melhor_inicial[1]) * 100
    return fit_melhor_inicial, melhor_solucao_final, fit_melhor, tempo_execucao, ganho_relativo
 

def ag_1deletecross_cluster_ag(pontos, n_geracoes, tam_pop, elit_pct, n_cluster=2):
    grafos_cluster = fn.separar_grupos(pontos, n_cluster)
    tempo_inicio = time.time()
    pop_inicial = gerar_populacao_inicial(pontos, tam_pop)
    melhor_inicial = min(pop_inicial, key=lambda x: x[1])
    fit_melhor_inicial = melhor_inicial[1]

    pop_grupos = []
    for i in grafos_cluster:  
        grupo = grafos_cluster[i]  

        pop_inicial = gerar_populacao_inicial(grupo, tam_pop)
        sol_final = ag_1deletecross(
            pop_inicial,
            n_geracoes,
            tam_pop,
            elit_pct
        )
        pop_grupos.append(sol_final[5])

    pop_concat = fn.juntar_populacoes_por_centro(pop_grupos)
    #for i in pop_concat:
    #    print("Fit individuo:", i[1])
    sol_concat = ag_1deletecross(
            pop_concat,
            n_geracoes,
            tam_pop,
            elit_pct
            )

    melhor_solucao_final = sol_concat[1]
    #print(fn.duplicados(melhor_solucao_final))
    tempo_fim = time.time()
    tempo_execucao = tempo_fim - tempo_inicio
    fit_melhor = sol_concat[2]

    ganho_relativo = ((melhor_inicial[1] - fit_melhor) / melhor_inicial[1]) * 100
    return fit_melhor_inicial, melhor_solucao_final, fit_melhor, tempo_execucao, ganho_relativo
