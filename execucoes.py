import tkinter as tk
import functions as fn
import time
import algoritmos as alg

berlin52 = fn.criar_grafo_berlin52()
ch150 = fn.criar_grafo_ch150()
rd400 = fn.criar_grafo_rd400()

def execucao(grafo, nome_grafo):
    n_geracoes = 500
    tam_pop = 100
    elit_pct = 0.025
    for i in range(20):
        
        nome_algoritmo = "AG Original"
        print(f"{nome_grafo} - {nome_algoritmo} - Execução {i+1}")
        resultados  = alg.algoritmo_genetico(
            grafo.vertices,
            n_geracoes,
            tam_pop,
            elit_pct
        )
        fn.adicionar_info_csv(
            "resultados.csv",
            nome_grafo,
            i+1,
            nome_algoritmo,
            resultados[0],
            resultados[2],
            resultados[3],
            resultados[4]
        )
        

        nome_algoritmo = "AG 1DeleteCross"
        print(f"{nome_grafo} - {nome_algoritmo} - Execução {i+1}")
        pop_inicial = alg.gerar_populacao_inicial(grafo.vertices, tam_pop)
        resultados  = alg.ag_1deletecross(
            pop_inicial,
            n_geracoes,
            tam_pop,
            elit_pct
        )
        fn.adicionar_info_csv(
            "resultados.csv",
            nome_grafo,
            i+1,
            nome_algoritmo,
            resultados[0],
            resultados[2],
            resultados[3],
            resultados[4]
        )
        
        nome_algoritmo = "AG 1DC-Solucao-Cluster2x2"
        print(f"{nome_grafo} - {nome_algoritmo} - Execução {i+1}")
        n_clusters = 2
        resultados  = alg.ag_1deletecross_cluster_solucao(
            grafo.vertices,
            n_geracoes,
            tam_pop,
            elit_pct,
            n_cluster=n_clusters
        )
        fn.adicionar_info_csv(
            "resultados.csv",
            nome_grafo,
            i+1,
            nome_algoritmo,
            resultados[0],
            resultados[2],
            resultados[3],
            resultados[4]
        )

        
        nome_algoritmo = "AG 1DC-AG-Cluster2x2"
        print(f"{nome_grafo} - {nome_algoritmo} - Execução {i+1}")
        n_clusters = 2
        resultados  = alg.ag_1deletecross_cluster_ag(
            grafo.vertices,
            n_geracoes,
            tam_pop,
            elit_pct,
            n_cluster=n_clusters
        )
        fn.adicionar_info_csv(
            "resultados.csv",
            nome_grafo,
            i+1,
            nome_algoritmo,
            resultados[0],
            resultados[2],
            resultados[3],
            resultados[4]
        )
        






     



fn.criar_csv()
execucao(berlin52, "berlin52")
execucao(ch150, "ch150")
execucao(rd400, "rd400")


