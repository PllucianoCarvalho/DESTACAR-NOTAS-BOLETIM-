#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/Aplicativos/DestacadorBoletins_v3_2_1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_SRC="$SCRIPT_DIR/destacador_boletins_v3_2_1.py"
SCRIPT_DST="$APP_DIR/destacador_boletins_v3_2_1.py"
VENV="$APP_DIR/venv"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/destacador-boletins-v3_2_1.desktop"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERRO: Python 3 não foi encontrado."
  echo "Instale com: sudo apt install python3"
  exit 1
fi

if [[ ! -f "$SCRIPT_SRC" ]]; then
  echo "ERRO: não encontrei o script Python ao lado deste instalador:"
  echo "  $SCRIPT_SRC"
  echo "Baixe os dois arquivos da versão 3.2.1 e mantenha-os na mesma pasta."
  exit 1
fi

if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
  echo "ERRO: Tkinter não está instalado para este Python."
  echo "Execute: sudo apt update && sudo apt install python3-tk"
  exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR"

# Copia para uma instalação separada; não altera a v3.1.
cp "$SCRIPT_SRC" "$SCRIPT_DST"

# Recria o ambiente virtual caso esteja quebrado após uma atualização do Python.
if [[ -x "$VENV/bin/python" ]] && ! "$VENV/bin/python" -m pip --version >/dev/null 2>&1; then
  rm -rf "$VENV"
fi
if [[ ! -x "$VENV/bin/python" ]]; then
  if ! python3 -m venv "$VENV"; then
    echo "ERRO ao criar o ambiente virtual. Confirme que python3-venv está instalado:"
    echo "  sudo apt install python3-venv"
    exit 1
  fi
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install "PyMuPDF==1.24.11"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Destacador de Boletins v3.2.1
Comment=Destaca notas baixas, calcula aproveitamento e gera relatório pedagógico
Exec="$VENV/bin/python" "$SCRIPT_DST"
Icon=applications-education
Terminal=false
Categories=Education;Office;
StartupNotify=true
EOF

chmod 644 "$DESKTOP_FILE"
update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true

echo
echo "Instalação da v3.2.1 concluída."
echo "Programa: $SCRIPT_DST"
echo "Ambiente virtual: $VENV"
echo "Atalho: Destacador de Boletins v3.2.1 no menu de aplicativos"
echo "A instalação da v3.1 foi mantida."
