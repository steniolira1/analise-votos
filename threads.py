# META 5 - VERSÃO COM THREADS

# IMPORTES:

import os
import threading
import time

from leitura import ler_dados
from filtro import filtrar_dados
from medias import (
    MUNICIPIO_ESCOLHIDO,
    separar_municipio,
    media_do_municipio,
    media_dos_demais,
    medias_por_partido,
    medias_por_cargo,
)
from resultados import maior_media, mostrar_vencedor

# FUNÇÕES

def trabalhador(nome_tarefa, funcao, df, resultados, trava):
    """
    Código que cada thread executa.
    Todas as threads rodam DENTRO do mesmo processo (mesmo PID) e
    compartilham a memória: por isso podem gravar no mesmo dicionário
    "resultados". A trava (Lock) garante que só uma grava por vez.
    """
    print(f"[THREAD {nome_tarefa}] PID = {os.getpid()}, thread = {threading.get_ident()}")
    resultado = funcao(df)

    with trava:
        resultados[nome_tarefa] = resultado


def executar_com_threads(df_municipio, df_demais):
    """
    Cria 1 thread para cada uma das 4 tarefas da meta 3,
    espera todas terminarem e devolve (resultados, tempo).
    """
    tarefas = [
        ("media_municipio", media_do_municipio, df_municipio),
        ("media_demais", media_dos_demais, df_demais),
        ("por_partido", medias_por_partido, df_municipio),
        ("por_cargo", medias_por_cargo, df_municipio),
    ]

    resultados = {}
    trava = threading.Lock()
    threads = []

    inicio = time.perf_counter()

    for nome, funcao, df in tarefas:
        t = threading.Thread(target=trabalhador, args=(nome, funcao, df, resultados, trava))
        t.start()
        threads.append(t)

    # join(): a thread principal espera cada thread terminar
    for t in threads:
        t.join()

    fim = time.perf_counter()
    return resultados, fim - inicio


# # TESTE
# if __name__ == "__main__":
#     inicio_total = time.perf_counter()
#     print(f"Processo principal iniciado, PID = {os.getpid()}")

#     dados, _ = filtrar_dados(ler_dados())
#     df_municipio, df_demais = separar_municipio(dados, MUNICIPIO_ESCOLHIDO)

#     print("\nIniciando as threads...")
#     resultados, tempo_threads = executar_com_threads(df_municipio, df_demais)

#     fim_total = time.perf_counter()

#     # Exibição (fora da medição das threads)
#     nome = df_municipio["MUNICIPIO"].iloc[0]
#     print(f"\n===== RESULTADOS DE {nome} (THREADS) =====")
#     print(f"Média de votos em {nome}:    {resultados['media_municipio']:.2f}")
#     print(f"Média de votos nos demais: {resultados['media_demais']:.2f}")

#     partido, media_p, qtd_p = maior_media(resultados["por_partido"], df_municipio, "PARTIDO")
#     cargo, media_c, qtd_c = maior_media(resultados["por_cargo"], df_municipio, "CARGO")
#     mostrar_vencedor("PARTIDO COM A MAIOR MÉDIA DE VOTOS:", partido, media_p, qtd_p)
#     mostrar_vencedor("CARGO COM A MAIOR MÉDIA DE VOTOS:", cargo, media_c, qtd_c)

#     print("\n===== TEMPOS (THREADS) =====")
#     print(f"Tempo das 4 threads:              {tempo_threads:.4f} segundos")
#     print(f"Tempo total (leitura até o fim):  {fim_total - inicio_total:.4f} segundos")

#     print(f"\nProcesso principal finalizado, PID = {os.getpid()}")