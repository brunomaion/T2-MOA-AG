class Resultados:
    def __init__(self, execucoes=None):
        self.execucoes = execucoes if execucoes else []
    def adicionar_execucao(self, execucao):
        self.execucoes.append(execucao)

    def salvar_csv(self, nome_arquivo):
        import csv
        with open(nome_arquivo, mode='w', newline='') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(['Problema', 'Algoritmo', 'Tempo de Execução', 'Melhor Solução'])
            for execucao in self.execucoes:
                escritor.writerow([
                    execucao.problema,
                    execucao.algoritmo,
                    execucao.tempo_execucao,
                    execucao.melhor_solucao
                ])