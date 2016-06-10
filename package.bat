set PACKAGE_NAME=SystemCommands

rmdir /q /s build
mkdir build

cd src
zip ..\build\%PACKAGE_NAME%.keypirinha-package *.py *.ini *.ico lib/*.py icons/*.*

cd ..