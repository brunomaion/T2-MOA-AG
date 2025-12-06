import tkinter as tk
import functions as fn
import time


ch150 = fn.criar_grafo_ch150()


janela = tk.Tk()
janela.title("Genetic Algorithm - MOA")
janela.geometry("1000x800")

viewport = tk.Canvas(janela, width=500, height=500, bg="white")
viewport.pack(padx=10, pady=10)

solucao = [[100, 100], [200, 200], [200, 100], [100, 200]]

def atualizar():
    viewport.delete("all")
    nova_solucao = fn.embaralhar(solucao)
    fn.desenhar(nova_solucao, canvas=viewport, max_view_x=500, max_view_y=500)


fn.desenhar(solucao, canvas=viewport, max_view_x=500, max_view_y=500)
janela.after(2000, atualizar)
janela.mainloop()

