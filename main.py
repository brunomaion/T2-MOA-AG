import tkinter as tk
import functions as fn
import time

janela = tk.Tk()
janela.title("Genetic Algorithm - MOA")
janela.geometry("1000x800")

viewport = tk.Canvas(janela, width=500, height=500, bg="white")
viewport.pack(padx=10, pady=10)

#solucao = [[100, 100], [200, 200], [200, 100], [100, 200]]
solucao = [[0, 0], [0, 100], [100, 100], [100, 0]]


def produto_vetorial(a, b):
    return a[0] * b[1] - a[1] * b[0]

def cruzamento_delete_cross(p1, p2, p3, p4):
    d1 = produto_vetorial([p1[0]-p3[0], p1[1]-p3[1]], [p4[0]-p3[0], p4[1]-p3[1]])
    d2 = produto_vetorial([p2[0]-p3[0], p2[1]-p3[1]], [p4[0]-p3[0], p4[1]-p3[1]])
    d3 = produto_vetorial([p3[0]-p1[0], p3[1]-p1[1]], [p2[0]-p1[0], p2[1]-p1[1]])
    d4 = produto_vetorial([p4[0]-p1[0], p4[1]-p1[1]], [p2[0]-p1[0], p2[1]-p1[1]])
    if (((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4<0))):
        return True
    else:
        return False



def operador_delete_cross(solucao):
    tamanho = len(solucao)
    for i in range(tamanho-1):
        p1 = solucao[i]
        p2 = solucao[i+1]
        for j in range(tamanho-1):
            if j != i and j != i-1:
                p3 = solucao[j]
                p4 = solucao[j+1]
                #print(f"Verificando segmentos: ({p1}, {p2}) e ({p3}, {p4})")
                cruzamento = cruzamento_delete_cross(p1, p2, p3, p4)
                print(cruzamento)
                if cruzamento:
                    solucao[i+1:j+1] = reversed(solucao[i+1:j+1])
    return solucao

nova_solucao = operador_delete_cross(solucao)

def atualizar():
    viewport.delete("all")
    nova_solucao = fn.embaralhar(solucao)
    fn.desenhar(nova_solucao, canvas=viewport, max_view_x=500, max_view_y=500)


fn.desenhar(solucao, canvas=viewport, max_view_x=500, max_view_y=500)
janela.after(1000, atualizar)
janela.mainloop()
