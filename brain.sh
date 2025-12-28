#!/bin/bash

DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL="$DIR/models/tinyllama-q4.gguf"
LLAMA="$DIR/llama.cpp/main"
MEMORY="$DIR/memory.txt"

INPUT="$1"
CONTEXT=$(tail -n 15 "$MEMORY")

"$LLAMA" \
 -m "$MODEL" \
 -p "You are Blaze, the sarcastic BackTrack Linux dragon.
Keep responses short.
Memory:
$CONTEXT

User: $INPUT
Dragon:" \
 -n 50 \
 --temp 0.7 \
 --top-p 0.9 \
 2>/dev/null | head -n 1
