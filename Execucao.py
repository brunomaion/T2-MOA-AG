
class Execucao:
    def __init__(self, problema=None, algoritmo=None, tempo_execucao=0, melhor_solucao=None):
        self.problema = problema
        self.algoritmo = algoritmo
        self.tempo_execucao = tempo_execucao
        self.melhor_solucao = melhor_solucao