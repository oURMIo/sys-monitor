#!/bin/sh

OUT_FILE="/output/system_info.txt"

while true; do
  {
    echo "===== System Report ====="
    echo "Date: $(date)"
    echo ""
    echo "--- Uptime ---"
    uptime
    echo "--- Load Average ---"
    cat /proc/loadavg
    echo "--- Memory ---"
    free -h
    echo "--- Disk ---"
    df -h
    echo "--- Network Interfaces ---"
    ip addr show
    echo "--- Network Stats ---"
    netstat -i
    echo "--- Top Processes ---"
    ps aux --sort=-%mem | head -n 10
    echo ""
  } > "$OUT_FILE"
  sleep 10
done
