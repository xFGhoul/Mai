@echo off

echo [*] Starting Update

cd ..

cd ..
echo -------------------------------------

echo [*] Updating Requirements

poetry export -f requirements.txt --output requirements.txt
