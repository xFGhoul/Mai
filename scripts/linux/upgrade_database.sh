#!/bin/bash

clear

cd ..

cd ..

echo -------------------------------------

echo UPGRADING DATABASE...

aerich migrate

aerich upgrade

echo DATABASE UPGRADED.

echo -------------------------------------

sleep 5
exit