#!/usr/bin/env bash
# Installe la chaîne vidéo CarteGrise4x (Linux x86_64). Outils gratuits et open source uniquement.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p bin voices out tmp
pip install --break-system-packages -q numpy pillow fonttools brotli 2>/dev/null || pip install -q numpy pillow fonttools brotli
command -v ffmpeg >/dev/null || { echo "Installez FFmpeg (apt install ffmpeg / winget install ffmpeg)"; exit 1; }
[ -x bin/piper/piper ] || { curl -sL -o /tmp/piper.tgz https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz && tar xzf /tmp/piper.tgz -C bin; }
# Voix française SIWIS (corpus SIWIS, licence CC BY 4.0 : usage commercial autorisé avec attribution)
[ -f voices/fr-siwis-medium.onnx ] || { curl -sL -o /tmp/v.tgz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-fr-siwis-medium.tar.gz && tar xzf /tmp/v.tgz -C voices; }
echo "Chaîne prête : python3 concepts_src.py && python3 render.py concepts.json && python3 schedule.py"
