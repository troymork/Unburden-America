#!/usr/bin/env bash
# Usage: ./mix_audio.sh -v voice.mp3 -m music.mp3 -o out.mp3
set -e
while getopts "v:m:o:" opt; do
  case $opt in
    v) VOICE="$OPTARG";;
    m) MUSIC="$OPTARG";;
    o) OUT="$OPTARG";;
  esac
done
: "${OUT:=mix_out.mp3}"
ffmpeg -y -i "$VOICE" -i "$MUSIC" -filter_complex "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=longest[a]" -map "[a]" -c:a mp3 "$OUT"
echo "Rendered $OUT"
