#!/usr/bin/env bash

# Script de Inicialização do Simulador de Escalonamento (SO)
# Inicia a API Flask e serve a interface Web em http://localhost:5000

set -e

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

# Cria virtualenv se não existir
if [ ! -d "$VENV_DIR" ]; then
    echo "Criando ambiente virtual em $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

# Ativa o virtualenv
source "$VENV_DIR/bin/activate"

# Instala/verifica dependências
echo " Verificando dependências Python..."
pip install -q -r "$REQ_FILE"

# Informações para o usuário
echo ""
echo "  Simulador de Escalonamento de Processos (SO)"
echo ""
echo "  Abra no seu navegador: http://localhost:5000"
echo ""

# Inicia o servidor Flask
exec python3 "$SCRIPT_DIR/api.py"
