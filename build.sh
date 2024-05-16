#!/usr/bin/env bash

BASE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASE_PATH
mv dist old-dist
npm run build
touch dist/.nojekyll
mv old-dist/.git dist/
rm -Rf old-dist
chmod -R 755 *
