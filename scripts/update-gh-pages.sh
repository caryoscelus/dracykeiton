#! /usr/bin/env bash

pushd `dirname $0`/..
BRANCH=`git rev-parse --abbrev-ref HEAD`
echo "pushing ${BRANCH}..."
if [ ${BRANCH} =  "master" ]; then
    while IFS=' ' read LOCAL_REF LOCAL_SHA REMOTE_REF REMOTE_SHA; do
        if [ ${LOCAL_REF} = "refs/heads/master" ]; then
            FIRST_COMMIT=${REMOTE_SHA}
            LAST_COMMIT=${LOCAL_SHA}
            break
        fi
    done
    
    source env/bin/activate
    
    pushd ../dracykeiton-docs
    git checkout --detach master
    git diff-tree --quiet ${FIRST_COMMIT} ${LAST_COMMIT} -- dracykeiton/ docs/ && exit 0
    ( echo "auto-update docs on $(date +%F)" ; echo ; git log --pretty=format:"%H by %an @ %ad: %s" --date=format:"%F" ${FIRST_COMMIT}..${LAST_COMMIT} -- dracykeiton/ docs/; ) > commit-message.tmp
    
    ./scripts/build-docs.sh
    
    git checkout gh-pages
    
    cp -r ./docs/build/html/* .
    git add .
    # exit if there are no changes - unfortunately this doesn't seem to work
    # due to sphinx regenerating searchindex.js every time..
    # TODO: check if only searchindex.js is changed instead
    git diff-index --quiet --cached HEAD && exit 0
    git commit -F commit-message.tmp
    
    if [ ! -z ${AUTO_PUSH_DOCS} ]; then
        echo git push
    else
        echo "Now go review doc commit & push it!"
    fi
    
    deactivate
    
    popd
else
    echo "not on master, nothing to do"
fi
popd
exit 0
