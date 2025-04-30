from board import gerar_tabuleiro_com_bloqueios_melhorado, imprimir_tabuleiro
from solver import resolver_rainhas_com_bloqueios
import random
import json
import numpy as np
import matplotlib.pyplot as plt


def percentual_aleatorio(seed=None, min_perc=0.07, max_perc=0.13):
    rng = random.Random(seed)
    return rng.uniform(min_perc, max_perc)


def testar_tamanho(n, seed=None, resultados=[]):
    print(f"\nTestando tabuleiro {n}x{n} com bloqueios aleatórios")

    perc = percentual_aleatorio(seed)
    total_casas = n * n
    num_bloqueios = int(perc * total_casas)

    # Gerar tabuleiro com bloqueios usando numpy
    tabuleiro, bloqueios = gerar_tabuleiro_com_bloqueios_melhorado(
        n, num_bloqueios=num_bloqueios, seed=seed
    )
    tabuleiro = np.array(tabuleiro)  # Converter para numpy array

    print(f"Percentual de bloqueios: {perc*100:.2f}% ({num_bloqueios} casas)")
    if n <= 32:
        imprimir_tabuleiro(tabuleiro.tolist())  # Converter de volta para lista para impressão

    solucao, tempo, nos = resolver_rainhas_com_bloqueios(tabuleiro.tolist())

    resultado = {
        "tamanho_tabuleiro": n,
        "seed": seed,
        "percentual_bloqueios": perc,
        "num_bloqueios": num_bloqueios,
        "solucao_encontrada": bool(solucao),
        "tempo_processamento": tempo,
        "nos_visitados": nos,
    }
    resultados.append(resultado)

    if solucao:
        print(f"Solução encontrada em {tempo:.4f} segundos, nós visitados: {nos}")
        if n <= 32:
            tab_sol = tabuleiro.copy()
            for l, c in solucao:
                tab_sol[l, c] = "Q"
            imprimir_tabuleiro(tab_sol.tolist())
    else:
        print(f"Sem solução após {tempo:.4f} segundos, nós visitados: {nos}")


def salvar_resultados_json(resultados, arquivo="resultados.json"):
    with open(arquivo, "w") as f:
        json.dump(resultados, f, indent=4)
    print(f"\nResultados salvos em {arquivo}")


def plotar_grafico(resultados):
    tamanhos = [r["tamanho_tabuleiro"] for r in resultados]
    tempos = [r["tempo_processamento"] for r in resultados]
    nos_visitados = [r["nos_visitados"] for r in resultados]

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(tamanhos, tempos, marker="o", label="Tempo de Processamento (s)")
    plt.xlabel("Tamanho do Tabuleiro")
    plt.ylabel("Tempo (s)")
    plt.title("Desempenho do Algoritmo - Tempo de Processamento")
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(tamanhos, nos_visitados, marker="o", color="orange", label="Nós Visitados")
    plt.xlabel("Tamanho do Tabuleiro")
    plt.ylabel("Nós Visitados")
    plt.title("Desempenho do Algoritmo - Nós Visitados")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    seeds = [42, 123, 999, 2025]
    tamanhos = [8, 16, 32, 128]
    resultados = []

    for n, seed in zip(tamanhos, seeds):
        testar_tamanho(n, seed, resultados)

    salvar_resultados_json(resultados)
    plotar_grafico(resultados)
