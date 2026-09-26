# Simulador de Escalonamento de Processos

Implementação modular da Tarefa 1 de Sistemas Operacionais.

## Algoritmos

- FCFS
- SJF
- SRTF
- Prioridade sem preempção
- Prioridade com preempção
- Round-Robin
- Round-Robin com prioridade e envelhecimento

## Entrada

Os processos são lidos pelo stdin.

Formato:

```text
tempo_chegada duracao prioridade
```

Exemplo:

```text
0 5 2
0 2 3
1 4 1
3 3 4
```

## Configuração

No arquivo `config.txt`:

```text
quantum:2
aging:1
```

## Execução

```bash
python3 main.py < entrada.txt
```

Ou:

```bash
cat entrada.txt | python3 main.py
```

## Organização

- `processo.py`: estrutura do processo e métricas individuais.
- `config.py`: leitura do arquivo de configuração.
- `entrada.py`: leitura dos processos pelo stdin.
- `escalonador.py`: funcionalidades comuns dos escalonadores.
- `algoritmos/`: implementação individual dos algoritmos.
- `main.py`: execução e saída.
# Escalonamento_de_Processos
