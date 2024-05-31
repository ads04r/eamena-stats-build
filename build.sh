#!/usr/bin/env bash

BASE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $BASE_PATH
git pull
mv dist old-dist
npm run build
touch dist/.nojekyll
mv old-dist/.git dist/
rm -Rf old-dist
cd dist
chmod -R 755 *
git add .
git commit -a -m "Automatic commit/deploy from stoneheart"
git push -u origin master

