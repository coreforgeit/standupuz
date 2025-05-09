#!/usr/bin/env bash
if [ ! -d node_modules ] || [ -z "$(ls -A node_modules)" ]; then
  echo ">>> Installing node modules…"
  npm ci
fi
exec "$@"
