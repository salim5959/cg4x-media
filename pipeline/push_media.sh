#!/usr/bin/env bash
# Copie les vidéos rendues vers le dépôt public cg4x-media, pousse, puis vérifie l'URL publique de chacune.
# Usage : bash push_media.sh [ID ...]   (sans argument : toutes les vidéos de out/)
set -euo pipefail
cd "$(dirname "$0")"
REPO=/home/claude/cg4x-media
ids=("$@"); if [ ${#ids[@]} -eq 0 ]; then ids=($(ls out/*.mp4 | xargs -n1 basename | sed 's/.mp4$//')); fi
for id in "${ids[@]}"; do cp -u "out/$id.mp4" "$REPO/"; [ -f "out/${id}_cover.jpg" ] && cp -u "out/${id}_cover.jpg" "$REPO/"; done
cd "$REPO"
git add -A
if ! git diff --cached --quiet; then
  git commit -qm "Vidéos ${ids[0]}…${ids[-1]} (${#ids[@]})" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01JHE2XT5UDH8ZLqmmck3s7J"
  git push -q origin main 2>&1 | grep -v -e negotiation -e acknowledgments || true
fi
ok=0; ko=0
for id in "${ids[@]}"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -r 0-1023 "https://raw.githubusercontent.com/salim5959/cg4x-media/main/$id.mp4")
  if [ "$code" = "200" ] || [ "$code" = "206" ]; then ok=$((ok+1)); echo "$id" >> /home/claude/cg4x-social/public_ok.txt; else ko=$((ko+1)); echo "ABSENT $id ($code)"; fi
done
sort -u -o /home/claude/cg4x-social/public_ok.txt /home/claude/cg4x-social/public_ok.txt
echo "publiques: $ok  manquantes: $ko"
