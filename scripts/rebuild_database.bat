@echo off

cls

echo REBUIDLING DATABASE...

cd ..

echo REMOVING MIGRATIONS DIRECTORY

rmdir /S /Q migrations

echo REMOVED MIGRATIONS DIRECTORY

echo REMOVING AERICH.INI

del aerich.ini

echo REMOVED AERICH.INI

echo INITIALIZING TORTOISE_CONFIG

aerich init -t db.tortoise.config.default.TORTOISE_CONFIG

echo INITIALIZED TORTOISE_CONFIG

echo MONKEYPATCHING AERICH ERROR

fart.exe aerich.ini ./migrations migrations

echo MONKEYPATCHED AERICH ERROR

echo INITIALIZING DATABASE...

aerich init-db

echo INITIALIZED DATABASE.

:start
SET choice=
SET /p choice=Should This Script Be Run Again? [Y]/[N]: 
IF NOT '%choice%'=='' SET choice=%choice:~0,1%
IF '%choice%'=='Y' GOTO yes
IF '%choice%'=='y' GOTO yes
IF '%choice%'=='N' GOTO no
IF '%choice%'=='n' GOTO no
IF '%choice%'=='' GOTO no
ECHO "%choice%" is not valid
ECHO.
GOTO start

:no
EXIT

:yes
cd scripts
rebuild_database
PAUSE
EXIT