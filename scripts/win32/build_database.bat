@echo off

cls

cd ..

aerich init -t db.tortoise.config.default.TORTOISE_CONFIG

echo INITIALIZED TORTOISE_CONFIG

fart.exe aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

aerich init-db

echo Initizalized Database.

PAUSE
EXIT
