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

## 📁 Organização do Projeto

- `frontend/`: Interface Web (HTML, CSS e JavaScript).
- `api.py`: Servidor Flask que serve a interface e expõe o endpoint `/simular`.
- `run_backend.sh`: Script para inicialização em 1 comando com virtualenv.
- `requirements.txt`: Dependências Python (Flask e Flask-CORS).
- `processo.py`: Estrutura de dados do processo e suas métricas.
- `config.py` e `config.txt`: Leitura e parâmetros de configuração para o modo CLI.
- `entrada.py` e `entrada.txt`: Leitura dos processos via `stdin`.
- `escalonador.py`: Classe base com controle de timeline, cálculo de métricas e desempates.
- `algoritmos/`: Módulos individuais de cada algoritmo de escalonamento.
- `resultados/`: Arquivos JSON gerados com resultados de simulações.
- `main.py`: Ponto de entrada para a execução no terminal.
