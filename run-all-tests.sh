#! /usr/bin/env bash

pushd `dirname $0`

source env/bin/activate
py.test dracykeiton/
deactivate

source env2/bin/activate
py.test dracykeiton/
deactivate

popd
