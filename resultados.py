# META 4 - PARTIDO E CARGO COM A MAIOR MÉDIA DE VOTOS

# IMPORTES:

import os

from leitura import ler_dados
from filtro import filtrar_dados
from medias import (
    MUNICIPIO_ESCOLHIDO,
    separar_municipio,
    medias_por_partido,
    medias_por_cargo,
)

# FUNÇÕES

def maior_media(medias, df_municipio, coluna):
    """
    Recebe as médias já calculadas (meta 3) e devolve o vencedor:
    - nome   -> partido ou cargo com a maior média
    - media  -> valor da maior média
    - qtd    -> quantos registros sustentam essa média
    """
    nome = medias.idxmax()
    media = medias.max()
    qtd = int((df_municipio[coluna] == nome).sum())
    return nome, media, qtd


def mostrar_vencedor(titulo, nome, media, qtd):
    """Mostra o vencedor de forma destacada."""
    print(f"\n{titulo}")
    print(f"  {nome}")
    print(f"  Média de votos: {media:.2f}")
    print(f"  Registros:      {qtd}")


# # TESTE
# if __name__ == "__main__":
#     print(f"Processo principal iniciado, PID = {os.getpid()}")

#     dados, _ = filtrar_dados(ler_dados())
#     df_municipio, _ = separar_municipio(dados, MUNICIPIO_ESCOLHIDO)
#     municipio = df_municipio["MUNICIPIO"].iloc[0]

#     por_partido = medias_por_partido(df_municipio)
#     por_cargo = medias_por_cargo(df_municipio)

#     partido, media_p, qtd_p = maior_media(por_partido, df_municipio, "PARTIDO")
#     cargo, media_c, qtd_c = maior_media(por_cargo, df_municipio, "CARGO")

#     print(f"\n===== RESULTADOS DE {municipio} =====")
#     mostrar_vencedor("PARTIDO COM A MAIOR MÉDIA DE VOTOS:", partido, media_p, qtd_p)
#     mostrar_vencedor("CARGO COM A MAIOR MÉDIA DE VOTOS:", cargo, media_c, qtd_c)

#     print(f"\nProcesso principal finalizado, PID = {os.getpid()}")