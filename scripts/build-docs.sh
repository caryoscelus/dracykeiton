#! /usr/bin/env bash

pushd `dirname $0`/..
source env/bin/activate
pushd docs
make html
popd
deactivate
popd

exit 0
