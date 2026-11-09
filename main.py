# META 7 - COMPARAÇÃO FINAL: THREADS VS PROCESSOS
 
# IMPORTES:
 
import os
import statistics
import time
 
from leitura import ler_dados
from filtro import filtrar_dados
from medias import MUNICIPIO_ESCOLHIDO, separar_municipio
from resultados import maior_media, mostrar_vencedor
from threads import executar_com_threads
from processos import executar_com_processos
 
# CONFIGURAÇÕES
 
# Quantas vezes cada versão é executada.
# Repetir reduz a influência do acaso (o sistema operacional
# está sempre fazendo outras coisas ao mesmo tempo).
REPETICOES = 5
 
# FUNÇÕES
 
def medir(nome_versao, executar, df_municipio, df_demais):
    """Executa uma versão REPETICOES vezes e devolve (resultados, lista de tempos)."""
    tempos = []
    resultados = None
 
    for rodada in range(1, REPETICOES + 1):
        print(f"\n--- {nome_versao}: rodada {rodada} de {REPETICOES} ---")
        resultados, tempo = executar(df_municipio, df_demais)
        tempos.append(tempo)
 
    return resultados, tempos
 
 
def mesmos_resultados(res_a, res_b):
    """Confere se as duas versões chegaram exatamente aos mesmos números."""
    return (
        round(res_a["media_municipio"], 6) == round(res_b["media_municipio"], 6)
        and round(res_a["media_demais"], 6) == round(res_b["media_demais"], 6)
        and res_a["por_partido"].round(6).equals(res_b["por_partido"].round(6))
        and res_a["por_cargo"].round(6).equals(res_b["por_cargo"].round(6))
    )
 
 
def resumo(tempos):
    """Média, menor, maior e desvio padrão de uma lista de tempos."""
    return {
        "media": statistics.mean(tempos),
        "menor": min(tempos),
        "maior": max(tempos),
        "desvio": statistics.stdev(tempos) if len(tempos) > 1 else 0.0,
    }
 
 
def mostrar_tabela(tempos_t, tempos_p, resumo_t, resumo_p):
    """Mostra os tempos de cada rodada lado a lado."""
    print(f"\n{'Rodada':<16}{'Threads (s)':>14}{'Processos (s)':>16}")
    print("-" * 46)
    for i, (t, p) in enumerate(zip(tempos_t, tempos_p), start=1):
        print(f"{i:<16}{t:>14.4f}{p:>16.4f}")
    print("-" * 46)
    for chave, rotulo in [("media", "Média"), ("menor", "Menor"),
                          ("maior", "Maior"), ("desvio", "Desvio padrão")]:
        print(f"{rotulo:<16}{resumo_t[chave]:>14.4f}{resumo_p[chave]:>16.4f}")
 
 
# PROGRAMA PRINCIPAL
# Obrigatório no Windows por causa dos processos.
if __name__ == "__main__":
    inicio_programa = time.perf_counter()
    print(f"Processo principal iniciado, PID = {os.getpid()}")
 
    # 1. Leitura e filtro UMA única vez (fora da comparação)
    inicio = time.perf_counter()
    dados, _ = filtrar_dados(ler_dados())
    df_municipio, df_demais = separar_municipio(dados, MUNICIPIO_ESCOLHIDO)
    tempo_preparo = time.perf_counter() - inicio
    nome = df_municipio["MUNICIPIO"].iloc[0]
    print(f"Dados lidos e filtrados em {tempo_preparo:.2f} segundos")
 
    # 2. As duas versões, com os mesmos dados
    res_threads, tempos_t = medir("THREADS", executar_com_threads, df_municipio, df_demais)
    res_processos, tempos_p = medir("PROCESSOS", executar_com_processos, df_municipio, df_demais)
 
    # 3. Resultados da análise (iguais nas duas versões)
    print(f"\n\n===== RESULTADOS DE {nome} =====")
    if mesmos_resultados(res_threads, res_processos):
        print("Conferência: threads e processos chegaram aos MESMOS resultados.")
    else:
        print("ATENÇÃO: threads e processos chegaram a resultados DIFERENTES!")
 
    print(f"\nMédia de votos em {nome}:    {res_threads['media_municipio']:.2f}")
    print(f"Média de votos nos demais: {res_threads['media_demais']:.2f}")
    partido, media_p, qtd_p = maior_media(res_threads["por_partido"], df_municipio, "PARTIDO")
    cargo, media_c, qtd_c = maior_media(res_threads["por_cargo"], df_municipio, "CARGO")
    mostrar_vencedor("PARTIDO COM A MAIOR MÉDIA DE VOTOS:", partido, media_p, qtd_p)
    mostrar_vencedor("CARGO COM A MAIOR MÉDIA DE VOTOS:", cargo, media_c, qtd_c)
 
    # 4. Tempos
    resumo_t = resumo(tempos_t)
    resumo_p = resumo(tempos_p)
    print(f"\n\n===== TEMPOS DAS 4 TAREFAS ({REPETICOES} rodadas) =====")
    mostrar_tabela(tempos_t, tempos_p, resumo_t, resumo_p)
 
    # 5. Conclusão explícita
    if resumo_t["menor"] <= resumo_p["menor"]:
        menor_versao, menor_valor = "THREADS", resumo_t["menor"]
    else:
        menor_versao, menor_valor = "PROCESSOS", resumo_p["menor"]
 
    if resumo_t["media"] <= resumo_p["media"]:
        melhor, pior = "THREADS", "PROCESSOS"
        media_melhor, media_pior = resumo_t["media"], resumo_p["media"]
    else:
        melhor, pior = "PROCESSOS", "THREADS"
        media_melhor, media_pior = resumo_p["media"], resumo_t["media"]
 
    diferenca = media_pior - media_melhor
    vezes = media_pior / media_melhor if media_melhor > 0 else float("inf")
 
    print("\n\n===== CONCLUSÃO =====")
    print(f"MENOR TEMPO: {menor_versao}, com {menor_valor:.4f} segundos numa única rodada.")
    print(f"MELHOR DESEMPENHO (menor tempo médio): {melhor}.")
    print(f"  {melhor}: {media_melhor:.4f} s em média")
    print(f"  {pior}: {media_pior:.4f} s em média")
    print(f"  {melhor} foi {vezes:.1f} vezes mais rápida ({diferenca:.4f} s de diferença).")
 
    print("\nPor quê:")
    if melhor == "THREADS":
        print("  As threads rodam dentro do mesmo processo e compartilham a memória:")
        print("  são baratas de criar e não precisam copiar os dados.")
        print("  Cada processo precisa ser criado pelo sistema operacional e receber")
        print("  uma CÓPIA dos dados, o que custa mais do que os próprios cálculos,")
        print("  que levam só milissegundos.")
    else:
        print("  Os processos rodam em paralelo de verdade, em núcleos diferentes,")
        print("  sem a trava global do Python (GIL). Com tarefas pesadas, esse ganho")
        print("  supera o custo de criar os processos e copiar os dados.")
 
    tempo_programa = time.perf_counter() - inicio_programa
    print(f"\nTempo total do programa: {tempo_programa:.2f} segundos")
    print(f"Processo principal finalizado, PID = {os.getpid()}")
 