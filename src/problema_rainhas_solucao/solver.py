from time import time
from heapq import heapify


def eh_seguro(colunas_ocupadas, diag1_ocupadas, diag2_ocupadas, linha, coluna, n):
    if colunas_ocupadas[coluna]:
        return False
    if diag1_ocupadas[linha - coluna + n - 1]:
        return False
    if diag2_ocupadas[linha + coluna]:
        return False
    return True


def resolver_rainhas_com_bloqueios(tabuleiro):
    n = len(tabuleiro)
    solucao = []
    tempo_inicio = time()
    contador_nos = 0

    colunas_ocupadas = [False] * n
    diag1_ocupadas = [False] * (2 * n - 1)
    diag2_ocupadas = [False] * (2 * n - 1)

    opcoes_por_coluna = [0] * n
    for linha in range(n):
        for coluna in range(n):
            if tabuleiro[linha][coluna] == ".":
                opcoes_por_coluna[coluna] += 1

    colunas_disponiveis = [(o, c) for c, o in enumerate(opcoes_por_coluna)]
    heapify(colunas_disponiveis)

    colunas_disponiveis_count = sum(1 for _, c in colunas_disponiveis)

    def colunas_suficientes(linha):
        return colunas_disponiveis_count >= n - linha

    def dfs(linha):
        nonlocal contador_nos
        if linha == n:
            return True
        if not colunas_suficientes(linha):
            return False

        for _, coluna in colunas_disponiveis:
            contador_nos += 1
            if tabuleiro[linha][coluna] == "." and eh_seguro(
                colunas_ocupadas, diag1_ocupadas, diag2_ocupadas, linha, coluna, n
            ):
                colunas_ocupadas[coluna] = True
                diag1_ocupadas[linha - coluna + n - 1] = True
                diag2_ocupadas[linha + coluna] = True
                solucao.append((linha, coluna))

                temp_colunas = [(o, c) for o, c in colunas_disponiveis if c != coluna]
                heapify(temp_colunas)
                colunas_disponiveis[:] = temp_colunas

                if dfs(linha + 1):
                    return True

                solucao.pop()
                colunas_ocupadas[coluna] = False
                diag1_ocupadas[linha - coluna + n - 1] = False
                diag2_ocupadas[linha + coluna] = False
                colunas_disponiveis[:] = [
                    (opcoes_por_coluna[c], c)
                    for c in range(n)
                    if not colunas_ocupadas[c]
                ]
                heapify(colunas_disponiveis)

        return False

    if not pre_processar_tabuleiro(tabuleiro):
        return ([], time() - tempo_inicio, contador_nos)

    sucesso = dfs(0)
    tempo_gasto = time() - tempo_inicio
    return (
        (solucao, tempo_gasto, contador_nos)
        if sucesso
        else ([], tempo_gasto, contador_nos)
    )


def pre_processar_tabuleiro(tabuleiro):
    n = len(tabuleiro)
    linhas_validas = [False] * n
    colunas_validas = [False] * n
    for i in range(n):
        for j in range(n):
            if tabuleiro[i][j] == ".":
                linhas_validas[i] = True
                colunas_validas[j] = True
    return sum(linhas_validas) >= n and sum(colunas_validas) >= n
