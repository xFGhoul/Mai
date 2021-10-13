@echo off

cls

cd ..

cd ..

echo -------------------------------------

echo UPGRADING DATABASE...

aerich migrate

aerich upgrade

echo DATABASE UPGRADED.

echo -------------------------------------

PAUSE
EXIT
