#! /usr/bin/env bash

echo "Please run this script from the top dracykeiton directory"

# setup virtual environments for python 3..
pyvenv env
# ..and python 2
virtualenv env2

# install py.test, sphinx & dracykeiton
source env/bin/activate
pip install pytest
pip install sphinx
pip install -e .
deactivate

# install py.test & dracykeiton
source env2/bin/activate
pip install pytest
pip install -e .
deactivate

# install git hooks
ln -s `pwd`/githooks/pre-commit .git/hooks/
