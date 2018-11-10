#!/bin/bash
# #################################################
# This script demonstrates, how you can configure
# your BudgetPi to use a MySQL database
# #################################################

DB_DRIVER=mysql \
DB_NAME=live-budgetpi \
DB_HOST=192.168.1.250 \
DB_USER=budgetpi \
DB_PASS=BuDgEtPi \
CURRENCY="€" \
/usr/bin/python3 /home/pi/BudgetPi/main.py
