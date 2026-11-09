# META 6 - VERSÃO COM PROCESSOS
 
# IMPORTES:
 
import os
import multiprocessing
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
 
def trabalhador(nome_tarefa, funcao, df, fila_de_saida):
    """
    Código que cada processo filho executa.
    Cada filho tem o SEU PRÓPRIO PID e a SUA PRÓPRIA memória:
    ele recebe uma CÓPIA dos dados e não enxerga as variáveis do pai.
    Por isso o resultado volta para o pai pela fila (Queue).
    """
    print(f"[PROCESSO {nome_tarefa}] PID = {os.getpid()}, pai = {os.getppid()}")
    resultado = funcao(df)
    fila_de_saida.put((nome_tarefa, resultado))
 
 
def executar_com_processos(df_municipio, df_demais):
    """
    Cria 1 processo filho para cada uma das 4 tarefas da meta 3,
    recebe os resultados pela fila e devolve (resultados, tempo).
    """
    tarefas = [
        ("media_municipio", media_do_municipio, df_municipio),
        ("media_demais", media_dos_demais, df_demais),
        ("por_partido", medias_por_partido, df_municipio),
        ("por_cargo", medias_por_cargo, df_municipio),
    ]
 
    fila = multiprocessing.Queue()
    processos = []
 
    inicio = time.perf_counter()
 
    for nome, funcao, df in tarefas:
        p = multiprocessing.Process(target=trabalhador, args=(nome, funcao, df, fila))
        p.start()
        processos.append(p)
 
    # Primeiro recebe os 4 resultados da fila, depois faz o join().
    # Mesma ordem do código do professor (fila.get() antes do join()):
    # se o pai esperasse no join() antes de ler a fila, um filho com
    # resultado grande poderia ficar travado tentando entregá-lo.
    resultados = {}
    for _ in tarefas:
        nome, resultado = fila.get()
        resultados[nome] = resultado
 
    for p in processos:
        p.join()
 
    fim = time.perf_counter()
    return resultados, fim - inicio
 
 
# # TESTE
# # O bloco abaixo é OBRIGATÓRIO no Windows: sem ele, cada processo filho
# # executaria o programa inteiro de novo ao iniciar.
# if __name__ == "__main__":
#     inicio_total = time.perf_counter()
#     print(f"Processo principal iniciado, PID = {os.getpid()}")
 
#     dados, _ = filtrar_dados(ler_dados())
#     df_municipio, df_demais = separar_municipio(dados, MUNICIPIO_ESCOLHIDO)
 
#     print("\nIniciando os processos...")
#     resultados, tempo_processos = executar_com_processos(df_municipio, df_demais)
 
#     fim_total = time.perf_counter()
 
#     # Exibição (fora da medição dos processos)
#     nome = df_municipio["MUNICIPIO"].iloc[0]
#     print(f"\n===== RESULTADOS DE {nome} (PROCESSOS) =====")
#     print(f"Média de votos em {nome}:    {resultados['media_municipio']:.2f}")
#     print(f"Média de votos nos demais: {resultados['media_demais']:.2f}")
 
#     partido, media_p, qtd_p = maior_media(resultados["por_partido"], df_municipio, "PARTIDO")
#     cargo, media_c, qtd_c = maior_media(resultados["por_cargo"], df_municipio, "CARGO")
#     mostrar_vencedor("PARTIDO COM A MAIOR MÉDIA DE VOTOS:", partido, media_p, qtd_p)
#     mostrar_vencedor("CARGO COM A MAIOR MÉDIA DE VOTOS:", cargo, media_c, qtd_c)
 
#     print("\n===== TEMPOS (PROCESSOS) =====")
#     print(f"Tempo dos 4 processos:            {tempo_processos:.4f} segundos")
#     print(f"Tempo total (leitura até o fim):  {fim_total - inicio_total:.4f} segundos")
 
#     print(f"\nProcesso principal finalizado, PID = {os.getpid()}")
 
