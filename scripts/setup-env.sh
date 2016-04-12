#! /usr/bin/env bash

echo "Please run this script from the top dracykeiton directory"
echo "Setting up development environment..."

# setup virtual environments for python 3..
if [ ! -d env ]; then
    echo "Setting up py3 virtual env"
    pyvenv env
    # install py.test, sphinx & dracykeiton
    source env/bin/activate
    pip install pytest
    pip install sphinx
    pip install -e .
    deactivate
    echo "Done"
fi

# ..and python 2
if [ ! -d env2 ]; then
    echo "Setting up py2 virtual env"
    virtualenv env2
    # install py.test & dracykeiton
    source env2/bin/activate
    pip install pytest
    pip install -e .
    deactivate
    echo "Done"
fi

# setup docs / gh-pages work directory
[ -d ../dracykeiton-docs ] || git worktree add ../dracykeiton-docs gh-pages

# install git hooks
[ -f .git/hooks/pre-commit ] || ln -s `pwd`/githooks/pre-commit .git/hooks/
[ -f .git/hooks/pre-push ] || ln -s `pwd`/githooks/pre-push .git/hooks/

echo "All done"
