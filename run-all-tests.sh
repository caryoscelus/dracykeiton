#! /usr/bin/env bash

source env/bin/activate
py.test dracykeiton/
deactivate

source env2/bin/activate
py.test dracykeiton/
deactivate
