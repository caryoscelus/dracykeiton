#! /usr/bin/env bash

pushd `dirname $0`/..
source env
pushd docs
make html
popd
popd

exit 0
