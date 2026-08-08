#!/usr/bin/env bash
set -euo pipefail

repository_root="$(git rev-parse --show-toplevel)"
cd "$repository_root"

corpus_python="${CORPUS_PYTHON:-python3}"
if ! command -v "$corpus_python" >/dev/null 2>&1; then
  echo "Corpus validation requires $corpus_python on PATH." >&2
  exit 1
fi

"$corpus_python" scripts/build_peer_first_eligibility.py --check
"$corpus_python" scripts/import_authoritative_142.py
"$corpus_python" scripts/build_universal_review_queue.py
"$corpus_python" scripts/build_corpus_sets.py
"$corpus_python" scripts/build_final_exports.py
"$corpus_python" scripts/validate_corpus.py
"$corpus_python" scripts/validate_corpus_sets.py
git diff --exit-code
