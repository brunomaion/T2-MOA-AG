import tkinter as tk
import functions as fn
from ProblemaDesenho import ProblemaDesenho


eil101 = fn.criar_grafo_eil101()

pai1 = eil101.vertices
pai2 = fn.embaralhar(pai1)

ponto_aleatorio=fn.random_05()

filho1, filho2 = fn.operador_ox(pai1, pai2, ponto_aleatorio)

eil101.salvar_matriz_csv("matriz_adj_eil101.csv")

print(pai1[:5])
print(pai2[:5])
print(filho1[:5])
print(filho2[:5])


