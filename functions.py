
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
    ponto_rand = random.uniform(0.15, 0.4)
    ponto_inicio = int(tamanho * ponto_rand)
    ponto_fim = int(tamanho * (1 - ponto_rand))

    centro_pai1 = pai1[ponto_inicio:ponto_fim]
    centro_pai2 = pai2[ponto_inicio:ponto_fim]

    lista1 = pai1[ponto_fim:] + pai1[:ponto_fim]
    lista2 = pai2[ponto_fim:] + pai2[:ponto_fim]
    lista1 = [x for x in lista1 if x not in centro_pai2]
    lista2 = [x for x in lista2 if x not in centro_pai1]
    filho1 = lista1[ponto_inicio:] + centro_pai2 + lista1[:ponto_inicio]
    filho2 = lista2[ponto_inicio:] + centro_pai1 + lista2[:ponto_inicio]
    return filho1, filho2


#pai1 = [7,4,1,2,5,6,8,3]
#pai2 = [1,2,5,8,7,4,3,6]
#filho1, filho2 = operador_ox(pai1, pai2)
#print("Pai 1:", pai1)
#print("Pai 2:", pai2)
#print("Filho 1:", filho1)
#print("Filho 2:", filho2)


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


def funcao_objetiva_por_calculo(solucao):
    soma = 0
    for i in range(len(solucao)-1):
        soma += euclidean_distance(solucao[i], solucao[i+1])
    soma += euclidean_distance(solucao[-1], solucao[0])
    return soma