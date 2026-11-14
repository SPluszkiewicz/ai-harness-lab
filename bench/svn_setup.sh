#!/bin/sh
# Build a tiny SVN history inside the bench-tools container.
# Mounts expected: /workspace/app (git sample), /workspace/svn (empty dir).
set -eu
rm -rf /tmp/repo
svnadmin create /tmp/repo
cd /workspace/svn
rm -rf .svn ./*
svn checkout -q file:///tmp/repo .
cp -r /workspace/app/CMakeLists.txt /workspace/app/CMakePresets.json \
      /workspace/app/src /workspace/app/tests /workspace/app/AGENTS.md \
      /workspace/app/docs .
svn add -q --force .
svn commit -q --username alice -m "Initial import of the calculator" .
sed -i 's/Integer arithmetic\./Integer arithmetic, decimal only./' src/calculator.hpp
svn commit -q --username bob -m "Document that only decimal input is supported" .
sed -i 's/int result = 0;/int result = 0;  \/* alice: start identity *\//' src/calculator.cpp
svn commit -q --username alice -m "Clarify integer power identity" .
svn update -q
svn log -l 8
echo "SVN ready: alice import, bob header, alice power comment"
