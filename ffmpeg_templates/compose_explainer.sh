#!/usr/bin/env bash
# Usage: ./compose_explainer.sh -v voice.mp3 -m music.mp3 -i intro.png -o out.mp4 -t "Title text"
set -e
while getopts "v:m:i:o:t:" opt; do
  case $opt in
    v) VOICE="$OPTARG";;
    m) MUSIC="$OPTARG";;
    i) INTRO="$OPTARG";;
    o) OUT="$OPTARG";;
    t) TITLE="$OPTARG";;
  esac
done

: "${OUT:=explainer_out.mp4}"

# Create a simple title card (1920x1080) with FFmpeg drawtext
ffmpeg -y -f lavfi -i color=c=white:s=1920x1080:d=5 -i "$MUSIC" -filter_complex "\
[0:v]drawtext=text='${TITLE}':x=(w-text_w)/2:y=(h-text_h)/2:fontsize=72:fontcolor=black:box=1:boxcolor=white@0.0,format=yuv420p[v0];\
[1:a]volume=0.25[aud]" -map "[v0]" -map "[aud]" -shortest title.mp4

# Mix title + VO + music under
ffmpeg -y -i title.mp4 -i "$VOICE" -i "$MUSIC" -filter_complex "\
[1:a]volume=1.0[vo];[2:a]volume=0.15[bg];[vo][bg]amix=inputs=2:duration=longest[a]" \
-map 0:v -map "[a]" -c:v libx264 -pix_fmt yuv420p -c:a aac "$OUT"

echo "Rendered $OUT"
