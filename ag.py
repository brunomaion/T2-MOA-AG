import tkinter as tk
import functions as fn
import time
import algoritmos as alg

janela = tk.Tk()
janela.title("Genetic Algorithm - MOA")
janela.geometry("1000x800")

viewport = tk.Canvas(janela, width=500, height=500, bg="white")
viewport.pack(padx=10, pady=10)

#solucao = [[100, 100], [200, 200], [200, 100], [100, 200]]
#solucao = [[0, 0], [0, 100], [100, 100], [100, 0]]

grafo = fn.criar_grafo_rd400()
iter3 = alg.ag_1deletecross_cluster_solucao(
    grafo.vertices,
    n_geracoes=20,
    tam_pop=50,
    elit_pct=0.05,
    n_cluster=2
)
solucao = iter3[1]
print("\nAG 1DC Cluster Resultados:", "\nCusto solução encontrada:", iter3[2],"\nTempo de execução (s):", iter3[3], "\nGanho relativo (%):", iter3[4])
fn.desenhar(solucao, canvas=viewport, max_view_x=500, max_view_y=500)
janela.mainloop()
