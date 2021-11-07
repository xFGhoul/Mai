#!/bin/bash

clear

cd ..

cd ..

echo -------------------------------------

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo -------------------------------------

fart.exe aerich.ini ./migrations migrations

echo -------------------------------------

aerich init-db

echo -------------------------------------

sleep 5
exit
