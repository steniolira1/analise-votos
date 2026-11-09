# CONFERÊNCIA - comparar os dados de um município com a notícia
# Lê o CSV (sem alterar nada) e mostra o TOTAL de votos por cargo
# e por candidato, separado por turno.

import os
import pandas as pd

from leitura import CAMINHO_ARQUIVO
from medias import MUNICIPIO_ESCOLHIDO, normalizar

COLUNAS_CONFERENCIA = [
    "NR_TURNO",
    "NM_MUNICIPIO",
    "DS_CARGO",
    "NM_URNA_CANDIDATO",
    "SG_PARTIDO",
    "QT_VOTOS_NOMINAIS",
]

if __name__ == "__main__":
    df = pd.read_csv(
        CAMINHO_ARQUIVO,
        sep=";",
        encoding="latin-1",
        usecols=COLUNAS_CONFERENCIA,
    )

    alvo = normalizar(MUNICIPIO_ESCOLHIDO)
    mun = df[df["NM_MUNICIPIO"].map(normalizar) == alvo]

    print(f"Município: {MUNICIPIO_ESCOLHIDO}")
    print(f"Linhas do município (sem filtro): {len(mun)}")
    print(f"Turnos presentes no arquivo: {sorted(int(t) for t in mun['NR_TURNO'].unique())}")

    for turno, dados_turno in mun.groupby("NR_TURNO"):
        print(f"\n================ {turno}º TURNO ================")

        totais = dados_turno.groupby("DS_CARGO")["QT_VOTOS_NOMINAIS"].sum()
        print("\nTotal de votos nominais por cargo:")
        print(totais.to_string())

        for cargo, dados_cargo in dados_turno.groupby("DS_CARGO"):
            top = (
                dados_cargo.groupby(["NM_URNA_CANDIDATO", "SG_PARTIDO"])["QT_VOTOS_NOMINAIS"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
            )
            print(f"\n{cargo} - 5 mais votados:")
            print(top.to_string())