"""
META 1 - Leitura da base de dados do TSE

Este módulo só LÊ o arquivo CSV. O arquivo original nunca é alterado:
o pandas abre o arquivo em modo leitura e carrega os dados na memória.

As outras partes do projeto (filtro, médias, threads, processos) vão
importar a função ler_dados() daqui.
"""

import os
import time

import pandas as pd

# ---------------------------------------------------------------
# CONFIGURAÇÕES
# ---------------------------------------------------------------

# Caminho do CSV do TSE. Coloque o arquivo dentro da pasta "dados".
CAMINHO_ARQUIVO = os.path.join("dados", "votacao_candidato_munzona_2026_SP.csv")

# Colunas que o projeto usa.
# Chave = nome que vamos usar no código | Valor = nome da coluna no CSV do TSE
COLUNAS = {
    "MUNICIPIO": "NM_MUNICIPIO",
    "PARTIDO": "SG_PARTIDO",
    "CARGO": "DS_CARGO",
    "VOTOS": "QT_VOTOS_NOMINAIS",
}


# ---------------------------------------------------------------
# FUNÇÕES
# ---------------------------------------------------------------

def mostrar_colunas_do_arquivo(caminho):
    """Mostra as colunas que existem no CSV (lê só o cabeçalho)."""
    cabecalho = pd.read_csv(caminho, sep=";", encoding="latin-1", nrows=0)
    print("Colunas encontradas no arquivo:")
    for nome in cabecalho.columns:
        print(f"  - {nome}")


def ler_dados(caminho=CAMINHO_ARQUIVO):
    """
    Lê o CSV do TSE e devolve um DataFrame só com as colunas do projeto.

    - sep=";"           -> o TSE separa as colunas com ponto e vírgula
    - encoding="latin-1" -> o TSE usa essa codificação (acentos)
    - usecols           -> carrega só as colunas necessárias (mais rápido)
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}\n"
            "Coloque o CSV do TSE na pasta 'dados' ou ajuste CAMINHO_ARQUIVO."
        )

    try:
        df = pd.read_csv(
            caminho,
            sep=";",
            encoding="latin-1",
            usecols=list(COLUNAS.values()),
        )
    except ValueError:
        # Acontece quando algum nome em COLUNAS não existe no arquivo
        print("Erro: alguma coluna de COLUNAS não existe neste arquivo.")
        mostrar_colunas_do_arquivo(caminho)
        raise

    # Troca os nomes do TSE pelos nomes curtos usados no projeto
    df = df.rename(columns={tse: nosso for nosso, tse in COLUNAS.items()})
    return df


# # ---------------------------------------------------------------
# # TESTE DA META 1 (roda só quando executamos este arquivo direto)
# # ---------------------------------------------------------------

# if __name__ == "__main__":
#     print(f"Processo principal iniciado, PID = {os.getpid()}")

#     inicio = time.perf_counter()
#     dados = ler_dados()
#     fim = time.perf_counter()

#     print(f"\nLinhas lidas: {len(dados)}")
#     print(f"Colunas: {list(dados.columns)}")
#     print("\nPrimeiras 5 linhas:")
#     print(dados.head())
#     print(f"\nTempo de leitura: {fim - inicio:.3f} segundos")

#     print(f"\nProcesso principal finalizado, PID = {os.getpid()}")