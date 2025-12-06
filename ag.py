import tkinter as tk
import functions as fn
import algoritmos as alg

n_geracoes = 100
tamanho_populacao = 100
elitismo_porcentagem = 0.05

ch150 = fn.criar_grafo_ch150()
pop_inicial = alg.gerar_populacao_inicial(ch150, tamanho_populacao)
sol_inicial = min(pop_inicial, key=lambda x: x[1])[0]
sol_final = alg.algoritmo_genetico(
    pop_inicial,
    ch150,
    n_geracoes,
    tamanho_populacao,
    elitismo_porcentagem
)

janela = tk.Tk()
janela.title("Genetic Algorithm - MOA")
janela.geometry("1000x800")

viewport = tk.Canvas(janela, width=500, height=500, bg="white")
viewport.pack(padx=10, pady=10)



fn.desenhar(sol_final, canvas=viewport, max_view_x=500, max_view_y=500)
janela.mainloop()