#!/bin/sh

 nightlyInstall="false"
 while [ $# -gt 0 ]; do
   case $1 in
     --nightly) echo "Installing in nightly mode.";
                      nightlyInstall="true";;
   esac
   shift
 done

 if [ "${nightlyInstall}" = "true" ]; then
   rootDir="${HOME}/nightly/coriolis-2.x"
 else
   rootDir="${HOME}/coriolis-2.x"
 fi
   buildDir="${rootDir}/release/build-sky130_c4m"
 installDir="${rootDir}/release/install"
 rm -rf ${buildDir}
 rm -rf ${installDir}/lib64/python3.9/site-packages/pdks/sky130_c4m
 meson setup --prefix ${installDir} ${buildDir}
 meson install -C ${buildDir}
