#!/bin/sh
set -eu
rm -rf /tmp/repo
svnadmin create /tmp/repo
cd /workspace/svn
rm -rf .svn
svn checkout -q file:///tmp/repo .
cp -r /workspace/app/CMakeLists.txt /workspace/app/CMakePresets.json /workspace/app/src /workspace/app/tests .
svn add -q --force .
svn commit -q --username alice -m "Initial import of the calculator" .
sed -i 's/Integer arithmetic\./Integer arithmetic, decimal only./' src/calculator.hpp
svn commit -q --username bob -m "Document that only decimal input is supported" .
svn update -q
svn log -l 5
