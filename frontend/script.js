let processos = [
    // exemplo do PDF
    { id: "P1", chegada: 0, duracao: 5, prioridade: 2 },
    { id: "P2", chegada: 0, duracao: 2, prioridade: 3 },
    { id: "P3", chegada: 1, duracao: 4, prioridade: 1 },
    { id: "P4", chegada: 3, duracao: 3, prioridade: 4 }
];

// tabela de processos
const tbodyProcessos = document.getElementById('lista-processos');

function renderizarTabelaProcessos() {
    tbodyProcessos.innerHTML = '';

    processos.forEach((p, index) => {
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td><input type="text" value="${p.id}" onchange="atualizarProcesso(${index}, 'id', this.value)" style="width: 50px;"></td>
            <td><input type="number" value="${p.chegada}" onchange="atualizarProcesso(${index}, 'chegada', this.value)"></td>
            <td><input type="number" value="${p.duracao}" onchange="atualizarProcesso(${index}, 'duracao', this.value)"></td>
            <td><input type="number" value="${p.prioridade}" onchange="atualizarProcesso(${index}, 'prioridade', this.value)"></td>
            <td><button class="btn-delete" onclick="removerProcesso(${index})">X</button></td>
        `;

        tbodyProcessos.appendChild(tr);
    });
}

// usuário  quer adicionar um processo
document.getElementById('btn-add-processo').addEventListener('click', () => {
    const idSugerido = `P${processos.length + 1}`;
    processos.push({ id: idSugerido, chegada: 0, duracao: 1, prioridade: 1 });
    renderizarTabelaProcessos();
});

// Funções para manipular a lista de processos
function atualizarProcesso(index, campo, valor) {
    if (campo !== 'id') valor = parseInt(valor);
    processos[index][campo] = valor;
}

function removerProcesso(index) {
    processos.splice(index, 1);
    renderizarTabelaProcessos();
}

// Executar a simulação
document.getElementById('btn-simular').addEventListener('click', async () => {
    //  configurações
    const algoritmo = document.getElementById('algoritmo').value;
    const quantum = parseInt(document.getElementById('quantum').value);
    const aging = parseInt(document.getElementById('aging').value);

    const requestDados = {
        algoritmo,
        config: { quantum, aging },
        processos
    };
    console.log("Enviando para o Backend (Python):", requestDados);

    const btnSimular = document.getElementById('btn-simular');
    btnSimular.disabled = true;
    btnSimular.textContent = '⏳ Simulando...';

    // Chama a API Flask via POST
    const endpoint = (window.location.protocol.startsWith('http') && window.location.port === '5000')
        ? '/simular'
        : 'http://localhost:5000/simular';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestDados)
        });

        if (!response.ok) {
            const errJson = await response.json().catch(() => ({}));
            throw new Error(errJson.erro || `Erro HTTP ${response.status}`);
        }

        const resultado = await response.json();
        console.log("Resposta recebida:", resultado);

        // Desenhar Resultados na tela
        mostrarResultados(resultado);

    } catch (error) {
        alert(
            "Erro ao conectar com o Backend Python.\n\n" +
            "Certifique-se de que o servidor está rodando executando no terminal:\n" +
            "  ./run_backend.sh\n\n" +
            "E acesse o simulador no navegador em:\n" +
            "  http://localhost:5000\n\n" +
            "Detalhe técnico: " + error.message
        );
        console.error(error);
    } finally {
        btnSimular.disabled = false;
        btnSimular.textContent = '▶ Executar Simulação';
    }
});

function mostrarResultados(dados) {
    // tira a classe 'escondido' para exibir a área de resultados
    document.getElementById('area-resultados').classList.remove('escondido');

    // Preenche métricas
    document.getElementById('res-turnaround').innerText = dados.metricas.tempoMedioVida + " s";
    document.getElementById('res-espera').innerText = dados.metricas.tempoMedioEspera + " s";
    document.getElementById('res-trocas').innerText = dados.metricas.trocasContexto;

    // Métricas extras
    const elResposta = document.getElementById('res-resposta');
    if (elResposta) {
        elResposta.innerText = dados.metricas.tempoMedioResposta + " s";
    }
    const elTotal = document.getElementById('res-tempo-total');
    if (elTotal) {
        elTotal.innerText = dados.metricas.tempoTotalSimulacao + " s";
    }

    // Constrói a tabela de diagrama de tempo
    const container = document.getElementById('diagrama-container');

    // Coleta os IDs reais que apareceram na simulação (inclui processos do backend)
    const pIds = processos.map(p => p.id);

    let htmlTabela = '<table class="tabela-diagrama"><thead><tr><th>Tempo (s)</th>';

    pIds.forEach(id => {
        htmlTabela += `<th>${id}</th>`;
    });
    htmlTabela += '<th>Fila de Prontos</th>';
    htmlTabela += '</tr></thead><tbody>';

    // Para cada instante no tempo do array retornado pelo backend
    dados.diagramaTempo.forEach(linha => {
        htmlTabela += `<tr>`;
        htmlTabela += `<td>${linha.tempo} – ${linha.tempo + 1}</td>`;

        // Preenche ## (Executando) ou -- (Ocioso)
        pIds.forEach(id => {
            if (linha.processoExecucao === id) {
                htmlTabela += `<td class="executando">##</td>`;
            } else if (linha.processoExecucao === 'IDLE') {
                htmlTabela += `<td class="idle">--</td>`;
            } else {
                htmlTabela += `<td>--</td>`;
            }
        });

        // Coluna com a fila de prontos naquele instante
        const fila = (linha.filaProntos && linha.filaProntos.length > 0)
            ? linha.filaProntos.join(', ')
            : '—';
        htmlTabela += `<td class="fila-prontos">${fila}</td>`;

        htmlTabela += `</tr>`;
    });

    htmlTabela += '</tbody></table>';
    container.innerHTML = htmlTabela;
}

// Inicializa a tabela ao abrir a página
renderizarTabelaProcessos();
