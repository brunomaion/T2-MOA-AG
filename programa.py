import tkinter as tk
from tkinter import ttk, messagebox
import functions as fn
import algoritmos as alg
import time

SOLUCAO_INICIAL = None
SOLUCAO_FINAL = None
GRAFO_ATUAL = None

try:
    print("Carregando bases de dados...")
    GRAFOS = {
        "berlin52": fn.criar_grafo_berlin52(),
        "ch150": fn.criar_grafo_ch150(),
        "rd400": fn.criar_grafo_rd400(),
    }
    print("Bases de dados carregadas.")
except Exception as e:
    messagebox.showerror("Erro de Carregamento", f"Falha ao carregar os grafos: {e}")
    GRAFOS = {}

ALGORITMOS = {
    "AG Original": alg.algoritmo_genetico,
    "AG 1DeleteCross": alg.ag_1deletecross,
    "AG 1DC-Solucao-Cluster2x2": alg.ag_1deletecross_cluster_solucao,
    "AG 1DC-AG-Cluster2x2": alg.ag_1deletecross_cluster_ag,
}

def desenhar_solucao(solucao, nome_solucao):
    if solucao is not None:
        viewport.delete("all")
        fn.desenhar(solucao, canvas=viewport, max_view_x=500, max_view_y=500)
        label_status.config(text=f"Visualizando: {nome_solucao}", fg="blue")
    else:
        label_status.config(text=f"Erro: {nome_solucao} não está disponível. Execute o AG primeiro.", fg="orange")

def mostrar_inicial():
    desenhar_solucao(SOLUCAO_INICIAL, "Solução Inicial")

def mostrar_final():
    desenhar_solucao(SOLUCAO_FINAL, "Solução Final Encontrada")

def executar_algoritmo():
    global SOLUCAO_INICIAL, SOLUCAO_FINAL, GRAFO_ATUAL
    
    nome_grafo = var_grafo.get()
    nome_algoritmo = var_algoritmo.get()
    
    if not nome_grafo or nome_grafo not in GRAFOS:
        messagebox.showerror("Erro", "Selecione uma base de dados válida.")
        return

    GRAFO_ATUAL = GRAFOS[nome_grafo]

    try:
        n_geracoes = int(entry_geracoes.get())
        tam_pop = int(entry_populacao.get())
        elit_pct = float(entry_elitismo.get())
        n_cluster = int(entry_cluster.get())
    except ValueError:
        messagebox.showerror("Erro", "Parâmetros devem ser números inteiros/decimais válidos.")
        return
    
    algoritmo_func = ALGORITMOS[nome_algoritmo]
    
    try:
        
        viewport.delete("all")
        SOLUCAO_INICIAL = None
        SOLUCAO_FINAL = None
        label_status.config(text=f"Executando {nome_algoritmo} em {nome_grafo}...", fg="blue")
        janela.update_idletasks()

        start_time = time.time()
        
        
        SOLUCAO_INICIAL = GRAFO_ATUAL.vertices 

        
        if nome_algoritmo == "AG 1DeleteCross":
            
            pop_inicial_real = alg.gerar_populacao_inicial(GRAFO_ATUAL.vertices, tam_pop)
            resultados = algoritmo_func(pop_inicial_real, n_geracoes, tam_pop, elit_pct)
            
        elif "Cluster" in nome_algoritmo:
            
            resultados = algoritmo_func(
                GRAFO_ATUAL.vertices, n_geracoes, tam_pop, elit_pct, n_cluster=n_cluster
            )
        
        else: 
            resultados = algoritmo_func(GRAFO_ATUAL.vertices, n_geracoes, tam_pop, elit_pct)

        
        end_time = time.time()
        tempo_execucao = end_time - start_time
        
        
        
        
        melhor_custo = resultados[2]
        SOLUCAO_FINAL = resultados[1] 
        ganho_relativo = resultados[4]
        
        
        mostrar_final()
        btn_inicial.config(state=tk.NORMAL)
        btn_final.config(state=tk.NORMAL)

        label_status.config(
            text=f"Concluído! Custo Final: {melhor_custo:.2f} | Tempo Total: {tempo_execucao:.2f}s | Ganho Relativo: {ganho_relativo:.2f}%", 
            fg="green"
        )
        
    except Exception as e:
        label_status.config(text=f"ERRO: {e}", fg="red") 
        print(f"Erro na execução do algoritmo: {e}")
        messagebox.showerror("Erro de Execução", f"Ocorreu um erro: {e}")

janela = tk.Tk()
janela.title("AG Optimizer - Interface Gráfica")

style = ttk.Style()
style.configure("TFrame", padding=10, relief="groove")

frame_controle = ttk.Frame(janela)
frame_controle.pack(side="left", fill="y", padx=10, pady=10)

ttk.Label(frame_controle, text="Base de Dados (Grafo)", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
var_grafo = tk.StringVar(value="berlin52")
for nome in GRAFOS.keys():
    ttk.Radiobutton(frame_controle, text=nome, variable=var_grafo, value=nome).pack(anchor="w")

ttk.Separator(frame_controle, orient="horizontal").pack(fill="x", pady=10)

ttk.Label(frame_controle, text="Algoritmo", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
var_algoritmo = tk.StringVar(value="AG Original")
for nome in ALGORITMOS.keys():
    ttk.Radiobutton(frame_controle, text=nome, variable=var_algoritmo, value=nome).pack(anchor="w")

ttk.Separator(frame_controle, orient="horizontal").pack(fill="x", pady=10)

frame_parametros = ttk.Frame(frame_controle)
frame_parametros.pack(fill="x")

ttk.Label(frame_parametros, text="Parâmetros", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, sticky="w", pady=(0, 5))

ttk.Label(frame_parametros, text="N. Gerações:").grid(row=1, column=0, sticky="w")
entry_geracoes = ttk.Entry(frame_parametros, width=10)
entry_geracoes.insert(0, "500")
entry_geracoes.grid(row=1, column=1, sticky="w")

ttk.Label(frame_parametros, text="Tam. População:").grid(row=2, column=0, sticky="w")
entry_populacao = ttk.Entry(frame_parametros, width=10)
entry_populacao.insert(0, "100")
entry_populacao.grid(row=2, column=1, sticky="w")

ttk.Label(frame_parametros, text="Elitismo (%):").grid(row=3, column=0, sticky="w")
entry_elitismo = ttk.Entry(frame_parametros, width=10)
entry_elitismo.insert(0, "0.05")
entry_elitismo.grid(row=3, column=1, sticky="w")

ttk.Label(frame_parametros, text="N. Clusters:").grid(row=4, column=0, sticky="w")
entry_cluster = ttk.Entry(frame_parametros, width=10)
entry_cluster.insert(0, "2")
entry_cluster.grid(row=4, column=1, sticky="w")

ttk.Button(frame_controle, text="INICIAR EXECUÇÃO", command=executar_algoritmo).pack(fill="x", pady=20)

frame_visualizacao = ttk.Frame(janela)
frame_visualizacao.pack(side="right", fill="both", expand=True, padx=10, pady=10)

ttk.Label(frame_visualizacao, text="Visualização do Caminho", font=("Arial", 12, "bold")).pack(pady=(0, 5))

viewport = tk.Canvas(frame_visualizacao, width=500, height=500, bg="lightgray", highlightthickness=1, highlightbackground="black")
viewport.pack(padx=10, pady=10)

frame_botoes_viz = ttk.Frame(frame_visualizacao)
frame_botoes_viz.pack(pady=10)

btn_inicial = ttk.Button(frame_botoes_viz, text="Mostrar Solução Inicial", command=mostrar_inicial, state=tk.DISABLED)
btn_inicial.pack(side=tk.LEFT, padx=5)

btn_final = ttk.Button(frame_botoes_viz, text="Mostrar Solução Final", command=mostrar_final, state=tk.DISABLED)
btn_final.pack(side=tk.LEFT, padx=5)

label_status = tk.Label(frame_visualizacao, text="Pronto para iniciar.", font=("Arial", 10), fg="black")
label_status.pack(pady=10)

janela.mainloop()