@echo off

echo [*] Starting Rebuild Process

cd ..

cd ..

echo -------------------------------------

echo [*] Removing Migrations Directory

rmdir /S /Q migrations

echo [*] Migrations Directory Removed

echo -------------------------------------

echo [*] Remvoing aerich.ini

del aerich.ini

echo [*] aerich.ini Removed

echo -------------------------------------

echo [*] Initializing TORTOISE_CONFIG

aerich init -t db.tortoise.config.tortoise_config.TORTOISE_CONFIG

echo [*] TORTOISE_CONFIG Intialized

echo -------------------------------------

echo [*] Monkeypatching aerich.ini Error

fart.exe aerich.ini ./migrations migrations

echo [*] aerich.ini Error Monkeypatched

echo -------------------------------------

echo [*] Initializing Database

aerich init-db

echo [*] Database Intialized

echo -------------------------------------

PAUSE
EXIT
