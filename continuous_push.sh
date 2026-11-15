#!/bin/bash
while true; do
  git add isot_ledger.json takeout_archive/ 2>/dev/null
  git commit -m "Auto-contingency sync $(date)" 2>/dev/null
  git push origin main 2>/dev/null
  sleep 60
done
