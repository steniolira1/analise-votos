# META 3 - CÁLCULO DAS MÉDIAS

# IMPORTES:

import os
import time
import unicodedata

from leitura import ler_dados
from filtro import filtrar_dados

# CONFIGURAÇÕES

# Município analisado. Pode escrever com ou sem acento ("BORÁ" ou "Bora").
MUNICIPIO_ESCOLHIDO = "BORÁ"

# FUNÇÕES AUXILIARES

def normalizar(texto):
    """Deixa o texto em maiúsculas e sem acentos, para comparar nomes."""
    sem_acento = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join(c for c in sem_acento if not unicodedata.combining(c))
    return sem_acento.upper().strip()


def separar_municipio(df, municipio):
    """
    Divide os dados em duas partes:
    - linhas do município escolhido
    - linhas de todos os demais municípios
    """
    nomes = df["MUNICIPIO"].map(normalizar)
    alvo = normalizar(municipio)

    do_municipio = df[nomes == alvo]
    demais = df[nomes != alvo]

    if do_municipio.empty:
        raise ValueError(f"Município '{municipio}' não encontrado nos dados.")

    return do_municipio, demais


# FUNÇÕES DE CÁLCULO
# Cada função recebe um DataFrame e devolve um resultado.
# Elas não dependem umas das outras: isso permite rodar cada uma
# numa thread ou num processo separado nas próximas metas.

def media_do_municipio(df_municipio):
    """Média de votos por registro no município escolhido."""
    return df_municipio["VOTOS"].mean()


def media_dos_demais(df_demais):
    """Média de votos por registro em todos os outros municípios."""
    return df_demais["VOTOS"].mean()


def medias_por_partido(df_municipio):
    """Média de votos de cada partido no município (maior para menor)."""
    return df_municipio.groupby("PARTIDO")["VOTOS"].mean().sort_values(ascending=False)


def medias_por_cargo(df_municipio):
    """Média de votos de cada cargo no município (maior para menor)."""
    return df_municipio.groupby("CARGO")["VOTOS"].mean().sort_values(ascending=False)


# # TESTE
# if __name__ == "__main__":
#     print(f"Processo principal iniciado, PID = {os.getpid()}")

#     dados, _ = filtrar_dados(ler_dados())
#     df_municipio, df_demais = separar_municipio(dados, MUNICIPIO_ESCOLHIDO)

#     inicio = time.perf_counter()
#     media_mun = media_do_municipio(df_municipio)
#     media_dem = media_dos_demais(df_demais)
#     por_partido = medias_por_partido(df_municipio)
#     por_cargo = medias_por_cargo(df_municipio)
#     fim = time.perf_counter()

#     nome = df_municipio["MUNICIPIO"].iloc[0]
#     print(f"\nMunicípio analisado: {nome}")
#     print(f"Registros do município: {len(df_municipio)}")
#     print(f"Registros dos demais:   {len(df_demais)}")

#     print(f"\nMédia de votos em {nome}:      {media_mun:.2f}")
#     print(f"Média de votos nos demais:   {media_dem:.2f}")

#     if media_mun > media_dem:
#         print(f"-> {nome} está ACIMA da média dos demais municípios.")
#     else:
#         print(f"-> {nome} está ABAIXO da média dos demais municípios.")

#     print(f"\nMédia por partido em {nome}:")
#     print(por_partido.round(2).to_string())

#     print(f"\nMédia por cargo em {nome}:")
#     print(por_cargo.round(2).to_string())

#     print(f"\nTempo dos cálculos: {fim - inicio:.3f} segundos")
#     print(f"Processo principal finalizado, PID = {os.getpid()}")