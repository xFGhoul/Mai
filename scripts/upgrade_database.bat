@echo off

cls

echo UPGRADING DATABASE...

cd ..

aerich migrate

aerich upgrade

echo DATABASE UPGRADED.

PAUSE
EXIT