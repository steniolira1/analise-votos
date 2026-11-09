# Processos vs Threads com Dados do TSE

Projeto da disciplina de **Sistemas Operacionais** (Equipe 2).

Compara o desempenho de **processos** e **threads** em Python usando uma tarefa real:
a análise dos votos do 1º turno das eleições de 2026 em São Paulo, com foco no
município de **Borá-SP**.

## Resultado

A versão com **threads** venceu nos dois critérios:

| Critério                         | Threads    | Processos  |
| -------------------------------- | ---------- | ---------- |
| Menor tempo (melhor rodada)      | 0,0020 s   | 1,7140 s   |
| Tempo médio (5 rodadas)          | 0,0026 s   | 1,8402 s   |

As threads foram cerca de **696 vezes mais rápidas**. Criar processos e copiar os dados
para cada um custa quase 2 segundos no Windows, muito mais do que os cálculos, que levam
milissegundos.

## O que o programa calcula

1. A média de votos de Borá comparada à média dos demais municípios de SP.
2. A média de votos por partido e por cargo em Borá.
3. O partido e o cargo com a maior média de votos em Borá.
4. O tempo de execução das versões com threads e com processos.

| Resultado em Borá                    | Valor                           |
| ------------------------------------ | ------------------------------- |
| Média de votos em Borá               | 19,73                           |
| Média de votos nos demais municípios | 179,35                          |
| Partido com a maior média            | REDE (150,00, 1 registro)       |
| Cargo com a maior média              | Senador (208,14, 7 registros)   |

## Estrutura de pastas

```
analise-votos/
├── dados/
│   └── votacao_candidato_munzona_2026_SP.csv   (arquivo do TSE, nunca alterado)
├── leitura.py        Meta 1 - lê o CSV
├── filtro.py         Meta 2 - remove registros inválidos e zerados
├── medias.py         Meta 3 - calcula as médias
├── resultados.py     Meta 4 - partido e cargo com a maior média
├── threads.py        Meta 5 - executa as tarefas com threads
├── processos.py      Meta 6 - executa as tarefas com processos
├── main.py           Meta 7 - compara as duas versões e indica a vencedora
├── conferencia.py    Confere os totais de votos com fontes externas
├── requirements.txt
└── README.md
```

Cada arquivo importa as funções do anterior, então todos precisam ficar na mesma pasta.
Não dê a nenhum arquivo o nome `threading.py`: ele conflita com a biblioteca do Python.

## Requisitos

- Python 3.13 (testado no Windows com VS Code)
- pandas

Instalação:

```
python -m pip install -r requirements.txt
```

Se o comando `python` não for reconhecido no Windows, use o caminho completo do Python, por exemplo:

```
C:\Users\<usuario>\AppData\Local\Programs\Python\Python313\python.exe -m pip install -r requirements.txt
```

## Dados

Baixe o arquivo `votacao_candidato_munzona_2026_SP.csv` nos dados abertos do TSE
e coloque-o na pasta `dados`. O arquivo usa `;` como separador e codificação `latin-1`.

O projeto usa quatro colunas:

| Coluna no TSE        | Nome no código |
| -------------------- | -------------- |
| `NM_MUNICIPIO`       | `MUNICIPIO`    |
| `SG_PARTIDO`         | `PARTIDO`      |
| `DS_CARGO`           | `CARGO`        |
| `QT_VOTOS_NOMINAIS`  | `VOTOS`        |

## Como executar

Abra o terminal na pasta `analise-votos`. Para a comparação final, rode:

```
python main.py
```

O `main.py` lê os dados uma única vez, executa cada versão 5 vezes com os mesmos dados,
confere se as duas chegaram aos mesmos resultados e termina com a conclusão.
Leva cerca de 15 segundos.

Cada meta também pode ser executada sozinha:

```
python leitura.py      # Meta 1
python filtro.py       # Meta 2
python medias.py       # Meta 3
python resultados.py   # Meta 4
python threads.py      # Meta 5
python processos.py    # Meta 6
python conferencia.py  # Conferência dos totais
```

## Configurações

| Onde          | Variável               | Para que serve                                   |
| ------------- | ---------------------- | ------------------------------------------------ |
| `leitura.py`  | `CAMINHO_ARQUIVO`      | Caminho do CSV                                    |
| `filtro.py`   | `REMOVER_VOTOS_ZERO`   | `True` remove registros com 0 votos (padrão)      |
| `medias.py`   | `MUNICIPIO_ESCOLHIDO`  | Município analisado (aceita com ou sem acento)    |
| `main.py`     | `REPETICOES`           | Quantas rodadas cada versão executa (padrão: 5)   |

## Decisões da equipe

- **Votos zerados removidos.** 67% dos registros tinham 0 votos, porque cada candidato
  aparece em todas as zonas do estado. Mantê-los distorceria as médias.
- **Média por registro.** A média divide o total de votos pelo número de registros.
  Por isso a REDE lidera entre os partidos em Borá com 150 votos, valor que vem de um
  único registro (Marina Silva, Senador).
- **Arquivo original intocado.** O CSV só é lido; todo o processamento acontece em memória.
- **Comparação justa.** A leitura do CSV fica fora da medição, porque seu tempo varia
  entre execuções e dominaria o resultado.

## Threads vs processos no código

| Aspecto                | Threads (`threads.py`)                | Processos (`processos.py`)               |
| ---------------------- | ------------------------------------- | ---------------------------------------- |
| PID                    | O mesmo para todas                    | Um PID diferente para cada filho         |
| Memória                | Compartilhada                         | Separada; os dados são copiados          |
| Retorno dos resultados | Dicionário compartilhado + `Lock`     | Fila (`multiprocessing.Queue`)           |
| Espera                 | `join()`                              | `fila.get()` e depois `join()`           |

No Windows, o bloco `if __name__ == "__main__":` é obrigatório na versão com processos.
Sem ele, cada processo filho executaria o programa inteiro novamente.

## Situação

| Meta | Descrição                                   | Situação     |
| ---- | ------------------------------------------- | ------------ |
| 1    | Ler a base de dados                         | Concluída    |
| 2    | Filtrar os dados                            | Concluída    |
| 3    | Calcular as médias                          | Concluída    |
| 4    | Partido e cargo com a maior média           | Concluída    |
| 5    | Tempo da versão com threads                 | Concluída    |
| 6    | Tempo da versão com processos               | Concluída    |
| 7    | Comparação final e indicação da vencedora   | Concluída    |
