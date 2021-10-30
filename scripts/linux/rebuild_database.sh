#!/bin/bash

clear

echo Rebuilding Database

cd ..

cd ..

echo --------------------------------------

echo REMOVING MIGRATIONS DIRECTORY

rmdir migrations

echo REMOVED MIGRATIONS DIRECTORY

echo -------------------------------------

echo DELETING AERICH.INI

rm aerich.ini

echo REMOVED AERICH.INI

echo -------------------------------------

echo INITALIZING TORTOISE_CONFIG

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo INITALIZED TORTOISE_CONFIG

echo -------------------------------------

echo MONKEYPATCHING AERICH ERROR

fart.ext aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

echo -------------------------------------

echo INITALIZING DATABASE

aerich init-db

echo INITALIZED DATABASE.

echo -------------------------------------

sleep 5
exit
