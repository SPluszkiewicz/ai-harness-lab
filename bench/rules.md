# Project rules (given to every harness, same content)

- This is a C++17 / CMake project. The source tree is the current directory.
- There is no C++ toolchain on this host. Run every build, test, and compiler command inside the container `bench-tools`, from `/workspace/app`:
  `docker exec bench-tools sh -c "cd /workspace/app && <command>"`
- Presets: `release` and `debug`. Configure: `cmake --preset release`. Build: `cmake --build --preset release`. Test: `ctest --preset release` (add `-R <regex>` to select tests).
- Version control: never run `git commit`, `git push`, `git reset`, `git clean`, or `svn commit`. Reading history is fine (`git log`, `git diff`, `svn log`, `svn diff`).
- Do not touch files outside the current directory.
