#!/bin/bash
INSTALL_DIR=~/tools/bin
TEMPLATES_DIR=~/tools
CONFIG_DIR=~/.ft

mkdir -p $INSTALL_DIR
mkdir -p $CONFIG_DIR

for file in $PWD/app/*.py
do
  pyinstaller --onefile $file
done

for file in $PWD/dist/*
do
  cp --preserve=all $file $INSTALL_DIR
done

rm -rf $PWD/build
rm -rf $PWD/dist

for file in $PWD/*.spec
do
  rm -rf $file
done

cp -R --preserve=all  $PWD/templates $TEMPLATES_DIR
cp -i --preserve=all  $PWD/app/config ${CONFIG_DIR}

