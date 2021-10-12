@echo off

cls

cd ..

cd ..

echo -------------------------------------

aerich init -t db.tortoise.config.default.TORTOISE_CONFIG

echo INITIALIZED TORTOISE_CONFIG

echo .

echo -------------------------------------

fart.exe aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

echo -------------------------------------

aerich init-db

echo Initizalized Database.

echo -------------------------------------

PAUSE
EXIT
