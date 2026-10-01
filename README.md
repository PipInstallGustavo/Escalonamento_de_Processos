# Simulador de Escalonamento de Processos ⚙️

Implementação modular da **Tarefa 01 – Escalonamento de Processos** da disciplina de Sistemas Operacionais.

---

## 🎯 Algoritmos Implementados

- **FCFS** (*First-Come, First-Served*)
- **SJF** (*Shortest Job First*)
- **SRTF** (*Shortest Remaining Time First*)
- **Prioridade Não-Preemptiva**
- **Prioridade Preemptiva**
- **Round-Robin**
- **Round-Robin com Prioridade e Aging**

---

## 🚀 Como Executar

O projeto pode ser executado de **duas formas**: com **Interface Gráfica Web** ou via **Linha de Comando (Terminal)**.

### Opção 1: Interface Gráfica Web (Recomendado) 🌐

Basta executar o script de inicialização unificada:

```bash
./run_backend.sh
```

O script criará o ambiente virtual (`.venv`), instalará as dependências de `requirements.txt` e iniciará o servidor.

Em seguida, abra o navegador em:
👉 **[http://localhost:5000](http://localhost:5000)**

Pela interface, você pode:
- Adicionar, editar e remover processos dinamicamente.
- Escolher qualquer um dos 7 algoritmos.
- Ajustar os parâmetros de **Quantum** e taxa de **Aging**.
- Visualizar os cálculos detalhados de métricas (*Turnaround*, tempo de espera, trocas de contexto, etc.).
- Acompanhar o **Diagrama de Tempo / Execução** a cada instante.

---

### Opção 2: Linha de Comando (Modo CLI) 💻

Os processos são lidos via `stdin` com o formato:
```text
tempo_chegada duracao prioridade
```

Exemplo (`entrada.txt`):
```text
0 5 2
0 2 3
1 4 1
3 3 4
```

Configuração de Quantum e Aging no arquivo `config.txt`:
```text
quantum:2
aging:1
```

Execução:
```bash
python3 main.py < entrada.txt
```
ou:
```bash
cat entrada.txt | python3 main.py
```

---


# Estrutura do Projeto e Decisões de Implementação

## 1. Mapeamento do Processo e Estruturas de Dados (`processo.py`)
A classe `Processo` atua como o **Bloco de Controle de Processo (PCB)** do sistema, encapsulando os dados e o estado de cada tarefa:
- **`id`**: Identificador único do processo ($P1, P2, \dots$).
- **`status`**: Estado atual do processo (*PRONTO*, *EXECUTANDO*, *FINALIZADO*).
- **`prioridade` / `prioridade_dinamica`**: Prioridade estática e a ajustada dinamicamente pelo algoritmo de *Aging* para evitar *starvation*.
- **Controle de Tempo**: Armazena `tempo_chegada`, `tempo_execucao`, `tempo_restante` e métricas de desempenho (`tempo_inicio`, `tempo_fim`, `tempo_espera`, `tempo_turnaround`, `tempo_resposta`).

**Decisão:** Centralizar o estado e o histórico de execução no próprio objeto simplifica a manipulação da fila de prontos e garante precisão no cálculo das métricas.

---

## 2. Padrão de Projeto e Arquitetura do Escalonador (`escalonador.py` e `algoritmos/`)
A arquitetura do motor de simulação adota o **Padrão Strategy** com Herança:
- **Classe Base `Escalonador`**: Gerencia a linha do tempo ($T$), filas de entrada e prontos, contagem de trocas de contexto e centraliza as **regras globais de desempate** (1º Manter o processo atual na CPU; 2º Menor tempo restante; 3º Ordem de chegada/PID).
- **Classes Concretas (`algoritmos/`)**: Cada algoritmo (FCFS, SJF, SRTF, Prioridade, RR, RR+Aging) herda da classe base e sobrescreve apenas a regra de seleção do próximo processo.

**Decisão:** Elimina a duplicação de código. Adicionar um novo algoritmo não exige alterar a lógica de métricas ou as regras de desempate.

---

## 3. Desacoplamento da Interface e Persistência (`api.py`, `main.py`, `frontend/`)
- **Modo CLI (`main.py`, `entrada.py`)**: Realiza o *parsing* via `stdin`, permitindo testes automatizados e sem dependências gráficas no terminal.
- **Modo Web (`api.py`, `frontend/`)**: Servidor Flask leve que disponibiliza o endpoint `/simular` em JSON e serve a interface em HTML/CSS/JS para visualização dos gráficos.

**Decisão:** O motor de escalonamento é totalmente desacoplado da camada visual, podendo ser executado via linha de comando ou consumido via API Web.

---

## 4. Organização dos Arquivos

- `frontend/`: Interface gráfica web (HTML, CSS, JavaScript).
- `algoritmos/`: Implementações específicas de cada algoritmo de escalonamento.
- `resultados/`: Histórico em formato JSON gerado pelas simulações.
- `processo.py`: Classe do processo (PCB) e métricas individuais.
- `escalonador.py`: Classe base com motor de tempo, trocas de contexto e desempate.
- `main.py` e `entrada.py`: Ponto de entrada CLI e leitura de dados via `stdin`.
- `api.py`: Servidor Flask HTTP.
- `config.py` / `config.txt`: Configuração de parâmetros (Quantum e Aging).
- `run_backend.sh` / `requirements.txt`: Automação do ambiente de execução em um único comando.