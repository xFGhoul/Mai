@echo off

cls

cd ..

cd ..

echo -------------------------------------

aerich migrate

aerich upgrade

echo -------------------------------------

PAUSE
EXIT
