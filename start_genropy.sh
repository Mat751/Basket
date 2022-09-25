#!/bin/bash
gnrdbsetup mybasket
echo "lanciate migrazioni"
python3 /app/genropy_projects/Basket/packages/ball/lib/aggiungi_iscritti.py
echo "lancio i seeders"
python3 /app/genropy_projects/Basket/packages/ball/lib/RiempiPagamentiGenitori.py
echo "lancio gli stranieri"
gnrdaemon > /dev/null 2>&1 &
echo "avviato demone"
sleep 3
gnrwsgiserve mybasket
echo "avviato progetto"
