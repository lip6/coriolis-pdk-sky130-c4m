#!/bin/sh

    rootDir="${HOME}/coriolis-2.x"
   buildDir="${rootDir}/release/build-sky130-c4m"
 installDir="${rootDir}/release/install"
 rm -rf ${buildDir}
 rm -rf ${installDir}/lib64/python3.9/site-packages/pdks/sky130_c4m
 meson setup --prefix ${installDir} ${buildDir}
 meson install -C ${buildDir}
