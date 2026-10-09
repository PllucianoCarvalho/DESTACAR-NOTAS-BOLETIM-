#!/usr/bin/env bash
set -e
APP_DIR="$HOME/Aplicativos/DestacadorBoletins_v3_1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/destacador_boletins_v3_1.py"
if [ ! -f "$SCRIPT" ]; then
  echo "Não encontrei $SCRIPT"
  echo "Deixe o instalador e o script Python na mesma pasta."
  exit 1
fi
mkdir -p "$APP_DIR"
cp "$SCRIPT" "$APP_DIR/destacador_boletins_v3_1.py"
python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/venv/bin/python" -m pip install pymupdf
if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
  echo 'Tkinter não instalado. Execute: sudo apt install python3-tk'
  exit 1
fi
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/destacador-boletins-v3-1.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Destacador de boletins v3.1
Comment=Destaca notas baixas, soma faltas e classifica aproveitamento
Exec=$APP_DIR/venv/bin/python $APP_DIR/destacador_boletins_v3_1.py
Icon=application-pdf
Terminal=false
Categories=Office;Education;
EOF
chmod +x "$HOME/.local/share/applications/destacador-boletins-v3-1.desktop"
echo 'Instalação da v3.1 concluída. Procure Destacador de boletins v3.1 no menu.'
