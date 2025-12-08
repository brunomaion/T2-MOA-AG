import csv
from Grafo import Grafo
import random
import matplotlib.pyplot as plt
import numpy as np

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


def criar_grafo_berlin52():
    fname = "arquivos_tsp/berlin52.tsp"
    with open(fname, "r", encoding="utf-8") as f:
        texto = f.read()
    lines = texto.splitlines()
    lines = lines[6:-1]
    vertices=[]
    for line in lines:
        partes = line.split()
        _, x, y = partes
        vertices.append([float(x), float(y)])

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
    for i in range(n):
        matriz_rotulada.append([vertices[i]] + matriz[i])
    berlin52 = Grafo("berlin52", vertices, matriz_rotulada)
    return berlin52

def criar_grafo_berlin52():
    fname = "arquivos_tsp/berlin52.tsp"
    with open(fname, "r", encoding="utf-8") as f:
        texto = f.read()
    lines = texto.splitlines()
    lines = lines[6:-1]
    vertices=[]
    for line in lines:
        partes = line.split()
        _, x, y = partes
        vertices.append([float(x), float(y)])

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
    for i in range(n):
        matriz_rotulada.append([vertices[i]] + matriz[i])
    berlin52 = Grafo("berlin52", vertices, matriz_rotulada)
    return berlin52


def criar_grafo_berlin52():
    fname = "arquivos_tsp/berlin52.tsp"
    with open(fname, "r", encoding="utf-8") as f:
        texto = f.read()
    lines = texto.splitlines()
    lines = lines[6:-1]
    vertices=[]
    for line in lines:
        partes = line.split()
        _, x, y = partes
        vertices.append([float(x), float(y)])

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
    for i in range(n):
        matriz_rotulada.append([vertices[i]] + matriz[i])
    berlin52 = Grafo("berlin52", vertices, matriz_rotulada)
    return berlin52

def criar_grafo_rd400():
    fname = "arquivos_tsp/rd400.tsp"
    with open(fname, "r", encoding="utf-8") as f:
        texto = f.read()
    lines = texto.splitlines()
    lines = lines[6:-1]
    vertices=[]
    for line in lines:
        partes = line.split()
        _, x, y = partes
        vertices.append([float(x), float(y)])

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
    for i in range(n):
        matriz_rotulada.append([vertices[i]] + matriz[i])
    berlin52 = Grafo("rd400", vertices, matriz_rotulada)
    return berlin52

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

  for i in range(tamanho-3):
    for j in range(tamanho-1):
      p1 = solucao[i]
      p2 = solucao[i+1]
      p3 = solucao[j]
      p4 = solucao[j+1]
      cruzamento = cruzamento_delete_cross(p1, p2, p3, p4)
      if cruzamento:
        solucao[i+1:j+1] = reversed(solucao[i+1:j+1])
  return solucao

def operador_1delete_cross(solucao):
  tamanho = len(solucao)
  for i in range(tamanho-3):
    for j in range(tamanho-1):
      p1 = solucao[i]
      p2 = solucao[i+1]
      p3 = solucao[j]
      p4 = solucao[j+1]
      cruzamento = cruzamento_delete_cross(p1, p2, p3, p4)
      if cruzamento:
        solucao[i+1:j+1] = reversed(solucao[i+1:j+1])
        return solucao
  return solucao


def separar_grupos(solucao, n):
    xs = [p[0] for p in solucao]
    ys = [p[1] for p in solucao]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    intervalo_x = (maxx - minx) / n
    intervalo_y = (maxy - miny) / n
    limites = {}
    for iy in range(n):
        for ix in range(n):
            indice = iy * n + ix
            limites[indice] = {
                "minx": minx + ix * intervalo_x,
                "maxx": minx + (ix + 1) * intervalo_x,
                "miny": miny + iy * intervalo_y,
                "maxy": miny + (iy + 1) * intervalo_y
            }
    grupos = {i: [] for i in range(n * n)}
    for p in solucao:
        x, y = p
        for indice, lim in limites.items():
            if lim["minx"] <= x <= lim["maxx"] and lim["miny"] <= y <= lim["maxy"]:
                grupos[indice].append(p)
                break

    salvar_imagem_grupos(grupos, n, filename="grupos2d.png")


    return grupos


def juntar_grupos(grupos):
    nova_solucao = []
    for grupo in grupos:
        for i in grupo:
            nova_solucao.append(i)
    return nova_solucao

def duplicados(lista):
    for i in range(len(lista)):
        for j in range(i + 1, len(lista)):
            if lista[i] == lista[j]:
                return True
    return False

def juntar_populacoes_por_centro(pop_grupos):
    nova_pop = []
    n_clusters = len(pop_grupos)
    tamanho_pop = len(pop_grupos[0])

    for i in range(tamanho_pop):
        clusters_individuo = [pop_grupos[c][i][0] for c in range(n_clusters)]
        individuo_junto = juntar_grupos_por_centro(clusters_individuo)
        fitness = funcao_objetiva_por_calculo(individuo_junto)
        nova_pop.append([individuo_junto, fitness])

    return nova_pop


def indices_mais_proximos(grupo1, grupo2):
    min_dist = float('inf')
    idx1_prox = None
    idx2_prox = None

    for i, p1 in enumerate(grupo1):
        for j, p2 in enumerate(grupo2):
            dist = np.linalg.norm(np.array(p1) - np.array(p2))
            if dist < min_dist:
                min_dist = dist
                idx1_prox = i
                idx2_prox = j

    return idx1_prox, idx2_prox, min_dist

def juntar_2vetores_por_centro(grupo1, grupo2):
    idx1_prox, idx2_prox, _ = indices_mais_proximos(grupo1, grupo2)
    novo_grupo = grupo1[:idx1_prox] + grupo2 + grupo1[idx1_prox:] 
    return novo_grupo

def juntar_grupos_por_centro(grupos):
    if len(grupos) == 1:
        return grupos[0]
    else:
        novo_grupo = juntar_2vetores_por_centro(grupos[0], grupos[1])
        return juntar_grupos_por_centro([novo_grupo] + grupos[2:])





def criar_csv():
    with open("resultados.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Grafo",
            "Execução",
            "Algoritmo",
            "Fit Inicial",
            "Fit Final",
            "Tempo Execução (s)",
            "Ganho Relativo (%)"
        ])

def adicionar_info_csv(
    filename,
    grafo,
    execucao,
    algoritmo,
    fit_inicial,
    fit_final,
    tempo_exec,
    ganho_relativo
):
    with open(filename, mode='a', newline='') as file:  # 'a' = append
        writer = csv.writer(file)
        writer.writerow([
            grafo,
            execucao,
            algoritmo,
            fit_inicial,
            fit_final,
            tempo_exec,
            ganho_relativo
        ])




def salvar_imagem_grupos(grupos, n, filename="grupos2d.png"):
    plt.figure(figsize=(8, 8))
    cores = plt.cm.get_cmap("tab20", n*n)

    for idx, pontos in grupos.items():
        if len(pontos) == 0:
            continue
        xs = [p[0] for p in pontos]
        ys = [p[1] for p in pontos]
        plt.scatter(xs, ys, color=cores(idx), s=25, label=f"Grupo {idx}")

    plt.title(f"Divisão em {n}x{n} grupos")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis("equal")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()