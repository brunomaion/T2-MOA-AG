
from Grafo import Grafo
import random

def euclidean_distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5


def embaralhar(lista):
    copia = lista[:]
    random.shuffle(copia)
    return copia


# TRATAR O ch150.tsp
def criar_grafo_ch150():
    fname = "arquivos_tsp/ch150.tsp"
    with open(fname, "r", encoding="utf-8") as f:
        texto = f.read()

    lines = texto.splitlines()
    lines = lines[6:-1]

    vertices=[]
    for line in lines:
        nodo_x = float(line.split()[1])
        nodo_y = float(line.split()[2])
        vertices.append([nodo_x, nodo_y])

    n = len(vertices)
    matriz = []

    for _ in range(n):
        matriz.append([0] * n)

    for i in range(n):
        for j in range(n):
            if i != j:
                matriz[i][j] = euclidean_distance(vertices[i], vertices[j])


    
    matriz_rotulada = []
    matriz_rotulada.append([""] + vertices)

    # outras linhas: [v_i]  dist dist dist ...
    for i in range(n):
        matriz_rotulada.append([vertices[i]] + matriz[i])


    ch150 = Grafo("ch150", vertices, matriz_rotulada)
    return ch150



def operador_ox(pai1, pai2):
    tamanho = len(pai1)

    p1 = random.randint(0, tamanho - 2)
    p2 = random.randint(p1 + 1, tamanho - 1)

    filho1 = [None] * tamanho
    filho2 = [None] * tamanho

    filho1[p1:p2] = pai1[p1:p2]
    filho2[p1:p2] = pai2[p1:p2]

    pos = p2 % tamanho
    for i in range(tamanho):
        item = pai2[(p2 + i) % tamanho]
        if item not in filho1:
            filho1[pos] = item
            pos = (pos + 1) % tamanho

    pos = p2 % tamanho
    for i in range(tamanho):
        item = pai1[(p2 + i) % tamanho]
        if item not in filho2:
            filho2[pos] = item
            pos = (pos + 1) % tamanho

    return filho1, filho2



def funcao_objetiva_por_matriz(solucao, matriz):
    soma=0
    for i in range(len(solucao)-1):
        soma += busca_matriz(matriz, solucao[i], solucao[i+1])
    soma += busca_matriz(matriz, solucao[-1], solucao[0])
    return soma


def busca_matriz(matriz, ponto_a, ponto_b):
    for i in range(len(matriz)-1):
        if matriz[i+1][0] == ponto_a:
            for j in range(len(matriz)-1):
                if matriz[0][j+1] == ponto_b:
                    return matriz[i+1][j+1]
    return None


def mutacao_dois_pontos(solucao):
    sol = solucao.copy()
    tamanho = len(sol)
    p1, p2 = random.sample(range(tamanho), 2)
    sol[p1], sol[p2] = sol[p2], sol[p1]
    return sol




def desenhar(pontos, canvas, max_view_x, max_view_y, margem=25):

    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    largura_original  = xmax - xmin if xmax != xmin else 1
    altura_original   = ymax - ymin if ymax != ymin else 1

    escala_x = (max_view_x - 2 * margem) / largura_original
    escala_y = (max_view_y - 2 * margem) / altura_original

    pontos_norm = []
    for px, py in pontos:
        x = (px - xmin) * escala_x + margem
        y = (py - ymin) * escala_y + margem
        pontos_norm.append((x, y))

    for x, y in pontos_norm:
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
    n = len(pontos_norm)
    for i in range(n):
        x0, y0 = pontos_norm[i]
        x1, y1 = pontos_norm[(i + 1) % n]
        canvas.create_line(x0, y0, x1, y1, fill="blue", width=1)
