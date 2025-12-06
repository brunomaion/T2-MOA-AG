import csv

class Grafo:
    def __init__(self, nome="", vertices=None, matriz_adj=[]):
        # store name as string (remove accidental trailing comma which made it a tuple)
        self.nome = nome
        self.vertices = vertices if vertices else []  
        self.matriz_adj = matriz_adj
        self.solucao = []         

    def adicionar_vertice(self, ponto):
        self.vertices.append(ponto)


    def set_solucao(self, solucao):
        self.solucao = solucao

    def salvar_matriz_csv(self, nome_arquivo):
        with open(nome_arquivo, mode='w', newline='') as file:
            writer = csv.writer(file)
            for linha in self.matriz_adj:
                writer.writerow(linha)