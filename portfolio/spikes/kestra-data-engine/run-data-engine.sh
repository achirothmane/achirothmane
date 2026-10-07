#!/usr/bin/env bash
set -u

root="${1:?usage: run-data-engine.sh /absolute/path/to/data-engine [run-dir]}"
run_root="${2:-$PWD/run}"
out_dir="$run_root/out"
work_dir="$run_root/work"
memory_file="$run_root/memory.json"

mkdir -p "$out_dir" "$work_dir"

if [ ! -f "$root/go.mod" ] || [ ! -f "$root/cmd/dataengine/main.go" ]; then
  echo "Data Engine checkout not found at: $root" >&2
  exit 3
fi

cp "$root/examples/real-gpu-market/memory.json" "$memory_file"

(
  cd "$root"
  go run ./cmd/dataengine auto \
    --request examples/real-gpu-market/request.json \
    --catalog examples/real-gpu-market/catalog.json \
    --memory "$memory_file" \
    --work "$work_dir" \
    --out "$out_dir"
)
