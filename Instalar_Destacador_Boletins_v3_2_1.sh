#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$HOME/Aplicativos/DestacadorBoletins_v3_2_1"
DOWNLOADS="$HOME/Downloads"
SCRIPT_SRC="$DOWNLOADS/destacador_boletins_v3_2_1.py"
SCRIPT_DST="$APP_DIR/destacador_boletins_v3_2_1.py"
VENV="$APP_DIR/venv"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/destacador-boletins-v3_2_1.desktop"

if [[ ! -f "$SCRIPT_SRC" ]]; then
  echo "ERRO: não encontrei $SCRIPT_SRC"
  echo "Salve destacador_boletins_v3_2_1.py na pasta Downloads e tente novamente."
  exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR"

# Copia somente para a nova pasta; não altera as versões anteriores.
cp "$SCRIPT_SRC" "$SCRIPT_DST"

if [[ ! -x "$VENV/bin/python" ]]; then
  python3 -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install "PyMuPDF==1.24.11"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Destacador de Boletins v3.2.1
Comment=Destaca notas e calcula aproveitamento com estrelas
Exec=$VENV/bin/python $SCRIPT_DST
Icon=applications-education
Terminal=false
Categories=Education;Office;
StartupNotify=true
EOF

chmod 644 "$DESKTOP_FILE"
update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true

echo
echo "Instalação da v3.2 concluída."
echo "Programa: $SCRIPT_DST"
echo "Ambiente virtual: $VENV"
echo "Atalho: Destacador de Boletins v3.2.1 no menu de aplicativos"
echo
echo "A v3.1 não foi modificada."
