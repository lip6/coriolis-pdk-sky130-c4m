
project(
  'coriolis-pdk-sky130-c4m',
   version:  '2025.12.31',
   meson_version: '>= 1.2.0',
)

py       = import( 'python' ).find_installation( pure:false )
py_deps  = dependency( 'python3', required: true )
pdks_dir = py.get_install_dir() / 'pdks' / 'sky130_c4m'
techDir  = 'pdkmaster/C4M.Sky130/libs.tech/'
refDir   = 'pdkmaster/C4M.Sky130/libs.ref/'

cells_files = [ techDir + 'coriolis/sky130/StdCell5V0Lib.py'
              , techDir + 'coriolis/sky130/StdCell5V0Lib_fix.py'
              , techDir + 'coriolis/sky130/StdCellLib.py'
              , techDir + 'coriolis/sky130/StdCellLib_fix.py'
              , techDir + 'coriolis/sky130/MacroLib.py'
              , techDir + 'coriolis/sky130/IOLib.py'
              , techDir + 'coriolis/sky130/__init__.py'
              , techDir + 'coriolis/sky130/techno.py'
              , techDir + 'coriolis/sky130/techno_fix.py'
              ]

core2chip_files = [ techDir + 'coriolis/sky130/core2chip/__init__.py'
                  , techDir + 'coriolis/sky130/core2chip/sky130.py']

py.install_sources( files(    cells_files), subdir:'pdks/sky130_c4m' )
py.install_sources( files(core2chip_files), subdir:'pdks/sky130_c4m/core2chip') 
install_subdir(  refDir, install_dir:pdks_dir )
install_subdir( techDir, install_dir:pdks_dir, exclude_directories:[techDir + 'coriolis'] )


