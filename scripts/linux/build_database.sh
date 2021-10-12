#!/bin/bash

clear

cd ..

cd ..

echo -------------------------------------


echo INITIALIZING TORTOISE_CONFIG

aerich init -t db.tortoise.config.default.TORTOISE_CONFIG

echo INITALIZED TORTOISE_CONFIG

echo -------------------------------------

echo MONKEYPATCHING AERICH ERROR

fart.exe aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

echo -------------------------------------

echo INITIALIZING DATABASE...

aerich init-db

echo INITIALIZED DATABASE.

echo -------------------------------------

sleep 5
exit 