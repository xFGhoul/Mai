@echo off

cls

cd ..

cd ..

echo -------------------------------------

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo .

echo -------------------------------------

fart.exe aerich.ini ./migrations migrations

echo -------------------------------------

aerich init-db

echo -------------------------------------

PAUSE
EXIT
