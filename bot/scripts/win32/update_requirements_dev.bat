@echo off

echo [*] Starting Update

cd ..

cd ..
echo -------------------------------------

echo [*] Updating Requirements (Dev)

poetry export -f requirements.txt --output requirements.txt --dev
