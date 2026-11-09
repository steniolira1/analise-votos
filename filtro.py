# META 2 - FILTRO DOS DADOS

# IMPORTES:

import os
import time
import pandas as pd

from leitura import ler_dados

# CONFIGURAÇÕES

# Linhas com 0 votos puxam as médias para baixo.
# True = remove essas linhas | False = mantém
REMOVER_VOTOS_ZERO = True

# FUNÇÕES

def filtrar_dados(df):
    """
    Recebe o DataFrame da leitura e devolve um NOVO DataFrame filtrado.
    O DataFrame original não é alterado (trabalhamos numa cópia).

    Etapas:
    1. Remove linhas com campos vazios
    2. Garante que VOTOS é número (o TSE às vezes usa códigos como #NULO#)
    3. Remove votos negativos (o TSE usa -1 para "sem informação")
    4. Remove votos zerados (se REMOVER_VOTOS_ZERO = True)
    5. Tira espaços extras dos textos
    """
    dados = df.copy()
    relatorio = {"linhas_antes": len(dados)}

    # 1. Campos vazios
    antes = len(dados)
    dados = dados.dropna()
    relatorio["vazias"] = antes - len(dados)

    # 2. VOTOS como número (o que não for número vira vazio e sai)
    antes = len(dados)
    dados["VOTOS"] = pd.to_numeric(dados["VOTOS"], errors="coerce")
    dados = dados.dropna(subset=["VOTOS"])
    dados["VOTOS"] = dados["VOTOS"].astype(int)
    relatorio["nao_numericas"] = antes - len(dados)

    # 3. Votos negativos
    antes = len(dados)
    dados = dados[dados["VOTOS"] >= 0]
    relatorio["negativas"] = antes - len(dados)

    # 4. Votos zerados
    antes = len(dados)
    if REMOVER_VOTOS_ZERO:
        dados = dados[dados["VOTOS"] > 0]
    relatorio["zeradas"] = antes - len(dados)

    # 5. Espaços extras nos textos
    for coluna in ["MUNICIPIO", "PARTIDO", "CARGO"]:
        dados[coluna] = dados[coluna].astype(str).str.strip()

    relatorio["linhas_depois"] = len(dados)
    return dados.reset_index(drop=True), relatorio


def mostrar_relatorio(relatorio):
    """Mostra quantas linhas cada etapa do filtro removeu."""
    linhas = [
        ("Linhas antes do filtro", relatorio["linhas_antes"]),
        ("Removidas (vazias)", relatorio["vazias"]),
        ("Removidas (não numéricas)", relatorio["nao_numericas"]),
        ("Removidas (negativas)", relatorio["negativas"]),
        ("Removidas (zeradas)", relatorio["zeradas"]),
        ("Linhas depois do filtro", relatorio["linhas_depois"]),
    ]
    print("Relatório do filtro:")
    for nome, valor in linhas:
        print(f" - {nome:<28} {valor:>10}")


# # TESTE
# if __name__ == "__main__":
#     print(f"Processo principal iniciado, PID = {os.getpid()}")

#     dados = ler_dados()

#     inicio = time.perf_counter()
#     dados_filtrados, relatorio = filtrar_dados(dados)
#     fim = time.perf_counter()

#     print()
#     mostrar_relatorio(relatorio)
#     print("\nPrimeiras 5 linhas filtradas:")
#     print(dados_filtrados.head())
#     print(f"\nTempo do filtro: {fim - inicio:.3f} segundos")

#     print(f"\nProcesso principal finalizado, PID = {os.getpid()}")