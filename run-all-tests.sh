#! /usr/bin/env bash

pushd `dirname $0`

source env/bin/activate
py.test dracykeiton/
PY3=$?
deactivate

source env2/bin/activate
py.test dracykeiton/
PY2=$?
deactivate

popd

[ $PY2 -eq 0 ] && [ $PY3 -eq 0 ] && exit 0
exit 1
