#! /usr/bin/env bash

## You can use this script to update dracykeiton files in your game for now
## WARNING: it removes all the .py files, so don't use it if you have your own
## This will be fixed some time later

DRACYKEITON_REPO=https://github.com/caryoscelus/dracykeiton.git

if [ ! -d deps/dracykeiton ]; then
    mkdir -p deps/
    pushd deps
    git clone --depth=1 ${DRACYKEITON_REPO}
    popd
fi

pushd deps/dracykeiton
git pull
popd

# TODO: don't remove regular .py files?
rm game/*.py

for f in `ls deps/dracykeiton/dracykeiton/*.py | grep -v test_`; do
    cp ${f} game/
done
