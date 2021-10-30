@echo off

cls

echo REBUIDLING DATABASE...

cd ..

cd ..

echo -------------------------------------

echo REMOVING MIGRATIONS DIRECTORY

rmdir /S /Q migrations

echo REMOVED MIGRATIONS DIRECTORY

echo -------------------------------------

echo REMOVING AERICH.INI

del aerich.ini

echo REMOVED AERICH.INI

echo -------------------------------------

echo INITIALIZING TORTOISE_CONFIG

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo INITIALIZED TORTOISE_CONFIG

echo -------------------------------------

echo MONKEYPATCHING AERICH ERROR

fart.exe aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

echo -------------------------------------

echo INITIALIZING DATABASE...

aerich init-db

echo INITIALIZED DATABASE.

echo -------------------------------------

PAUSE
EXIT
