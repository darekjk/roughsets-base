#!/bin/bash

ISSET_ROUGHSETS_KDD99_TEST_DATA_FOLDER=$(echo $ROUGHSETS_KDD99_TEST_DATA_FOLDER)

if [ "$ISSET_ROUGHSETS_KDD99_TEST_DATA_FOLDER" == "" ]
then
  echo "Variable ROUGHSETS_KDD99_TEST_DATA_FOLDER not set"
  exit
else
  echo "ROUGHSETS_KDD99_TEST_DATA_FOLDER = $ROUGHSETS_KDD99_TEST_DATA_FOLDER"
fi

echo "Building ..."
rm -rf dist
python -m build
pip install dist/*.whl --force-reinstall

echo "Running unit tests ..."
python -m unittest discover -s $PWD/tests -t $PWD/tests

echo "Running flake8 tests ..."
flake8

echo "Running tox tests ..."
#tox

